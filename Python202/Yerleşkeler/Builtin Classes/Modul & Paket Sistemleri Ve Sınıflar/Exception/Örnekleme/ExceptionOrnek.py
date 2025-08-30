# ============================================================
# 📌 Exception, Alt Sınıfları ve BaseException — Örnek (Instance) Mantığı
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Temel Hiyerarşi
# ------------------------------------------------------------
# - Python'daki tüm exception sınıfları **BaseException**'dan türemiştir.
# - Kullanıcı kodunda genellikle Exception ve onun alt sınıfları kullanılır.
#
#   BaseException
#   ├── Exception                (genel hatalar, çoğu burada)
#   │   ├── ArithmeticError
#   │   │   ├── ZeroDivisionError
#   │   │   └── OverflowError
#   │   ├── LookupError
#   │   │   ├── IndexError
#   │   │   └── KeyError
#   │   ├── ValueError
#   │   │   └── UnicodeError
#   │   ├── TypeError
#   │   └── ... (daha birçok built-in exception)
#   ├── SystemExit               (exit çağrıldığında atılır)
#   ├── KeyboardInterrupt        (Ctrl+C)
#   └── GeneratorExit            (generator close())
#
# - BaseException’ın altındaki SystemExit, KeyboardInterrupt gibi bazı sınıflar
#   özel amaçlıdır ve genelde try/except ile YAKALANMAZ (bu yüzden except Exception: kullanılır).

# ------------------------------------------------------------
# 2️⃣ Örnek oluşturma mantığı
# ------------------------------------------------------------
# - Exception sınıfları normal Python sınıflarıdır.
# - Bir exception fırlatmak için onun **örneğini (instance)** oluşturursun.
# - raise Exception("mesaj") → burada Exception() bir instance döner.
# - raise ValueError("mesaj") → ValueError() da bir instance döner.
#
#   type(ValueError)        → <class 'type'>      (ValueError bir sınıf)
#   type(ValueError())      → <class 'ValueError'> (ValueError() bir instance)
#   isinstance(ValueError(), Exception) → True    (ValueError instance’ı, Exception’dan türemiştir)

# ------------------------------------------------------------
# 3️⃣ ValueError() örneği
# ------------------------------------------------------------
err = ValueError("Geçersiz değer")
print(isinstance(err, ValueError))     # True → Bu bir ValueError örneği
print(isinstance(err, Exception))      # True → Exception’dan türediği için
print(isinstance(err, BaseException))  # True → En tepede BaseException var
print(type(err))                       # <class 'ValueError'>
print(err.args)                        # ('Geçersiz değer',) → Exception base class’ın args tuple’ı

# ------------------------------------------------------------
# 4️⃣ Dunder attribute’lar (Exception/ValueError gibi sınıflarda)
# ------------------------------------------------------------
# - __init__(*args): Mesajı veya başka bilgileri args olarak saklar.
# - __str__(): str(instance) çağırıldığında args[0] varsa onu döner.
# - __repr__(): Debug temsili verir (class adı + args).
# - __reduce__(): Pickle için (ileri seviye).
# - __context__, __cause__, __suppress_context__, __traceback__: Exception chaining ve traceback bilgisi.
#
# Bunların çoğu **BaseException** içinde tanımlıdır, alt sınıflar genelde sadece __init__ ekler veya override eder.

# ------------------------------------------------------------
# 5️⃣ BaseException instance mantığı
# ------------------------------------------------------------
# - BaseException da normal bir sınıftır → instance oluşturabilirsin (ama pratikte yapmazsın).
# - raise BaseException("mesaj") → bu da çalışır ama genelde önerilmez.
# - Çünkü BaseException, sistem seviyesindeki exception’ları (SystemExit, KeyboardInterrupt) kapsar.
# - except Exception: blokları, BaseException’ın bazı alt sınıflarını YAKALAMAZ (örn. SystemExit).
# - Bu yüzden kritik sistem sinyalleri bozulmaz.

# ------------------------------------------------------------
# 6️⃣ Özet
# ------------------------------------------------------------
# ✔ Exception sınıfları → instance oluşturulabilir.
# ✔ raise sırasında instance oluşturmazsan (sadece sınıf verirsen) → Python otomatik olarak instance yaratır:
#       raise ValueError   → Python bunu raise ValueError() şeklinde dönüştürür.
# ✔ instance → hata tipinin verisini (mesaj, args) + traceback/context bilgilerini taşır.
# ✔ type(instance) → Hata tipini verir.
# ✔ isinstance(instance, Exception) → True ise bu normal bir hata sınıfıdır.
