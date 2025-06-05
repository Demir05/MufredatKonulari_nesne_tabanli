# Python'da her bir sınıf çağrılabilir bir nesnedir bir sıfını çağırmak için genelde obj = Sınıf() şeklinde bir tanımlama yapılır
# bir sınıfı çağrımak için kullandığın; list(),tuple(),str(),map(),reversed() gibi sınıf çağrıları, fonksiyon değil bir sınıf çağrısıdır arka planda obj = Class.__new__(cls,...) çağrırır
# bunların fonksiyon gibi görünmesinin nedeni kullanıcıya kolaylık sağlaması içindir
# built-in sınıflar,C dilinde yazılmışlardır dolasıyla kaynak kodlarına erişilemez

from inspect import isbuiltin

# str(),list()... bunların fonksiyon olmadığının kanıtı;

print(isbuiltin(str)) # False


# Sınıf nasıl çağrılır


# __call__() metodu;

# __call__() metodu,bir sınıfın örneğini,çağrılabilir yapan yegane metoddur bu metod sayesinde sınıf örneğini,fonksiyon gibi çağırabilirsin bunun için parantez(()) sözdizimsel işaretini kullan
# __call__() metodu,sınıfın kendisini çağrılabilir yapmaz bir sınıfı mesela str sınıfını,çağırmanı sağlayan şey,o sınıfta __call__() metodunun olması değil(zaten yok)
# str sınıfının örnekleme ile bağlı olduğu type sınıfında tanımlı olan __call__() metodudur bu sayede,tüm sınıflar tek bir noktadan kontrol edilir bu da merkezi yönetimi ve tutarlığı sağlar
# ayrıca sınıf çağrısı ile nesne yaratımı ayrılır
# __call__,diğer dunder metodlar gibi MRO kalıtımsal zincirini kullanarak metod çözümlemesi yapılabilir çağrılması halinde eğer sınıfın kendisinde yoksa miras aldığı sınıflarda aranır
# __call__ metodu,Descriptor bir nesnedir bu nedenle python,nesneyi çağrılabilir yapmak için Descriptor protokolünü uygular

# Sözdizimi: type.__call__(cls, *args, **kwargs) → object
# cls: çağrılcak olan sınıf, *args: sınıfa gelicek olan pozisyoneller, **kwargs: sınıfa gelcek olan keyword'ler -> bunlar,nesnenin değeri olcak olan argümanlar'dır


# Çalışması;
# Genel Not: nesne çağırmada python,o nesnenin ait olduğu sınıfta bulunan __call__ metodu üzerinden o nesneyi çağırır bunun nedeni çağrılma işlemininin
# nesnenin örneği olduğu sınıf tarafından belirlenmesidir

# # str("demir")  -> Bir sınıf çağırma işlemi
#
# # 1) Çağırma:
# # Python, str("demir") ifadesini görünce, bu bir "sınıf çağırma" işlemidir.
#
# # 2) Yorumlanma:
# # Bu, aşağıdaki zincirle eşdeğerdir:
# # → type(str).__call__(str, "demir")
# # (str sınıfı, type sınıfının bir örneğidir ve çağrılabilirliği __call__ ile tanımlıdır)
#
# # 3) __call__ çözümlemesi,burda bir attribute erişimi vardır bu nedenle __getattribute__ çağrılır:
# # → type.__dict__['__call__'].__get__(str, type(str))("demir")
# # (type sınıfındaki __call__ metodu descriptor'dür ve __get__ ile çağrılabilir hale getirilir ve __get__,str sınıfı için bağlanır bu işlemde yeni bir bound method elde ederiz
# # artık burada __call__ descriptor'ı değil, bound method'un  kendi __call__ metodu çağrılır -> hatırlarsan __call__,bir attribute erişimi ve __getattribute__,bound method nesnesinde __call__ metodunu bulur
# # bu çağrı zinciri bizi → str.__new__ → str.__init__ sürecine taşır (nesne oluşturma davranışı)
#
# # 4) Nesne oluşturulması:
# # Bu aşamadan sonra, __call__ metodu sırasıyla şunları yapar:
# # → str.__new__(str, "demir")  # bellekte yeni nesne oluşturur
#
# # ⛳ SONUÇ:
# # Bu zincir sonunda yeni bir string nesnesi oluşur → "demir"

# kanıt: type(str).__dict__['__call__'] is type.__call__.__get__(str,type) >> False gördüğün üzere type sınıfında bulunan __call__ metodu ile bu metoda descriptor
# protokülü uygulandığında dönen nesne aynı __call__ metodu değil

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

