# First Class Functions

# python'daki fonksiyonlar birinci sınıf vatandaştırlar ama ilk önce bunun ne olduğuna bakalım;

# Birinci Sınıf Vatandaş: eğer bir proglamama dilinde bir öğe şu 4 şeyi yapabiliyorsa o objeye,birinci sınıf vatandaş denir
# birinci sınıf vatandaşlar,veri muamalesi görürler verinin yaptığı herşeyi onlarda yapabilirler
# 1) değişkene atanabiliyorsa
# 2) bir fonksiyona argüman olarak verilebiliyorsa
# 3) bir fonksiyondan return ile geri döndürülebiliyorsa
# 4) veri yapılarında saklanabiliyorsa/taşınabiliyorsa

# fonksiyonlar, tüm bu ozelliklere sahiptirler bu nedenle normal bir veri gibi davranırlar
# her dilde birinci sınıf fonksiyon yoktur mesela C dilinde yok ama python gibi modern dillerde bu vardır

# fonksiyonlar birinci sınıf vatandaş oldukları için,closure,dektator gibi yapılar vardırlar

# 1) fonksiyonu değişkene atama

def merhaba():
    print("MERHABA")

s = merhaba # burda fonksiyonun kendisinin referansını sakladık eğer print edersek;
print(s) # <function merhaba at 0x791335dda3e0>

# şimdi s değişkeni artık merhaba fonksiyonunun referansını tuttuğu için s verisini çağırabiliriz;

print(callable(s)) # True gördüğün üzere s değişkeni çağrılabilir

s() # MERHABA

s = merhaba() # burda fonksiyonu çağırdık ve s değişkenine döndürdüğü değeri atadık eğer return -> None is s değişkeni None döner;
print(s) # None


# 2) bir fonksiyona argüman olarak verme

def sarmalayıcı(fon):
    fon()

sarmalayıcı(merhaba) # MERHABA

# argüman olarak aldığımız fonksiyonun kendisinin referansını döndürebiliriz
def sarmalayıcı2(fon):

    return fon

print(sarmalayıcı2(merhaba)) # <function merhaba at 0x7e0b317da3e0>
# sarmalayıcı2, aldığı argümanı döndürdüğü için çağırabiliriz;

sarmalayıcı2(merhaba)() # MERHABA
# sarmalayıca fonksiyonun referansını verdik sonra ise () ile çağırdık > merhaba() oldu aslında

# argüman olarak fonksiyon verirken çağırabilirsin bu durumda fonksiyonun return değeri argüman olarak geçer eğer return değeri yoksa None döner

def a():
    return "demir"

isim = sarmalayıcı2(a()) # bu durumda burda beklenen işlem şu olmalı: a fonksiyon çağrıdı, sonra "demir" değeri döndü
# sarmalayıcı2 fonksiyonunda return fon olduğu için bu işlem "demir" olarak bir obje dönmeli

print(isim) # demir
# gördüğün üzere demir değeri döndü


# 3) bir fonksiyonu return olarak geri döndürmek
# burda fonksiyonu return olarak döndürebiliriz iki tane durum oluşur;
# ilk fonksiyonun kendisinin referansını döndürebiliriz veya fonksiyonu çağırıp,return değerini döndürebiliriz

def a():
    print("a")
    def b():
        print("b")
        return "aslı"
    return b
# burda b() fonksiyonun içinden aslı değeri döner, dışta return b olduğu için a() fonksiyonu,b fonksiyonun kendisinin referansı döner
# ama ondan önce a() fonksiyonu çağrılırsa print("a") çalışır -> side efffect

s2 = a() # a
# şimdi s2 objesine yakından bakalım;

print(dir(s2)) # ['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__getstate__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__type_params__']
# s2 objesinin bir fonksiyona referans verdiğini çok net bir biçimde görüyoruz ama hangi fonksiyon ? ;
# burda şunu düşünmemiz gerekir biz statements işleminde a() fonksiyonunu çağrıdık ve s2'ye atadık bu python,atama işleminde ilk olarak sağ tarafı değerlendirdiği için;
# bu a() fonksiyonu çalışır sonra return değeri s2'ye atanır a() fonksiyonun return değerini hatırlayacak olursak: b() fonksiyonun referansı idi;

print(s2) # <function a.<locals>.b at 0x7890c361e200>
# şimdi ise çağıralım;

isim2 = s2() # b
print(isim2) # aslı

# şimdi fonksiyonu çağrıp return edelim;

def a():
    print("a")
    def b():
        print("b")
        return "aslı"
    return b()
# burda işlemler aynı ama a() fonksiyonu,return değeri olarak b fonksiyonun return değerini dönecek

isim = a()
"""
a
b
"""
print(isim) # aslı

# 4) veri yapılarında fonksiyonu saklayabilirsin
# bu işlemi aslında map() fonksiyonunu anlatırken lambda ile yapmıştık aynı şeyi bu sefer isimli fonksiyonlarla yapacağız :)

def topla(a:int,b:int) -> int:
    return a+b

def çarp(a:int,b:int) -> int:
    return a*b

işlemler = [topla,çarp]
# burda yalnızca fonksiyonların kendilerinin referanslarını verdik ama çağırmadık yoksa parametre vermediğimiz için hata alırdık
# (bu parametreler önceden tanımlı sabit isimler ama varsayılan değerleri olmadığı için argüman verirmek zorunda)
# ayrıca amacımız burda çağırmak değil zaten map fonksiyonunda lambda ile bu çağırmayı teker teker yapacağız

işlenmiş_veri = map(lambda i:i(10,20),işlemler)
print(*işlenmiş_veri) # 30 200

