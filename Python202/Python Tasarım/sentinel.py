
# =============================================================================
#  PYTHON: Sentinel Değerler — Sözel/Terorik Açıklama + Kullanım Alanları + Örnekler
# =============================================================================
#  "Sentinel" Nedir?
# =============================================================================
# • Sentinel, bir değişkenin veya parametrenin "özel bir durumu" temsil etmesi için
#   kullanılan benzersiz ve tanımlı bir nesnedir.
# • En yaygın kullanım alanı:
#     - Parametre verilmedi mi? (default argüman kontrolü)
#     - Özel anlamlı “geçerli olmayan” durumları işaretlemek
#     - “Bu işlem desteklenmiyor” gibi sinyaller göndermek
# • Sentinel değerin en önemli özelliği:
#     - Programın başka hiçbir yerinde aynı değerin tekrar oluşturulamaması
#     - Yalnızca senin kontrolünde olması
# =============================================================================


# =============================================================================
# 1) Sentinel ile None arasındaki fark
# =============================================================================
# • None Python'un kendi özel "değer yok" sembolüdür; tek örnektir (singleton).
# • Ancak bazı durumlarda None geçerli bir değer olabilir (örn: API parametresinde None geçmek)
# • İşte burada özel bir sentinel kullanılır ki "hiç verilmedi" ile "None verildi" ayrımı yapılsın.
#
# Örn:
# def f(x=None):
#     if x is None:
#         ... # hem "hiç verilmedi" hem "None verildi" burada aynı yere düşer
#
# • Sentinel ile bu iki durum birbirinden ayrılır.
# =============================================================================


# =============================================================================
# 2) Sentinel oluşturma yöntemleri
# =============================================================================
# 2.1 En basit ve yaygın yöntem:
#     _MISSING = object()
#
#     - object() Python'un temel sınıfıdır (her şey ondan türetilir)
#     - Burada oluşturulan örnek eşsizdir; başka hiçbir yerde aynı kimliğe sahip olamaz
#     - is karşılaştırmasında yalnızca kendi tanımladığın sentinel ile eşleşir
#
# 2.2 İsimlendirme
#     - Genellikle başında '_' ile özel olduğu belirtilir: _MISSING, _SENTINEL
#     - Büyük harfle yazılır çünkü sabit anlamı taşır
#
# 2.3 Gelişmiş kullanım (sınıf tabanlı sentinel)
#     - Bazı durumlarda sentinel'e anlam katmak için özel bir sınıf yazılır
#     - Bu sınıf genellikle __repr__ override edilerek loglarda anlamlı görünmesi sağlanır
# =============================================================================


# =============================================================================
# 3) Sentinel'in özellikleri
# =============================================================================
# • Benzersiz kimlik: "is" karşılaştırmasıyla doğrulanır
# • Hash'lenebilir: dict/set anahtarı olarak kullanılabilir
# • İmmutable: object() örneği üzerinde yeni attribute tanımlanamaz
# • Kopyalanamaz: copy.copy / deepcopy aynı referansı döndürür
# =============================================================================


# =============================================================================
# 4) Kullanım Senaryoları
# =============================================================================
# 4.1 Fonksiyon varsayılan argüman kontrolü
#     - None geçerli değer olduğunda "atanmadı" ile karıştırmamak için sentinel
#
# 4.2 Özel iş akışı sinyalleri
#     - Fonksiyon zincirlerinde "ben bu işi yapamam, başkasına pasla"
#     - NotImplemented ile benzer mantık ama kendi kontrolünde
#
# 4.3 API geliştirme
#     - Kullanıcıya açık olmayan, dahili durum işaretçileri
# =============================================================================


# =============================================================================
# 5) Örnekler
# =============================================================================

# 5.1 En basit sentinel tanımı
_MISSING = object()

def process_value(val=_MISSING):
    if val is _MISSING:
        print("Parametre verilmedi")
    elif val is None:
        print("Parametre None olarak verildi (geçerli)")
    else:
        print(f"Parametre değeri: {val}")

process_value()        # Parametre verilmedi
process_value(None)    # Parametre None olarak verildi (geçerli)
process_value(42)      # Parametre değeri: 42


# 5.2 Sentinel ile zincirleme kontrol
FAST_PATH = object()

def fast_handler(x):
    if not isinstance(x, int):
        return FAST_PATH  # "ben yapamam" sinyali
    return x * 2

def slow_handler(x):
    return f"Slow işlem: {x}"

def handle(x):
    result = fast_handler(x)
    if result is FAST_PATH:
        result = slow_handler(x)
    return result

print(handle(10))     # 20
print(handle("txt"))  # Slow işlem: txt


# 5.3 Sınıf tabanlı sentinel (loglarda anlamlı görünür)
class Sentinel:
    __slots__ = ("_name",)
    def __init__(self, name):
        self._name = name
    def __repr__(self):
        return f"<Sentinel: {self._name}>"

UNSET = Sentinel("UNSET")

def config_loader(cfg=UNSET):
    if cfg is UNSET:
        return "Default config yüklendi"
    return f"Config dosyası: {cfg}"

print(config_loader())          # Default config yüklendi
print(config_loader("cfg.yml")) # Config dosyası: cfg.yml


# =============================================================================
# Özet
# =============================================================================
# • Sentinel değerler, kontrol akışında özel durumları ayırt etmek için kullanılır.
# • _MISSING = object() en hızlı ve sade yöntemdir.
# • Sınıf tabanlı sentinel ise okunabilirlik ve loglarda netlik sağlar.
# • None ile sentinel'in farkı: None dilin kendi anlamı olan sabiti, sentinel ise tamamen senin kontrolünde özel bir işaretçidir.
# =============================================================================
