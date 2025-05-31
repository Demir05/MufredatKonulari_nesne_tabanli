from inspect import *
# Python'da Herşey Bir Nesnedir


# Nesne: bellekte yer kaplayan ve belirli bir davranışa sahip olan her şey,nesne olarak adlandırılır python'da her şey bir nesnedir
# bir nesnenin 3 temel özelliği vardır;

# 1) kimlik(id):bellekteki konumu/adresi olmalıdır
# 2) tür(type): bir sınıfa ait olmalıdır
# 3) değer(value): nesneler,bir değer taşıyabilmelidir

print(id(str()))  # 11775216
print(type(str())) # <class 'str'>
print(str()) # ''


# Tasarımsal Amacı

# sadelik sunması: her şey aynı şekilde değerlendirilebilir
# genellik sunar: her yapı aynı kurala uyar
# güçlü soyutlama sunar: dili tek mantıkla öğrenebilirsin


# Bu Yapının Avantajları

# nesneler üzerinde işlem yapmayı genelleştirebilirsin
# tüm nesneler,birinci sınıf vatandaştırlar
# sınıflar üzerinde işlem yapabilir  hatta metaclass oluşturabilirsin
# gelişmiş programlar yazabilirsin
# python'un her şeyi nesne olarak temsil etmesi dilin tutarlığını,genişletilebilirliğini,sadeceliğini ve gücünü aynı anda sağlar



# Bazı Temel Sınıflar

# type,python'da bulunan tüm sınıfların oluşturulduğu sınıf nesnesi

print(type(str))
print(type(filter))
print(type(reversed))
"""
<class 'type'>
<class 'type'>
<class 'type'>
tüm nesneler,sınıf oldukları için ve python'da bulunan sınıflar,type sınıfından türetildikleri için <class 'type'> döner
"""

# function: def veya lambda ile tanımlanmış olan user-definded fonksiyonlar,function sınıfının örneğidirler
# function sınıfını,kullanıcı doğrudan göremez yalnızca fonksiyon tanımlamada python tarafından otomatik oluşturur

def merhaba():
    pass

print(type(merhaba)) # <class 'function'>

l = lambda:print(...)

print(type(l)) # <class 'function'>

# builtin_function_or_method: python'da C dilinde yazılmış olan builtin fonksiyonların miras aldığı bir sınıftır
# bu sınıf C dilinde yazıldığı için kaynak kodlarına erişilemez dolaysısyla builtin fonksiyonlar da bu sınıftan örnek aldıkları için hiç bir builtin fonksiyonun kaynak kodlarına erişilemez
# builtin_function_or_method sınıfı,builtin fonksiyonların performans açısından kritik olması ve bu fonksiyonların mümkün oldukça hızlı çalışması gerekmesi için oluşturulmuştur

print(type(max)) # <class 'builtin_function_or_method'>
print(type(sorted)) # <class 'builtin_function_or_method'>


# Module: python'da bir .py dosyasını veya dış kütüphaneyi import ile içeri aktardığında bu yüklenen şey bir modül nesnesi olur
# ve modül nesneleri module sınıfından türemişlerdir
# module sınıfı,python'da birden fazla değeri(str,int,function) düzenli bir şekilde taşıyan kapsayıcılardır bu kapsayıcılar fonksiyon değillerdir

import math

print(type(math)) # <class 'module'>


# Generator Sınıfı:python'da yield kullanan veya expression ile oluşturulan nesnelerin miras aldığı sınıftır
# bu sınıflar __next__(),__iter__(),.send(),.throw(),.close() gibi metodlara sahiptirler
# generatator sınıfı,nesnenin kendisini kontrol edebilen bir sınıftır
from collections.abc import Generator

def coroutine() -> Generator[int,None,None]:
    yield 1
    yield 2
    yield 3

print(type(coroutine)) # <class 'function'>
# şuan coroutine fonksiyonun türü bir fonksiyon,çağrılması gerek

cor = coroutine()

print(type(cor)) # <class 'generator'>

gene = (i for i in range(1))

print(type(gene))  # <class 'generator'>



# Sınıf ve Fonksiyon için tasarımsal farklar


# python'da bir yapı: yeni bir davranış modeli üretmek istiyorsa,içinde durumunu(state) tutuyorsa,çağrıldığında yeni bir nesne döndürüyorsa bu yapı Class(sınıf) olur
# sınıflar,bir davranışı modellemek için oluşturulur ve çağrıldıklarında yeni bir nesne üretirler

# eğer python'da bir yapı: sadece bir işlem yapacaksa,girilen veriyi dönüştürüp geri verecekse,state(durum) tutmuyorsa bu yapı fonksiyon olur
# fonksiyonlar,anlık görevler için çağrılır çalışırlar sonra sonra ererler ve doğrudan bir sonuç döndürürler


# örnekler;

# reversed() bir sınıftır çünkü bir nesne döner,bu nesne tersten dolaşılabilir ve durum(state) tutar

# sorted() bir fonksiyondur çünkü verilen bir iterable'dan bir liste döner,bu işlem tek seferliktir,durum tutmaz,çalışır -> sonucu üretir-> işlevi biter
""""""
"""
İsim               Tür          Açıklama
------------------ ------------ ------------------------------
reversed           Sınıf        Sınıf (iterator üretir)
sorted             Fonksiyon    Fonksiyon (liste döner)
range              Sınıf        Sınıf (lazy iterable)
enumerate          Sınıf        Sınıf (iterator döner)
zip                Sınıf        Sınıf (çoklu iterable)
iter               Fonksiyon    Fonksiyon (iterator üretir)
next               Fonksiyon    Fonksiyon (bir sonraki eleman)
map                Sınıf        Sınıf (lazy map)
filter             Sınıf        Sınıf (koşullu filter)
lambda             Fonksiyon    Fonksiyon (anonim)
tee                Fonksiyon    Fonksiyon (çoklayıcı iterable üretir)
sum                Fonksiyon    Fonksiyon (toplam)
max                Fonksiyon    Fonksiyon (en büyük)
min                Fonksiyon    Fonksiyon (en küçük)
len                Fonksiyon    Fonksiyon (uzunluk)
abs                Fonksiyon    Fonksiyon (mutlak değer)
list               Sınıf        Sınıf (dizi)
tuple              Sınıf        Sınıf (sabit dizi)
str                Sınıf        Sınıf (metin)
dict               Sınıf        Sınıf (anahtar-değer)
set                Sınıf        Sınıf (kümeler)
frozenset          Sınıf        Sınıf (değiştirilemez küme)
Counter            Sınıf        Sınıf (sayıcı dict)
defaultdict        Sınıf        Sınıf (varsayılan dict)
OrderedDict        Sınıf        Sınıf (sıralı dict)
namedtuple         Sınıf        Fonksiyon → Sınıf üretir (tuple-türevi)
count              Sınıf        Sınıf (sonsuz sayaç)
cycle              Sınıf        Sınıf (sonsuz döngü)
repeat             Sınıf        Sınıf (tekrarlayıcı)
isfunction         Fonksiyon    Fonksiyon test fonksiyonu
isbuiltin          Fonksiyon    Built-in kontrolü
isclass            Fonksiyon    Sınıf kontrolü
isgeneratorfunction Fonksiyon    Generator fonksiyon mu?
"""


# Python'da her bir sınıf çağrılabilir bir nesnedir bir sıfını çağırmak için genelde obj = Sınıf() şeklinde bir tanımlama yapılır
# bir sınıfı çağrımak için kullandığın; list(),tuple(),str(),map(),reversed() gibi sınıf çağrıları, fonksiyon değil bir sınıf çağrısıdır arka planda obj = Class.__new__(cls,...) çağrırır
# bunların fonksiyon gibi görünmesinin nedeni kullanıcıya kolaylık sağlaması içindir
# built-in sınıflar,C dilinde yazılmışlardır dolasıyla kaynak kodlarına erişilemez


# Sınıf nasıl çağrılır


# __call__() metodu;

# sınıflar çağrıldıklarında aslında onları çağıran şey type sınıfında olan __call__() metodunun ta kendisidr
# sınıfların çağrılabilirliği type sınıfı tarafından kontrol edilir çünkü sınıflar, type sınıfından türemişlerdir  o sınıfları çağrımak type sınıfının görevidir
# __call__ metodunda ek bir kontrol mekanizması vardır eğer çağrımak istenen sınfta __new__(),__init__(),__str__() gibi özel metodlar yoksa;
# python,MRO miras zincirinde yukarı çıkarak bu metodları bulur

"""
type.__call__(A)
└── A.__new__(A)              → bulamazsa → object.__new__(A)
└── A.__init__(a)             → eğer __new__ geri A örneği döndürdüyse """


# Sözdizimi: type.__call__(cls, *args, **kwargs) → object
# cls: çağrılcak olan sınıf, *args: sınıfa gelicek olan pozisyoneller, **kwargs: sınıfa gelcek olan keyword'ler

# Avantajları: tüm sınıflar tek bir noktadan kontrol edilir bu da merkezi yönetimi ve tutarlığı sağlar ayrıca sınıf çağrısı ile nesne yaratımı ayrılır


metin = str([1,2,3]) # -> burda bir sınıf çağrısı olduğunu biliyorsun arka planda;

metin = type.__call__(str,[1,2,3]) # burda str sınıfından örnek yaratmak için str yazdık cls parametresine
"""
metin = type.__call__(str, [1, 2, 3])
 ↳ str.__new__(str, [1, 2, 3])
        ↳ (init atlanır çünkü str immutable)
"""
# __call__() metodu,__new__() metodunu otomatik çağırır

print(metin) # [1, 2, 3]


print(getattribute_name(str,["__call__"])) # __call__'adlı metod -> Tanımlı!
# Peki neden ?: çünkü getattr,hasattr gibi fonkisyonlar MRO arama zincirini kullanırlar bu durumda sınıfın kendisinde olmasa bile miras aldığı sınıfta varsa ikiside bu niteliği bulabilir

print(repr(str())) # ''
print(list()) # []

# str(),list()... bunların fonksiyon olmadığının kanıtı;

print(isfunction(str)) # False


# Bir Sınıftan Örnek Oluşturma Nasıl Yapılır

# 1) öncelikle bir örnek oluşturmanın ilk adımı __new__() Metodudur,__new__(), metodu,sınıftan nesne yaratmak için kullanılır

""" Sözdizimi: __new__(cls,*args,**kwargs) -> object:
                    retrun ...
cls: sınıfın kendisidir bu,__new__() metodunun,hangi sınıf için çağrıldığını belirtir bu özellikle miras için şarttır (alt bir sınıf varsa)
aynı zamanda cls parametresine subclass veremezsin sadece alt örneği olan sınfıları kabul edebilir 
args ve kwargs: bunlar sınıfa gelen verilerdir bu verileri __new__() metodu doğrudan kullanır veya __init__() metoduna gönderir 

    """
# __new__(cls,*args,*kwargs) bu sözdizimi genel bir tavsiye şablonudur python,bu parametrelerde seni kısıtlamaz
# her sınıfın __new__() metodu için tanımladığı parametreler farklı olabilir,her sınıf bu parametreleri kendi sınıfın özelliği doğrultusunda özelleştirebilir
# __new__() metodu,mutlaka yeni oluşturduğu nesneyi dönmelidir bu dönen nesnenin durumu şu iki duruma bağlıdır;
# Not: C dilinde yazılan sınıflar *kwargs kabul etmezler

# 1) -> Immutable sınıflarda nesne oluştururken içerik doğrudan __new__() metodu ile verilir ve bu sınıflarda __init__ tanımlı değildir veya kullanılmaz
class ImmutableStr(str):
    def __new__(cls, içerik):
        print("→ __new__")
        return super().__new__(cls, içerik)

    def __init__(self, içerik):
        print("→ __init__")  # Genelde bir şey yapmaz
"""
bu örnekte bir tane sınf oluşturulmuştur bu sınıfın özelliği immutable olmasıdır
gördüğün üzere tüm içerik doğrudan __new__() metodu ile veriliyor,return super().__new__(cls, içerik) -> burda sınıf ve obje verdik
__init__() tanımlı ama bir şey yapmıyor çünkü bu içerik tamamen __new__()'de oluşturuldu ve bu immutable nesneyi __init__(),dolduramaz bu nedenle kullanılmaz!
"""

# 2) -> Mutable sınıflarda nesne oluşturuken __new__() metodu sadece boş bir nesne oluşturur bu boş nesneyi __init__() metodu doldurur
# __init__() metodu,görevi nesneyi başlatmaktır ve herangi bir değer döndürmez dikkat et return yok
class Mutable:
    def __new__(cls, *args, **kwargs):
        print("→ __new__ (boş nesne yaratıldı)")
        return super().__new__(cls)

    def __init__(self, isim):
        print("→ __init__ (veri atandı)")
        self.isim = isim
"""
burda __new__() metodu boş bir nesne döndü bu boş nesneyi,__init__() metodunda doldurduk 
return super().__new__(cls) -> burda sadece sınıf( verdik herangi bir obje verilmedi 
"""


# Örnekler;

# ilk olarak immutable olan sınıflardan başlayalım

# type sınıfında bulunan __call__() metodu ile herangi bir sınıftan örnek/nesne oluşturabiliriz;

string_c = type.__call__(str,"demwwwir")

print(string_c) # demwwwir

string_a = str("demir")
# burda string sınfını str() ile çağrıdık ve kendi sınıfından bir önrek oluşturdu aynı işlemi __new__() ile dışardan yapabiliriz;

string_b = str.__new__(str,"demir")
# burda __new__() metodunda cls belirtmemiz gerekiyordu bu nedenle str yazdık kendi sınıfından bir string sınıfı oluşturcak
print(string_a, string_b) # demir demir

# Şimdi ise mutable bir sınıfa bakalım;

listem = list.__new__(list)
# burda cls parametresine sınıfın kendisini verdik(list,sınıfının kendisinin referansını döner)

print(listem) # []
# Nedeni: Mutable sınıflarda, __new__() metodu, boş bir nesne döner bu nesne,__init__() metodu ile doldurur

a= listem.__init__("12345")
# burda self parametresine kendisini vermemize gerek yok

print(a) # None
# Nonde döner çünkü __init__() metodu herangi bir değer döndürmez in-place işlem yapar;

print(listem)  # ['1', '2', '3', '4', '5']


