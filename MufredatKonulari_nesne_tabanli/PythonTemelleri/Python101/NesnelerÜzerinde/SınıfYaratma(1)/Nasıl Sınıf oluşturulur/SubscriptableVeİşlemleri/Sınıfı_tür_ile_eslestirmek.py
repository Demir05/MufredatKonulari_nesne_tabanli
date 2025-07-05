# 📦 __class_getitem__ → NEDİR?
# `__class_getitem__`, bir SINIFIN üzerine [ ] operatörünü uyguladığımızda çalışan özel (dunder) bir metottur.
# Yani A[x] yazıldığında, A.__class_getitem__(x) çağrılır.
# ✅ Sınıf düzeyinde çağrılır, nesne örneği oluşturmaz. Yani 'MyClass[T]' gibi ifadelerde çalışır.
# ✅ Bu metod sayesinde, sınıf tanımları alt sınıf gibi özelleştirilebilir.
# ✅ __getitem__ ile karıştırılmamalıdır; o nesne seviyesinde [] kullanımını sağlar.

# 🚫 __class_getitem__ yalnızca sınıf üzerinde çalışır, örnek üzerinde çalışmaz.
# 🔧 Bu metod kullanılarak sınıfın __getitem__ davranışı sınıf düzeyinde modellenmiş olur.
# cls → sınıfın kendisini temsil eder (tıpkı classmethod'lardaki gibi).
# item → köşeli parantez içine verilen tür veya değer (örnek: MyClass[str] → item = <class 'str'>) veriler, otomatik olarak tuple olarak saklanır
# Bu metot sadece sınıf düzeyinde çağrılır, örneklenmiş nesnelerde çalışmaz.
# @classmethod ile işaretlenmesine gerek yoktur çünkü Python bu özel metodu otomatik olarak cls ile çağırır.


# 🧠 Amaç:
# Bu metodun amacı sınıfları "subscriptable" hale getirmektir.
# Genellikle tip bildirimi (type hinting) ve generic yapılar için kullanılır.
# Ancak sadece typing değil, kendi API'lerini yazan geliştiriciler de bu yapıyı kullanabilir.

# 🧪 Basit örnek:
class MyMetaAware:
    def __class_getitem__(cls, item):
        print(f"__class_getitem__ çağrıldı! Alınan parametre: {item}")
        return f"MyMetaAware[{item}]"

# Kullanımı:
print(MyMetaAware[int])  # __class_getitem__ çağrılır

# 🔎 Nerelerde kullanılır?
# - typing.Generic sınıflarında: Box[str] gibi kullanımların arkasındaki mekanizma budur.
# - ORM sistemlerinde: sütun tiplerini dinamik olarak belirlemek için.
# - DSL (Domain Specific Language): özel yazım kuralları için sınıf davranışı kontrolü.

# 🧩 Farkı nedir?
# __getitem__ → Nesneler (örnekler) için [] işaretini yakalar (x[0])
# __class_getitem__ → Sınıflar için [] işaretini yakalar (X[0])

# 🛠️ Bizim de tanımlayabileceğimiz bir yapıdır.
class Vector:
    def __class_getitem__(cls, item):
        print(f"Vector parametrelendi: {item}")
        return cls  # istersen tip kontrolü, yeni sınıf üretimi vs. burada yapabilirsin

Vector[int]  # Çıktı: Vector parametrelendi: <class 'int'>


# ❗ Yanlış/Karışık Kullanım Örneği
class A:
    ad = "A Sınıfı"

    # __class_getitem__ → özel bir sınıf düzeyi metottur.
    # Amacı, genellikle tür parametrelemesi yapmak için kullanılır.
    def __class_getitem__(cls, item):
        # Sadece 'a' değeri geldiğinde, class attribute olan 'ad' değerini döndürür.
        # Bu, __class_getitem__'in alışılmış kullanım amacına aykırıdır.
        if item == "a":
            return cls.ad

# 🔹 Burada A["a"] ifadesi __class_getitem__'i çağırır.
aa = A["a"]
print(aa)  # "A Sınıfı" → çünkü yukarıda cls.ad döndürülüyor.

# ⛔ Ancak aşağıdaki ifade hata verir:
# aa = A["a"]()  ❌
# Çünkü A["a"] ifadesi bir sınıf dönmek yerine bir string ("A Sınıfı") döndürdü.
# Ve string objesi çağrılabilir (callable) olmadığı için TypeError alınır.

# 🔍 Neden uygun değil?
# __class_getitem__'in amacı, örneğin:
#   Box[int], Box[str], Response[User]
# gibi tür bildirimleri ve parametrik generic yapılardır.

# Senin örneğinde bu tür bir generic yapı yok.
# __class_getitem__ burada sadece bir kontrol ve erişim aracı gibi kullanılmış.
# Bu nedenle "yanlış değil ama amaç dışı bir kullanım" denebilir.

# 🔄 Peki bu yapı neyi döndürmeli?
# Eğer __class_getitem__ çağrıldığında bir sınıf döndürseydi, örneğin:
# class A:
#     def __class_getitem__(cls, item):
#         class Inner:
#             def __init__(self):
#                 self.name = item
#         return Inner
#
# aa = A["Ali"]()  ✅  # Bu sefer çalışır çünkü sınıf döner, örneklenebilir olurdu.

# 🧠 return ne işe yarar?
# __class_getitem__ bir fonksiyondur ve sonucu döndürmesi beklenir.
# Python'da [] ifadesi aslında __getitem__ veya __class_getitem__ çağrısıdır.
# Bu çağrıdan dönen şey her ne ise — ister sınıf, ister tür, ister değer — o alınır.

# 📌 Sonuç olarak:
# ✔ return gerekli çünkü [] ifadesi bir şey döndürmeli.
# ❗ Ama döndürdüğün şeyin mantıklı ve kullanılabilir olması gerekir.
# 🔧 __class_getitem__'in ideali: generic yapı + tür uyumu
# 🔍 Örneğinde ise sadece class attribute dönüyor → bu, fonksiyonel ama kafa karıştırıcı.

from abc import ABC, abstractmethod

class GenericAlias:
    def __init__(self, cls, *items):
        self.cls = cls
        self.items = items
        print(items)
    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

class Generic(ABC):

    def __init__(self):
        raise TypeError("Bu sınıf örneklenemez !")

    def __class_getitem__(cls, item):
        return GenericAlias(cls, item)


class A(Generic):

    def __init__(self, isim):
        self.isim = isim


isim = A[str,int]("demir")
print(isim.isim)
isim2=type(A).__mro__[1].__dict__['__call__'].__get__(A).__call__("dem")
isim2 = object.__new__(A,isim2)
type(isim2).__dict__['__init__'](isim2,"demir3")
print(isim2.isim)