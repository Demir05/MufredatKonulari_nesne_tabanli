# ---------------------------------------------
# 🎯 KONU: Argüman alan sınıf tabanlı decorator
# ---------------------------------------------

# Python'da decorator'e argüman verildiğinde, iki aşamalı bir çağrı zinciri oluşur.

# Örneğin:
# @Decorator(arg)
# def func(): ...

# Bu ifade çözülürken şöyle işler:
# 1. Decorator(arg) → bir nesne döndürür
# 2. Bu nesne (genellikle callable) → func ile çağrılır

# Yani şu eşdeğer:
# func = Decorator(arg)(func)

# ---------------------------------------------
# 🧱 Sınıf ile nasıl yazılır?
# ---------------------------------------------

# Adım 1: Sınıfın __init__ metodu, decorator'e verilen ARGÜMANLARI alır.
# Bu sırada decorator henüz bir fonksiyonu sarmıyor, sadece parametreleri alıyor.
# __init__, Decorator fonksiyonu görevinde değil en dış fonksiyon görevinde

# Adım 2: oluşan sınıf örneği, süslenen fonksiyonu alabilmek için callable olmalıdır.
# __call__ metodu, wrapper fonkiyonu değil artık Decorator fonksiyonu görevini alır yani func argümanını alır
# ve wrapper() fonksiyonunu döndürür

# Bu yüzden sınıf hem __init__ hem __call__ metoduna sahip olmalıdır.

# ---------------------------------------------
# 🧪 Ne olur?
# ---------------------------------------------

# @Decorator("log")
# def f(): ...

# Bu satır aslında şuna dönüşür:
#   f = Decorator("log")(f)

# 1. Decorator("log") → __init__ çağrılır, parametre alınır
# 2. (f) → __call__ çağrılır, f fonksiyonu süslenir
# 3. Dönen wrapper fonksiyonu f'nin yerine geçer

# ---------------------------------------------
# 🧠 Özet Zincir
# ---------------------------------------------

# @Decorator(arg)
#    ↳ çağrılır → Decorator.__init__(self, arg)
#    ↳ dönen nesne (self), sonra süslediği fonksiyonla çağrılır
#         → self.__call__(func)
#         → wrapper dönülür
#         → artık func = wrapper

# Bu sayede sınıf hem parametre alır hem de decorator davranışı gösterir.

#------------------------------------------------------------------
# ÖRNEK:
class Log:
    def __init__(self, prefix="LOG"):
        # 1. Decorator'e verilen parametre burada alınır
        self.prefix = prefix

    def __call__(self, func):
        # 2. Gerçek decorator işlevi burada yapılır
        def wrapper(*args, **kwargs):
            print(f"[{self.prefix}] {func.__name__} çağrılıyor...")
            result = func(*args, **kwargs)
            print(f"[{self.prefix}] {func.__name__} tamamlandı.")
            return result
        return wrapper

@Log(prefix="DEBUG")
def topla(a, b):
    return a + b

@Log(prefix="INFO")
def selamla(isim):
    print(f"Merhaba, {isim}!")

# Fonksiyonları çalıştır:
print(topla(3, 4))
selamla("Ayşe")

"""
[DEBUG] topla çağrılıyor...
[DEBUG] topla tamamlandı.
7
[INFO] selamla çağrılıyor...
Merhaba, Ayşe!
[INFO] selamla tamamlandı.
"""

# ---------------------------------------------------------------
# 🎓 self.target_log — Nesneye (örneğe) özgü state taşıma yapısı
# ---------------------------------------------------------------

# 📌 Tanım:
#   self.target_log gibi bir yapı, bir sınıfın örneklerine özel veri tutmak için kullanılır.
#   Bu sayede her örnek (instance) kendi "durumunu" (state) saklayabilir.

# 🧠 Kullanım amacı:
#   - Fonksiyonun süslenmesi sırasında alınan ayarları veya çalışma verilerini saklamak
#   - Aynı sınıftan farklı örnekler üretip, her birinin ayrı veri taşımasını sağlamak
#   - Fonksiyon çağrıldıkça oluşan veriyi örnek içinde tutmak (örn: log, sayaç, flag)

# ✅ Avantajları:
#   - İzole state: Her örnek kendi durumunu taşır
#   - Kolay debug/test: Dışarıdan erişilip analiz yapılabilir
#   - Genişletilebilirlik: Daha sonra ek özellikler eklemek kolay olur

# 🔄 Alternatif yapılarla farkı:
#   - Global değişken: Tüm örnekler aynı yeri paylaşır, çakışma olur
#   - Closure: Kapsam içindeki fonksiyonlarla sınırlı ve genellikle dıştan erişilemez
#   - self.attribute: Örnek bazlı, erişilebilir, düzenlenebilir ➜ en esnek ve Pythonic yapı

# ------------------------------------------------------------------
# 🔎 Basit bir örnek: her decorator örneği kendi log'unu tutar
# ------------------------------------------------------------------

class Logger:
    def __init__(self, name):
        self.name = name              # Örnek adı
        self.logs = []                # 🎯 Burada self.logs = örneğe ait log listesi

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self.logs.append(f"{func.__name__} çalıştı")
            return result
        return wrapper

# Her biri farklı state taşıyan örnekler
logger_a = Logger("A")
logger_b = Logger("B")

@logger_a
def greet():
    print("Hi!")

@logger_b
def bye():
    print("Bye!")

greet()
bye()
greet()

# 📋 Her decorator örneği kendi log'unu tutar
print(logger_a.logs)   # ➜ ['greet çalıştı', 'greet çalıştı']
print(logger_b.logs)   # ➜ ['bye çalıştı']

# ------------------------------------------------------------------------
# 🎯 KONU: Decorator NESNESİ oluşturmanın amacı, avantajı ve kullanımı
# ------------------------------------------------------------------------

# ✅ Normalde bir decorator şöyle tanımlanır:
#     @Decorator("x")
#     def f(...): ...
# Bu durumda Decorator(...) çağrısı her seferinde yeni bir decorator nesnesi oluşturur.

# 🔁 Bunun yerine bir decorator NESNESİ oluşturabiliriz:
#     d = Decorator("x")
#     @d
#     def f(...): ...
# Böylece aynı decorator nesnesi birden fazla fonksiyonda tekrar tekrar kullanılabilir.

# ------------------------------------------------------------------------
# 📌 AVANTAJLARI:
# ------------------------------------------------------------------------

# 1️⃣ 🔁 TEKRAR EDEN KULLANIM:
#     Aynı parametrelerle süsleme yapacaksak, her seferinde @Decorator(...) yazmak yerine
#     bir defa d = Decorator(...) tanımlarız ve onu tekrar tekrar kullanırız.

# 2️⃣ 🧠 PAYLAŞILAN DURUM (STATE) TUTMA:
#     Sınıf içinde self.count, self.log, self.name gibi veriler tanımlanarak
#     farklı fonksiyonların ortak durumları izlenebilir (örnek: çağrı sayısı, loglama, vs.)

# 3️⃣ 🧩 YAPILANDIRILABİLİR DAVRANIŞ:
#     Bir decorator nesnesine ayarlanabilir parametreler (debug=True, prefix=">>") verilip,
#     davranışı esnek hâle getirilebilir.

# 4️⃣ 🧼 DAHA TEMİZ KOD:
#     DRY (Don't Repeat Yourself) ilkesine uygundur. Tek noktadan konfigürasyon yapılır.

# ------------------------------------------------------------------------
# ❓ PEKİ BU SADECE SINIF (CLASS) DECORATOR'LARDA MI GEÇERLİ?
# ------------------------------------------------------------------------

# ✅ HAYIR. Bu yapı fonksiyon tabanlı decorator’lar için de geçerlidir.
#    Yani bir decorator fonksiyonu, argüman alacak şekilde yazılmışsa,
#    onu da NESNE gibi saklayıp tekrar tekrar kullanabiliriz.

# 📌 ÖRNEK:
# def deco(prefix):
#     def actual_decorator(func):
#         def wrapper(*args, **kwargs):
#             print(f"{prefix}: {func.__name__}")
#             return func(*args, **kwargs)
#         return wrapper
#     return actual_decorator

# d = deco(">>")
# @d
# def f(): ...

# ✅ Gördüğün gibi: fonksiyon decorator'larında da aynı mantıkla NESNE gibi davranış kullanılabilir.

# ------------------------------------------------------------------------
# 🧠 SONUÇ:
# - Hem sınıf tabanlı hem fonksiyon tabanlı decorator'larda NESNE oluşturmak mümkündür.
# - Amaç: tekrar kullanabilirlik, ortak state, merkezi kontrol ve yapılandırılabilirliktir.
# - Tek dikkat edilmesi gereken konu: ortak decorator nesnesi state (self.attr) tutuyorsa,
#   bu paylaşılan veriler bilinçli olarak kullanılmalı veya izolasyon yapılmalıdır.
# ------------------------------------------------------------------------

# 👇 ÖNCE: d = Decorator("A") kullanımı nedir, neden yapılır?
# ---------------------------------------------------------------------

# Bu satır, Decorator sınıfından bir NESNE (örnek) oluşturur.
# Bu nesne artık bir decorator gibi kullanılabilir.
# Örnek:
# d = Decorator("A")

# Böylece bu decorator nesnesini birden fazla fonksiyon için tekrar tekrar kullanabiliriz:
# @d
# def f1(a):
#    ...

# @d
# def f2(a):
#    ...

# NOT:
# Burada hem f1 hem de f2, aynı "d" nesnesi ile süslenmiş olur.
# Yani __call__ metodu ikisi için de aynı nesne üzerinden çalışır.

# ---------------------------------------------------------------------
# ❓ PEKİ neden böyle yaptık? Her fonksiyona ayrı ayrı decorator yazamaz mıydık?
# ---------------------------------------------------------------------

# Elbette yazabiliriz:
# @Decorator("A")
# def f1(a):
#    ...

# @Decorator("A")
# def f2(a):
#    ...

# ✅ Bu durumda her @Decorator("A") çağrısı, YENİ BİR Decorator NESNESİ oluşturur.
# Yani:
#   f1 = Decorator("A")(f1)
#   f2 = Decorator("A")(f2)
# şeklinde işler.

# Bu yöntemde f1 ve f2 farklı decorator nesneleri ile süslenmiş olur.
# Dolayısıyla self.func gibi bir değişken "ezilmez" çünkü her sınıf örneği ayrıdır.

# ---------------------------------------------------------------------
# ⚠️ Ama biz ne yaptık?
#   d = Decorator("A")
#   @d
#   def f1...
#   @d
#   def f2...
#   → Bu şekilde aynı nesne tekrar tekrar kullanıldığı için, self.func üzerine yazılır!
# ---------------------------------------------------------------------

# Bu durumda:
#   1. d(f1) çağrıldığında self.func = f1 olur
#   2. d(f2) çağrıldığında self.func = f2 olur → f1 fonksiyonu artık f2'yi çağırır!
#   Çünkü wrapper içinde self.func kullanılıyor ve bu değişken en son ne ise o çalışır.

# ---------------------------------------------------------------------
# 🧠 Özetle:
# - Eğer her fonksiyon için farklı decorator istiyorsan → @Decorator(...) kullan
# - Eğer aynı nesne ile süsleme yapacaksan → self içinde state (durum) tutma!
#   Bunun yerine func'ı wrapper içinde lokal tut
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 💥 EZİLME NEDİR? NEDEN OLUR?
# ---------------------------------------------------------------------

# Eğer bir decorator sınıfı içinde:
#   self.func = func  # gibi bir atama yaparsan
# Bu fonksiyon, sınıfın örneği (instance'ı) üzerinde saklanmış olur.

# Örnek:
class Decorator:
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        self.func = func  # ⛔️ KRİTİK NOKTA: Bu sadece 1 adet func saklar!

        def wrapper(*args, **kwargs):
            print(f"[wrapper] çalışıyor → self.func = {self.func.__name__}")
            return self.func(self.name, *args, **kwargs)

        return wrapper


# 🧪 Şimdi aynı decorator nesnesini iki kez kullanalım:
d = Decorator("ahmet")

@d
def f1(ad):
    print(f"f1 çalıştı: {ad}")

@d
def f2(ad):
    print(f"f2 çalıştı: {ad}")

# ---------------------------------------------------------------------
# 🔍 Ne olur?
# ---------------------------------------------------------------------

# @d uygulaması şuna eşdeğerdir:
#   f1 = d(f1) → bu sırada self.func = f1 olur
#   f2 = d(f2) → BU ANDA self.func ÜZERİNE YENİDEN f2 YAZILIR!
# Dolayısıyla self.func artık sadece f2'yi gösterir.

# ❗️ Ama wrapper fonksiyonu hala self.func üzerinden çağırma yapar:
#   return self.func(...)

# Bu durumda hem f1() hem f2() çağrıldığında aslında f2 çalışır çünkü:
#   - wrapper içinde kullanılan self.func = en son atanan = f2

# ---------------------------------------------------------------------
# 🎬 ÇIKTI:
f1()  # 🔥 Beklenen: f1 çalışır, AMA → f2 çalışır!
f2()  # ✅ Zaten f2

# ---------------------------------------------------------------------
# ✅ NEDEN?
# Çünkü:
# - self.func = tek bir attribute
# - @d ile süslenen her fonksiyon self.func'i YENİDEN YAZAR (ezme!)
# - wrapper içinde self.func kullanıldığı için → hep en son fonksiyonu çağırır

# ---------------------------------------------------------------------
# ✅ ÇÖZÜM:
# Her fonksiyon için ayrı bir func referansı kullan:
# func'ı wrapper içinde LOKAL olarak sakla, self içinde değil!
# Böylece her wrapper kendi func'ına sadık kalır, kimse kimseyi ezmez.


class Decorator:
    def __init__(self, value):
        self.value = value

    def __call__(self, func):
        # self.func ->  ezilme
        def wrapper(*args, **kwargs):
            self.func = func
            print(self.func.__name__)
            return self.func(*args, **kwargs)
        return wrapper

d = Decorator("A")

@d
def a(*args, **kwargs):
    ...

@d
def b(*args, **kwargs):
    ...

a()
b()