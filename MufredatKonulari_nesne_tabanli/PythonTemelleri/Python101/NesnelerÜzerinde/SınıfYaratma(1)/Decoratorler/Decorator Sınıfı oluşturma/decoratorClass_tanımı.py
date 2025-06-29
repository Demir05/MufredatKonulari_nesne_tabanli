# 📌 Python'da Sınıf Tabanlı Decorator Kullanımı
from jedi.inference.gradual.typing import Callable


# Bir sınıfı decorator olarak kullanmak mümkündür.
# Bunun için __init__ ve __call__ metodlarının tanımlı olması gerekir.

# ---------------------------------------------------------
# NEDEN __init__ GEREKLİ?
# Çünkü Python, decorator'ı şu şekilde çağırır:
#   @MyDecorator
#   def f(): ...
#   => f = MyDecorator(f)
# Burada decorator’a gelen argüman (fonksiyon) __init__ ile alınır.

# ---------------------------------------------------------
# NEDEN __call__ GEREKLİ?
# f() çağrıldığında aslında şu olur:
# MyDecorator(f)()  --> yani sınıf örneği () ile çağrılır
# Eğer __call__ tanımlı değilse => TypeError oluşur
# Bu yüzden sınıfın __call__ metodu olmalı ki fonksiyon gibi çağrılabilsin.

# ---------------------------------------------------------
# SINIFIN DEKORATOR OLARAK AVANTAJLARI:
# - state (durum) tutabilir
# - birden fazla metot barındırabilir
# - konfigürasyon ve esnek kullanım sağlar
# - kodu organize etmek için daha profesyonel bir yapıdır

# ---------------------------------------------------------
# ÖZET:

# ✔ Sınıf tabanlı decorator kullanmak:
#   - init ile fonksiyonu yakalar
#   - call ile çağrılabilir hale getirir
#   - durum saklama (stateful) sağlar
#   - gelişmiş loglama, zamanlama, erişim kontrolü gibi sistemler kurmaya olanak verir

# ---------------------------------------------------------
# ÖRNEK: Sınıf decorator

class Zamanlayici:
    def __init__(self, func):
        self.func = func  # decorator içine gönderilen fonksiyonu sakla

    def __call__(self, *args, **kwargs): # __call__, wrapper gibi çalıştığından dolayı ek bir fonksiyon tanımlanmamıştır
        import time
        start = time.time()
        result = self.func(*args, **kwargs)
        end = time.time()
        print(f"Fonksiyon {self.func.__name__} {end - start:.2f} sn sürdü.")
        return result

# Fonksiyonumuzu sınıf ile süsleyelim
@Zamanlayici
def uzun_islem():
    from time import sleep
    sleep(1)
    print("İşlem tamam!")

uzun_islem()  # Çalıştığında Zamanlayici sınıfı tarafından sarılır ve zaman ölçer

# ---------------------------------------------------------------------
# ÖRNEK: ÇÖZÜMLEME

# Bir sınıf decorator olarak tanımlanıyor
class MyDecorator:
    # 1. Adım: @MyDecorator satırı çalıştığında __init__ devreye girer
    def __init__(self, func):
        print(">>> __init__ çağrıldı")  # Fonksiyon, decorator sınıfına aktarılır
        self.func = func

    # 3. Adım: Fonksiyon çağrıldığında __call__ çalışır
    def __call__(self, *args, **kwargs): # __call__, wrapper görevini üstlenir
        print(">>> __call__ çağrıldı")  # Süslenmiş fonksiyon çağrılıyor
        print(">>> Fonksiyon çalışmadan önce")  # Çağrı öncesi işlemler
        result = self.func(*args, **kwargs)     # Orijinal fonksiyon çalıştırılır
        print(">>> Fonksiyon çalıştıktan sonra")  # Çağrı sonrası işlemler
        return result # return, normal decorator kullanımıdır

# 2. Adım: Bu satır çalışınca => selamla = MyDecorator(selamla)
@MyDecorator
def selamla():
    print("Merhaba!")

# 4. Adım: selamla() çağrıldığında aslında MyDecorator.__call__() çalışır
selamla()

#--------------------------------------------
# ÖZET:

# 1. Python, @decorator ifadesini görür.

# 2. Bu ifade şu anlama gelir:
#    süslenen_fonksiyon = DecoratorSınıfı(süslenen_fonksiyon)

# 3. Bu işlem gerçekleştiğinde, decorator sınıfının __init__ metodu çalışır.
#    Yani, süslenen fonksiyon nesnesi sınıfa argüman olarak gönderilir.
#    __init__, ile bu argümanı alırız ve saklarız

# 4. Decorator sınıfının bir örneği (instance) oluşur ve bu örnek artık süslenen fonksiyonun yerini alır.

# 5. Program ilerleyip süslenen fonksiyon çağrıldığında (örneğin: süslenen_fonksiyon()),
#    aslında sınıfın __call__ metodu tetiklenmiş olur.

# 6. __call__ metodunun içinde istersek fonksiyonu çağırmadan önce/sonra işlemler yapabiliriz,
#    ve en sonunda orijinal fonksiyonu çalıştırabiliriz (veya hiç çalıştırmayabiliriz).

# 7. Eğer decorator sınıfı içinde @staticmethod veya @classmethod tanımlanmışsa,
#    bunlar sınıfın iç işlevleri olarak çağrılabilir ama decorator mekanizmasının temel akışını etkilemezler.


class Logger:
    def __init__(self, func:Callable):
        self._func = func
        self.count = 0
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.__str__()}")
        return self._func(*args, **kwargs)
    def __str__(self):
        return f" Benim adım >>> {self._func.__name__} VE Benim değerim >>> {self.count}"

@Logger
def hello(*args, **kwargs):
    print("Hello World!")

@Logger
def hello2(*args, **kwargs):
    print("Hello World 2!")

hello()
hello2()
hello()
hello2()
"""
 Benim adım >>> hello VE Benim değerim >>> 1
Hello World!
 Benim adım >>> hello2 VE Benim değerim >>> 1
Hello World 2!
 Benim adım >>> hello VE Benim değerim >>> 2
Hello World!
 Benim adım >>> hello2 VE Benim değerim >>> 2
Hello World 2!

"""



