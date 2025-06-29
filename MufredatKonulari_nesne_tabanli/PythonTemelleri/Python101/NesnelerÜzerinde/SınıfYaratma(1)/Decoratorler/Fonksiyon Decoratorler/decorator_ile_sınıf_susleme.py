# 🔹 CLASS DECORATOR NEDİR?
# - Python’da sınıfları süsleyen (yani @ ile uygulanan) fonksiyonlardır.
# - Bu decorator fonksiyonlar, sınıfı (bir type nesnesi) argüman olarak alır
#   ve geri yine bir type nesnesi döndürmelidir.
import random


# 🔹 SÖZ DİZİMİ
# @decorator
# class MyClass:
#     ...

# Bu, şuna dönüşür:
# MyClass = decorator(MyClass)

# 🔹 TEMEL AMAÇLAR
# - Sınıfa method, property, attribute eklemek
# - Register, debug, log gibi davranışlar kazandırmak
# - Metaclass gibi görünmeden sınıf yapısını kontrol etmek
# - Singleton, freeze, validation gibi örüntüler (patterns) oluşturmak

# 🔹 BASİT BİR DECORATOR ÖRNEĞİ
def add_repr(cls):
    # Sınıfa __repr__ metodu ekler, eğer yoksa
    if '__repr__' not in cls.__dict__:
        def __repr__(self):
            return f"<{cls.__name__} instance: {self.__dict__}>"
        cls.__repr__ = __repr__
    return cls

# 🔹 WRAPPER CLASS NEDİR ve NEDEN GEREKİR?

# Eğer yalnızca sınıfa attribute/metod eklemek istiyorsan yukarıdaki yapı yeterlidir.

# Ancak...
# Eğer:
# - Sınıfın orijinal __init__, __call__, __getattr__ gibi özel metodlarını değiştirmek istiyorsan,
# - Sınıfı özelleştirmek veya örnekleri manipüle etmek istiyorsan,
# - Ya da sınıf yerine alt bir sınıf (subclass) vermek istiyorsan...
# O zaman bir "wrapper class" tanımlarsın!

def wrapper_class_decorator(cls):
    # Orijinal sınıfın bir alt sınıfını oluştur
    class Wrapper(cls):
        def __init__(self, *args, **kwargs):
            print(f"[LOG] {cls.__name__} initialized with {args}")
            super().__init__(*args, **kwargs)

        def __getattr__(self, attr):
            print(f"[TRACE] Accessing attribute: {attr}")
            return super().__getattribute__(attr)

    return Wrapper

# 🔹 NEDEN WRAPPER BİR CLASS (FONKSİYON DEĞİL)?
# Çünkü Python, sınıfları tip (type) olarak bekler.
# Eğer fonksiyon döndürürsen, Python artık o objeyi sınıf gibi kullanamaz:
# MyClass() çağrısı artık hata verir.
# O yüzden wrapper fonksiyon değil, wrapper sınıf döndürmek zorundasın.

# 🔹 KULLANIM ALANI
# - Singleton pattern (aynı instance tekrar döndürmek)
# - Cache mekanizması (örnekleri cache’lemek)
# - Monitoring, izleme
# - Lazy-loading
# - Dynamic subclassing

# 🔹 SONUÇ OLARAK
# - Sınıf decorator'leri sade bir decorator ile sınıf davranışını genişletebilir.
# - Ancak ciddi manipülasyon veya izleme gerekiyorsa, wrapper sınıf kullanılır.
# - Bu wrapper, orijinal sınıfın bir alt sınıfı gibi davranarak tüm metodları override edebilir.


def acces_control(cls):
    # Yeni sınıfı oluştururken, cls'ten kalıtım alıyoruz
    class Wrapper(cls):
        pass  # Şimdilik sadece boş bir sınıf


    for k, v in list(cls.__dict__.items()):
        # Özel (magic) ve '_' ile bitenleri eliyoruz
        if not k.endswith("_") and not k.startswith("__"):
            # Yeni isim üret: random bir string ile gizle
            new_name = f"_{''.join(random.choices(string.ascii_lowercase, k=8))}"
            # Yeni sınıfa bu değişkeni ekle
            setattr(Wrapper, new_name, v)
            # Eski adı sil (gizle)
            delattr(Wrapper, k)

    # Metadata'yı koru (isim, docstring, metotlar vs.)
    return update_class_wrapper(Wrapper)



# 💡 Amaç: mappingproxy sayesinde sınıf attribute'ları korunur, dışarıdan rastgele değiştirilmeleri engellenir.

# ⚠️ SORUN: mappingproxy içindeki bazı attribute'lar taşınamaz olabilir!
# Özellikle C dilinde yazılmış gömülü methodlar, closure'lı fonksiyonlar, descriptor'ler,
# property, staticmethod, classmethod gibi sarmalayıcı yapılar doğrudan aktarılırken hata verebilir.

# ❌ Örnek sorunlu kullanım:
# for k, v in cls.__base__.__dict__.items():
#     type(cls).__setattr__(cls, k, v)  # bazı v değerleri "mappingproxy" ile uyumsuz olabilir!

# Bu tür durumlarda Python aşağıdaki hataları fırlatabilir:
# - AttributeError: attribute '__dict__' of 'type' objects is not writable
# - TypeError: can't set attributes of built-in/extension type

# ✅ Güvenli örnek:
# __repr__ gibi basit fonksiyonları doğrudan geçirmek genellikle sorunsuzdur:
# type(cls).__setattr__(cls, "__repr__", __repr__)

# ✅ Çözüm:
# - Kopyalanacak attribute'ları filtrele (örneğin sadece kullanıcı tanımlı methodlar).
# - property/staticmethod gibi özel türleri tür kontrolü ile aktar.
# - mappingproxy'den gelen değerlerin taşınabilirliğini try-except ile korumaya al.

# 🔐 Bu yapı, sınıf dekoratörlerinde "gerçek class wraps" fonksiyonu yazarken karşılaşılan temel sınırlamadır.

def add__str__(cls):
    if "__str__" not in cls.__dict__:
        def __str__(self):
            return f"Class({cls.__name__})"
        type(cls).__setattr__(cls,"__str__",__str__)


def add__repr__(cls):
    if "__repr__" not in cls.__dict__:
        def __repr__(self):
            return f"{cls.__name__}({self.__dict__!r})"
        type(cls).__setattr__(cls,"__repr__",__repr__)

def visual_methods(cls:type):
    add__str__(cls)
    add__repr__(cls)
    return cls
@visual_methods    
class Deneme:
    def __init__(self):
        pass

d = Deneme()
d.__dict__["x"] = 10
print(d)
print(f"{d!r}")




def update_class_wrapper(cls):
    wraps = ("__name__", "__module__", "__doc__","__qualname__","__annotations__")
    cb = cls.__base__
    wrapsupdate= {k:v for k,v in cb.__dict__.items() if not (k.startswith("__") and k.endswith("__")) }
    for w in wraps:
        setattr(cls, w, getattr(cb, w))
    for k,v in wrapsupdate.items():
        if k not in cls.__dict__:
            cls.__class__.__setattr__(cls,k,v)
    return cls

def sensor(cls):
    @update_class_wrapper
    class Wrapper(cls):
        def __init__(self, *args, **kwargs):
            print(f"[LOG] {cls.__name__} initialized with {args}")
            super().__init__(*args, **kwargs)
    return Wrapper
@sensor
class A:
    """aaaaaa"""
    x=20
    def __init__(self, x):
        self.x = x
    def __str__(self):
        return "merhababa"
a = A(10)
print(A.__name__)
print(A.__dict__)
print(A.__bases__)

import random,string

def acces_control(cls):

    class Wrapper(cls):
        h=1

    for k, v in {k: v for k, v in cls.__dict__.items() if not k.endswith("_")}.items():
        delattr(cls, k)
        setattr(cls, f"_{''.join(random.choices(string.ascii_lowercase, k=8))}", v)
    return update_class_wrapper(Wrapper)


@acces_control
class Deneme:
    __x = 2

Deneme()
print(Deneme.__dict__) #-> '_fodk': 2


