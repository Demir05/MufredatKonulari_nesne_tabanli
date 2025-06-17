# --------------------------------------------------------
# 📘 KONU: Bir Fonksiyona Birden Fazla Decorator Verme
# --------------------------------------------------------

# Python'da bir fonksiyona birden fazla decorator eklenebilir.
# Bu decorator'lar yukarıdan aşağıya sırayla uygulanır,
# ama çağırılma sırasında en içteki (en alttaki) önce çalışır.

# ----------------------------------------
# 🧪 ÖRNEK: Fonksiyon Seviyesinde
# ----------------------------------------

def deco1(func):
    def wrapper(*args, **kwargs):
        print("deco1: başla")
        result = func(*args, **kwargs)
        print("deco1: bitir")
        return result
    return wrapper

def deco2(func):
    def wrapper(*args, **kwargs):
        print("deco2: başla")
        result = func(*args, **kwargs)
        print("deco2: bitir")
        return result
    return wrapper

# 🔻 Kullanım
@deco1       # en dışta
@deco2       # önce deco2(func) çağrılır → sonra deco1(wrapped_func)
def f():
    print("asıl fonksiyon")

f()

# ✅ ÇIKTI:
# deco1: başla
# deco2: başla
# asıl fonksiyon
# deco2: bitir
# deco1: bitir

# ----------------------------------------
# 🔁 Sıralama Mantığı:
# f = deco1(deco2(f))
# Yani süsleme yukarıdan aşağıya, çalıştırma içten dışa olur.
# ----------------------------------------


# --------------------------------------------------------
# 🧱 SINIF TABANLI DECORATOR İLE ÇOKLU KULLANIM
# --------------------------------------------------------

class Log:
    def __init__(self, label):
        self.label = label

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"[{self.label}] başla")
            result = func(*args, **kwargs)
            print(f"[{self.label}] bitir")
            return result
        return wrapper

@Log("A")
@Log("B")
def hello():
    print("hello")

hello()

# ✅ ÇIKTI:
# [A] başla
# [B] başla
# hello
# [B] bitir
# [A] bitir

# ----------------------------------------
# 🔁 Bu da şu şekilde çözülür:
# hello = Log("A")(Log("B")(hello))
# Yani yine decorator zinciri sıralı uygulanır.
# ----------------------------------------

# --------------------------------------------------------
# 🤔 DEĞİŞEN BİR DURUM VAR MI? (FONKSİYON vs. SINIF DECORATOR)
# --------------------------------------------------------

# Hayır, mantık aynı.
# Hem fonksiyon bazlı decorator'lar, hem sınıf bazlı decorator'lar
# aynı decorator zinciri mantığına göre çalışır:
#   @A
#   @B
#   def f(): ...
# → f = A(B(f))

# Tek fark, decorator'ın sınıf ya da fonksiyon olması değil;
# decorator'ın ne yaptığıdır.


# --------------------------------------------------------
# ⚠️ AYNI İSİMLİ FONKSİYONA SIRAYLA DECORATOR EKLEME
# --------------------------------------------------------

# Şöyle bir kullanım düşünelim:

@deco1
def x():
    print("ilk sürüm")

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
