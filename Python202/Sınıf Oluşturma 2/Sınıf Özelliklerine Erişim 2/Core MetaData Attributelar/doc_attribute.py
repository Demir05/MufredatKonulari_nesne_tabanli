# ============================================
# 📘 PYTHON'DA __doc__ ATTRIBUTE — AÇIKLAMA
# ============================================

# ✅ __doc__ nedir?
# -----------------------
# - Her sınıf, fonksiyon veya modül tanımı, Python'da
#   opsiyonel olarak bir "açıklama metni" (docstring) ile başlatılabilir.
# - Bu açıklama, `__doc__` attribute'u olarak otomatik atanır.
# - Programın kendi kendini açıklaması için kullanılır (self-documenting code).

# ✅ Ne işe yarar?
# -----------------------
# - IDE'ler, help() fonksiyonu, sphinx gibi dokümantasyon araçları
#   bu attribute'u kullanarak açıklama üretir.
# - Fonksiyon/sınıf hakkında kullanıcıya bilgi vermek için idealdir.

# ✅ Nerede kullanılır?
# -----------------------
# - Geliştirici rehberleri, otomatik API dökümantasyonu,
#   terminal çıktılarında bilgi sunmak gibi durumlarda.

# ✅ Yöntem:
# -----------------------
# - Açıklama metni, tanımın hemen altına üçlü tırnak içinde yazılır.

# 🔹 Basit örnek:
class Animal:
    """Hayvan sınıfı: türleri ve davranışları temsil eder."""
    pass

print(Animal.__doc__)
# Çıktı: Hayvan sınıfı: türleri ve davranışları temsil eder.

# 🔹 Fonksiyonlar için:
def greet(name: str) -> str:
    """Kullanıcıyı karşılayan basit bir fonksiyon."""
    return f"Merhaba, {name}!"

print(greet.__doc__)
# Çıktı: Kullanıcıyı karşılayan basit bir fonksiyon.

# ✅ ORM gibi gerçek hayat kullanım:
class User:
    """
    🧾 Kullanıcı Modeli
    - İsim, e-posta ve şifre içerir
    - ORM sistemi içinde tabloya karşılık gelir
    """
    name: str
    email: str
    password: str

# Geliştirici terminalde hızlıca bilgi alabilir:
print(User.__doc__)

print(
    type(User()).__dict__["__doc__"]

)
print(type.__class__.__dict__["__doc__"].__get__(type,type))

