# =========================================================
# 🧠 PYTHON'DA __slots__ ve METACLASS İLİŞKİSİ — TEORİK AÇIKLAMA
# =========================================================

# ✅ __slots__ nedir?
# ---------------------
# __slots__ özel bir attribute'dur.
# Bir sınıfta __slots__ tanımlandığında:
#  - Sınıfın __dict__ attribute'u kaldırılır
#  - Dinamik olarak yeni attribute atanması engellenir
#  - Bellek kullanımı optimize edilir (özellikle çok sayıda nesne yaratıldığında)

# 🔸 Örnek:
# class Person:
#     __slots__ = ("name", "age")

# ✅ Metaclass ile ilişkisi nedir?
# ----------------------------------
# - __slots__ doğrudan metaclass özelliği değildir.
# - Ancak metaclass, sınıf oluşmadan hemen önce çalıştığı için
#   __slots__ kullanımını kontrol edebilir, zorunlu kılabilir ya da otomatik olarak oluşturabilir.

# ✅ Ne işe yarar bu ilişki?
# ---------------------------
# - ORM, validation, memory-sensitive class dizaynlarında,
#   sınıfın optimize edilmesini merkezi bir yapıdan (metaclass) sağlayabilirsin.
# - Özellikle büyük sistemlerde __slots__ zorunluluğu getirmek için çok etkilidir.

# ✅ Sonuç:
# ----------
# - Metaclass, __slots__'u kontrol etmez ama sınıfa eklenmesini zorunlu kılabilir.
# - __slots__ ise doğrudan Python'un belleği yönetme mekanizmasına katkı sağlar.
# - Metaclass bu yönetimi merkezileştirebilir.

# =========================================================
# 🧪 ÖRNEK 1: __slots__ kullanımı zorunlu hale getirme
# =========================================================

class RequireSlotsMeta(type):
    def __new__(cls, name, bases, dct):
        # Eğer __slots__ tanımı yoksa hata ver
        if "__slots__" not in dct:
            raise TypeError(f"{name} sınıfında '__slots__' tanımı zorunludur.")
        return super().__new__(cls, name, bases, dct)

# Geçerli sınıf (slots var)
class User(metaclass=RequireSlotsMeta):
    __slots__ = ("username", "email")
    def __init__(self, username, email):
        self.username = username
        self.email = email

# Geçersiz sınıf (slots eksik)
# class BadUser(metaclass=RequireSlotsMeta):
#     def __init__(self):
#         self.x = 1  # ❌ Hata: __slots__ tanımlanmadı

# =========================================================
# 🧪 ÖRNEK 2: Attribute'lara göre otomatik __slots__ üretme
# =========================================================

class AutoSlotsMeta(type):
    def __new__(cls, name, bases, dct):
        # Sadece doğrudan tanımlı ve özel olmayan değişkenleri topla
        slot_fields = [key for key, val in dct.items()
                       if not key.startswith("__") and not callable(val)]
        dct["__slots__"] = tuple(slot_fields)
        return super().__new__(cls, name, bases, dct)

class Product(metaclass=AutoSlotsMeta):
    name = ""
    price = 0.0

# Artık __slots__ = ("name", "price") otomatik eklenmiş oldu
print(Product.__slots__)  # ('name', 'price')


# ===============================================================
# 🧠 PYTHON'DA __annotations__ VE __slots__ ETKİLEŞİMİ — AÇIKLAMA
# ===============================================================

# ✅ __annotations__ nedir?
# -------------------------
# - Sınıf içindeki attribute'lara verilen type hint bilgilerini tutan özel bir sözlüktür.
# - Bu sözlük otomatik olarak Python tarafından oluşturulur.
# - __annotations__ sadece "hangi değişkenin hangi tipte olduğunu" belirtir, değer içermez.

# Örnek:
# class User:
#     name: str
#     age: int
#
# print(User.__annotations__)  ➜ {'name': <class 'str'>, 'age': <class 'int'>}

# ✅ __slots__ nedir?
# --------------------
# - Sınıfa hangi attribute'ların atanabileceğini sınırlayan özel bir mekanizmadır.
# - Bellek tasarrufu sağlar, __dict__ ve __weakref__ gibi dinamik yapıların oluşturulmasını engeller.

# Bu iki yapı doğrudan bağlı değildir,
# ancak __annotations__ içindeki alanları kullanarak __slots__ listesini otomatik oluşturabiliriz.

# Böylece hem IDE desteği korunur (çünkü type hint yazıyoruz)
# hem de bellek optimizasyonu yapılır (__slots__ sayesinde)

# ===============================================================
# 🧪 ÖRNEK: __annotations__'dan __slots__ OLUŞTURMA
# ===============================================================

class AutoSlotsMeta(type):
    def __new__(cls, name, bases, dct):
        # Sınıfın tanımında __annotations__ varsa, içindeki key'leri al
        hints = dct.get("__annotations__", {})
        # Bu key'leri __slots__ olarak tanımla
        dct["__slots__"] = tuple(hints)
        return super().__new__(cls, name, bases, dct)

# Bu sınıfta sadece type hint yazdık, değer atamadık
class Person(metaclass=AutoSlotsMeta):
    name: str
    age: int

# Metaclass sayesinde __slots__ tanımı otomatik oluştu
print(Person.__slots__)  # ('name', 'age')

# Artık Person sınıfı bellekte optimize çalışır
# Dinamik attribute eklenemez (örneğin: p.surname = "..." hata verir)
