# ============================================================
# 📌 PYTHON'DA EXCEPTION SINIF HİYERARŞİSİ — ÖZET TANIMLAR
# ============================================================
# Tüm exception’lar BaseException’dan türetilir.
# Exception sınıfı ise "uygulama seviyesindeki" normal hataların ebeveynidir.
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Exception’dan Miras Alan Sınıflar
# ------------------------------------------------------------
# Exception → BaseException → object

# 🧮 ArithmeticError
# - Matematiksel işlemlerle ilgili genel hata sınıfıdır.
# - Alt sınıfları:
#     ZeroDivisionError, OverflowError, FloatingPointError
# Örnek:
#     1 / 0  → ZeroDivisionError
#     math.exp(1000) → OverflowError

# 🔍 LookupError
# - Arama/erişim işlemleri başarısız olduğunda kullanılır.
# - Alt sınıfları:
#     IndexError, KeyError
# Örnek:
#     [1, 2][5]     → IndexError
#     {"a": 1}["b"] → KeyError

# 🔤 ValueError
# - Doğru tipte ama geçersiz değer alındığında fırlatılır.
# Örnek:
#     int("abc") → ValueError

# 🏷️ TypeError
# - Yanlış türde nesne üzerinde işlem yapılmaya çalışıldığında fırlatılır.
# Örnek:
#     "a" + 5 → TypeError

# 📂 OSError
# - İşletim sistemi kaynaklı hataların genel sınıfı.
# - Alt sınıfları: FileNotFoundError, PermissionError, TimeoutError...
# Örnek:
#     open("olmayan.txt") → FileNotFoundError

# 📡 ImportError
# - Modül veya isim import edilemediğinde fırlatılır.
# - Alt sınıf: ModuleNotFoundError
# Örnek:
#     import olmayan_modul → ModuleNotFoundError

# 🧵 RuntimeError
# - Belirli bir kategoriye uymayan, çalışma zamanındaki genel hatalar.
# Örnek:
#     raise RuntimeError("Genel hata")

# 💡 NotImplementedError
# - Bir metot/sınıf henüz uygulanmamışsa fırlatılır (abstract metodlarda yaygın).
# Örnek:
#     class A:
#         def f(self): raise NotImplementedError()

# ------------------------------------------------------------
# 2️⃣ BaseException’dan Miras Alan (Exception’dan Değil) Sınıflar
# ------------------------------------------------------------
# Bu sınıflar, “uygulama hatası” değil, “özel sinyal” niteliğindedir.
# Bu yüzden except Exception ile yakalanmazlar (bilinçli tasarım).

# 🚪 SystemExit
# - sys.exit() çağrıldığında fırlatılır, programı sonlandırır.
# - Kod içinde yakalanabilir ama genelde bırakılır ki program çıksın.
# Örnek:
#     import sys; sys.exit()

# ⌨️ KeyboardInterrupt
# - Kullanıcı Ctrl+C (SIGINT) gönderdiğinde fırlatılır.
# Örnek:
#     while True: pass  # Ctrl+C ile durdur → KeyboardInterrupt

# 🔄 GeneratorExit
# - Bir generator kapatıldığında (close()) fırlatılır.
# - Genelde generator içinde cleanup yapmak için kullanılır.
# Örnek:
#     def g():
#         try:
#             yield 1
#         finally:
#             print("temizlik")
#     gen = g(); next(gen); gen.close()  # GeneratorExit tetiklenir

# ============================================================
# 📌 ÖZET TABLO
# ============================================================
# | Kategori | Sınıf | Açıklama | Örnek |
# |----------|-------|----------|-------|
# | ArithmeticError alt | ZeroDivisionError | Sıfıra bölme hatası | 1/0 |
# | LookupError alt | IndexError | Liste/dizi index geçersiz | [][5] |
# | LookupError alt | KeyError | Dict’te olmayan anahtar | {}["a"] |
# | Exception alt | ValueError | Geçersiz değer | int("abc") |
# | Exception alt | TypeError | Yanlış tür işlemi | "a"+1 |
# | Exception alt | OSError | OS kaynaklı hata | open("x") |
# | Exception alt | ImportError | Import başarısız | import x |
# | BaseException alt | SystemExit | Program sonlandırma | sys.exit() |
# | BaseException alt | KeyboardInterrupt | Ctrl+C kesmesi | döngü içinde Ctrl+C |
# | BaseException alt | GeneratorExit | Generator kapanışı | gen.close() |
