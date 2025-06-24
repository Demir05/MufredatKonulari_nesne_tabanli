# --------------------------------------------------------
# 📘 KONU: Bir Fonksiyona Birden Fazla Decorator Verme
# --------------------------------------------------------

# Python'da bir fonksiyona birden fazla decorator eklenebilir.
# Bu decorator'lar yukarıdan aşağıya sırayla uygulanır,
# ama çağırılma sırasında en içteki (en alttaki) önce çalışır.

## -------------------------------------------------------------------
# 🎯 KONU: Nested Decorator Zinciri — Tanımsal ve Adım Adım Açıklama
# -------------------------------------------------------------------

# 🔧 İki adet decorator tanımlıyoruz: deco1 ve deco2
# Her biri kendi wrapper fonksiyonu ile "süsleme" işlemi yapıyor

def deco1(func):
    # deco1(func) çağrıldığında, func içine deco2'nin wrapper'ı gelir!
    def wrapper(*args, **kwargs):
        print("deco1: başla")

        # Burada func, deco2'nin wrapper fonksiyonudur!
        result = func(*args, **kwargs)

        print("deco1: bitir")
        return result
    return wrapper

def deco2(func):
    # deco2(func) çağrıldığında, func içine orijinal hello() gelir!
    def wrapper(*args, **kwargs):
        print("deco2: başla")

        # Burada func, orijinal hello fonksiyonudur!
        result = func(*args, **kwargs)

        print("deco2: bitir")
        return result
    return wrapper

# -----------------------------------------
# ⚙️ Decorator uygulama sırası:
# 1️⃣ hello -> deco2(hello) yapılır
# 2️⃣ deco1(deco2(hello)) ile sarılır
# -----------------------------------------

@deco1
@deco2
def hello():
    print("orijinal hello çalıştı")

# -----------------------------------------
# 🎯 Zincir Mantığı:
# hello = deco1(deco2(hello))
# - deco2(hello) ➝ wrapper_deco2 (func = hello)
# - deco1(wrapper_deco2) ➝ wrapper_deco1 (func = wrapper_deco2)
# -----------------------------------------

# Artık hello = wrapper_deco1

hello()

# -----------------------------------------
# ✅ Beklenen Çıktı:
# deco1: başla
# deco2: başla
# orijinal hello çalıştı
# deco2: bitir
# deco1: bitir
# -----------------------------------------

# 📌 Bu çıktıdan şu sonuç çıkar:
# - İlk çağrılan: en dış decorator = deco1
# - İlk sarılan: en iç decorator = deco2
# - Orijinal fonksiyon: en içte
# - Çalışma sırası: dıştan içe ➝ içten dışa geri

# 🎓 Tanımsal Özet:
# ✔️ Uygulama sırası: C ➝ B ➝ A (içten dışa)
# ✔️ Çağrılma sırası: A ➝ B ➝ C ➝ f() ➝ C ➝ B ➝ A (dıştan içe ➝ içten dışa)

# -------------------------------------------------------------------
# 🎯 KONU: Sınıf Tabanlı Nested Decorator Zinciri — Adım Adım Açıklama
# -------------------------------------------------------------------

# 🔧 İki adet sınıf tabanlı decorator tanımlıyoruz

class Deco1:
    def __call__(self, func):
        # Deco1 çağrıldığında bu __call__ tetiklenir
        # func = Deco2 tarafından dönmüş wrapper fonksiyonu

        def wrapper(*args, **kwargs):
            print("Deco1 başla")

            # func burada Deco2'nin wrapper fonksiyonu!
            result = func(*args, **kwargs)

            print("Deco1 bitir")
            return result
        return wrapper

class Deco2:
    def __call__(self, func):
        # Deco2 çağrıldığında bu __call__ tetiklenir
        # func = orijinal hello fonksiyonu

        def wrapper(*args, **kwargs):
            print("Deco2 başla")

            # func burada orijinal hello fonksiyonu!
            result = func(*args, **kwargs)

            print("Deco2 bitir")
            return result
        return wrapper

# -----------------------------------------
# ⚙️ Decorator uygulama sırası:
# 1️⃣ hello -> Deco2() ➝ __call__(hello) ➝ wrapper2
# 2️⃣ Deco1() ➝ __call__(wrapper2) ➝ wrapper1
# -----------------------------------------

@Deco1()  # en son sarılan ➝ en dış katman
@Deco2()  # ilk sarılan ➝ en iç katman
def hello():
    print("Orijinal hello çalıştı")

# -----------------------------------------
# 🎯 Zincir Mantığı:
# hello = Deco1()(Deco2()(hello))
# - Deco2(hello) ➝ wrapper_deco2 (func = hello)
# - Deco1(wrapper_deco2) ➝ wrapper_deco1 (func = wrapper_deco2)
# -----------------------------------------

# Artık hello = wrapper_deco1

hello()

# -----------------------------------------
# ✅ Beklenen Çıktı:
# Deco1 başla
# Deco2 başla
# Orijinal hello çalıştı
# Deco2 bitir
# Deco1 bitir
# -----------------------------------------

# 📌 Bu çıktıdan şu sonuç çıkar:
# - İlk çağrılan: Deco1’in wrapper'ı
# - İlk sarılan: Deco2 (en içte)
# - Orijinal fonksiyon: en içte
# - Akış: Deco1 ➝ Deco2 ➝ hello ➝ Deco2 ➝ Deco1

# 🎓 Tanımsal Özet:
# ✔️ Sınıf decorator’larında da uygulama sırası: içten dışa
# ✔️ Çağırılma sırası: dıştan içe
# ✔️ Tek fark: davranışlar __call__ fonksiyonuna gömülüdür


# --------------------------------------------------------
# ⚠️ AYNI İSİMLİ FONKSİYONA SIRAYLA DECORATOR EKLEME
# --------------------------------------------------------

# Şöyle bir kullanım düşünelim:

@deco1
def x():
    print("ilk sürüm")# deco1: başla

@deco2
def x():
    print("ikinci sürüm")

x()

# 🔍 Ne olur?

# Python yukarıdan aşağıya çalışır.
# İlk olarak:
#   x = deco1(x)
# sonra ikinci kez:
#   x = deco2(x)  ← BU YAZILAN SON SATIR GEÇERLİ OLUR

# Yani bir önceki decorator tamamen **geçersiz hale gelir**.
# Çünkü aynı isimli fonksiyon yeniden tanımlanmıştır.

# ✅ ÇIKTI:
# deco2: başla
# ikinci sürüm
# deco2: bitir

# ----------------------------------------
# 🔁 Bu davranış Python'un "en son tanım geçerlidir" kuralından gelir.
# İkinci decorator aslında başka bir fonksiyonu süslemiyor;
# aynı isimli fonksiyonu **başka bir decorator ile yeniden tanımlıyor**.
# ----------------------------------------

# --------------------------------------------------------
# 🧠 SONUÇ:
# --------------------------------------------------------

# ✅ Birden fazla decorator kullanılabilir, sıralama önemlidir.
# ✅ Hem fonksiyon hem sınıf decorator'ları aynı kurala uyar.
# ✅ Aynı isimli fonksiyona üst üste decorator vermek,
#    önceki tanımı **yok eder**, sadece en son tanım geçerli olur.

global_log = []
class Logla:
    logs = []
    def __init__(self, arg): # Dış fonksiyon, decorator'e verilen argümanı alır
        self._arg = arg # asıl fonksiyon
    def __call__(self,func): # Decorator gibi davrancak,fonksiyon argümanını alcak
        self.target_log = global_log if self._arg == "global" else self.logs
        def wrapper(*args, **kwargs): # sarmalıyıcı
            result = func(*args, **kwargs)
            self.target_log.append(f"function name >>> {func.__name__} , result >>> {result}"
                             f"args >>> {args} , kwargs >>> {kwargs}")
            return result
        return wrapper

class Print:
    def __init__(self, log_instance:Logla):
        self.instance = log_instance # , Logla sınıfın döndürdüğü örnek olur
    def __call__(self, *args, **kwargs):
        print(self.instance.__class__,f" Print'e girilen argüman >>> {args}")
        return self.instance(*args, **kwargs)

@Print
@Logla("logs")
def test(*args, **kwargs):
    return "anan"

l=test("44")
print(l)
print(global_log)