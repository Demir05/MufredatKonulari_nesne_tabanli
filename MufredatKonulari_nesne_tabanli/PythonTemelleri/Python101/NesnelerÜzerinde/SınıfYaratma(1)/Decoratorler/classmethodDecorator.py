# -----------------------------------------------------------------------
# @classmethod Decorator'ü
# -----------------------------------------------------------------------
from string import ascii_letters


# @classmethod, sınıfın kendisini (cls) parametre olarak alan özel bir metod türüdür.
# Bu metodlar, sınıf düzeyinde çalışır ve sınıfla ilgili işlemleri gerçekleştirmek için kullanılır.
# classmethod'lar class method'larıdır bu nedenle doğrudan class attribute'lara erişimi vardır bunun dışında kalan class body'de tanımlı olan tüm fonksiyonlar, instance method'durlar
#  - bu nedenle doğrudan sınıf attribute'larına değil örnek attribute'ları ile çalışırlar classmethod'ların farkı tam olarak budur işte

# -----------------------------------------------------------------------
# Neden Var? Amacı Nedir?
# -----------------------------------------------------------------------

# 1. Sınıf düzeyinde işlem yapmayı sağlar. Örnekten değil, doğrudan sınıfın kendisiyle ilgilidir.
# 2. Sınıfla ilgili konfigürasyon, durum ya da nesne yaratımı gibi işlemlerde kullanılır.
# 3. Alt sınıflar tarafından miras alındığında, cls parametresi sayesinde alt sınıfın kendisi ile çalışır.
#    Bu sayede "factory" gibi yapılar kurulabilir → esneklik ve yeniden kullanılabilirlik sağlar.
# 4. daha fazla kontrol sağlar şöyle düşün:
#   sınıftan bir örnek oluşturmayı fonksiyonla sağlıyorsun burda __init__() kullanmaktan daha fazla esnekliğe sahipsin çünkü ekstra bir katman oluşur bu katmanda;
#   input doğrulama, loglama, ön işlem/temizlik, varsayılanlar, hata yönetimi yapabilirsin 

# -----------------------------------------------------------------------
# Sözdizimi:

# class SınıfAdı:
#     @classmethod
#     def fonksiyon_adı(cls, ...):
#         ...
   # Bu bir sınıf metodudur, bu yüzden ilk parametresi "cls" olur
    # → "cls", metoda hangi sınıf üzerinden ulaşıldıysa **o sınıfı** temsil eder.
    # → tıpkı instance method'lardaki "self" gibi, ama "sınıf" için.
    # cls → örneğin Hayvan, Kedi, Kopek olabilir
        # bu sayede alt sınıf kendi "isim" değerini değiştirebilir

# Çağrılma:
# SınıfAdı.fonksiyon_adı(...)
# veya
# örnek.fonksiyon_adı(...)  → burada da cls, örneğin ait olduğu sınıfı temsil eder

# -----------------------------------------------------------------------
# Örnek:

class Araba:
    marka = "Renault"

    def __init__(self, model):
        self.model = model

    @classmethod
    def marka_degistir(cls, yeni_marka):
        cls.marka = yeni_marka

# Hem sınıf üzerinden hem örnek üzerinden çağrılabilir
Araba.marka_degistir("Toyota")
print(Araba.marka)  # → Toyota

a = Araba("Corolla")
a.marka_degistir("Honda")
print(Araba.marka)  # → Honda  (sınıfın tüm örnekleri etkilenir)

# -----------------------------------------------------------------------
# Teknik Detaylar:

# Sınıf tanımında:
# Araba.__dict__['marka_degistir'] → classmethod objesi
# Çağırıldığında:
# Araba.__dict__['marka_degistir'].__get__(None, Araba) → bound method döner
# Bu method, Araba sınıfını (cls) ilk argüman olarak alır.

# -----------------------------------------------------------------------
# @classmethod vs @staticmethod

# @staticmethod:
# ----------------
# • class.method --> method (bağlı değil)
# • instance.method --> method (bağlı değil)
# • __get__ sadece fonksiyonu döner → self/cls yok
# • Sadece fonksiyonel düzen sağlar

# @classmethod:
# ----------------
# • class.method --> cls otomatik geçilir (Kitap vs AltKitap)
# • instance.method --> yine cls olarak sınıf geçilir
# • __get__ → sınıfa bağlı callable döner → cls bağlıdır
# • Factory method / miras uyumu / davranış aktarımı sağlar
# -----------------------------------------------------------------------
# Ne Zaman Kullanılır?

# - Sınıfa özel ayarlar/değişkenler üzerinde işlem yapılacaksa
# - Alt sınıflarda dinamik olarak işlem yapılması gerekiyorsa
# - Yeni nesne yaratımı için alternatif factory method oluşturulacaksa


class Myclassmethod:
    def __init__(self, func):
        # Orijinal fonksiyon nesnesini saklar
        self.__func__ = func

    def __get__(self, instance, owner):
        # Burası descriptor protokolüdür.
        # Ne zaman `Kitap.dosyadan_olustur` gibi bir erişim olsa burası çalışır.

        # instance → örnek üzerinden erişildiyse örnek olur (a.dosyadan_olustur gibi)
        # owner   → sınıfın kendisi olur (her zaman)

        # Bağlı (bound) sınıf metodu döner
        def bound(*args, **kwargs):
            return self.__func__(owner, *args, **kwargs)

        return bound
"""
classmethod, staticmethod'a göre OOP'Nin önemli bir yapı parçasıdır 
kurucu fonksiyon olarak çalışabilir
miras yapılarında zincirde doğru sınıfı(cls) doğru yakalamalıdır 
sınıfa dinamik davranışlar kazandırmak için kullanılır 
tüm bunlar bu decotator'ü daha karmaşık kılar
"""
# -----------------------------------------------------------------------
# Örnek: Factory Method

class Kitap:
    def __init__(self, isim, sayfa):
        self.isim = isim
        self.sayfa = sayfa

    @classmethod
    def dosyadan_olustur(cls, veri: str):
        isim, sayfa = veri.split(",")
        return cls(isim, int(sayfa))

k = Kitap.dosyadan_olustur("Python101,350")
print(k.isim, k.sayfa)  # → Python101 350


class Hayvan:
    isim = "Tanımsız"

    # Bu bir sınıf metodudur, bu yüzden ilk parametresi "cls" olur
    # → "cls", metoda hangi sınıf üzerinden ulaşıldıysa **o sınıfı** temsil eder.
    # → tıpkı instance method'lardaki "self" gibi, ama "sınıf" için.
    @classmethod
    def isim_ayarla(cls, isim):
        # cls → örneğin Hayvan, Kedi, Kopek olabilir
        # bu sayede alt sınıf kendi "isim" değerini değiştirebilir
        cls.isim = isim

# Alt sınıflar
class Kedi(Hayvan): pass
class Kopek(Hayvan): pass

# cls = Kedi → Kedi sınıfının "isim" attribute'u değişir
Kedi.isim_ayarla("Tekir")

# cls = Kopek → Kopek sınıfının "isim" attribute'u değişir
Kopek.isim_ayarla("Karabaş")

# Şimdi bakalım hangi sınıf ne olmuş:
print(Kedi.isim)     # Tekir
print(Kopek.isim)    # Karabaş
print(Hayvan.isim)   # Tanımsız (değişmedi!)

# örnekler;

# Örnek 1 --------------------------------------------
class A:
    isim = "demir"

    def degistir(cls,name: str):
        cls.isim = name
# Burda @classmethod decorator'ü kullanmadık

a = A()

a.degistir("ozan")

print(A.isim) # demir
# çünkü a.degistir(..)'de cls = a objesi olur bu durumda bu örneğe özel(instance attribute) ataması yapıldı

print(a.isim)  # ozan

# şimdi @classmethod ile süsleyelim:

class A:
    isim = "demir"

    @classmethod
    def degistir(cls,name: str):
        cls.isim = name

a = A()

a.degistir("ozan")

print(A.isim) # ozan
# Gördüğün üzere herangi bir sıkıntı olmadı
# çünkü cls = A sınıfı

# örnek 2 ----------------------------------------

class Kayıt:
    from string import ascii_letters

    def __init__(self,isim):
        self.isim = isim

    @classmethod
    def dosyadan_olustur(cls, isim):
         if all(karakter in ascii_letters for karakter in isim):
            return cls(isim)
         else:
             raise TypeError("Geçersiz ad !")

k = Kayıt("ozan")

k1 = k.dosyadan_olustur("demir")
# burda örnek üzerinden yeni bir sınıf örneği oluşturduk

print(k1.isim) # demir

try:
    k2 = k1.dosyadan_olustur("ışılay")
except TypeError as e: print(e) # Geçersiz ad !

# örnek 3 --------------------------------------

# cls parametresi, özellikle davranış zincirinde çok önemli rol oynar ve nedeni aslında basit:
# cls,

print(
    k1.__class__.__dict__['dosyadan_olustur'].__get__(None,type(k1)).__call__
)

class A:
    @classmethod
    def f(cls):
        print("A",cls)

class B(A):
    @classmethod
    def f(cls):
        print("B",cls) # cls,bu classmethod'a hangi sınıf üzerinden erişildiyse o sınıfı temsi eder
        super(B,cls).f() # B sınıfının miras aldığı tüm sınıflarda(mro) aranan "f" fonksiyonunu arar
        # B.__mro__[1] B -> subclass demektir mro zincirinde hangi sınıftan aramaya başlanacağını belirler
        # dolasıyla A sınıfından aranmaya başlanır ve A sınıfında f fonksiyonu vardır
        # cls ise hangi örnek üzerinden çözümleme yapılcağını belirler burda cls = C olur çözümeleme C sınıfında olur

class C(B):
    pass

c=C()
c.f()

print(
    type(c).__mro__[1].__dict__['f'] # ilk olarak B sınıfında f fonksiyonu bulundu bu nedenle ilk olarak: B <class '__main__.C'> yazılır
)
"""
B <class '__main__.C'> -> f fonksiyonuna C sınıfından erişildiği için cls = C olur
A <class '__main__.C'>
"""