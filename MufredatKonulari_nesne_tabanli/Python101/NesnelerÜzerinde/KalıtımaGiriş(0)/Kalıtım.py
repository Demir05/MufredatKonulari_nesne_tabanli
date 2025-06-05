# Kalıtım
""""""
# kalıtım: bir sınıf nesnesi,başka bir sınıf nesnesinin __bases__ üzerinden referans olarak onun davranışlarını mro miras zinciri ile devraldığı bir yapıdır
# Kalıtım sayesinde bir sınıf,başka bir sınıfın davranışlarını devralabilir ve oluşturulan objeler,MRO zinciri yoluyla atalarına çıkarak davranışlarını çözümleyebilir


# __bases__: bir sınıfın doğrudan hangi sınıflardan miras aldığını gösteren bir tuple'idir(metod değil attribute) sınıf tanımında parantez içine verilen sınıflar, doğruca bu yapı ile ilişkilendirilir(__closure__ aynısı aga)
# doğrudan kelimesini açalım; bir sınıf başka bir sınıftan miras aldığında(yani tanımlamada parantez içine verilse) __bases__ içinde yalnızca o sınıf olabilir
# tüm sınıflar,object sınıfından miras alıyor olasda bu zaten miras olarak aldığı sınıf için bu,dolaylı bir miras olur yani sınıfımız,doğrudan değil dolaylı olarak object sınıfından miras alıyor olur
# bu nedenle __bases__,bu dolaylı olan object sınıfını tutmaz

# __bases__,python tarafından eager evalutaion işlemine göre yapılır sınıf tanımında hemen ve tamamen oluşturulur

# örnek;

class Demir:

    def __repr__(self):
        return "demir'in sınıfı"

class Kücük_demir(Demir):
    ...

"""
burda iki tane sınıf oluşturduk bunlardan biri Demir sınıfından referans alır 
"""
print(Kücük_demir.__bases__) # (<class '__main__.Demir'>,)
# gördüğün üzere Kücük_demir sınıfı,DOĞRUDAN demir sınıfından miras alıyor ama tabii dolaylı yoldan object sınıfından da miras alır çünkü tüm sınflar,object sınıfından miras alırlar
# ama __bases__,yalnızca doğrudan miras alınan sınıfları döner;


"""
    “Örnekleme, nesnelerin veya sınıfların herangi bir kalıtımsal donatma yapmaksızın davranışlarını kontrol eder 
    Tüm sınıfların oluşturulma,attribute manpülasyonü vb. süreçlerini type sınıfı belirler; çünkü tüm sınıflar, type sınıfının örneğidir.
    Bu durum type sınıfını bir metaclass yapar metaclass,sınıfların nasıl oluşturulcağını ve onların nasıl davranıcağını tanımlayan özel bir sınıftır .

    Miras ise  sınıflar arası,sınıfların kullanabilceği attribute'ları belirler bu,sınıfları kalıtımsal olarak donatır .
    Tüm sınıfların en temel atası object sınıfıdır, çünkü tüm sınıflar ondan miras alır.
    Bu nedenle tüm sınıflar, object sınıfının davranışlarını taşır.”
    
[type]  ─────────┐
  ▲              │
  │              │
[object] ◄───────┘

MyClass:
  - instance of: type
  - subclass of: object

my_obj:
  - instance of: MyClass
"""


# __class__: bir nesnenin ait olduğu sınıfı döner __class__,bu nesne,hangi sınıfın örneği ?,hangi sınıfa ait ? soruların cevaplarını verir
#ama __class__ bir metod değil bir attribute'dır ve __class__'ın kendisi örnek değil bir attirbute'dır

# örnekler;

print(str().__class__) # <class 'str'>
# string nesnesi,str sınıfının bir örneğidir ait olduğu sınıf str sınıfıdır

print(object.__class__)  # <class 'type'>
# object sınıfı,type sınıfının örneğidir çünkü type bir metaclass'tır

print(type.__class__)  # <class 'type'>
# type sınıfının örneği,type sınıfıdır

print(str.__bases__) # (<class 'object'>,)
# __bases__ metodu,bize sınıfın,hangi sınıflardan miras aldığını gösterir -> (<class 'object'>,) str sınıfı, object sınıfından mirâs alır
# bu durumda,str sınıfı, object sınıfının davranışlarını devalır

print(object.__bases__) # ()
# object sınıfı zaten en temel sınıftır diğer hiçbir sınıftan miras almaz bu nedene bases demeti boştur

print(type.__bases__) # (<class 'object'>,)
# type sınıfı,mirasını object sınıfından alır çünkü tüm sınıflar mirası object sınıfından alır



# __mro__: bir sınıfın metod çözümlemesi yaparken izleyeceği sıralı miras zinciridir,sınıf,bu zincirden öncelikle kendisinden başlayarak sıralı bir şekilde atalarına çıkar
# mro zincirinde sınıfın kendisi de yer alır çünkü mro zinciri,ilk olarak sınıfın kendisinden başlar
# __mro__,bir attribute'dır metod değildir ve tuple olarak döner
# metod çözümlemesi: python,bir metod çağrıldığında o metodu nerde arayacağını belirlemesidir burda mro zinciri kullanılır TÜM DUNDER METODLAR BU MRO ZİNCİRİNİ KULLANRAK METOD ÇÖZÜMLEMESİ YAPARAK;
# SINIFIN KENDİSİNDE OLMAYAN BİR METODU,MİRASLARINDA ARAYABİLİR VE KULLANABİLİR


print(str.__mro__) # (<class 'str'>, <class 'object'>)
# str sınıfı,sıralı miras zincirinde kendisi dışında object sınıfı vardır çünkü str sınıfı,object sınıfından miras alır
# aynı zamanda kendisini olmadan düşünürsek str sınıfı,doğrudan object sınıfından miras aldığı için,__bases__ demetinde object sınıfı bulunur

print(object.__mro__) # (<class 'object'>,)
# object sınıfı,metod çözümlemesi yaparken izleyebilceği sıralı miras zincirinde sadece kendisinden arama yaoabilir
# çünkü object,en temel sınıftır ve miras almaz

print(type.__mro__) # (<class 'type'>, <class 'object'>)
# type sınıfın miras zincirinde,kendisi ve miras aldığı tek sınıf olan object sınıfı vardır yani type sınıfı,bir tek object sınıfından miras alır


# isinstance() Fonksiyonu

# isinstance() fonksiyonu,builtin olan (yani C dilinde yazılmış) bir python fonksiyonudur
# isinstance fonksiyonu,belirtilen nesnenin örneğinde yani ait olduğu sınıfta ve bu sınıfın miras aldığı ata sınıflarda verilen sınıf veya sınıfları arar

# isinstance() builtin bir fonksiyondur bu nedenle kaynak kodlarına erişilemez ama eğer python ile yazılsaydı şuna benzer idi;

def my_isinstance(obj, cls):
    obj_type = obj.__class__
    return any(base is cls for base in obj_type.__mro__)


# Çalışması

# 1) isinstance fonksiyonu,verilen objenin __class__ attirbute'sunu kullanır bu sayede hangi sınıfa ait olduğunu bulur

# 2) burda dönen sınıfın __mro__ zincirine bakılır çünkü isinstance fonkiyonu,sadece sınıfın kendisinin değil o sınıfın miras aldığı sınıflarda da örnek kontrolü yapar
# belirtilen sınıf veya sınıflar,bu miras zincirinde varsa True döner
# yoksa False döner


# sözdizimi: isinstance(obj,class_tuple) obj: herangi bir nesne class_or_tuple: python sınıfı veya tuple içinde birden fazla sınıf belirtebilirsin bu sayede
# verilen objeyi,birden fazla sınıfla karşılaştırabilirsin ve yapısında any fonksiyonu olduğu  için herangi bir sınfın bu MRO zincirinde olması yeterlidir


# örnekler;

# öncelikle manuel yapalım;

print(object in str.__class__.__mro__) # True
# object sınıfı,str sınıfının örneği olan type sınıfın miras aldığı bir sınıf bu nedenle True

print(isinstance("",str)) #  # True
print(isinstance("",object)) # True
print(isinstance("",type)) # False
# çünkü string nesnesinin örneği olan(ait olduğu sınıf) str sınıfıdır ve str sınıfının kendisinde ve miras aldığı sınıflar arasında type sınıfı olmaz
# zaten sınıflar,type sınıfına miras olarak değil örneği olarak bağlıdır
print(isinstance(str,type)) # True



# issubclass() Fonksiyonu

# issubclass() fonksiyonu, yerleşik (builtin) bir Python fonksiyonudur ve C dilinde yazılmıştır.
# Verilen sınıfın, belirtilen sınıf veya sınıflardan miras alıp almadığını kontrol eder.
# Eğer verilen sınıfın kendisi veya atalarında belirtilen sınıf bulunursa True; aksi takdirde False döner.


# Çalışması

# 1) issubclass fonksiyonu,verilen sınıfın __mro__ zincirini kullanır bu sayede sıralı miras zincirine erişir kendisi ve tüm atalarının davranışlarını alır

# 2) bu sıralı miras zincirinde,belirtilen sınıf veya sınıflardan herangi bir tanesi varsa çünkü any fonksiyonu kullanılır True yoksa False döner


# issubclass(),builtin bir fonksiyon olduğu için kaynak kodlarına erişilemez ama python ile yazılsaydı şuna benzerdi;

def my_issubclass(subcls, supercls):
    if not isinstance(subcls, type):
        raise TypeError("First argument must be a class")
    return any(base is supercls for base in subcls.__mro__)

# sözdizimi: subclass(class,class_or_tuple) class: herangi bir sınıf ama sınıf vermezsen TypeError hatası alırsın
# class_or_tuple:sınıf veya tuple içinde sınflar

print(issubclass(object,type)) # False
# object sınıfının kendisi ve ataları(zaten kendisi var sadece) type sınıfından miras almaz

print(issubclass(type,object)) # True