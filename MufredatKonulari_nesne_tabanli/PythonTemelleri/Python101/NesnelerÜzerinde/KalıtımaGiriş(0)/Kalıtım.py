# Kalıtım
""""""
# kalıtım: bir sınıf nesnesi,başka bir sınıf nesnesinin __bases__ üzerinden referans olarak onun davranışlarını mro miras zinciri ile devraldığı bir yapıdır
# Kalıtım sayesinde bir sınıf,başka bir sınıfın davranışlarını devralabilir ve oluşturulan objeler,MRO zinciri yoluyla atalarına çıkarak davranışlarını çözümleyebilir



"""🔸 Örnekleme (instantiation), sınıflardan nesne oluşturma işlemidir.  
    Bu işlem, herhangi bir kalıtımsal yapı gerektirmeden çalışır — yani sınıfın davranışı, doğrudan sınıf tanımıyla ve type sınıfıyla ilgilidir.

🔸 Python'da tüm sınıfların oluşturulma süreci, attribute ekleme, silme, erişim gibi davranışları `type` sınıfı tarafından belirlenir.  
    Çünkü Python'da **tüm sınıflar**, `type` sınıfının örnekleridir.

🔸 Bu durum `type`'ı özel bir sınıf haline getirir → bu tür sınıflara **metaclass** denir.  
    Metaclass, sınıfların nasıl **oluşturulacağını** ve nasıl **davranacağını** tanımlar.

🔸 Miras (inheritance) ise sınıflar arasında **kodu paylaşmak ve davranış aktarmak** için kullanılır.  
    Bir sınıf başka bir sınıftan miras aldığında, onun attribute ve metotlarına erişebilir — bu da kalıtımsal donanım sağlar.

🔸 Python’daki tüm sınıfların **en temel atası `object` sınıfıdır**.  
    Çünkü tüm sınıflar doğrudan veya dolaylı olarak `object`’ten miras alır.  
    Bu yüzden tüm sınıflar, `object`’in davranışlarını taşır (örneğin: `__str__`, `__eq__`, `__class__`, vb).
    
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



# 🔹 __base__ attribute'u:
# ---------------------------------------------
# __base__, bir sınıfın doğrudan miras aldığı **ilk** sınıfı verir.
# Yani sınıfın MRO (Method Resolution Order) zincirinde, kendisinden hemen sonraki sınıfı gösterir.
# Bu attribute bir sınıfa aittir (örneğe değil).
# ---------------------------------------------
# 🔹 __bases__ ile farkı:
# - __bases__ bir tuple’dır ve sınıfın miras aldığı tüm sınıfları içerir (birden fazla olabilir).
# - __base__ ise sadece bu tuple’ın ilk elemanıdır. Yani: cls.__base__ == cls.__bases__[0]

# Örnek:
class A: pass
class B(A): pass

print(B.__bases__)  # (<class '__main__.A'>,) → tüm üst sınıflar (tuple)
print(B.__base__)   # <class '__main__.A'>    → sadece ilk üst sınıf

# ---------------------------------------------
# 🔹 Attribute çözümleme zinciri:
# B.__base__ → bir attribute erişimidir → bu zincirle çözülür:

# 1. Python, bunun attribute olduğunu anlar:
#    → type(B).__getattribute__(B, '__base__')

# 2. Sıra MRO zincirine göre type sınıfının __dict__’inde aranır sınıfın kendisine bakılmaz çünkü __base__,special method'dur doğrudan ait olduğu sınıftan arama başlanır:
#    → type.__dict__['__base__'] → bu bir descriptor’dur

# 3. Eğer bu nesne descriptor ise:
#    → descriptor.__get__(B, type(B)) çağrılır

# 4. Sonuçta B.__base__ → <class '__main__.A'> döner

# ---------------------------------------------
# NOT:
# - __base__ sadece sınıf nesneleri için geçerlidir. Örnekler bu attribute’a sahip değildir.
# - Eğer çoklu kalıtım kullanılmışsa (örneğin class C(A, B)), __base__ yalnızca A'yı verir.
#   Diğer tüm miras sınıfları __bases__ ile erişilebilir.




# __bases__: Bir sınıfın **doğrudan miras aldığı** sınıfları gösteren bir tuple’dır.
#           Bu bir metod değil, bir attribute’tur.

# 📌 "Doğrudan" kelimesi şunu ifade eder:
#     → Sınıf tanımında parantez içinde yazılmış sınıflardır.
#     → Örneğin: class B(A): ...  → burada A, B'nin doğrudan base sınıfıdır.

# 🔁 Dolaylı miraslar burada yer almaz:
#     → Tüm sınıflar object'ten miras alsa da,
#       eğer bu object sınıfı base olarak doğrudan belirtilmediyse __bases__ içinde görünmez.


# Örnek:
# class A: pass
# class B(A): pass
# B.__bases__ → (<class '__main__.A'>,)  ✅ sadece A var
# A.__bases__ → (<class 'object'>,)      ✅ çünkü A doğrudan object'ten türedi

# ⚙️ __bases__, sınıf tanımı anında (class bloğu işlendiğinde) Python tarafından
#     hemen (eager evaluation) oluşturulur ve type sistemi tarafından atanır.



# 🧠 A.__bases__ → Bu bir sınıf attribute'udur
#    Python bunu obj.attr gibi işler → bu da bir __getattribute__ çağrısıdır

# 1) Python attribute erişimini başlatır:
#    → type(A).__getattribute__(A, '__bases__') -> burda sınıfın kendisine bakılmaz çünkü __bases__, special attribute erişim işlemidir

# 2) __getattribute__ içinde, A'nın sınıfı (type) üzerinden __dict__ sözlüğüne bakılır:
#    → type.__dict__['__bases__'] bulunur

# 3) Bu bir descriptor’dur (getset_descriptor):
#    → <attribute '__bases__' of 'type' objects>

# 4) Python descriptor protokolünü çalıştırır:
#    → descriptor.__get__(A, type)

# 5) Geri dönen sonuç:
#    → A sınıfının bases tuple’ı döner → örneğin: (<class 'object'>,)

# ✅ Yani: A.__bases__ = descriptor.__get__(A, type) sonucudur

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




# 📌 __class__ attribute'u: 
#     Her Python nesnesinin ait olduğu sınıfı (type) gösteren özel bir attribute’tur.
#     Bu bir metod değil, attribute’tur → yani erişim `obj.__class__` ile yapılır.

# 💡 __class__, Python’un nesne modelinde "hangi sınıfın örneğisin?" sorusunun cevabıdır.
#     Örnek: type(a) == a.__class__

# 🔍 __class__ bir descriptor’dur (getset_descriptor) → __get__() protokolü ile çözülür
# ============================================================
# 🧍🏻 1. INSTANCE (Nesne) DÜZEYİNDE __class__ ÇÖZÜM ZİNCİRİ
# ============================================================

# obj.__class__ → attribute erişimidir → şu zincirle çözülür:

# 1) Python, bu erişimin attribute olduğunu fark eder:
#    → type(obj).__getattribute__(obj, '__class__')

# 2) __getattribute__ metodu çalışır ve objenin kendisine bakılmaz çünkü, __class__, special attribute'dur python burda özel bir erişim uygular objenin kendisini atlar
#    → obj.__class__.__dict__['__class__'] 

# 3) Bu attribute bir descriptor’dur → getset_descriptor
#    → Python: descriptor.__get__(obj, type(obj)) çağırır

# 4) Geri dönen sonuç: obj’nin ait olduğu sınıf (örneğin: <class '__main__.A'>)

# Örnek:
# class A: pass
# a = A()
# a.__class__  → <class '__main__.A'>

# ============================================================
# 🏗️ 2. CLASS (Sınıf) DÜZEYİNDE __class__ ÇÖZÜM ZİNCİRİ
# ============================================================

# A.__class__ → burada A bir sınıf olduğundan, çözüm zinciri metaclass'tan başlar:

# 1) Python:
#    → type(A).__getattribute__(A, '__class__') çağırır
#    (çünkü A bir sınıftır ve sınıfların sınıfı = type)

# 2) type.__dict__['__class__'] aranır → yine descriptor bulunur -> Sınıfın kendisine bakılmaz çünkü __class__, special attribute'dur 

# 3) Python: descriptor.__get__(A, type) çağırır

# 4) Geri dönen sonuç: A'nın metaclass'ı → <class 'type'>

# Örnek:
# class A: pass
# A.__class__ → <class 'type'>

# ============================================================
# ✅ SONUÇ

# ✔️ __class__ → attribute'tur, bir metod değildir
# ✔️ Çözüm zinciri her zaman __getattribute__ ile başlar
# ✔️ Ardından descriptor protokolü devreye girer (__get__)
# ✔️ Tüm nesnelerde __class__ bulunur
# ✔️ Nesneler için: sınıfını verir
# ✔️ Sınıflar için: metaclass'ı verir (genellikle type)

# Not: __class__ sayesinde hem örneklerin hem sınıfların "tip bilgisi" elde edilir

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




# 📌 __mro__ : "Method Resolution Order" (Metod Çözümleme Sırası) anlamına gelir.
#     Bu attribute, bir sınıfın metod/attribute ararken izleyeceği miras zincirini, sıralı biçimde içerir.

# 🔍 __mro__, bir attribute’tur (metod değildir) → ve bir tuple olarak döner.
#     Tuple içindeki her eleman → sınıfın kendisi ve atalarıdır (MRO sırasına göre).

# ⚙️ MRO zinciri, her zaman sınıfın kendisiyle başlar.
#     Python, bir attribute/metod erişiminde önce sınıfın kendisine bakar,
#     sonra sırasıyla miras aldığı sınıflara doğru çıkar.

# 🧠 Bu zincir, Python'un tüm attribute erişimlerinde kullanılır.
#     Özellikle dunder metodlar (__getattribute__, __setattr__, __call__ vb.)
#     bir sınıfta bulunmazsa, Python bu zincir boyunca yukarı çıkarak aramaya devam eder.

# 🎯 Bu sayede, sınıf kendisinde tanımlı olmayan metodları/özellikleri
#     base sınıflardan "miras alarak" kullanabilir.



# 🧠 type.__mro__ → Bu da bir attribute erişimidir

# 1) Python, attribute erişimini fark eder:
#    → type(type).__getattribute__(type, '__mro__')

# 2) __getattribute__, type sınıfının __dict__'ine bakar(attribute erişimlerinde __dict__ önemli rol oynar):
#    → type.__dict__['__mro__'] bulunur

# 3) Bu bir descriptor'dur (getset_descriptor)

# 4) Python descriptor protokolünü uygular:
#    → descriptor.__get__(type, type) çağrılır

# 5) Sonuç: type sınıfının MRO zinciri döner
#    → (<class 'type'>, <class 'object'>)

# ✅ __mro__, __getattribute__ zinciriyle çözülen özel bir sınıf attribute'udur
#    ve sınıf üzerinde tanımlıdır (örneğin: A.__mro__)

# Not:
# - __mro__ sadece sınıflarda vardır
# - obj.__mro__ ❌ hata verir çünkü örnekler MRO'ya sahip değildir

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
# isinstance fonksiyonu,belirtilen nesnenin ait olduğu sınıfta ve bu sınıfın miras aldığı ata sınıflarda verilen sınıf veya sınıfları arar

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