# ============================================================
# 📌 RAISE — DETAYLI TANIM + PRATİKLER
# ============================================================

# ------------------------------------------------------------
# 1️⃣ raise NEDİR?
# ------------------------------------------------------------
# - Python’da exception fırlatmak (tetiklemek) için kullanılan anahtar kelimedir.     # hata üretme mekanizması
# - Program akışını anında durdurur ve exception zincirini başlatır.                   # kontrolü except'e taşır
# - raise ile fırlatılan hata try/except ile yakalanabilir.                             # yönetilebilir hata
# - raise kullanarak hem standart hem de kendi özel hata tiplerini fırlatabilirsin.    # custom exception

# ------------------------------------------------------------
# 2️⃣ raise NASIL KULLANILIR?
# ------------------------------------------------------------
# - Temel kullanım: hata tipi + opsiyonel mesaj.                                       # tip ve mesaj bir arada
# - Örnek: raise ValueError("Geçersiz değer")                                          # tip + açıklama
# - Ayrıca bir exception nesnesi de doğrudan fırlatılabilir.                           # hazır nesne fırlatma
# - Parametresiz raise sadece except bloğu içinde kullanılabilir.                      # re-raise

# ------------------------------------------------------------
# 3️⃣ PARAMETRESİZ RAISE (RE-RAISE)
# ------------------------------------------------------------
# - except bloğunda yakalanan hatayı tekrar fırlatmak için kullanılır.                 # hata zincirini devam ettirir
# - Avantajı: Hata üst seviyeye iletilir, ama burada ek loglama vs yapılabilir.        # ek bilgi ekleyebilirsin
try:
    1 / 0
except ZeroDivisionError:
    print("log: sıfıra bölme")  # ek işlem
    raise  # aynı ZeroDivisionError tekrar fırlatılır

# ------------------------------------------------------------
# 4️⃣ raise FROM ile HATA ZİNCİRİ OLUŞTURMA
# ------------------------------------------------------------
# - "Bu hatanın asıl sebebi başka bir hatadır" demek için kullanılır.                  # sebep bağlama
# - raise YeniHata(...) from EskiHata(...)                                             # __cause__ set edilir
# - Traceback'te "The above exception was the direct cause of the following exception" yazar. # zincir bilgisi
try:
    int("abc")
except ValueError as e:
    raise RuntimeError("Dönüşüm yapılamadı") from e

# ------------------------------------------------------------
# 5️⃣ raise İLE ÖZEL EXCEPTION SINIFLARI
# ------------------------------------------------------------
# - Kendi hata tipini tanımlayabilirsin (Exception’dan miras alarak).                  # custom exception
# - Böylece hataları kategorize edebilir, sadece istediğin tipleri yakalayabilirsin.   # tip bazlı yönetim
class MyCustomError(Exception):
    """Özel hata tipi"""
    pass

def risky():
    raise MyCustomError("özel hata oluştu")  # kendi tipini fırlat

# try:
#     risky()
# except MyCustomError as e:
#     print("özel hata yakalandı:", e)

# ------------------------------------------------------------
# 6️⃣ raise KULLANIMINDA EN İYİ PRATİKLER
# ------------------------------------------------------------
# ✅ Doğru exception tipini seç.                  # ValueError, TypeError, OSError...
# ✅ Anlamlı hata mesajı ekle.                     # Hatanın nedenini açık yaz
# ✅ try bloğunu dar tut, hatanın yerini netleştir. # geniş try → hata kaynağı belirsiz olur
# ✅ re-raise yaparken ek bilgi ekleyebilirsin.    # loglama, metrik toplama

# ------------------------------------------------------------
# ⚠️ SIK HATALAR
# ------------------------------------------------------------
# ❌ Exception("...") ile her şeyi genel fırlatmak → tip ayrımı yapılamaz.
# ❌ raise'ı kontrol akışı gibi kullanmak → exceptionlar istisnai durum içindir.
# ❌ try bloğunu aşırı geniş tutmak → gereksiz hataları yakalayabilir.
# ❌ Sebep zincirini kaybetmek (raise from kullanmamak) → hata analizi zorlaşır.
