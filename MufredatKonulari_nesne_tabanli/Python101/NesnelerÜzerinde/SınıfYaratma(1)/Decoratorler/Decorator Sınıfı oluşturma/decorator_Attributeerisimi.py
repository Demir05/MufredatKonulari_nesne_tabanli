# -----------------------------------------------------
# 📘 KONU: @decorator.x Kullanımı (Sınıf ve Fonksiyon Düzeyi)
# -----------------------------------------------------

# Bu kullanımda decorator bir nesne (sınıf, örnek, modül vs.) olur.
# 'x' ise bu nesne üzerinde tanımlanmış bir decorator fonksiyonudur.

# ----------------------------------------
# 1️⃣ Sınıf içinde tanımlandığında:
# ----------------------------------------

# class Decorators:
#     @staticmethod
#     def x(func):
#         def wrapper(...):
#             ...
#         return wrapper

# Kullanım:
# @Decorators.x
# def f(): ...

# 🔍 ÇÖZÜMLEME:
# - Python, önce Decorators.x ifadesini çözer.
# - Bu, aslında sınıf üzerinde bir attribute erişimidir:
#       Decorators.__getattribute__('x')
# - 'x' fonksiyonu @staticmethod olduğu için doğrudan döner.
# - Sonra decorator çağrısı yapılır:
#       f = x(f)
# - Böylece f, wrapper fonksiyonuyla süslenmiş olur.

# ----------------------------------------
# 2️⃣ Modül veya nesne içinde fonksiyonlar:
# ----------------------------------------

# class deco:
#     @staticmethod
#     def y(func):
#         def wrapper(...):
#             ...
#         return wrapper

# Kullanım:
# @deco.y
# def g(): ...

# 🔍 ÇÖZÜMLEME:
# - deco nesnesi üzerinden 'y' fonksiyonuna erişilir:
#       deco.__getattribute__('y')
# - y callable olduğu için doğrudan çalıştırılır:
#       g = y(g)
# - g artık süslenmiş haldedir.

# ----------------------------------------
# ✅ ORTAK SONUÇ:
# @decorator.x kullanımı, basit bir attribute erişimi + decorator çağrısıdır.
# Değişen hiçbir özel kural yoktur.
# Bu yapı sadece decorator fonksiyonlarını sınıf/modül içinde gruplamaya yarar.
# Hem okunabilirliği artırır hem modüler yapılar kurmaya izin verir.

# ----------------------------------------
# 🧠 TEMEL FORMÜL:
# @decorator.x
#   ↳ decorator.x → attribute (fonksiyon) erişimi (__getattribute__)
#   ↳ decorator.x(func) → gerçek decorator uygulaması
#   ↳ func = wrapper → fonksiyon sarılır ve süslenmiş olur

# ---------------------------------------------
# 🎓 Sınıf içinde decorator.x nasıl tanımlanır?
# ---------------------------------------------

class Decorators:
    @staticmethod
    def uppercase(func):
        # Fonksiyonun sonucunu büyük harfe çeviren decorator
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper

    @staticmethod
    def exclaim(func):
        # Sonuca ünlem ekleyen decorator
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) + "!"
        return wrapper

@Decorators.uppercase
def selam():
    return "merhaba"

@Decorators.exclaim
def duyuru():
    return "dikkat"

# selam() → "MERHABA"
# duyuru() → "dikkat!"


# ---------------------------------------------
# 🧪 Fonksiyon veya modül düzeyinde decorator.x
# ---------------------------------------------

# Fonksiyon değil, bu bir "grup" (namespace) gibi kullanılır:
class deco:
    @staticmethod
    def double(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) * 2
        return wrapper

    @staticmethod
    def reverse(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)[::-1]
        return wrapper

@deco.double
def sayi():
    return 21

@deco.reverse
def mesaj():
    return "selam"




