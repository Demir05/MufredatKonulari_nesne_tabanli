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

# Adım 2: __init__'in döndürdüğü nesne, süslenen fonksiyonu alabilmek için callable (yani __call__) olmalıdır.

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