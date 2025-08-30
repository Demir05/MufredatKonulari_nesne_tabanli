# ============================================================
# 📌 PYTHON'DA TRY / EXCEPT / ELSE / FINALLY
# ============================================================
# Bu 4 blok birlikte ya da ayrı ayrı kullanılabilir.
# Amaç: hataları yakalamak, alternatif işlem yapmak ve cleanup sağlamak.
# ============================================================

# ------------------------------------------------------------
# 1️⃣ try
# ------------------------------------------------------------
# - Hata yakalama yapısının başlangıç bloğudur.
# - İçine yazılan kod çalıştırılır.
# - Eğer bu blok içinde exception oluşursa, Python uygun except bloğuna atlar.
# - Eğer hata olmazsa except atlanır, else varsa ona geçilir, finally her durumda çalışır.
#
# Örnek:
# try:
#     x = 1 / 0   # Hata: ZeroDivisionError
# except ZeroDivisionError:
#     print("sıfıra bölme hatası yakalandı")

# ------------------------------------------------------------
# 2️⃣ except
# ------------------------------------------------------------
# - try içinde oluşan hataları yakalar.
# - Spesifik hata tipleri verilebilir (önerilen) veya tamamen genel (Exception) yazılabilir.
# - Birden fazla except bloğu olabilir (farklı hata tiplerini ayrı ayrı yakalamak için).
# - Hata nesnesini yakalamak için "as" kullanılabilir.
#
# Örnek:
# try:
#     int("abc")
# except ValueError as e:
#     print("ValueError:", e)

# ------------------------------------------------------------
# 3️⃣ else
# ------------------------------------------------------------
# - try bloğu **başarılı şekilde** (hatasız) tamamlanırsa çalışır.
# - except bloğu çalışmışsa else atlanır.
# - Genelde "try içinde hata olmadı, şimdi şu ek işlemi yap" mantığında kullanılır.
#
# Örnek:
# try:
#     result = int("123")
# except ValueError:
#     print("geçersiz sayı")
# else:
#     print("dönüşüm başarılı:", result)

# ------------------------------------------------------------
# 4️⃣ finally
# ------------------------------------------------------------
# - Hata olsa da olmasa da her zaman çalışır.
# - Kaynak kapatma, temizleme (cleanup) gibi işlemler için kullanılır.
# - return veya break olsa bile finally çalışır (istisna: process kill).
#
# Örnek:
# try:
#     f = open("test.txt", "w")
#     f.write("Merhaba")
# finally:
#     f.close()  # Dosya her durumda kapanır

# ============================================================
# 📌 EN İYİ KULLANIM ÖRNEĞİ
# ============================================================
# try:
#     # riskli işlem
# except BelirliHata:
#     # hata yönetimi
# else:
#     # hata yoksa yapılacak ek işlemler
# finally:
#     # her durumda cleanup


# ============================================================
# 7️⃣ try içinde exception zincirleme (except ... as e: raise ... from e)
# ============================================================
# Amaç:
# - Alt katmanda oluşan hatayı yakalayıp, üst katmana "daha anlamlı" bir tip ile iletmek.
# - Aynı zamanda "sebep zinciri" (__cause__) kaybolmasın diye raise from kullanmak.

def read_number(text: str) -> int:
    try:
        return int(text)                       # Burada ValueError olabilir
    except ValueError as e:                    # e → orijinal hata nesnesi
        # ValueError'ı doğrudan kullanıcıya vermek istemiyoruz.
        # Bunun yerine domain'e uygun RuntimeError fırlatıyoruz.
        raise RuntimeError("Number parsing failed") from e

# Deneme:
# read_number("abc")
# Traceback'te şunu görürsün:
# ValueError: invalid literal for int() with base 10: 'abc'
#
# The above exception was the direct cause of the following exception:
# RuntimeError: Number parsing failed

# 📌 Not:
# - raise from e → __cause__'a e'yi atar → zincir görünür
# - raise from None → __context__ veya __cause__'u gizler

# ------------------------------------------------------------
# Neden önemli?
# - Büyük projede hata tipini "anlamlı hale getirmek" gerekir.
# - Alttaki teknik detayı saklamadan üst katmana iletmek debug için hayat kurtarır.
# - Doğrudan "raise" yaparsan zincir __context__ ile kurulur ama "direct cause" olarak görünmez.


# ============================================================
# 8️⃣ finally ile kaynak temizleme best practices
# ============================================================
# Amaç:
# - try bloğu nasıl biterse bitsin (normal çıkış, return, break, exception),
#   finally bloğu HER ZAMAN çalışır.
# - Dosya kapatma, veritabanı bağlantısı bırakma, lock açma, network soketi kapatma gibi işlemler burada yapılır.

# 📌 Basit örnek:
def write_data(path: str, data: str):
    f = open(path, "w", encoding="utf-8")      # kaynak (dosya) açtık
    try:
        f.write(data)                          # burada hata olabilir
        # raise RuntimeError("yazma hatası")   # simülasyon için açabilirsin
    finally:
        print("[finally] dosya kapatılıyor")
        f.close()                              # kaynak serbest bırakılır

# write_data("test.txt", "merhaba")

# ------------------------------------------------------------
# Best practice:
# - finally bloğu "mutlaka yapılması gereken" cleanup kodları içermelidir.
# - finally içinde exception fırlatma çok risklidir → orijinal hatayı gömebilir.
# - try ile finally arasında "return" olsa bile finally çalışır.

# ÖRNEK: return olsa bile finally çalışır
def test_finally():
    try:
        print("işlem başladı")
        return "return değer"
    finally:
        print("temizlik yapılıyor...")

# print(test_finally())
# ÇIKTI:
# işlem başladı
# temizlik yapılıyor...
# return değer

# ------------------------------------------------------------
# Context manager alternatifi:
# - with ifadesi (context manager), try/finally temizleme desenini otomatik yapar.
# - Örn: with open(...) as f:  → blok bitince otomatik f.close()
# - Ancak try/finally hâlâ gerekli olabilir:
#     • Birden fazla cleanup işlemi varsa
#     • with kullanamayacağın özel kaynak yönetimlerinde
