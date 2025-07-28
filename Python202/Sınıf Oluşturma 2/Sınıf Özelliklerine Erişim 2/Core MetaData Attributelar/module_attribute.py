# ==========================================================
# 🧠 PYTHON'DA __module__ ATTRIBUTE — DETAYLI AÇIKLAMA
# ==========================================================

# ✅ __module__ nedir?
# ---------------------
# - Her sınıf tanımlandığında Python otomatik olarak bu attribute'u ekler.
# - Sınıfın tanımlandığı dosyanın (modülün) adını tutar.
# - Yani bu sınıfın "hangi modüle ait olduğunu" gösterir.

# 🔸 Örneğin:
# - Eğer sınıf main.py dosyasında tanımlanmışsa değeri: "__main__"
# - Eğer başka bir dosyada tanımlanmış ve import edilmişse değeri: "dosya_adi" veya "paket.adı"

# ✅ Neden önemlidir?
# ---------------------
# - Sınıfın **nerede tanımlandığını** anlamamıza yarar.
# - Debug (hata ayıklama) ve logging (loglama) gibi işlemlerde kullanılır.
# - Gelişmiş sistemlerde sınıfın ait olduğu modülü dinamik olarak belirlemek için kullanılır.
# - Sphinx gibi dokümantasyon araçları, sınıfların tam yerini buradan alır.

# ✅ Gerçek hayatta nasıl kullanılır?
# ------------------------------------
# - ORM sistemleri sınıfın hangi modülden geldiğini anlamak için kullanır.
# - Dinamik import işlemleri yapılırken (örneğin: getattr(importlib.import_module(...), ...))
# - Büyük projelerde modüller arası ayrımı otomatikleştirmek için

# ✅ Değeri değiştirilebilir mi?
# -------------------------------
# - Evet, bir string olduğu için elle değiştirilebilir:
#   MyClass.__module__ = "yeni.modul.adi"
# - Ancak bu önerilmez! Çünkü introspection ve debug işlemlerinde kafa karışıklığı yaratır.

#   `__name__` bir script’in çalışma bağlamını belirlerken,
#   `__module__` bir nesnenin tanım bağlamını tutar.


# ✅ Aralarındaki Fark
# ----------------------
# | Özellik        | __name__               | __module__              |
# |----------------|------------------------|--------------------------|
# | Nerede Tanımlı?| Global                 | Sınıf/fonksiyon içi     |
# | Ne Anlatır?    | Dosya çalıştırma şekli | Sınıfın tanım yeri      |
# | Tipi           | str                    | str                     |
# | Kullanım Alanı | main kontrolü          | ORM, debugger, loglama  |


# ✅ Neden İkisine de ihtiyaç var?
# ---------------------------------
# - `__name__` programın nasıl çalıştığını anlamak için (main mi import mu)
# - `__module__` ise bir sınıfın nerede yazıldığını takip etmek için gereklidir.
# - Örneğin: bir ORM sistemi veya seri hale getirme (serialization) işlemi yaparken
#   bir sınıfın geldiği modülü bilmen gerekir ➜ `__module__`

# ✅ Bonus: __module__ + __qualname__ birlikte kullanılır!
# ---------------------------------------------------------
# - Bir sınıfın tam yolunu belirtmek için:
#   full_path = f"{cls.__module__}.{cls.__qualname__}"

# ✅ Örnek:
# ----------
class Person:
    pass

print(Person.__module__)  # 👉 "__main__" (eğer bu dosyada tanımlandıysa)


# ============================================================
# 🏗️ ORM SİSTEMİ İÇİN __module__ KULLANIMI — ÖRNEK SENARYO
# ============================================================

# 📦 Diyelim ki farklı modüllerde model sınıflarımız var
# Örneğin, user.py ve product.py dosyalarında modeller tanımlanmış

# 👉 user.py
class User:
    id: int
    name: str

# 👉 product.py
class Product:
    id: int
    price: float

# ⚙️ ORM Sistemimiz: Kayıtlı modelin hangi modülde olduğunu
# __module__ sayesinde otomatik olarak anlayacak

# =============================
# 🔧 ORM Utility Function
# =============================

def get_model_path(cls):
    """
    Modelin tam yolunu (modül + sınıf adı) döndürür.
    """
    return f"{cls.__module__}.{cls.__qualname__}"


# =============================
# 🧪 ÖRNEK KULLANIM
# =============================

print(get_model_path(User))     # "user.User" (user.py'de tanımlıysa)
print(get_model_path(Product))  # "product.Product"

# =============================
# 🚀 Neden Önemli?
# =============================
# - ORM sistemleri modelleri kayıt ederken tam tanım kullanır
# - Modül + sınıf adı bir ID gibi davranabilir
# - Dinamik yüklemelerde (örneğin importlib ile) modül adı gerekir
# - Aynı ada sahip ama farklı modüldeki sınıflar çakışmaz

# Örn:
#   importlib.import_module("product").Product
#   getattr(importlib.import_module(cls.__module__), cls.__name__)
