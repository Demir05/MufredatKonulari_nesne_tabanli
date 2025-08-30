# ============================================================
# 📌 ASSERT — DETAYLI TANIM + ÖRNEKLER
# ============================================================

# ------------------------------------------------------------
# 1️⃣ ASSERT NEDİR?
# ------------------------------------------------------------
# - "Bu koşul doğru olmalı" şeklinde programın kendi kendine
#   yaptığı bir kontrol mekanizmasıdır.
# - assert ifadesi çalıştırıldığında:
#       - Eğer koşul True → program normal devam eder.
#       - Eğer koşul False → AssertionError exception fırlatılır.
# - Yapısı:
#       assert koşul, "opsiyonel hata mesajı"
#
# Örnek:
# x = 5
# assert x > 0, "x pozitif olmalı"  # True → devam
# assert x < 0, "x negatif olmalı"  # False → AssertionError

# ------------------------------------------------------------
# 2️⃣ NEREDE KULLANILIR?
# ------------------------------------------------------------
# - Geliştirme (development) aşamasında,
#   kodun varsayımlarının doğru çalışıp çalışmadığını test etmek için.
# - Debugging ve unit test’lerde hızlı kontrol noktaları eklemek için.
# - "Bu noktaya geldiğinde şu koşul her zaman doğru olmalı" dediğin yerlerde.

# ------------------------------------------------------------
# 3️⃣ PRODUCTION'DA NEDEN DİKKATLİ KULLANILMALI?
# ------------------------------------------------------------
# - Python, -O (optimize) modu ile çalıştırıldığında (ör: python -O app.py)
#   assert ifadeleri tamamen kaldırılır.
#   Yani production ortamda güvenlik veya kritik iş mantığı kontrolü olarak
#   assert kullanırsan, bu kontroller optimize modda çalışmaz!
# - Production kodunda "kullanıcı girdi doğrulaması", "yetki kontrolü"
#   gibi kritik durumlar için assert yerine if + raise tercih edilmelidir.
#
# KÖTÜ ÖRNEK (production’da güvenlik açığı):
# def check_password(pwd):
#     assert pwd == "1234", "şifre hatalı"
#     print("Giriş başarılı")
# # python app.py → çalışır, python -O app.py → assert yok, herkes girer!
#
# İYİ ÖRNEK:
# def check_password(pwd):
#     if pwd != "1234":
#         raise ValueError("şifre hatalı")
#     print("Giriş başarılı")

# ------------------------------------------------------------
# 4️⃣ PRATİK ÖRNEKLER
# ------------------------------------------------------------
# A) Debug amaçlı veri kontrolü
def divide(a, b):
    assert isinstance(a, (int, float)), "a sayı olmalı"
    assert isinstance(b, (int, float)), "b sayı olmalı"
    assert b != 0, "b sıfır olamaz"
    return a / b

print(divide(10, 2))   # 5.0
# print(divide(10, 0)) # AssertionError: b sıfır olamaz

# B) Geliştirme aşamasında algoritma doğruluğu testi
def sort_and_check(data):
    sorted_data = sorted(data)
    # Varsayım: listenin sıralı hali en küçükten en büyüğe olmalı
    assert all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1)), \
           "sıralama başarısız"
    return sorted_data

print(sort_and_check([3, 1, 2]))  # [1, 2, 3]

# ------------------------------------------------------------
# 5️⃣ ÖZET
# ------------------------------------------------------------
# - assert = geliştirme sürecinde kendi kendini test mekanizması
# - False olduğunda AssertionError fırlatır
# - Production’da kritik kontrollerde kullanılmaz, çünkü optimize modda çalışmaz
# - Kullanıcı giriş doğrulaması, veri güvenliği gibi konularda
#   if + raise kullanılmalı


# ============================================================
# 📌 ASSERT vs TRY/EXCEPT vs IF+RAISE (Guard Clause)
# ============================================================

# ------------------------------------------------------------
# 1️⃣ assert
# ------------------------------------------------------------
# - Geliştirme sırasında içsel varsayım (invariant) doğrulama aracı.   # üretim için değil, debug için
# - Koşul False olursa AssertionError fırlatır.                        # hata tipi sabittir
# - -O (optimize) modu ile tamamen kaldırılır.                         # güvenlik için kullanılamaz
# - Kullanıcı girdi/güvenlik doğrulaması için uygun değildir.          # production'da risklidir
# - En iyi kullanım: algoritma doğruluğu ve test aşaması.              # developer iddiaları
x = 5
assert x > 0, "x pozitif olmalı"  # doğru → devam
# assert x < 0, "x negatif olmalı"  # yanlış → AssertionError

# ------------------------------------------------------------
# 2️⃣ try / except
# ------------------------------------------------------------
# - Çalışma zamanında beklenen hataları yakalar.                        # kontrollü hata yönetimi
# - Spesifik exception tipleri ile kullanılmalı.                        # hatayı doğru sınıfa göre yakala
# - Hata olursa except çalışır, olmazsa else çalışır.                   # akış kontrolü sağlar
# - Kaynak temizleme finally ile yapılır.                               # cleanup işlemleri
try:
    y = int("123")
except ValueError as e:
    print("geçersiz sayı:", e)  # hata olduğunda çalışır
else:
    print("dönüşüm başarılı:", y)  # hata yoksa çalışır

# ------------------------------------------------------------
# 3️⃣ if + raise (Guard Clause)
# ------------------------------------------------------------
# - Ön koşul sağlanmazsa hemen hata atar ve fonksiyondan çıkar.         # erken çıkış
# - Production’da input, yetki, veri doğrulama için uygundur.           # optimize moddan etkilenmez
# - Anlamlı exception tipi kullanılmalı (ValueError, TypeError vb.).    # hatayı doğru sınıfa ayır
def divide(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):  # tip kontrolü
        raise TypeError("a ve b sayısal olmalı")
    if b == 0:                                                              # sıfır kontrolü
        raise ZeroDivisionError("b sıfır olamaz")
    return a / b

print(divide(10, 2))  # 5.0
# print(divide(10, 0))  # ZeroDivisionError

# ------------------------------------------------------------
# 🧭 Karar Rehberi
# ------------------------------------------------------------
# - “Bu her zaman doğru olmalı; yanlışsa bu bir BUG’tır.”       → assert
# - “Kullanıcı/çevre hata yapabilir; düzgün mesajla yönet.”    → if ...: raise ...
# - “Riskli çağrı yapıyorum; hata beklenebilir, alternatifim var.” → try / except

# ------------------------------------------------------------
# ⚠️ Sık Hatalar
# ------------------------------------------------------------
# - assert ile input/güvenlik kontrolü yapmak → optimize modda kaybolur.
# - except: ile tüm hataları yakalamak → gerçek hataları gizler.
# - try bloğunu gereğinden geniş tutmak → hatanın kaynağı bulunmaz.
# - Exception ile hata atmak → tip ayrımı yapılamaz, her şey genel olur.
