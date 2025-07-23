# ==========================================
# 🧠 __classcell__ ATTRIBUTE — NEDİR?
# ==========================================

# 🔹 __classcell__, Python'un sınıf tanım sürecinde kullanılan özel bir cell (hücre) yapısıdır.
# 🔹 Amaç: class gövdesindeki `super()` kullanımının doğru çalışmasını sağlamaktır.

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



# 📖 __class__ ve __classcell__ İLİŞKİSİ — Derin Python Mekanizması

# 🔹 Bir sınıfın içinde `super()` ya da `__class__` kullanıldığında
# Python, bu fonksiyonda `__class__` değişkenine ihtiyaç olduğunu anlar

# 🧠 Ancak bu sırada sınıf (örneğin A) henüz oluşmamıştır!
# Yani doğrudan "__class__ = A" yazmak mümkün değildir.
# Bunun yerine Python şöyle bir numara yapar:

# ➤ 1. Adım: `__class__` closure'ı oluşturur (bu bir cell objesidir)
# ➤ 2. Adım: Bu closure hücresini `__classcell__` ismiyle namespace’e koyar
#           → sen __new__ içinde namespace["__classcell__"] şeklinde görebilirsin
#           → ama bu hücre hâlâ boştur! (empty)

# 🔄 Bu noktada __class__ aslında "tanımlı" ama değeri yoktur. (gecikmeli yerleştirme)

# ➤ 3. Adım: `type.__new__()` çağrıldığında:
#            - Artık sınıf (`A`) oluşturulmuştur
#            - Python, `__classcell__` içindeki cell objesinin içine bu sınıfı (A) yerleştirir
#            - Yani closure artık boş değil! ⇒ __class__ artık geçerli!

# 📦 Bu mekanizma sayesinde:
# - Fonksiyonlar sınıfın tanımı tamamlandığında doğru `__class__` referansına sahip olur
# - `super()` çağrısı artık sorunsuz çalışır

# 🚨 Eğer `__classcell__`'i iletmezsen (boş bırakırsan), Python `RuntimeError` fırlatır:
# "super(): __class__ cell not found"

# ✅ Sonuç:
# `__classcell__`, sınıf oluşana kadar __class__'ı tutan bir taşıyıcıdır
# Python onu type'a verir, type onu fonksiyonların closure’ına yerleştirir
# Senin metaclass `__new__()` metoduna gelmesi sadece bu iletimde bir duraktır

# 🧠 En net özeti:
# "__class__ closure'ı oluşturulur → __classcell__ ile taşınır → type() ile doldurulur"


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

# Bu özel anahtar, class namespace’ine otomatik olarak eklenir
# ve Python tarafından `type.__new__`'a iletilmelidir.

# Eğer silinir veya düzgün aktarılmazsa `super()` çalışamaz.

# 🔴 TEHLİKELİ DURUMLAR
# ----------------------

# ❌ 1. classcell'i elle silmek
def __new__(cls, name, bases, namespace):
    namespace.pop("__classcell__", None)  # <-- bu `super()` hatasına yol açar!
    return super().__new__(cls, name, bases, namespace)


# ✅ DOĞRU KULLANIM
# ---------------------
class SafeMeta(type):
    def __new__(cls, name, bases, namespace):
        # __classcell__ varsa, dokunma, olduğu gibi aktar
        return super().__new__(cls, name, bases, namespace)

# ✨ Özet:
# - __classcell__ = class gövdesinde `__class__`/`super()` için gerekli
# - Silme, poplama, işlemlerinden kaçın
# - Doğrudan `namespace` ile çalışmak en güvenli yoldur


