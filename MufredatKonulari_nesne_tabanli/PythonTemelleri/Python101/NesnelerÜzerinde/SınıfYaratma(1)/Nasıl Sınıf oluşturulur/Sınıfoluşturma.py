# 📦 Class (Sınıf) Kavramı

# Python'da class (sınıf); veri (attribute) ve bu veriye ait davranışları (method) aynı yapı altında tanımlamak için kullanılır.
# Sınıf, nesne yönelimli programlamanın (OOP) temel taşıdır ve gerçek dünyadaki nesneleri yazılımda temsil etmeyi sağlar.**Bilginin zihinsel yapısını, doğrudan koda aktarma yoludur.**

# ✅ Sınıfın Amacı:
# - Aynı türden, ortak özellik ve davranışlara sahip nesneleri tanımlamak.
# - Kodun yeniden kullanılabilirliğini, organizasyonunu ve ölçeklenebilirliğini artırmak.

# 🔍 Neden sınıf kullanırız?

# 1) **Karmaşık yapıları yönetmek için:**
#    Gerçek dünyadaki problemler çoğu zaman karmaşıktır. 
#    Sınıflar bu karmaşıklığı; parçalara ayırarak nesneler üzerinden daha yönetilebilir hale getirir.

# 2) **Kod tekrarını azaltmak için:**
#    Benzer yapıya sahip ama farklı verilere sahip nesneler için kodu her seferinde tekrar yazmak yerine;
#    bir sınıf tanımlanır ve ondan örnek (instance) alınarak esnek kullanım sağlanır.

# 3) **Anlamlı bir yapı ve organizasyon için:**
#    Veriler (attributes) ve işlemler (methods) aynı yerde toplandığı için kod;
#    daha düzenli, okunabilir ve hataya daha kapalı hale gelir.

# 4) **Genişletilebilir ve sürdürülebilir sistemler kurmak için:**
#    Sınıflar, kalıtım (inheritance) sayesinde başka sınıflardan özellik ve davranış alabilir.
#    Bu sayede yazılım daha modüler ve esnek olur.

# ⚙️ Teknik olarak:
# - Bir sınıftan nesne üretildiğinde Python sırasıyla:
#   → __new__() metodu ile bellekte bir nesne oluşturur,
#   → ardından __init__() metodu ile bu nesneyi başlatır (initialize eder).

# 🧾 Sınıf Tanımı (Sözdizimi):

class ClassName:
    def __init__(self):
        pass  # Nesne örneği oluşturulduğunda çalışacak yapılandırıcı metot

"""
🔹 class:
    - Python'da kullanıcı tanımlı veri tipleri (şablonlar) oluşturmak için kullanılır.
    - class = şablon üretici. İçinde tanımlanan methodlar ve attribute'lar ile bir nesnenin davranışı ve verisi tanımlanır.

🔹 ClassName:
    - Bu class'ın adı ve aynı zamanda veri tipi (type).
    - ClassName() şeklinde çağrıldığında yeni bir örnek (instance) oluşturulur.
    
    
🔹 def __init__(self):
    - __init__ özel bir methoddur; sınıftan bir nesne üretildiğinde otomatik olarak çalışır.
    - Genellikle nesneye ait ilk verileri başlatmak (initialize etmek) için kullanılır.
    - __init__ methodu varsayılan olarak Python'da object sınıfından miras alınır ve override edilebilir.

🔹 self:
    🧠 Nihai Tanım (ileri seviye):
        - self, bir instance method'a hangi nesne (örnek) üzerinden erişildiyse onu temsil eden referanstır.
        - Bu referans, methodun "hangi nesneye ait olduğunu" bilir ve o nesnenin attribute’larına doğrudan erişim sağlar.
        - Yani self, dinamik bağlamda "çalışma zamanında" örnek çözümlenmesini (instance binding) mümkün kılar.
        - Her instance method'un ilk parametresi self olmalıdır çünkü bu sayede method örnek odaklı davranabilir.
        - Python'da class-level ve instance-level veri ayrımını sağlayan temel anahtardır.

    ✅ self sayesinde:
        - Her nesne kendi verisini taşır (`self.name`, `self.id`, `self.settings`)
        - Aynı class’tan oluşturulan iki nesne birbirinden bağımsız çalışır.
        - Nesne tabanlı programlamanın (OOP) temelini oluşturur.

    📌 Kısaca:
        - self = methoda erişen "örnek"
        - self.__class__ = bu örneğin bağlı olduğu sınıf
        - self.__dict__ = örneğe ait veriler (özelleştirilmiş alanlar)

🔥 Örnek:
class User:
    def __init__(self, name):
        self.name = name  # self sayesinde örneğe veri bağlanır

u = User("Demir")
print(u.name)         # Demir
print(u.__class__)    # <class '__main__.User'>
"""


# 🔸 CLASS BODY (Sınıf Gövdesi)

# Python'da 'class' anahtar kelimesi ile tanımlanan her sınıf, kendi özel blok yapısı (scope) içinde tanımlanır.
# Bu blok — yani sınıf gövdesi (class body) — sınıf tanımlandığı anda bir kez çalıştırılır.

# Sınıf gövdesi, içinde yer alan tüm ifadeleri sırayla çalıştırır ve bu sırada tanımlanan:
# - isimler
# - metotlar
# - değişkenler
# bir geçici sözlük (namespace) içinde tutulur. Bu sözlük, sınıfa ait tüm attribute'ları içerir.

# ✅ Bu geçici sözlük, teknik olarak "class locals" olarak adlandırılır ve bir frame (yürütme bağlamı) üzerinde oluşturulur.
# Bu frame, 'locals()' sözlüğüne benzer şekilde çalışır ancak sınıfa özeldir.

# 🔧 Sınıf gövdesindeki tüm bu içerik (isimler, metotlar, değişkenler...) toplandıktan sonra:
# Python bu sözlüğü, 'type' metasıınıfı kullanarak bir sınıf nesnesine dönüştürür:
#
#   class_obj = type(class_name, bases, class_namespace)
#
# Yani Python, aslında her sınıfı arka planda `type()` çağrısıyla dinamik olarak üretir.

# 📌 Sonuç olarak: bir sınıf tanımı yapıldığında,
#   1. Yeni bir scope (sözlük) oluşturulur.
#   2. Bu scope içindeki her şey çalıştırılır ve sözlüğe eklenir.
#   3. 'type' kullanılarak bir sınıf nesnesi oluşturulur.
#   4. Oluşan sınıf, global namespace'e atanır (örneğin: MyClass = type(...)).

# 🧠 Ekstra bilgi: Bu mekanizma, Python'da metaclass, descriptor, __new__, __init_subclass__ gibi ileri özelliklerin temelini oluşturur.


class Araba:
    x = 10
    def run(self):
        ...
# 1) geçici bir local sözlük oluşturulcak
local = {} # temsili

# 2) bu local sözlüğün içine sınıfta tanımlı olan tüm arribute'lar eklencek
local["x"] = 10
local["run"] = lambda self:...

# 3) local sözlüğü, type fonksiyonu ile bir sınıf nesnesine çevrilcek
Araba_ = type("Araba_",(),local)

# 4) Araba_ adını global scope'a ekler


# Sınıf gövdesinde tanımlı herşey "sınıf tanımında " çalıştırılır mesela;

class Z:
    print("class Z tanımlandı")
# class Z tanımlandı -> ÇALIŞTI
# burda sınıfı, çağırmana gerek yoktu sınıf gövdesinde tanımlı olan nenseler,sınıf tanımlamada bir kez  çalıştırılır




# 🔹 __init__ metodu nedir?

# Python'da __init__ metodu, bir sınıftan nesne (object) oluşturulduğunda
# otomatik olarak çağrılan "başlatıcı" (initializer) metottur.
# Nesne bellekte oluşturulduktan hemen sonra çalışır ve o nesneye ait
# başlangıç verilerini (attribute'ları) tanımlamak için kullanılır.

# Söz dizimi:
# class SınıfAdı:
#     def __init__(self, parametreler):
#         self.özellik = değer

# NOT: __init__ metodu bir constructor (yapıcı) değildir.
# Asıl yapıcı metot __new__'dur. __init__, sadece nesne belleğe alındıktan
# sonra çalışır ve o nesneye ilk değer atamalarını yapar.

# Örnek:
class Kullanici:
    def __init__(self, ad, yas):
        self.ad = ad
        self.yas = yas

# kullanici = Kullanici("Ali", 30)
# Yukarıdaki ifade şunları yapar:
# 1. Python önce __new__ metodunu çağırır → bellekte yeni bir boş nesne oluşturur
# 2. Sonra __init__ ile bu nesneyi başlatır → ad ve yas verisi atanır

# 🔍 Peki neden biz __new__ metodunu genelde görmeyiz?

# Çünkü __new__ metodu, nesne oluşturmanın çok daha düşük seviyeli bir aşamasıdır.
# Genellikle immutable (değiştirilemez) türlerle çalışırken özelleştirilir (örneğin: tuple, str).
# Python sınıf söz diziminde __new__ yerine __init__ yazılır çünkü:
# → Geliştiriciye nesnenin "inşası" değil, "başlangıç verisi" ilgilidir.

# Python'daki varsayılan class davranışı, __new__ metodunu örtülü (implicit) olarak çağırır.
# Yani sınıf tanımında yazmasan bile aslında __new__ önce çağrılır, ardından __init__.

# 🔸 __init__ vs __new__ farkı:

# __new__(cls, ...) → sınıf örneğini yaratır → static method gibi çalışır
# __init__(self, ...) → oluşturulan örneği başlatır → instance method'dur

# İleri düzey kullanımda __new__ şunun gibi tanımlanabilir:
# def __new__(cls, ...):
#     örnek = super().__new__(cls)
#     return örnek

# Ama %99 kullanımda sadece __init__ yeterlidir çünkü çoğu zaman sadece
# nesneye veri atamak isteriz, yaratma sürecine müdahale etmeyiz.


# Örnek 1;

class A:
    def __init__(self):
        self.isim = "d"
        # burda "d" değeri,self yani a ismine bağlanır ve saklanır
        # aynı zamanda hiçbir parametre tanımlamadık dolasıyla hiçbir veri almadan,hard-coded yaparak nesneye,"d" adını otomatik verdik
        # bu durumda kullanıcının A() çağrı işleminde herangi bir parametre vermesine gerek kalmaz ama bu sınıftan oluşturulan tüm nesneler;
        # hepsinin isim değeri, "d" olur

a = A()
print(a.isim) # a

# Örnek 2;

class B:
    def __init__(self,nesne):
        self.nesne = "B"
        # burda nesne adında bir pozisyonel bazlı sabit isim tanımladık, bu durumda B() sınıf çağrısında
        # kullanıcının nesne parametesine,argüman vermesini zorunlu kıldık self ile de nesne parametresini, nesneye ait hâle getirdik

b = B("b") # B(),bizden bir tane zorunlu parametre'ye argüman istiyor bu nedenle değer verdik
print(b.nesne) # B

# örnek 3;

class Öğrenci:
    def __init__(self,ad,yaş,okul):
        self.ad = ad
        self.yaş = yaş
        self.okul = okul

ogrenci1 = Öğrenci("demir",20,"AÜ")

print(", ".join(f"{getattr(ogrenci1,name)}" for name in ogrenci1.__dir__() if not name.startswith("__") ))
# demir, 20, AÜ

