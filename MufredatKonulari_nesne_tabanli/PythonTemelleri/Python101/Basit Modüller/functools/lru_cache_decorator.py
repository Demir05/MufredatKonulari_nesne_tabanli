# -------------------------------------------------------
# ✅ Python: functools.lru_cache Decorator – Derinlemesine Açıklama
# -------------------------------------------------------

from functools import lru_cache

# 🔷 @lru_cache
# -------------------------------------------
# lru_cache (Least Recently Used cache), Python'da recursive veya tekrar eden fonksiyonlarda
# aynı argümanlarla yapılan çağrıların sonucunu bir "cache" bellekte tutarak performansı artıran,
# yerleşik (built-in) bir cache mekanizması sağlayan decorator'dur.

# 🔍 Kullanım Söz Dizimi:
# @lru_cache(maxsize=128)
# def my_func(x):
#     ...

# ⚙️ Nasıl Çalışır?
# -------------------------------------------
# 1️⃣ Fonksiyon her çağrıldığında, verilen argümanlara göre bir "anahtar" (hash) oluşturur.
# 2️⃣ Eğer bu anahtar daha önce hesaplanmışsa, **önceden hesaplanan değer cache'den döner**.
# 3️⃣ Eğer bu anahtar yoksa, fonksiyon hesaplanır, sonucu cache'e kaydedilir.
# 4️⃣ Cache dolmuşsa → En az kullanılan (LRU) öğe silinir, yeni öğe eklenir.

# 💡 Performans Farkı:
# Normal recursive fonksiyonlarda, alt fonksiyon çağrıları **tekrar tekrar hesaplanır**.
# lru_cache, her alt problemi **sadece bir kez çözer**. Özellikle Fibonacci gibi problemler için 1000 kat hız kazandırır.

# 🧪 Parametre: maxsize
# -------------------------------------------
# ➤ maxsize → Cache belleğinde tutulacak maksimum farklı sonucu belirler.
# ➤ Eğer maxsize=None verilirse → cache boyutu sınırsız olur, hiçbir sonuç silinmez.
# ➤ Eğer maxsize=128 verilirse ve 129. farklı giriş yapılırsa:
#     🔄 En az kullanılan (en eski) giriş silinir, yeni değer eklenir.

# ➕ maxsize değeri belirtilebilir:
#    - Yüksek değer: Daha çok cache, daha az tekrar hesaplama, ama daha çok bellek
#    - Düşük değer: Az bellek, ama sık cache temizleme
#    - Uygulamanın büyüklüğüne göre belirlenmelidir

# 🔁 Recursive Fonksiyonlar için:
# -------------------------------------------
# Recursive yapılar çok fazla alt fonksiyon çağrısı yapar. Örneğin fib(100):
#    - fib(99), fib(98), fib(97)... gibi onlarca kez aynı alt fonksiyonlar çağrılır
#    - lru_cache bu tekrarları ortadan kaldırarak hesaplamayı lineer hale getirir

# .cache_info() metodu, cache'in istatistiksel bilgilerini verir.
# Dönen değer bir namedtuple'dır: CacheInfo(hits, misses, maxsize, currsize)
# hits     → Cache'e denk gelen, hesaplamadan dönen çağrı sayısı
# misses   → Cache'te bulunamayan, hesaplanmak zorunda kalan çağrılar
# maxsize  → LRU cache'in tanımlanan maksimum kapasitesi
# currsize → Şu anda kaç farklı argüman kombinasyonu cache'de tutuluyor

# .cache_clear() metodu, cache belleğini tamamen sıfırlar.
# Tüm önceden saklanmış sonuçlar unutulur.
# Genellikle testlerde, ölçümlerde ya da runtime'da yeni hesaplama zorlandığında kullanılır.


# --------------------------------------------------
# ✅ @lru_cache Kullanım Alanları
# --------------------------------------------------

# 1. 🔁 Recursive Fonksiyonlar
# --------------------------------------------------
# Fibonacci, DFS, n! gibi tekrar eden alt çağrılar içeren yapılar.
# Aynı alt problemi defalarca çözmek yerine, sonucu saklar ve doğrudan döndürür.

# 2. 📡 API İstekleri
# --------------------------------------------------
# Aynı endpoint'e aynı argümanlarla tekrar istek yapılacaksa,
# sonucu cache'e koyar → 2. kez aynı URL çağrıldığında anında yanıt döner.

# 3. 🧮 Hesaplama Maliyetli Fonksiyonlar
# --------------------------------------------------
# Büyük matris işlemleri, istatistiksel analiz, graf hesaplamaları.
# Özellikle input sabitse sonucu cache'lemek çok kazanç sağlar.

# 4. 🔍 Veri Sorguları
# --------------------------------------------------
# Aynı SQL query'lerini tekrar tekrar çalıştırmak yerine,
# ilk sorguyu cache'e alır, sonraki çağrılar için cache'den getirir.

# 5. 🧾 Config/Ayar Okuma
# --------------------------------------------------
# Dosyadan okunan ayarlar, sabit yapıdaki veriler tekrar tekrar yüklenmek yerine cache'ten alınabilir.

# 6. 📂 Dosya Parsing
# --------------------------------------------------
# Özellikle büyük JSON/XML dosyaları tekrar işlenmek yerine parse edilmiş versiyonları saklanabilir.

# 7. 🧠 NLP, AI & ML ön hesaplamalar
# --------------------------------------------------
# Tokenizasyon, ön işlem, vektör dönüşüm gibi adımlar cache ile hızlandırılabilir.

# --------------------------------------------------
# ⚠️ Kullanılmaması Gereken Durumlar:
# --------------------------------------------------
# 1. Fonksiyon çıktısı değişkense (örn: zaman, rastgelelik içeriyorsa)
# 2. Fonksiyon yan etki yapıyorsa (örn: dosya yazıyor, DB değiştiriyor)
# 3. Büyük veri döndürüyorsa (RAM şişebilir)


from functools import lru_cache



# -----------------------------------------------
# 🔍 lru_cache(typed=True) Açıklaması
# -----------------------------------------------

# @lru_cache, fonksiyonun sonuçlarını "girdi -> çıktı" şeklinde cache (önbellek) yapan bir decorator'dür.
# typed parametresi, bu eşlemede fonksiyon argümanlarının sadece değerine değil,
# veri tipine göre de ayırt edilip edilmediğini kontrol eder.

# 🔸 typed=False (varsayılan)
# - Argümanlar sadece değere göre karşılaştırılır.
# - f(1) ve f(1.0) aynı kabul edilir → cache ortak olur.

# 🔸 typed=True
# - Argümanların tipleri de anahtarın parçası olur.
# - f(1) ≠ f(1.0) → ayrı ayrı cache anahtarları

# Bu ayar, tip duyarlı hesaplamalarda doğruluk açısından çok önemlidir.

# -----------------------------------------------
# Örnek Fonksiyon
# -----------------------------------------------

@lru_cache(typed=True)  # 🔧 Tip duyarlılığı aktif
def process(value):
    print(f"→ Hesaplandı: {value!r} (type: {type(value).__name__})")
    return value

# -----------------------------------------------
# 🧪 Çağrılar
# -----------------------------------------------

process(5)      # 🟡 İlk kez: hesaplanır ve cache'e eklenir
process(5)      # ✅ Cache HIT: tekrar hesaplanmaz
process(5.0)    # 🟡 Yeni tip (float): farklı anahtar → hesaplanır
process(5.0)    # ✅ Cache HIT

# Eğer typed=False olsaydı:
# process(5) ve process(5.0) aynı kabul edilir, sadece ilk çağrı hesaplanırdı

# -----------------------------------------------
# Ne Zaman typed=True Kullanılır?
# -----------------------------------------------

# ✔️ Eğer fonksiyonun çıktısı argümanın sadece değeri değil, veri tipiyle de değişiyorsa:
#    → typed=True kullanmak gerekir

# ❌ Eğer çıktı, tipi fark etmiyorsa:
#    → typed=False (varsayılan) tercih edilebilir → daha az bellek

# -----------------------------------------------
# Örnek Sonuçlar:
#
# → Hesaplandı: 5 (type: int)
# → Hesaplandı: 5.0 (type: float)
#
# → Sonraki aynı çağrılar cache'den döner
# -----------------------------------------------


# 🧠 Uygulama Örneği:

import time

@lru_cache(maxsize=3)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

start = time.perf_counter()
print(fib(50))
end = time.perf_counter()
print(f"Süre: {end - start:.4f} sn")

print(fib.cache_info()) # CacheInfo(hits=198, misses=201, maxsize=3, currsize=3)

# hits = 198
# -------------------------------------------
# Cache'e denk gelen başarılı sorgu sayısıdır.
# Yani fonksiyon çağrısı önceden cache'e kaydedilmişti, tekrar hesaplama yapılmadı.
# Bu durumda direkt olarak cache'deki değer kullanıldı.
# Yüksek hit oranı = verimli cache kullanımı demektir.

# misses = 201
# -------------------------------------------
# Cache'te bulunamayan, yani hesaplanmak zorunda kalan çağrı sayısıdır.
# Fonksiyon çağrısı daha önce yapılmamış → cache'te yoktu → hesaplandı ve cache'e eklendi.
# Yüksek miss oranı → ya cache yeni başlıyor, ya da maxsize çok küçük!

# maxsize = 3
# -------------------------------------------
# Cache'te aynı anda tutulabilecek maksimum farklı fonksiyon sonucu sayısıdır.
# maxsize=3 demek → cache, en fazla 3 farklı girdi için sonucu saklar.
# Yeni bir girdi geldiğinde → en az kullanılan (LRU) silinir.

# currsize = 3
# -------------------------------------------
# Şu anda cache'te tutulan farklı sonucu sayısıdır.
# Genellikle maxsize’a ulaşır → ve orada sabit kalır.

@lru_cache(maxsize=None)
def file_extension(filename: str) -> str:
    return filename.split('.')[-1].lower()

print(file_extension("test.txt"))


@lru_cache()
def planet_gravity(planet: str) -> float:
    planets = {"earh":9.81, "mars":3.7}
    return planets.setdefault(planet,None)

print(planet_gravity("earh"))
print(planet_gravity("mars"))


def give_key(typed: bool,*args, **kwargs):
    if typed:
        _args = tuple(map(normalize_type,args))
        _kwargs = {k:normalize_type(v) for k,v in kwargs.items()}
        return hash((_args, frozenset(_kwargs.items())))
    return hash((args, frozenset(kwargs.items())))

def normalize_type(x):
    if isinstance(x,float) and x.is_integer():
        return int(x)
    elif isinstance(x,bool):
        return int(x)
    return x

class Mylru_cache:

    def __init__(self,*,maxsize=None, typed= False):
        self.__maxsize = maxsize
        self.__typed = typed
        self.__cache = {}

    def __call__(self, func):
        self.__func = func
        def wrapper(*args,**kwargs):
            key = give_key(self.__typed,*args,**kwargs)
            if key not in self.__cache:
                self.__cache[key] =  func(*args,**kwargs)
                return self.__cache[key]
            return self.__cache[key]

        return wrapper

@Mylru_cache()
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(50))
