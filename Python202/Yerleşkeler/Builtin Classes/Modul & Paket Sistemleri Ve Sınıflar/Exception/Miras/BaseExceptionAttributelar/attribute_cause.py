# ============================================================
# 📌 __cause__ Attribute — Tanım
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Nedir?
# ------------------------------------------------------------
# - __cause__, bir exception’un "doğrudan nedeni"ni saklayan attribute’tur.
# - Sadece "raise ... from ..." kullanıldığında veya manuel olarak set edildiğinde dolar.
# - Exception chaining (istisna zincirleme) mekanizmasının parçasıdır.
#
# ------------------------------------------------------------
# 2️⃣ Nerede kullanılır?
# ------------------------------------------------------------
# ✔ Daha düşük seviyedeki teknik hatayı yakalayıp, onu anlamlı bir üst seviye hataya çevirmek.
# ✔ Orijinal hatayı kaybetmeden, üst katmanda anlamlı bir hata mesajı sağlamak.
# ✔ Loglarda hangi hatanın, hangi başka hatadan kaynaklandığını net görmek.
#
# ------------------------------------------------------------
# 3️⃣ raise ... from ... davranışı
# ------------------------------------------------------------
# raise NewError(...) from old_exception
# → NewError instance'ının __cause__ attribute’u old_exception olur.
# → Traceback’te "The above exception was the direct cause of the following exception:" satırı çıkar.
#
# ------------------------------------------------------------
# 4️⃣ Basit örnek
# ------------------------------------------------------------
def parse_number(s: str) -> int:
    try:
        return int(s)  # ValueError olabilir
    except ValueError as e:
        # Burada ValueError'ı kaybetmeden üst seviyeye daha anlamlı hata atıyoruz
        raise RuntimeError("Sayı parse edilemedi") from e

try:
    parse_number("abc")
except Exception as ex:
    print("Hata tipi:", type(ex).__name__)
    print("Üst seviye mesaj:", ex)
    print("Orijinal hata (__cause__):", repr(ex.__cause__))  # __cause__'a erişim

# Çıktı:
# Hata tipi: RuntimeError
# Üst seviye mesaj: Sayı parse edilemedi
# Orijinal hata (__cause__): ValueError("invalid literal for int() with base 10: 'abc'")
#
# Traceback’te ayrıca:
# ValueError...
# The above exception was the direct cause of the following exception:
# RuntimeError...
#
# ------------------------------------------------------------
# 5️⃣ Manuel set etme
# ------------------------------------------------------------
# __cause__ normal bir attribute gibi elle atanabilir:
try:
    raise ValueError("Eski hata")
except ValueError as e:
    new_exc = RuntimeError("Yeni hata")
    new_exc.__cause__ = e  # manuel set
    raise new_exc
