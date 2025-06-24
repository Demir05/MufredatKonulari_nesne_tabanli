


class A:
    x = "demir"
    y= 10
a = A()

# ========================================
# 📘 __dict__ ATTRIBUTE – TANIM
# ========================================

# __dict__, bir nesnenin (instance ya da sınıf) sahip olduğu attribute'ları saklayan
# sözlük (dictionary) tabanlı bir yapıdır.

# Ancak dikkat!
# __dict__ bir metod değil, bir attribute’dur. Yani çağrılmaz → obj.__dict__ ✅
# (obj.__dict__() ❌ çalışmaz)

# ========================================
# 🔍 NEYİ SAKLAR?
# - Instance düzeyinde → sadece o örneğe ait attribute'lar (__init__ içinde tanımlananlar gibi)
# - Class düzeyinde → sınıf gövdesinde(class body) tanımlı attribute'lar (__dict__ burada bir "mappingproxy" nesnesidir, yani salt okunur)

# ========================================
# 🧪 NE ZAMAN KULLANILIR?
# - Bir nesneye ait attribute'ları incelemek, dinamik olarak eklemek, silmek veya analiz yapmak için kullanılır
# - inspect, vars(), dir() gibi araçlar da bu attribute’tan yararlanır
# - Attribute Erişim Protokolü’nde önemli bir rol oynar çünkü Python, attribute erişiminde __dict__'i kullanır


# ========================================
# ⚙️ INSTANCE (ÖRNEK) DÜZEYİNDE __dict__ – ÇAĞRI ZİNCİRİ
# ========================================

# Örnek: obj.__dict__

# 1) Python bu attribute’a erişmek ister -> çünkü obj.__dict__ bir attribute erişimidir
#    → type(obj).__getattribute__(obj, '__dict__') 

# 2) __getattribute__ metodu çalışır:
# Objeye bakılmaz çünkü bu bir special attibute erişim işlemidir doğrudan objenin ait olduğu sınıfa bakılır
#    → obj.__class__.__dict__'te '__dict__' adında bir descriptor aranır ✅(type sınıfında bulunan __dict__,bir descriptor'dır))

# 3) type objesi (__class__) üzerinde tanımlı olan descriptor:
#    → <attribute '__dict__' of 'type' objects>

# 4) Bu bir data descriptor olduğu için:
#    → descriptor.__get__(obj, obj.__class__) çağrılır

# 5) Sonuç olarak: örneğe ait attribute'ları içeren gerçek sözlük (dict) döner(çünkü __dict__,bir method değil, bir attribute'dur bu nedenle doğrudan gerçek __dict__ döner,bound method dönmez):)

# ========================================
# ⚙️ CLASS (SINIF) DÜZEYİNDE __dict__ – ÇAĞRI ZİNCİRİ
# ========================================

# Örnek: MyClass.__dict__

# 1) Python erişimi başlatır:
#    → type(MyClass).__getattribute__(MyClass, '__dict__')

# 2) type sınıfı üzerinde tanımlı '__dict__' descriptor'ı bulunur: (python,sınıfın kendisinde arama yapmaz! bu bir special method attribute işlemidir)
#    → <attribute '__dict__' of 'type' objects>

# 3) descriptor.__get__(MyClass, type) çağrılır

# 4) Bu durumda dönen şey:
#    → MyClass’a ait attribute’ları tutan "mappingproxy" nesnesidir(çünkü __dict__,bir attribute'dur method değil bu nedenle Descriptor çözümlemesinden sonra mappingproxy nesnesi döner)
#     (salt okunur dict)

# ========================================
# 🧠 ÖZET & NOTLAR

# ✔️ Instance'da: obj.__dict__ → gerçek, değiştirilebilir dict döner
# ✔️ Sınıfta:   cls.__dict__ → mappingproxy (salt okunur görünüm) döner

# ✔️ __dict__ bir descriptor’dır (getset_descriptor)
# ✔️ Python bu attribute’a ulaşmak için __getattribute__ + descriptor protokolünü birlikte kullanır

# ✔️ Tüm sınıflar __dict__ içermez → __slots__ kullanan sınıflarda __dict__ olmayabilir!
# ✔️ type sınıfında __dict__ bulunurken, object sınıfında __dict__ bulunmaz ! 

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
print(a.__class__.__dict__['__dict__'].__get__(a)) # {'x': 10} -> Gerçek dict burda döner sonrasında çağırmamıza gerek yok çünkü __dict__ bir attribute'dur



# vars() Builtin Fonksiyonu

# vars() fonksiyonu,verilen nesneye ait attribute'ların saklandığı __dict__ sözlüğünü döndüren bir python builtin fonksiyonudur
# vars(),yüksek seviye bir çağrıdır ve bu onu,okunabilir kılar bu nedenle __dict__ yerine tercih edilir

# Kullanım Alanları: genelde debug amacıyla tercih edilir


# Çalışması

# vars() fonksiyonun iki farklı davranışı vardır;

# 1) Eğer argüman verilmişse,verilen nesnenin __dict__ attribute'una erişir burda python,-> metod çözümlemesi yapar çünkü burda bir attribute çağırma işlemi var

    # 1) type(obj).__getattribute__(obj,'__dict__') çağrılılır,
        # 1) öncelikle objenin kendisinde __dict__ attribute'u aranır -> obj.__dict__['__dict__'] 
        # 2) eğer bulunamazsa -> obj.__class__.__dict__['__dict__'] aranır

    # 2) bulunan __dict__ attribute'u, bir descriptor'dır ve bu nedenle __get__ metodu çağrılır
    # obj.__class__.__dict__['__dict__'].__get__(obj) -> gerçek __dict__ burda döner

    # 3) python,bu dönen __dict__ bound nesnesini return ile dışarı döndürür

# 2) Eğer argüman verilmemişse,vars() fonksiyonu;mevcut scope'da tanımlı olan isimleri döndürür
# bunu locals() ile yapar

print(vars()) # -> locals() fonkisyonu,mevcut scope'da tanımlı ki global scope'tayız değerleri dict türünde döner
print(vars(a)) # {'x': 10}



# __getattribute__() Metodu

# __getattribute__() metodu,python'da bir nesne üzerinde herangi bir attribute nesnesine(özellik veya metod) erişmek istediğinde daima ilk çalışan bir metoddur
# builtin sınıflar,genelde kendilerine özgü özelleştirilmiş __getattribute__ metoduna sahiptirler ve bu metodu,C düzeyinde override etmişlerdir

# __getattribute__() metodu,güçlü bir metoddur çünkü;
# 1) her niteliğe ulaşmak istenildiğinde daima çalışır(bu niteliklere dunder metodlar da dahildir)
# 2) override edilmesi halinde,her attribute erişimini bu metod,filtreleyebilir,loglayabilir,değiştirebilirsin
# 3) bu metod,her şeyin üstündedir yani herangi bir yerde nitelik erişiminde bu metod çağrılırır bu durum aynı zamanda bu metodu,tehlikeli kırar
# çünkü çok kolay bir şekilde loop'a sokabilirsin(anlatılcak)

# sözdizimi: __getattribute__(instance,name:str) instance: sınıfın örneğidir, name: (string türünde) erişmek istediğin niteliğin adı

 # Bu özel metot, bir nesne üzerinden HER attribute erişiminde çağrılır.
    # Yani a.x gibi bir ifade çalıştırıldığında devreye girer.
    
    # 📌 Önemli: a.x bir EXPRESSION'dır → Python burada bir DEĞER bekler.
    # Bu nedenle __getattribute__ mutlaka bir return içermelidir.
    
    # Aksi takdirde TypeError: __getattribute__() should return a value hatası alınır.

# ========================================
# ⚙️ ATTRIBUTE ERİŞİMİNDE ÇAĞRI ZİNCİRİ
# ========================================

# Örnek: obj.x
    
# 1) Python şu çağrıyı yapar:
#    → type(obj).__getattribute__(obj, 'x') çünkü attribute erişimleri örneğin,ait olduğu sınıf tarafından çözülür(örnekleme kuralı)

# 2) Bu metot içindeki temel işlem sıralaması:

# a) obj.__dict__ içinde 'x' adında bir attribute var mı? ✅ → varsa döndürülür
# b) obj.__class__.__dict__ içinde 'x' var mı? ✅ → varsa ve:
#     - data descriptor ise → descriptor.__get__(obj, obj.__class__) çağrılır burda __get__ metodu,obj'ye bağlanır 
#     - eğer attr,bir method ise bu  işlemler sonucunda bound method elde ederiz bu method'u kullanabilmek için çağırmamız gerekir: descriptor.__get__(obj, obj.__class__).__call__(*args,**kwargs)
#     - eğer attr,sadece bir attribute ise bu işlemler, kendisini doğrudan döner
# c) __getattr__ override edilmişse → obj.__getattr__('x') çağrılır
# d) Hiçbiri bulunamazsa → AttributeError fırlatılır

# sınıf düzeyinde ise örnek: A.x;
# sınıf düzeyindeki attribute erişimi,meteclass tarafından çözülür ve bu durumda da yine __getattribute__ metodu çağrılır:

# type(A).__getattribute__(A, 'x')

# 2) Bu metot içindeki temel işlem sıralaması:

# a) A.__dict__ içinde 'x' adında bir attribute var mı? ✅ → varsa döndürülür, yoksa MRO zinciri üzerinden arama yapılır + type.__dict__...(__getattribute__ metodu,sadece sınıf ve onun mirasları değil aynı zamanda type sınıfının da __dict__'ini kullanır))
#     - data descriptor ise → descriptor.__get__(obj, obj.__class__) çağrılır burda __get__ metodu,obj'ye bağlanır 
#     - eğer attr,bir method ise bu  işlemler sonucunda bound method elde ederiz bu method'u kullanabilmek için çağırmamız gerekir: descriptor.__get__(obj, obj.__class__).__call__(*args,**kwargs)
#     - eğer attr,sadece bir attribute ise bu işlemler kendisi doğrudan döner
# b) __getattr__ override edilmişse → obj.__getattr__('x') çağrılır
# c) Hiçbiri bulunamazsa → AttributeError fırlatılır

# ⚠️ İSTİSNA: Eğer erişilen attribute özel (dunder) bir metodsa (örnek: __str__, __repr__, __call__)
#    - Python bu durumda, doğrudan obj'nin ait olduğu sınıftan (type(obj)) başlar(objenin/sınıfın kendisine bakılmaz)
#    - Çünkü bu metodlar davranışsal olarak yorumlanır (örnek: print(obj) veya obj())
#    - ÖRNEK: print(obj) → type(obj).__str__(obj)
#             obj()       → type(obj).__call__(obj, ...)

# NOT: Bu nedenle __str__, __repr__, __call__ gibi metodlar için __getattribute__ zinciri devreye girmeden
#      doğrudan sınıfın ait olduğu sınıftan (type(obj)) çözümleme başlatılır.

# ========================================
# 🧠 NOTLAR
# - __getattribute__ override edilirken dikkatli olunmalı!
#   İçeride tekrar self.x gibi çağrılar yapılırsa YİNE __getattribute__ çalışır ve sonsuz döngüye girilir.
#   Bu yüzden object.__getattribute__(self, name) gibi doğrudan üst sınıftan çağrılmalıdır.

# - Descriptor protokolü (obj.x → descriptor.__get__()) bu zincirlemenin bir parçasıdır.
#   Yani bir attribute, descriptor (özellikle data descriptor) ise Python onun __get__() metodunu çağırır.

# ========================================
# 🔁 ÖZET
# obj.x → type(obj).__getattribute__(obj, 'x')
#     → obj.__dict__ → obj.__class__.__dict__ → descriptor protokolü → __getattr__ (fallback) → AttributeError


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
# __getattr__ metodu,__getattribute__ metodunun aksine nesnenin veya miraslarındaki __dict__ özelliği ile ilginmez,attribute aramaz eğer özellik yoksa bu metod çalışmak için tasarlanmıştır
# __getattr__() metodu,object sınıfında tanımlı olan bir metod değildir bu nedenle sınıflar,ihtiyaçları hâlinde bu metodu manuel tanımlamaları gerekmekte aksi halde varsayılan olarak çalışmaz
# aynı zamanda __getattr__ metodun maaliyeti,__getattribute__ metoduna göre daha hafiftir

# sözdizimi: __getattr__(instance,name:str) instance:sınıfın örneğidir, name:bulunmayan özelliğin (string türünde) adı

  # Bu özel metot, sadece __getattribute__ AttributeError fırlattığında çağrılır.
    # Yani erişilmek istenen attribute, nesnede tanımlı DEĞİLSE devreye girer.

    # 📌 Bu da bir EXPRESSION bağlamında çalışır → a.bilmedigim_attr gibi.
    # Bu yüzden buradan da MUTLAKA bir değer dönmelidir.


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

# getattr() fonksiyonu,belirtilen objede,o objenin ait olduğu sınıflarda ve o sınıfın mîraslarında  verilen attribute değerini getiren builtin dolasıyla
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



# -----------------------------
# 🔍 hasattr() Built-in Fonksiyonu
# -----------------------------

# ✔️ Tanım:
# hasattr(obj, attr) → Belirtilen nesnede (obj), verilen attribute (attr) adında bir özellik olup olmadığını kontrol eder.
# Dahili olarak getattr(obj, attr) fonksiyonunu kullanır; ancak AttributeError yakalanır ve bastırılır.
# Eğer attribute bulunursa → True, bulunamazsa → False döner.

# ✔️ Davranış:
# - getattr() çağrısını içeride yapar.
# - getattr() çağrısı başarısız olursa AttributeError fırlatır ama hasattr() bunu yutar ve False döner.
# - Bu sayede kod, AttributeError yerine güvenli bir şekilde bool sonuçla ilerler.

# -----------------------------
# 🎯 Kullanım Amaçları
# -----------------------------

# 1. Attribute kontrolü:
#    Nesneye ait bir attribute’a erişmeden önce onun var olup olmadığını kontrol etmek için kullanılır.
#    Bu, AttributeError almamak için güvenli bir yoldur.

# 2. Dinamik yapı kontrolü:
#    Özellikle dinamik veri yapılarında (örneğin JSON, API yanıtları) belirli bir alanın olup olmadığını kontrol etmek için idealdir.

# 3. Pythonic kontrol akışı:
#    isinstance() gibi tip kontrolü yerine, nesnenin davranışına (duck typing) göre yönlendirme yapılmak istendiğinde kullanılır.
#    Örn: hasattr(obj, "__iter__") → iterable mı?

# 4. Esneklik ve modülerlik:
#    Kodun farklı nesne türleriyle patlamadan çalışmasını sağlar. Özellikle geniş çaplı kütüphanelerde (pydantic, marshmallow) yaygındır.

# -----------------------------
# 💡 Gerçek Dünya Örneği:
# -----------------------------

# API’den gelen veri içeriği bilinmiyorsa:
# if hasattr(veri, "_fields"):   # _fields → namedtuple özelliği
#     print(veri._fields)

# Veya:
# if hasattr(obj, "process"):
#     if callable(getattr(obj, "process")):
#         obj.process()
#     else:
#         print(obj.process)  # Değer sadece gösterilir

# -----------------------------
# ⚠️ Dikkat Edilmesi Gerekenler
# -----------------------------

# - hasattr(), içeride getattr çağırdığı için attribute erişim zincirini (MRO, descriptor, __getattr__) tetikler.
# - Bu durum performans açısından pahalı olabilir; çok sık ve bilinçsiz kullanımı önerilmez.
# - Gereksiz kontrollerden kaçın, sadece belirsiz yapılarda (örneğin dış veri kaynakları) kullan.

# -----------------------------
# 🧪 Sözdizimi:
# -----------------------------

#    hasattr(obj, attr: str) -> bool
#    obj  : her tür Python nesnesi olabilir
#    attr : kontrol edilecek attribute adı (str türünde olmalı)

# -----------------------------
# ✅ Özette:
# hasattr() fonksiyonu, bir attribute’un varlığını güvenli şekilde kontrol eder.
# AttributeError almadan, bool olarak sonucu bildirir ve bu sayede kodu daha sağlam, dinamik ve pythonic hale getirir.


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

# setattr() fonksiyonu, verilen bir nesnenin attribute (özellik) değerini **dinamik olarak ayarlamak** için kullanılan bir Python yerleşik fonksiyonudur.
# Bu, doğrudan nokta (.) operatörü ile yapılan atamalara eşdeğerdir fakat dinamik senaryolarda tercih edilir.

# 💬 Kullanım Amacı:
# - Özellikle attribute adı değişken olarak elde ediliyorsa (`attr_name = "isim"`)
# - Reflection, meta-programlama, config parser, json->obj gibi durumlarda

# 🧠 Sözdizimi:
# setattr(obj, attr: str, value: Any)
# obj    → attribute'u atanacak nesne
# attr   → string olarak attribute ismi
# value  → atanacak değer

# ⚙️ İç Mekanizma:
# obj.__setattr__(attr, value) fonksiyonu çağrılır.
# Eğer sınıf `__setattr__()` override etmişse bu fonksiyon çağrılır, aksi halde varsayılan mekanizma devrededir.

# 🧪 Çalışma Adımları:
# 1. Python, doğrudan `obj.__setattr__(attr, value)` çağrısı yapar.
# 2. Eğer `__setattr__()` override edilmişse özel davranış çalışır.
# 3. Aksi halde, `obj.__dict__[attr] = value` şeklinde attribute eklenir/güncellenir.

# 🆚 __setattr__ ile Farkı:
# - setattr() dışarıdan çağrılır, objeyi ve ismi sen verirsin
# - __setattr__ objenin iç davranışıdır, setattr() tarafından tetiklenir
# - __setattr__ override edilerek, setattr() çağrılarına özel davranışlar kazandırılır

# 🔍 Örnek:
class A:
    def __setattr__(self, name, value):
        print(f"Setting {name} to {value}")
        super().__setattr__(name, value)

a = A()
setattr(a, "x", 42)  # Output: Setting x to 42
print(a.x)           # 42



# delattr() fonksiyonu, verilen bir nesne üzerindeki attribute'u silmek için kullanılan Python yerleşik fonksiyonudur.
# Noktalı sözdizimiyle `del obj.attr` ifadesine eşdeğerdir, ancak dinamik hale getirir.

# 💬 Kullanım Amacı:
# - Attribute silme işlemlerinde attribute adı dinamik olarak belirleniyorsa
# - Meta-programlama, temizlik işlemleri, attribute reset işlemleri

# 🧠 Sözdizimi:
# delattr(obj, attr: str)
# obj    → attribute'u silinecek nesne
# attr   → silinecek attribute'un adı (string)

# ⚙️ İç Mekanizma:
# Python, `obj.__delattr__(attr)` metodunu çağırır
# Eğer sınıf `__delattr__()` metodunu override etmişse, o çalışır
# Aksi takdirde varsayılan olarak `del obj.__dict__[attr]` yapılır

# 🆚 __delattr__ ile Farkı:
# - delattr(): dış fonksiyondur → objeyi ve ismi sen verirsin
# - __delattr__(): objenin iç mantığıdır, override edilerek silme kontrolü özelleştirilebilir
# - delattr(obj, "x") çağrısı → obj.__delattr__("x") demektir

# 🔍 Örnek:
class B:
    def __init__(self):
        self.x = 123
    def __delattr__(self, name):
        print(f"Deleting {name}")
        super().__delattr__(name)

b = B()
delattr(b, "x")  # Output: Deleting x



# -------------------------------------
# 🔍 __dir__() Dunder (Special) Method
# -------------------------------------

# ✔️ Tanım:
# __dir__() metodu, bir nesne için `dir(obj)` fonksiyonu çağrıldığında otomatik olarak devreye giren özel bir dunder metottur.
# Bu metodun görevi, kullanıcıya veya geliştiriciye nesnenin sahip olduğu attribute’ları (özellikler + metodlar) listelemektir.

# Python’da varsayılan olarak:
# - obj.__dict__ → örneğe ait attribute’lar
# - obj.__class__ ve onun MRO zinciri → sınıf ve üst sınıflardaki attribute’lar
# - bazı dahili özellikler (__class__, __init__, vs.)
# bunların tümü `dir()` fonksiyonu tarafından topluca döndürülür.

# Ancak `__dir__()` metodu override edilirse, bu davranış tamamen kontrol altına alınabilir.

# -------------------------------------
# 🎯 Kullanım Amaçları:
# -------------------------------------

# 1. ❗ Özelleştirilmiş dir çıktısı:
#    Kullanıcının sadece belirli attribute’ları görmesini isteyebilirsin (örneğin: sadece public olanlar).

# 2. 🔍 Dinamik yapı:
#    __getattr__ ile dinamik attribute üretimi varsa, bu özellikleri `dir()` çıktısına eklemek faydalı olabilir.

# 3. 💼 Dokümantasyon kolaylığı:
#    Geliştiricilere daha anlamlı bir attribute listesi sunabilirsin.

# -------------------------------------
# 📌 __dir__() vs __dict__:
# -------------------------------------

# - __dict__: sadece örnek üzerinde tanımlı attribute’ları içerir (bir sözlük olarak).
# - __dir__: hem örnek hem sınıf (ve MRO) dahil olmak üzere geniş bir görünüm sunar (bir liste döner).
# - __dir__() metodu özelleştirilebilir; __dict__ özelleştirilemez (read-only proxy olabilir).

# -------------------------------------
# 💡 Örnek:
# -------------------------------------
# class Terminator:
#     def __dir__(self):
#         return ["model", "year", "destroy()"]

# t = Terminator()
# dir(t) # → ['model', 'year', 'destroy()']

# -------------------------------------
# 🧪 Sözdizimi:
# -------------------------------------

# def __dir__(self) -> list:
#     return ["özellik1", "özellik2", ...]

# Geri dönüş mutlaka **liste** olmalı (aksi takdirde TypeError alınır).



# 🔗 GÜNCELLENMİŞ __dir__() Çağrı Zinciri (Detaylı)

# 1) dir(obj) çağrıldığında Python, objenin __dir__ attribute’una erişmek ister.
#    Bu bir attribute erişimi olduğundan önce __getattribute__ metodu çalışır:
#    → type(obj).__getattribute__(obj, '__dir__')

# 2) __getattribute__ metodu çalışır → attribute'lar aşağıdaki sırayla aranır(temel işlem sırası):
#    → obj.__class__.__dict__['__dir__'] varsa alınır (objenin kendisine bakılmaz çünkü __dir__, special method attribute'dur)
#    → yoksa MRO zincirinde aranır
#    → descriptor ise: __get__ metodu çağrılır ve bound method elde edilir çünkü __dir__ bir method'dur 

# 3) Elde edilen bound method çağrılır:
#    → obj.__dir__() (burdaki __dir__() metodu descriptor'ı değil obje bağlı olan gerçek __dir__() metodudur))

# 4) __dir__ override edilmişse → senin tanımladığın liste döner
#    override edilmemişse → varsayılan dir mantığı uygulanır:
#    - obj.__dict__.keys()                 → örneğe ait attribute’lar
#    - obj.__class__.__dict__.keys()       → sınıfa ait attribute’lar
#    - MRO zincirindeki sınıfların __dict__’i
#    - Dahili attribute’lar (__class__, __doc__, __init__, vs.)

# 📝 Not:
# Eğer override edilmiş __dir__ metodu yoksa veya descriptor değilse,
# Python yine de type(obj).__dir__(obj) yoluyla varsayılan çıktıyı oluşturur.
# Aynı zamanda __dir__() metodu, hem type hem de object sınıfında bulunur bu sayede varsayılan __dir__ davranışı sergilenebilir
#  bu davranış bu sınıflarda bulunan: __dir__ metodunda yapılır


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

# 4) dir() ile hiç bilmediğin bir objeyi keşfedebilirsin burda getattr() fonksiyonundan yardım alabilrsin


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



# __slots__ özelliği:

# Python'da sınıf örnekleri (instance), attribute'larını dinamik olarak saklamak için bir sözlük kullanır → __dict__.

# Bu esneklik sayesinde her örneğe istediğimiz sayıda ve isimde attribute atayabiliriz. Ancak:
# → Bu sözlük (dict) yapısı hafıza açısından pahalıdır.
# → Özellikle çok sayıda örnek oluşturulan sınıflarda, bellek tüketimi artar.

# __slots__ özelliği bu problemi çözmek için vardır.

# Tanım:
# __slots__, sınıf seviyesinde tanımlanan özel bir attribute'dur.
# Bu yapı, sınıfın örneklerinin hangi attribute'lara sahip olacağını sınırlı tutar. bunu tuple kullanarak yapar.
# Böylece Python, __dict__ oluşturmadan, sabit hafıza blokları üzerinden çalışır (daha hızlı ve daha az yer kaplar).

# Yani __slots__:
# → Sınıf örneğinin attribute'larını liste/tampon gibi sabit yapılarla saklamasına neden olur.
# → __dict__ devre dışı kalır (eğer elle tekrar eklenmemişse). ama sınıfın kendisinde __dict__ attribute'u hala bulunur.
# → Dinamik attribute eklemeyi engeller.

# Örnek:
class Kişi:
    __slots__ = ("ad", "yaş")  # sadece bu iki attribute izinlidir

    def __init__(self, ad, yaş):
        self.ad = ad
        self.yaş = yaş

print(f" Kişi özellikleri: {Kisi.__dict__}")
# k = Kişi("Ali", 30)
# k.soyad = "Kara"  # AttributeError: 'Kişi' object has no attribute 'soyad'

# Avantajları:
# 1) Bellek tüketimini azaltır (özellikle çok sayıda örnekte).
# 2) Dinamik attribute eklenmesini engeller → hata önleme & performans.
# 3) __dict__ ve __weakref__ gibi attribute'ları istemiyorsak kontrol sağlar.

# Dezavantajları:
# - Esneklik kaybı: Dinamik attribute atayamazsın.
# - Karmaşık çoklu miras yapılarında dikkatli kullanılmalı.
# - Varsayılan olarak __dict__ yoktur (eğer özellikle eklenmemişse).

# Not:
# __slots__ = ("ad", "yaş", "__dict__")  # Eklenirse dinamik özellikler de atanabilir.
# Bu durumda __slots__ kullanmana rağmen __dict__'in geri geldiğini unutma.
# Bu yapı genelde kademeli geçiş için veya özel durumlar için kullanılır.
# bu yapıda bulunan "ad" ve "yaş", bellekte daha az yer kaplar 

# Ek olarak:
# - __slots__ bir tuple ya da iterable olmalıdır. ve bu sınıf immutable olmalıdır 
# - Tanımlanan her isim, bir string olmalı.
# - Tanım sınıf düzeyinde yapılır, örnekler düzeyinde __slots__ tanımlanmaz.

# Bellek yönetimi:
# __slots__ ile tanımlanan attribute'lar Python'ın düşük seviyeli (C yapısında) yapılarla tutulur.
# __dict__'teki gibi isim-değer eşlemesi yoktur.
# Bu da hem RAM kullanımını hem de erişim hızını düşürür.

# delattr:
# __slots__ ile tanımlı bir attribute, delattr(obj, 'ad') ile silinebilir.
# Ancak silindikten sonra tekrar aynı attribute atanmadıkça erişim hatası alınır.

# __setitem__, __delitem__ gibi mapping methodlarıyla ilgisi yoktur.

# __getattribute__ yine çalışır, çünkü tüm attribute erişimleri bu metodla başlar.

# Kısaca:
# __slots__ → bellek verimliliği + davranış kısıtlaması sağlar.
# Ancak gelişmiş esneklik ve dinamiklik gerekiyorsa __dict__ içeren sınıflar daha uygund



# ============================================
# 📌 __slots__ ve __dict__ FARKI

# __dict__ → dinamik, esnek, büyük bellek tüketir, her attribute burada tutulur
# __slots__ → sabit, kısıtlı, daha az bellek kullanır, hızlı erişim sağlar

# NOT: __slots__ kullanıldığında __dict__ tamamen yok edilmez;
# eğer __dict__'i manuel olarak eklersen __slots__ + __dict__ birlikte kullanılabilir:
#     __slots__ = ('ad', '__dict__')  → bu sayede hem sabit hem dinamik yapı olur

# ============================================
# 🔍 METOD ÇÖZÜMLEMESİ

# __slots__ bir metod değildir → sınıf attribute'udur (tuple/list olur)
# Bu nedenle bir çağırma işlemi içermez. Ama attribute erişimidir.

# Örneğin: Ogrenci.__slots__
#    → type(Ogrenci).__getattribute__(Ogrenci, '__slots__')

# Python bu erişimde __getattribute__ metodunu kullanır.
#    → descriptor çözümlemesi yoktur çünkü __slots__ non-descriptor bir attribute'dur.

# ============================================
# 🔸 KISITLAR:

# 1) __slots__ sadece new-style class'larda çalışır → yani object'ten türeyen sınıflar
# 2) Miras yapısında dikkatli kullanılmalı:
#    → Alt sınıfta yeni __slots__ tanımlanırsa, üst sınıftakiler dahil edilmelidir.
# 3) Pickle gibi bazı işlemlerle uyumsuzluk yaşanabilir (örnekler serialize edilemeyebilir)

#
class Terminator:
    __slots__ = ("model","year") # burda sadece model ve year attribute'ları tanımlandı
    # __slots__ kullanıldığı için __dict__ attribute'u kaldırıldı

    def __init__(self):
        self.model = "T-800"
        self.year = 1984


t1 = Terminator()        

print(t1.model)  # T-800
print(t1.year)   # 1984

try:
    t1.serial_number = "12345"  # Hata: 'Terminator' object has no attribute 'serial_number'
except AttributeError as e:
    print(e)    

try:
    print(t1.__dict__)  # Hata: 'Terminator' object has no attribute '__dict__'
except AttributeError as e:
    print(e)

print(t1.__slots__) # ('model', 'year') → __slots__ attribute'u burada görünüyor


del t1.model  # Bu çalışır çünkü model __slots__ içinde tanımlı

print(t1.__slots__) # ('model', 'year') çünkü delattr,sadece slot'da tanımlı olan attribute'un değerini siler
# ama __slots__, sınıf düzeyinde hangi isimlerin kullanılacağını gösterir yani isimler(slot tanımları) silinmez sadece örnekteki değeri siler


class Terminator:
    __slots__ = ("model","year","__dict__") # burda sadece model ve year attribute'ları tanımlandı
    # __slots__ kullanıldığı için __dict__ attribute'u kaldırıldı

    def __init__(self):
        self.model = "T-800"
        self.year = 1984


t1 = Terminator()        

print(t1.__dict__)


