# ==========================================
# 🧠 __classcell__ ATTRIBUTE — NEDİR?
# ==========================================

# 🔹 __classcell__, Python'un sınıf tanım sürecinde kullanılan özel bir cell (hücre) yapısıdır.
# 🔹 Amaç: class gövdesindeki `super()` kullanımının doğru çalışmasını sağlamaktır.

# 🧩 Nasıl çalışır?
#
# 1️⃣ Python sınıf tanımını derlerken, gövde içinde `super()` ifadesi gördüğünde,
#    o sınıfa özel bir hücre (`__classcell__`) oluşturur.
#
# 2️⃣ Bu hücre, sınıf daha oluşturulmadan bile sınıfın kim olduğunu işaret eder.
#    Böylece `super()`, gerçek sınıf referansını closure içinde kullanabilir.
#
# 3️⃣ Metaclass'ın `__new__` metoduna bu `__classcell__` keyword parametre olarak geçilir.
#    Eğer `__classcell__` iletilmezse,
#    `super()` için gereken sınıf referansı eksik olur ve
#    `RuntimeError: __class__ cell not found` hatası alınır.

# 🔍 Örnek akış:
#
# class Meta(type):
#     def __new__(cls, name, bases, namespace, **kwargs):
#         # Burada __classcell__ var mı diye kontrol edebilirsin
#         # namespace.get('__classcell__') → <cell at ...>
#         return super().__new__(cls, name, bases, namespace, __classcell__=kwargs.get('__classcell__'))
#
# class Base:
#     pass
#
# class Sub(Base, metaclass=Meta):
#     def foo(self):
#         super().foo()  # -> super() için __classcell__ gereklidir!

# 🎯 Özet Tablo:
#
# | Özellik            | Açıklama |
# |--------------------|----------|
# | Oluşturma zamanı   | Sınıf gövdesi derlenirken |
# | Tip                 | Gizli cell hücresi |
# | Kullanım amacı     | `super()` çağrısının bağlamı için sınıf referansı sağlamak |
# | Metaclass ilgisi   | `__new__` içinde yakalanmalı ve `super().__new__`'e iletilmeli |
# | Hata durumunda     | `RuntimeError: __class__ cell not found` oluşur |

# ✅ Kısacası:
# - `__classcell__`, `super()` için gereken sınıf bilgisini saklayan gizli bir cell'dir.
# - Python otomatik oluşturur ama metaclass'ında uygun şekilde iletmeyi unutma.


class MetaBasic(type):
    def __new__(metacls, name, bases, namespace, **kwargs):
        # __classcell__ kontrolü
        has_cell = '__classcell__' in kwargs
        print(f"[MetaBasic] __classcell__ var mı? {has_cell}")

        # __classcell__ varsa super().__new__'e iletilebilir
        return super().__new__(metacls, name, bases, namespace,
                               __classcell__=kwargs.get('__classcell__'))


class Base:
    def greet(self):
        print("– Base.greet çağrıldı")


# Bu sınıf super() içeriyor:
class Foo(Base, metaclass=MetaBasic):
    def greet(self):
        super().greet()
        print("– Foo.greet çağrıldı")


# Test
f = Foo()
f.greet()


class MetaLogger(type):
    def __new__(metacls, name, bases, namespace, **kwargs):
        # __classcell__'e dikkat et:
        cell = kwargs.get('__classcell__')
        print(f"[MetaLogger] Yeni sınıf: {name}, __classcell__ var mı? {bool(cell)}")
        return super().__new__(metacls, name, bases, namespace,
                               __classcell__=cell)

    def __call__(cls, *args, **kwargs):
        print(f"[MetaLogger.__call__] {cls.__name__}() çağrılıyor.")
        return super().__call__(*args, **kwargs)


class Base:
    def __init__(self):
        print("– Base.__init__ çalıştı")

    def greet(self):
        print("– Base.greet çağrıldı")


class Foo(Base, metaclass=MetaLogger):
    def __init__(self):
        super().__init__()  # super()'un doğru çalışması için __classcell__ gerekli
        print("– Foo.__init__ çalıştı")

    def greet(self):
        super().greet()
        print("– Foo.greet çağrıldı")


# Test edelim:
obj = Foo()
obj.greet()


# =======================================================
# 📌 __classcell__ ve Metaclass'ta Tehlikeli Kullanımlar
# =======================================================

# 🔷 __classcell__ Nedir?
# -----------------------
# Python, class tanımı sırasında `super()` gibi yapılar varsa
# bu class gövdesinde kullanılacak `__class__` için özel bir
# bağlama (closure) ihtiyaç duyar. İşte bu bağ `__classcell__` ile sağlanır.

# Bu özel anahtar, class namespace’ine otomatik olarak eklenir
# ve Python tarafından `type.__new__`'a iletilmelidir.

# Eğer silinir veya düzgün aktarılmazsa `super()` çalışamaz.

# 🔴 TEHLİKELİ DURUMLAR
# ----------------------

# ❌ 1. classcell'i elle silmek
def __new__(cls, name, bases, namespace):
    namespace.pop("__classcell__", None)  # <-- bu `super()` hatasına yol açar!
    return super().__new__(cls, name, bases, namespace)

# ❌ 2. classcell içeren namespace'i yeni dict ile kopyalamak
def __new__(cls, name, bases, namespace):
    new_namespace = dict(namespace)  # ⚠️ Shallow-copy yapar, özel cell objesi kaybolur
    return super().__new__(cls, name, bases, new_namespace)

# 🧪 Örnek: Hatalı kullanımın etkisi
class BrokenMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace = dict(namespace)  # ⚠️ __classcell__ yok oldu
        return super().__new__(cls, name, bases, namespace)

class Test(metaclass=BrokenMeta):
    def method(self):
        return super().__init__()  # 🔴 RuntimeError: __class__ not set

# ✅ DOĞRU KULLANIM
# ---------------------
class SafeMeta(type):
    def __new__(cls, name, bases, namespace):
        # __classcell__ varsa, dokunma, olduğu gibi aktar
        return super().__new__(cls, name, bases, namespace)

# ✨ Özet:
# - __classcell__ = class gövdesinde `__class__`/`super()` için gerekli
# - Silme, poplama, `dict()` gibi copy işlemlerinden kaçın
# - Doğrudan `namespace` ile çalışmak en güvenli yoldur
