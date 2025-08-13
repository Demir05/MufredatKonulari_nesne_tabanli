# ============================================================
# 📌 __context__ Attribute — Tanım ve Detaylar
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Nedir?
# ------------------------------------------------------------
# - Bir exception instance’ının __context__ attribute’u,
#   bu exception fırlatılmadan hemen önce *aktif olan* başka bir exception
#   varsa, ona referans tutar.
#
# - Yani "şu hata sırasında bu başka hata oluştu" bilgisini saklar.
# - Türü: Exception veya None
#
# ------------------------------------------------------------
# 2️⃣ Nasıl oluşur?
# ------------------------------------------------------------
# - Bir exception handler (except bloğu) içinde başka bir exception raise edilirse
#   Python, yeni exception’ın __context__ alanına önceki exception’ı otomatik koyar.
#
# - Bu durum **raise from** kullanılmadığında olur.
# - Eğer `raise ... from ...` kullanılırsa __context__ yerine __cause__ set edilir.
#
# ------------------------------------------------------------
# 3️⃣ Kullanım Alanları
# ------------------------------------------------------------
# ✔ Exception zincirleme → Hata akışını anlamak.
# ✔ Debugging → Asıl hatanın neden oluştuğunu geriye doğru takip etmek.
# ✔ Loglama → Önceki ve sonraki hataları birlikte kaydetmek.
#
# ------------------------------------------------------------
# 4️⃣ Örnek: Otomatik dolma
# ------------------------------------------------------------
try:
    int("abc")                # ValueError oluşur
except ValueError:
    1 / 0                     # ZeroDivisionError oluşur

# Bu örnekte ZeroDivisionError instance’ının __context__’i
# otomatik olarak ValueError instance’ına referans olur.
try:
    try:
        int("abc")
    except ValueError as e1:
        1 / 0
except ZeroDivisionError as e2:
    print("Şimdiki hata:", type(e2).__name__)
    print("Önceki hata (__context__):", repr(e2.__context__))

# Çıktı:
# Şimdiki hata: ZeroDivisionError
# Önceki hata (__context__): ValueError("invalid literal for int() with base 10: 'abc'")
#
# ------------------------------------------------------------
# 5️⃣ __context__ vs __cause__
# ------------------------------------------------------------
# - __context__ → raise from kullanılmazsa, önceki exception otomatik atanır.
# - __cause__   → raise from kullanılırsa manuel atanır, __context__ bastırılır.
#
# ------------------------------------------------------------
# 6️⃣ __suppress_context__ ile ilişkisi
# ------------------------------------------------------------
# - Bir exception’ın __suppress_context__ attribute’u True yapılırsa,
#   traceback’te __context__ bilgisi gösterilmez.
# - Bu genelde raise from kullanıldığında otomatik yapılır.
#
# ------------------------------------------------------------
# 7️⃣ Özet
# ------------------------------------------------------------
# __context__:
# - Bir exception, başka bir exception sırasında oluştuğunda otomatik dolar.
# - raise from kullanılmazsa devreye girer.
# - Hata zincirini görmek ve debug etmek için önemlidir.
