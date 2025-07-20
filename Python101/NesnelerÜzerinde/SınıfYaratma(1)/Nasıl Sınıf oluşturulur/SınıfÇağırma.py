# Python'da her bir sınıf çağrılabilir bir nesnedir bir sıfını çağırmak için genelde obj = Sınıf() şeklinde bir tanımlama yapılır
# bir sınıfı çağrımak için kullandığın; list(),tuple(),str(),map(),reversed() gibi sınıf çağrıları, fonksiyon değil bir sınıf çağrısıdır arka planda obj = Class.__new__(cls,...) çağrırır
# bunların fonksiyon gibi görünmesinin nedeni kullanıcıya kolaylık sağlaması içindir
# built-in sınıflar,C dilinde yazılmışlardır dolasıyla kaynak kodlarına erişilemez

from inspect import isbuiltin

# str(),list()... bunların fonksiyon olmadığının kanıtı;

print(isbuiltin(str)) # False


# Sınıf nasıl çağrılır


# __call__() metodu:

# __call__ metodu, bir sınıfın örneğini çağrılabilir (callable) hâle getiren özel bir metottur.
# Yani bir nesneyi parantez () ile çağırmak istediğimizde bu metod devreye girer.

# ❗Ancak __call__ metodu, sınıfın *kendisini* çağrılabilir yapmaz.
# Örneğin: str sınıfında __call__ tanımlı değildir. Buna rağmen str("abc") gibi bir kullanım mümkündür çünkü:

# 🔄 Python'daki tüm sınıflar, type sınıfının örneğidir. Yani:
#     str.__class__ is type
# Bu nedenle str("abc") ifadesi çalıştığında aslında çağrılan:
#     type.__call__(str, "abc") ifadesidir.

# ✅ Yani sınıf çağrılabilirliğini, doğrudan type sınıfında tanımlı olan __call__ metodu sağlar.
#     Bu yaklaşım; sınıf oluşturma, nesne yaratımı ve başlatma işlemlerini merkezi ve tutarlı bir şekilde yönetmeyi sağlar.

# 🔖 KONU: __call__ — Instance düzeyi vs Sınıf düzeyi farkı

# 🧠 1. INSTANCE DÜZEYİNDE __call__
# Bu örnekte __call__, sınıfın içindeki bir instance method'dur
# Bu sayede sınıfın örnekleri, fonksiyon gibi çağrılabilir

class A:
    def __call__(self):
        print("🟢 Instance düzeyinde __call__ çalıştı")

a = A()   # A örneği oluşturuluyor
a()       # a.__call__() çağrılır, self = a

# ⬆️ Yukarıda: __call__ metodu, örnek (instance) üzerinde çağrılır
# Bu, bir nesneyi "callable" (fonksiyon gibi çalışabilir) hale getirir
# a.__call__() ile aynı şeydir


# 🧠 2. SINIF DÜZEYİNDE __call__ (Metaclass ile)
# Eğer ClassName() çağrıldığında __call__ çalışsın istiyorsan,
# bu durumda metaclass'ın __call__ metodunu override etmen gerekir

class Meta(type):
    def __call__(cls, *args, **kwargs):
        print("🔵 Metaclass düzeyinde __call__ çalıştı")
        instance = super().__call__(*args, **kwargs)
        return instance

class B(metaclass=Meta):
    def __init__(self):
        print("🔵 B sınıfı __init__ çalıştı")

b = B()  # ➜ Meta.__call__ ➜ B.__init__

# ⬆️ Burada: B() çağrıldığında önce Meta.__call__ devreye girer
# Meta.__call__ içinde __init__ çalıştırılır ve örnek döndürülür
# Bu yapı genellikle: Singleton, Factory Pattern, Dependency Injection gibi yerlerde kullanılır

# 🔁 Özet:
# a()  ➜ a.__call__()       ➜ INSTANCE düzeyi __call__
# B()  ➜ Meta.__call__(...) ➜ SINIF düzeyi __call__ (metaclass üzerinden)

# ========================================
# ✅ SONUÇ

# ✔️ `obj()` veya `A()` işlemleri aslında çok katmanlıdır
# ✔️ __call__ bir davranış gibi görünür ama önce __getattribute__ ile bulunur
# ✔️ En sonunda __call__ gerçekten çağrılır
# ✔️ Sınıflar için __call__, type üzerinden yürür – metaclass’ın kontrolündedir

class A:
    ozellik= 12
    def __call__(self):
        print("çağrıldım")

a = A()
# şimdi burda A() sınıfını çağırdık ve yeni bir nesne oluşturulma işlemi yaptık ama A sınıfını çağırmamızı
# sağlayan durum A sınıfında __call__ tanımlı olması değil bu sınıfın örnekleme  olarak bağlandığı type sınıfında __call__ tanımlı olması
# A sınıfında __call__ metodunun olması,o sınıfın örneğinin çağrılabilir yapar

a() # çağrıldım
# burda bir çağrılma işlemi var ilk olarak python şöyle bir adım izler;
# a.__class__.__call__(a)

# basit örnekler;

# amacımız str sınıfı çağırmak olsun bu sınıfı çağıralabilir yapan şey type sınıfında __call__() metodunun tanımlı olması bu sayede
# type sınıfının örneği olan str sınıfını çağırabiliriz;

metin = str() # -> burda bir sınıf çağrısı olduğunu biliyorsun arka planda;

metin = type.__call__(str) # burda str sınıfından örnek yaratmak için str yazdık

print(metin) # ''

# sınıfın kendisinde __call__ metodu tanımlı olmayabilir;

'__call__' in dir(str) or print("yok") # yok

#print(getattribute_name(str,["__call__"])) # __call__'adlı metod -> Tanımlı!
# Peki neden ?: çünkü getattr,hasattr gibi fonkisyonlar MRO arama zincirini kullanırlar bu durumda sınıfın kendisinde olmasa bile miras aldığı sınıfta varsa ikiside bu niteliği bulabilir

print(repr(str())) # ''
print(list()) # []



# callable() Fonksiyonu

# callable() fonksiyonu,built-in bir fonksiyondur ve C dilinde yazılmıştır bu nedenle hızlıdır ama kaynak kodlarına erişilemez
# callable fonksiyonu,verilen objenin ait olduğu(yani örneği oldu sınıfta) __call__ metodunu arar eğer bu metodu bulursa True bulamazsa False döndürür
# callable fonksiyonu,

# sözdizimi: callable(obj) -> bool , obj: herangi bir python objesi

print(callable(str)) # True
# Neden True döner? çünkü: string sınıfının kendisinde olmasa bile örneği olduğu type sınıfında __call__ metodu tanımlıdır bu nedenle True döner

print(callable(str())) # False
# çünkü string nesnesi,str sınıfının örneğidir ve str sınıfında __call__ metodu tanımlı olmaz bu nedenle False döner

class Demir:
    def __call__(self):
        pass

demir = type.__call__(Demir)

print(callable(demir)) # True
# demir nesnesinin ait olduğu sınıf,Demir sınıfı ve bu sınıfta __call__ metodu tanımlıdır


# Bir Sınıftan Örnek Oluşturma Nasıl Yapılır

# 1) öncelikle bir örnek oluşturmanın ilk adımı __new__() Metodudur,__new__(), metodu,sınıftan nesne yaratmak için kullanılır
# __new__() metodu,metod çözümlemesini MRO sıralı miras zincirine göre yapar

""" Sözdizimi: __new__(cls,*args,**kwargs) -> object:
                    retrun ...
cls: sınıfın kendisidir bu,__new__() metodunun,hangi sınıf için çağrıldığını belirtir bu özellikle miras için şarttır 
aynı zamanda cls parametresine subclass veremezsin 
args ve kwargs: bunlar sınıfa gelen verilerdir bu verileri __new__() metodu doğrudan kullanır veya __init__() metoduna gönderir 

    """

# __new__(cls,*args,*kwargs) bu sözdizimi genel bir tavsiye şablonudur python,bu parametrelerde seni kısıtlamaz
# her sınıfın __new__() metodu için tanımladığı parametreler farklı olabilir,her sınıf bu parametreleri kendi sınıfın özelliği doğrultusunda özelleştirebilir
# __new__() metodu,metod çözümlemesi yapar bu durumda MRO sıralı miras zincirinde __new__() metodu tanımlı olan sınıfları sırasıyla dener en sonunda en temel sınıf olan object sınıfından metodu alır
# bunun  sonucunda sınıfın kendisinde __new__() metodu olmasada eğer miras alığı sınıflarda varsa o sınıftan,nesne oluşturulabilir
"""
for cls in CLass.__mro__:
    if '__new__' in cls.__dict__:
        new = cls.__dict__['__new__']
        break
"""

# __new__() metodu,mutlaka yeni oluşturduğu nesneyi dönmelidir bu dönen nesnenin durumu şu iki duruma bağlıdır;

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
# burda self parametresine kendisini vermemize gerek yok -> çünkü burda zaten örnekten bu metodu çağırdığımız için instance parametresine ihtiyacımız kalmadı

print(a) # None
# None döner çünkü __init__() metodu herangi bir değer döndürmez in-place işlem yapar;

print(listem)  # ['1', '2', '3', '4', '5']

