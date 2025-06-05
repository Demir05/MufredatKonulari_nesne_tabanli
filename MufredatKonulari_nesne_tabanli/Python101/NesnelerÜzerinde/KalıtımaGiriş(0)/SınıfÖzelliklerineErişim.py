class A:
    x = "demir"
    y= 10
a = A()

# __dict__ Özelliği

# __dict__,bir nesneye ait tüm atanmış olan tüm attributes(özellik ve metodlarn) ve değerlerinin tutulduğu özel bir python sözlüğüdür
# nesneye özgü davranışlar bu sözlükte tutulur
# __dict__,yalnızca örnek üzerinde tanımlanmış attribute'ları barındırır sınıfın,miras aldığı sınıflarda bulunan attribute'ları
# örnekteki _dict__ barındırmaz bu durum yapının hafif olmasını sağlar
# Python’da bir özniteliğe erişildiğinde (obj.x), bu değer önce obj.__dict__ içinde aranır.
# Bu yüzden __dict__, attribute erişimi ve yönetiminin temel taşıdır.

# aynı zamanda builtin sınıfların nesnelerinde,__dict__  tanımlı değildir bunun sebebi bu nesnelerin, hafif olmasını sağlamaktır
# genelde user-definded nesnelerde,__dict__ kullanılır

# Not: __dict__ özelliği object sınıfından mîras alınıp kullanılsa da __dir__() metodu içinde görünmez

# __dict__ sözlüğü tekil bir python sözlüğüdür ama bu sözlük,kullanıldığı nesneye göre üç farklı sınıftan mîras alır

# 1) <class 'dict'>: sınıfın örneği olan nesnede bulunan __dict__,normal bir python sözlüğüdür
# bu durumda bu sözlüğe statik olarak anahtar eklenebilir veya kaldırılabilir mesela;
a.__dict__['z'] = "aslı"; print(a.z) # aslı
# burda statik olarak bir anahtar ekledik

# 2) <class 'mappingproxy'>: mappingproxy,python'da normal bir dict gibi davranan ama salt okunur(değiştirilmeyen)
# bir nesnedir bu proxy sınıfında,values(),keys(),items() gibi viewLookup'lar kullanılabilir ama herangi bir şekilde
# sözlüğü manipüle edemezsin aynı zamanda bu nesne,canlıdır dolasıyla yeni bir özellik eklenmesi durumunda anında güncellenir
# bu dict sınıfı,sınıfın kendisinde bulunan __dict__'in örneği olduğu sınıftır

# 3) __dict__,meta sınıflarda; Descriptor nesnesi gibi davranır bu durumda type.__dict__ gibi bir erişimde descriptor protokolü uygulanır bunun sebibi type sınıfı C dilinde
# yazılmıştır ve bazı metodlar özel davranışlar sergiler aynı zamanda da bu dict, mapping proxy nesnesi olduğu için manipüle edilemez


# Çalışması;

# Python'da obj.__dict__ ifadesi yazıldığında aşağıdaki adımlar izlenir:

# 1) Python aslında obj.__getattribute__('__dict__') çağrısını yapar
#    Çünkü tüm attribute erişimleri __getattribute__ üzerinden çözülür.

# 2) İlk olarak obj'nin kendi __dict__ sözlüğüne bakılmaz! (Bu kafa karıştırıcıdır.)
#    Çünkü '__dict__' özel bir isimdir(istisnai durum) ve genellikle sınıf tarafından bir descriptor ile sağlanır.python,her zaman burda descriptor protokolünü uygular

# 3) Python, obj'nin sınıfına gider:
#    cls = type(obj)

# 4) Sınıfın __dict__ sözlüğünde '__dict__' adlı attribute aranır:
#    attr = cls.__dict__['__dict__']

# 5) Bu bulunan __dict__ nesnesi, büyük olasılıkla bir descriptor’dır (getset_descriptor)
#    Eğer attr, descriptor ise Python,Descriptor protokolünü uygular:
#        attr.__get__(instance, owner) çağrılır ve gerçek dict elde edilir

# 6) Eğer descriptor yoksa (olmazsa), attr doğrudan döndürülür

# 7) Sonuç olarak genellikle elde edilen şey obj’nin gerçek attribute sözlüğüdür:
#    örnek: {'x': 10, 'y': 20}

# 8) Eğer sınıf descriptor sağlamamışsa veya obj'nin __dict__'i yoksa (örneğin __slots__ kullanılmışsa),
#    AttributeError fırlatılır

# ⚠️ Not:
# - obj.__dict__ sadece örneklerde sözlük döndürür
# - Sınıflarda (A.__dict__) → mappingproxy döner
# - Built-in türlerde (__dict__) → getset_descriptor tarafından sağlanır

# örnekler;

print(A.__dict__) # {'__module__': '__main__', 'x': 'demir', 'y': 10, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}
# burda A sınıfının kendisinde bulunan tanımlı olan tüm özellikleri görüyorsun ama bu sınıfın miras aldığı diğer sınıflardaki özellikler __dict__'de olmaz

print(A.__dict__.__class__) # <class 'mappingproxy'>
# Gördüğün üzere örneği oldu sınıf,mappingproxy sınıfı

A.isim = "demir" # -> A sınıfına,yeni bir attribute ekledik şimdi bu Attribute nesnesini, Canlı olan salt okunur mappping proxy sözlüğünde bakalaım;
print(A.__dict__)  #{'__module__': '__main__', 'x': 'demir', 'y': 10, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__':
# <attribute '__weakref__' of 'A' objects>, '__doc__': None, 'isim': 'demir'}

print(a.__dict__) # {'z': 'aslı'}
# a nesnesinin,sahip olduğu özellik bu hatırlarsan tanımda ekledik;

a.__dict__["yeni"] = "merhaba"

print(a.__dict__)  # {'z': 'aslı', 'yeni': 'merhaba'}

# Descriptor durumuna bir örnek;
class A:
    def __init__(self):
        self.x = 10

a = A()

print(a.__class__.__dict__['__dict__']) # <attribute '__dict__' of 'A' objects> -> bu bir bound nesnesi
print(a.__class__.__dict__['__dict__'].__get__(a)) # {'x': 10} -> Gerçek dict burda döner



# vars() Builtin Fonksiyonu

# vars() fonksiyonu,verilen nesneye ait attribute'ların saklandığı __dict__ sözlüğünü döndüren bir python builtin fonksiyonudur
# vars(),yüksek seviye bir çağrıdır ve bu onu,okunabilir kılar bu nedenle __dict__ yerine tercih edilir

# Kullanım Alanları: genelde debug amacıyla tercih edilir


# Çalışması

# vars() fonksiyonun iki farklı davranışı vardır;

# 1) Eğer argüman verilmişse,verilen nesnenin __dict__ attribute'una erişir burda python,-> metod çözümlemesi yapar çünkü burda bir attribute çağırma işlemi var

    # 1) obj.__getattribute__('__dict__') çağrılılır, çözümlemesi-> obj.__class__.__dict__['__dict__']

    # 2) __dict__,özel bir isimdir python bunu,her zaman descriptor protokolü ile çözer;
    # obj.__class__.__dict__['__dict__'].__get__(obj) -> gerçek __dict__ burda döner

    # 3) python,bu dönen __dict__ bound nesnesini return ile dışarı döndürür

# 2) Eğer argüman verilmemişse,vars() fonksiyonu;mevcut scope'da tanımlı olan isimleri döndürür
# bunu locals() ile yapar

print(vars()) # -> locals() fonkisyonu,mevcut scope'da tanımlı ki global scope'tayız değerleri dict türünde döner
print(vars(a)) # {'x': 10}


# __getattribute__() Metodu

# __getattribute__() metodu,python'da bir nesne üzerinde herangi bir attribute nesnesine(özellik veya metod) erişmek istediğinde daima ilk çalışan bir metoddur
# bu metodu,genelde user-definded sınıflar override etmezler çünkü object sınıfından miras olarak gelir ve tüm user-definded sınıflar bu metodu,devralabilirler
# builtin sınıflar,genelde kendilerine özgü özelleştirilmiş __getattribute__ metoduna sahiptirler ve bu metodu,C düzeyinde override etmişlerdir

# __getattribute__() metodu,güçlü bir metoddur çünkü;
# 1) her niteliğe ulaşmak istenildiğinde daima çalışır
# 2) override edilmesi halinde,her attribute erişimini bu metod,filtreleyebilir,loglayabilir,değiştirebilir
# 3) bu metod,her şeyin üstündedir yani herangi bir yerde nitelik erişiminde bu metod çağrılırır bu durum aynı zamanda bu metodu,tehlikeli kırar
# çünkü çok kolay bir şekilde loop'a sokabilirsin(anlatılcak)

# sözdizimi: __getattribute__(instance,name:str) instance: sınıfın örneğidir, name: (string türünde) erişmek istediğin niteliğin adı


# Çalışması;

# __getattribute__ metodunun nitelikleri getirmesi, verilen objenin kendisinde sonra örneği olduğu sınıfta veya miraslarında bulunan __dict__ üzerinden yapılır.
# Çünkü __getattribute__ metodu, metod çözümlemesi (attribute resolution) yapar ve MRO (Method Resolution Order) zincirinde arama yapar.

# 1) İlk olarak örneğin (self) __dict__ sözlüğüne bakılır → varsa:
#    return self.__dict__['x']

# 2) Eğer örnek üzerinde bulunamazsa, bu defa MRO zincirine göre sınıflar üzerinde arama yapılır:
#    self.__class__.__dict__['x'], sonra base class'lar...

#    Teknik olarak zincir:
#    self.__getattribute__('x') → self.__class__.__dict__['x'] → base class → object...

# 3) Bulunan nesne eğer **descriptor** ise, Python descriptor protokolünü uygular;
#    Aksi halde, nesnenin kendisini doğrudan döner.

# Descriptor Nedir:
#    Bir sınıfın başka bir sınıf nesnesi üzerinden erişildiğinde özel davranış sergilemesini sağlayan yapıdır.
#    __get__, __set__ veya __delete__ metodlarından en az birine sahip olması gerekir.

# Descriptor Davranışı:
#    type(self).__dict__['x'] bir descriptor ise →
#    onun __get__ metodu çağrılır: __get__(instance, owner)

# 4) Eğer özellik tüm bu adımlarda bulunamazsa → AttributeError hatası fırlatılır.
#    Eğer `__getattribute__()` metodu override edilmemişse ve hata alınırsa, Python otomatik olarak
#    `__getattr__()` metodunu çağırır. Ama `__getattribute__()`'i manuel çağırırsan (örneğin: A.__getattribute__(a, 'x')),
#    Python `__getattr__()` metodunu çağırmaz. Bu sadece `obj.x` gibi sözdizimsel kullanımlarda devreye girer.
# Neden Tehlikeli;

class Demir:

    def __getattribute__(self, item:str):
        return self.x
"""
self.x ifadesi yazıldığı anda python,tekrar __getattribute__() metodunu çağırır çünkü bu metod,her şeyin üstünde ve  nitelik çağrısında ilk bu metod çağrılırır
"""
demir = Demir()
try:
    print(demir.x)
    # burda python arka planda şu işlemleri yapar;
    # demir.__getattribute__('x'): AttributeError -> demir.__class__.__getattribute__(demir,'x')
except RecursionError: # loop
    print("loop")

# basit örnekler;

isim = "demir"
print(str.__getattribute__(isim,"upper")()) # DEMIR
# str sınıfında bulunan __getattribute__ metodunu çağırarak upper() fonksiyonuna eriştik

print(object.__getattribute__(isim,"upper")()) # DEMIR
# burda ise object sınıfında bulunan __getattribute__ metodunu çağırarak upper fonksiyonunu çağırdık

print(isim.__getattribute__("title")()) # Demir
# burda instance parametresine argüman vermedik çünkü __getattribute__ metodunu,zaten örnek üzerinden çağırdık



# __getattr__() Metodu

# __getattr__() metodu,yalnızca __getattribute__ metodu başarısız olup,AttributeError istisnası fırlatırsa çalışan bir yedek metoddur
# __getattr__ metodu,__getattribute__ metodunun aksine nesnenin veya miraslarınaki __dict__ özelliği ile ilginmez,attribute aramaz eğer özellik yoksa bu metod çalışmak için tasarlanmıştır
# __getattr__() metodu,object sınıfında tanımlı olan bir metod değildir bu nedenle sınıflar,ihtiyaçları hâlinde bu metodu manuel tanımlamaları gerekmekte aksi halde varsayılan olarak çalışmaz
# aynı zamanda __getattr__ metodun maaliyeti,__getattribute__ metoduna göre daha hafiftir

# sözdizimi: __getattr__(instance,name:str) instance:sınıfın örneğidir, name:bulunmayan özelliğin (string türünde) adı

class Sınıfım:

    def __getattr__(self, item):
        print(f"{item} bulunamadı :/")


self = Sınıfım()

self.olmayan_özellik # olmayan_özellik bulunamadı :/

# burda arka planda şu işlemler oldu;
# 1) self.olmayan_özellik ifadesi tetiklenir
# 2) Python, self.__getattribute__('olmayan_özellik') çağrısını yapar
# 3) __getattribute__, önce self.__dict__['olmayan_özellik'] içinde arar (örnek düzeyi)
# 4) Bulamazsa, self.__class__.__dict__ ve MRO üzerinden sınıflarda arar
# 5) Hâlâ bulunamazsa AttributeError fırlatılır
# 6) Python bu durumda __getattr__('olmayan_özellik') çağrısını yapar
# 7) self.__getattr__ varsa onu çağırır, yoksa self.__class__.__getattr__ ve MRO zincirini kullanır
# 8) Sınıfım'da tanımlı olduğu için → Sınıfım.__getattr__(self, 'olmayan_özellik') çalışır



# getattr() Builtin fonksiyonu

# getattr() fonksiyonu,belirtilen objede,o objenin ait olduğu sınıflarda ve o sınıfın mîraslarında verilen attribute değerini getiren builtin dolasıyla
# C dilinde yazılmış olan bir python fonksiyonudur
# bu fonksiyonu,dinamik bir nokta,sözdizimsel işareti olarak düşünebilirsin çünkü bu fonksiyon bir objede attribute'a erişmeyi dinamik ve modüler kırar

# Sözdizimi: getattr(obj,attribute:Str,*,default=None) obj: herangi bir python objesi, attribute:değeri getirilcek olan string türünde özelliğin adı
# default: eğer özellik bulunamazsa ve AttributeError alınırsa döndürülcek olan varsayılan değer,varsayılan olarak None değeri atanmıştır bu durumda bu fonksiyon dışarıya AttributeError döndürür


# Çalışması;

# getattr() fonksiyonun kendisi,MRO zincirini ve __dict__'İ kullanmaz bu işlemi __getattribute__ kendi içinde çözümler işte adımları;

def attr(obj:object,attr:str,*,default= None)-> object:
    try:
        at = obj.__class__.__getattribute__(obj,attr) # -> obj.__dict__['attr'] = ERR. -> obj.__class__...
        return at
    except AttributeError:
        try:
            at= obj.__class__.__getattr__(obj,attr)
            return at
        except AttributeError:
            if default is not None:
                return default
            raise AttributeError(f"{attr} not found.")

print(attr(str,"upper")) # <method 'upper' of 'str' objects>

# örnekler;

print(getattr(str(),"lower")) # <built-in method lower of str object at 0xb3acf0>

isim= "demir"
print(getattr(isim,"title")()) # Demir

# daha gelişmiş bir örnek;

from collections import namedtuple as np
Kisi = np("Kisi",["isim","yas"])
kisi1 = Kisi(
    isim="demir",
    yas=20
)

for alan in kisi1._fields:
    print(getattr(kisi1,alan))
"""
demir
20
"""



# hasattr() Builtin fonksiyonu

# hasattr() fonksiyonu,belirtilen nesnede,onun ait olduğu sınıfta ve o sınıfın miraslarında verilen attribute(özellik veya metodu) getattr() fonksiyonu yardımıyla arayan
# eğer bulabilirse True AttributeError alırsada hatayı bastırarak False dönen builtin(C dilinde yazılan) bir python fonksiyonudur
# bu fonksiyon,kendi yapısında getattr() fonksiyonunu kullanır ama hatayı bastırarak bool türünde bir nesne döner dolasıyla getattr() fonksiyonun davranışlarının tümünü kapsar

# hasattr() fonksiyonunun amacı

# bir nesnenin iç yapısını kontrol etmeye yarar,AttributeError hatalarını önlemek(olmayan bir özelliği getattr ile erişmeye çalışırsan hata alırsın )
# bu nedenle ilk başta o özelliğe sahip olup olmadığını kontrol edebilirsin
# dinamik kod yazmak,yani nesnenin hangi özelliklere sahip olup olmadğını önceden bilmiyorsan kullanabilirsin bu sayede de hata almazsın
# esneklik sunar,farklı nesnelerde çalışırken kodun patlamasını önler
# dinamik nesne işlemleri için uygundur bu sayede kodun mödülerliği artar.

# hasattr() fonksiyonun kullanım alanları;

# bir sınıfın belirli bir değişkenine veya özelliğini kontrol etmek için kullanılır
# excepction handling yapmak
# bir API den gelen JSON verisinde alan adlarının olup olmadığını kontrol etmek(hatırla namedtuple alan adları vardı )

# tanımda ve burda değişkenin onceden bilmediğin özelliğini bilmiyorsan hata almamak için kullanımından bahsettik bu sadece basit bir attribute kontrolü değildir
# bir nesnenin tipine göre davranış değiştirmek için de kullanılır özellikle dinamik olan python kodlarında hayati bir önem taşır;
# şöyle düşün:namedtuple sınıfını öğrenirken nested tuple'den bahsettik döngü kurarken şu anki yapının ne olduğunu örenmek için isinstance() fonksiyonunu kullandık ve eğer değişken
# tuple ise bir kez daha for döngüsü yazmıştık ya bunun yerine hasattr() kullanmak daha güvenli sağlam dolayısıyla pythonic bir çözüm olurdu çünkü direkt nesnein tipine göre işlem yapardık -> mesela hasattr(veri,"_fields") > burda _fields özelliği sadece namedtuple de yer alır şunları asla unutma;
# hasattr() + getattr() kombinasyonu ile;
# alan var mı ?,varsa değerini al,eğer gerekirse callable() kullan ve nesne callable ise cağır değilse değerini yazdır

# DİKKAT: gerektiğinde kullan bir kontrol işlemi yaptığı için eğer çok fazla kullanılsan performans düşebilir
# bu nedenle nerde kullanacağını iyi bilmen gerekir belirsiz(JSON ) veri yapılarında kontrol amaçlı kullanabilirsin.


# sözdizimi: hasattr(obj,attribute:str) obj:herangi bir python nesnesi, attribute:aranacak olan attribute ve bu string türünde olmalıdır

# hadi kendimiz yazalım;

def my_hasattr(o:object,atr:str) -> bool:

    try:
        attr(o,atr)
        return True
    except AttributeError:
        return False

print(my_hasattr(str,"upper")) # True

# örnekler;

print(hasattr(dict,'setdefault')) # True
print(hasattr(set,'union')) # True
print(hasattr(set,'extend')) #  False

# hasattr() nested olan neselerde tür belirlemede kullanılır

if hasattr(kisi1,"_fields"): # burda verinin,namedtuple olduğunu doğruladık
    for alan in kisi1._fields:
        print(getattr(kisi1,alan))

# mesela bu örnekte amaç iç içe olan verileri recursive fonksiyon yardımıyla düzlemek;

def duzle(obj):
    for eleman in obj:
        if hasattr(eleman,"extend"):
            yield from duzle(eleman)
        else:
            yield eleman

gen = duzle(["1","2","3","4",["6","7"]])

for i in gen:print(i)
"""
1
2
3
4
6
7
"""



# __dir__() Metodu

# __dir__() metodu,bir nesneye ait attribute adlarının listesini döndürmek için tanımlanmış bir metoddur
# __dir__,tamamen görsel ve destekleyici amaçlıdır bu nedenle de Attribute erişim sisteminde görev yapmaz bu onu,override etmeyi güvenli kırar

# Kullanım Amacı

# 1) öz-inceleme desteği vermek: kullanıcıların ve araçların(IDE) nesnenin hangi özelliklere sahip olduğunu görmesini sağlar
# 2) gizlemek ve özelleştirmek: bazı nitelikleri gizleyebilir ya da sadece belirli şartlar altında gösterilmesini sağlayabilirsin
# ayrıca dir() fonksiyonun çağrılması sonucu döndürülülen attribute'ları belirleyebilirsin __dir__() metodunu,override edebilirsin


# __dir__() VS __dict__

# __dir__() bir metod iken, __dict__ bir sözlüktür
# __dir__() -> liste döndürür,__dict__ -> <class 'dict'> döndürür
# __dir__() metodunun amacı görselliktir ama __dict__'İn ise veri saklama ve attribute erişimidir
# __dir__() metodu,override etmeye uygundur ama __dict__,KESİNLİKLE uygun değildir çünkü __dict__;
# pythonun,attribute erişim sisteminde doğrudan kullanılır eğer overeride edersen attribute sistemine karşı gelmiş olursun, attribute sistemini tehlikeye atarsın


# Çalışması;

# obj.__dir__() İÇİN

# 1) python,ilk olarak __getattribute__() metodunu çağrırır (çünkü obj.__dir__,bir Attribute erişimidir)

# 2) obj.__getattribute__('__dir__') işlemi yapılır bu işlem;

    # -> obj.__dict__['__dir__'] eğer bulunmazsa -> obj.__class__.__dict__[...] ,-> MRO ZİNCİRİ şeklinde metod çözümlemesi yapılır( bunu __getattribute__ yapar)
    # Eğer bunun sonucunda __dir__() metodu, object sınıfında bulunursa varsayılan __dir__() davranışı gerçekleştirilir;
    # -> ) obj.__dict__,type(obj).__dict__, mro() zincirindeki nitelikler,
    # Dahili özellikler
    # gibi kaynakları birleştirerek otomatik attribute listesi döndürür.,__dir__'in varsayılan davranışı,bu böyle sağlanır

# 3) eğer bulunan nesne,Descriptor ise python,Descriptor protokolünü uygular;
    # -> obj.__dict__['__dir__'].__get__(obj,obj.__class__) -> bu sayede yeni bir bound method elde ederiz
    # değilse -> direkt nesnenin kendisi döndürülür artık burada __dir__ descriptor'ı değil, method-wrapper'ın kendi __dir__ metodu çağrılır
# # # bu çağrı zinciri bizi → genellikle object.__dir__(obj) olur ve bir liste döner


print(str.__dir__(str))
"""
['__new__', '__repr__', '__call__', '__getattribute__', '__setattr__', 
'__delattr__', '__init__', '__or__', '__ror__', 'mro', '__subclasses__', 
'__prepare__', '__instancecheck__', '__subclasscheck__', '__dir__', '__sizeof__', 
'__basicsize__', '__itemsize__', '__flags__', '__weakrefoffset__', '__base__', 
'__dictoffset__', '__name__', '__qualname__', '__bases__', '__mro__', '__module__', 
'__abstractmethods__', '__dict__', '__doc__', '__text_signature__', '__annotations__',
 '__type_params__', '__hash__', '__str__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', 
 '__ge__', '__reduce_ex__', '__reduce__', '__getstate__', '__subclasshook__', '__init_subclass__', 
 '__format__', '__class__']
"""


# dir() Builtin Fonksiyonu

# dir() fonksiyonu,bir nesneye ait attribute'ları adlarını liste olarak döndürmeye sağlayan builtin(C dilinde yazılmış olan bir fonksiyondur)
# bu fonksiyon introspection function sınıfına girer yani ASLA hata döndürülmemelidir bu durumda kendi yapısında kontrol mekanizmaları ile dinamik olarak
# davranış değiştirir kullanıcıya sessiz,hatasız,yumuşak bir kullanım sağlar


# Kullanım alanları

# 1) REPL 'de ben hangi isimleri oluşturdum neler yaptığım soruna cevap olabilir debug amaçlı dir() fonksiyonu kullanılabilir

# 2) dir() ile belirli bir değişkenin mevcut scope'da tanımlı olup olamdığını dinamik bir şekilde bulabilirsin

# 3) dir() ile argüman vermeyerek mevcut scope'da tanımlı olan isimleri öğrenenilirsin

# 4)dir() ile hiç bilmediğin bir objeyi keşfedebilirsin burda getattr() fonksiyonundan yardım alabilrsin


# dir() fonksiyonun iki tane davranışı vardır;

# 1) argüman verilmişse;
    #  nesnede __dir__() metodunun olup olmadığını kontrol eder
    # -> eğer nesnede __dir__() metodu varsa direkt -> obj.__dir__() ile döndürür -> burda __dir__ çözümlenir...
    # -> eğer nesnede __dir__() metodu yoksa, o zaman güvenli fallback mekanizması devreye girer ve object.__dir__(obj) ile varsayılan __dir__() davranışı sağlanır

# 2) argüman verilmemişse;
    # dir() fonksiyonu,mevcut local scope'ta tanımlanan isimleri listeler ve döndürür
    # bunu sorted(locals().keys()) ile sağlar

 # Temsili dir() fonksiyonu;

def dir_(obj):
    # Bu satırda __getattribute__ devreye girer
    if hasattr(obj, '__dir__'):
        # hasattr(obj, '__dir__') → obj.__getattribute__('__dir__') dener

        # bu satır da yine attribute erişimi:
        return obj.__dir__()  # bu da obj.__getattribute__('__dir__')() demektir
    else:
        ...


