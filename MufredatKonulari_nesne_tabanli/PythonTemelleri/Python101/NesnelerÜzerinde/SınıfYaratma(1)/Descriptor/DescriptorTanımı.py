# 🔷 Descriptor: Python'da attribute (özellik) erişimini özelleştirmek için kullanılan bir protokoldür.
from jedi.inference.value import instance


# ➤ Descriptor bir sınıftır, ama her sınıf descriptor değildir.
#     En az bir tanesi tanımlanmışsa descriptor sayılır: __get__, __set__, __delete__

# ➤ Descriptor sınıfı, başka bir sınıfın class attribute’ü (sınıf niteliği) olarak tanımlanmalıdır.
#     Örneğin: class MyClass: field = MyDescriptor()
#   Instance methodlar'da tanımlanan descriptor() python tarafından çağrılmaz çünkü atttribute normal bir nesne olur
#   python,o nesne için descriptor protokolü uygulamaz bu nedenle de descriptor çağrılmaz

# ➤ Descriptor yalnızca sınıflara özgüdür.
#     Fonksiyonlar veya sıradan değişkenler descriptor olarak işlev göremez.

# ➤ Descriptor’ün amacı, bir sınıf örneğinin attribute’lerine erişim, yazma veya silme işlemlerini kontrol etmektir.
#     Bu sayede getter-setter yapısı, veri validasyonu, logging gibi özellikler entegre edilebilir.

# ➤ Descriptor, Python’un "attribute access" sistemine düşük seviyede müdahale etmemizi sağlar.
#     Yani nesne.attr → aslında nesne.__class__.__dict__["attr"].__get__(nesne, type(nesne)) gibi çalışır.

# ➤ Descriptor’ler, özellikle ORM, data modeling, validation, property yönetimi gibi alanlarda çok güçlüdür.

# 🔧 Kısaca descriptor:
#   - Kontrol (controlled access) sağlar
#   - Genellikle class attribute olarak tanımlanır
#   - __get__, __set__, __delete__ gibi metodlarla tanınır
#   - "Descriptor protokolü" dediğimiz bu kurallar ile attribute davranışı özelleştirilir


# 🔷 __get__(self, instance, owner)
# ➤  self → descriptor sınıfından tanımlanmış olan attribute nesnesidir.
#   descriptor sınıfının bir örneğini (instance) temsil eder.
# ➤ instance → descriptor'ın bağlı olduğu sınıfın örneği
# ➤ owner    → descriptor'ın tanımlı olduğu sınıfın kendisi
# ➤ Ne zaman çağrılır? → obj.attr şeklinde attribute erişimi yapıldığında
# ➤ Geriye genellikle veriyi (örneğin saklanan değeri) döndürür

# Kullanım senaryosu:
# - Okuma erişimini özelleştirmek
# - Lazy loading (tembel yükleme) gibi işlemler
# - Cache sistemleri, property-like davranışlar


# 🔷 __set__(self, instance, value)
# ➤ instance → descriptor'ın bağlı olduğu sınıfın örneği
# ➤ value    → kullanıcı tarafından obj.attr = value şeklinde atanan değer
# ➤ Ne zaman çağrılır? → obj.attr = value yazımı yapılınca
# ➤ Geriye bir şey döndürmez, direkt olarak içsel atama yapılır

# Kullanım senaryosu:
# - Veri doğrulama (validation)
# - Dönüşüm işlemleri (örneğin string’i int’e çevirme)
# - Otomatik loglama, değiştirme bildirimleri


# 🔷 __delete__(self, instance)
# ➤ instance → descriptor’ın tanımlı olduğu sınıfın örneği
# ➤ Ne zaman çağrılır? → del obj.attr yazıldığında
# ➤ Geriye bir şey döndürmez, ilgili attribute silinmiş gibi davranılır

# Kullanım senaryosu:
# - Özel silme mantıkları (örneğin dış dosyadan da veri silme)
# - Silme öncesi kontrol
# - Geriye dönülemeyen değişiklikler



# -------------------------------------
# Non-Data Descriptor NEDİR?
# -------------------------------------
# Sadece __get__ metodu tanımlanırsa, bu yapı NON-DATA DESCRIPTOR olur.
# Non-data descriptor'ların önceliği düşüktür:
# Eğer örnek sözlüğünde (instance.__dict__) aynı isimde bir alan varsa, descriptor devre dışı kalır.
#   Non-data descriptor’ların önceliği düşüktür çünkü Python, kullanıcıya daha yüksek esneklik ve override hakkı tanımak ister.
#   Bu sayede descriptor sistemini zorunlu kılmak yerine(Nondata Descriptor), ihtiyaç olduğunda devreye giren bir sistem olarak konumlandırır.

class OnlyGetDescriptor:
    def __get__(self, instance, owner):
        return "Descriptor'dan gelen"

class Example:
    x = OnlyGetDescriptor()  # descriptor, sınıf attribute'u olarak atanıyor

e = Example()
e.__dict__["x"] = "Instance'dan gelen"  # örnek sözlüğüne aynı isimle değer verildi

print(e.x)  # Non-data descriptor devre dışı → "Instance'dan gelen" yazılır
print(e.__class__.__dict__["x"].__get__(e,e.__class__)) # bu non-data descriptorlerin neden ihtiyaç halinde
# devreye giren bir sistem olduğunu gösterir bu bize, yüksek esneklik,düşük seviye erişim ve override hakkı tanır

# -------------------------
# DESCRIPTOR YAPISI - ÖRNEK
# -------------------------

class UpperCaseDescriptor:
    """
    DATA DESCRIPTOR örneği.
    __get__ ve __set__ metodları tanımlandığı için veri yazma ve okuma işlemlerini kontrol eder.
    """
    def __get__(self, instance, owner):
        # instance → descriptor'ü barındıran sınıfın örneği (örn: Person)
        # owner    → descriptor'ü barındıran sınıfın kendisi (örn: <class 'Person'>)
        return instance.__dict__.get("name", "")

    def __set__(self, instance, value):
        # Değer yazılmadan önce işlem yapılabilir (örneğin uppercase)
        instance.__dict__["name"] = value.upper()

# --------------------------
# Descriptor'ün Kullanımı
# --------------------------
class Person:
    name = UpperCaseDescriptor()  # descriptor sınıfa attribute olarak atanıyor

# descriptor'ün sihirli şekilde çalışması için:
# => descriptor mutlaka BİR SINIFIN ATTRIBUTE'U olarak tanımlanmalı
# Aksi takdirde, descriptor protokolü (get, set) otomatik tetiklenmez.

p = Person()
p.name = "ahmet"     # __set__ → "AHMET" olarak kaydedilir
print(p.name)        # __get__ → "AHMET" okunur

# --------------------------
# SONUÇLAR:
# --------------------------
# 1. Descriptor'ler sadece sınıf attribute'u olarak tanımlandığında işler.
# 2. __get__ varsa: Non-data descriptor (düşük öncelik)
# 3. __get__ + __set__/__delete__ varsa: Data descriptor (yüksek öncelik)
# 4. Data descriptor, örnek sözlüğü override edemez.

# ─────────────────────────────────────────────────────────────
# DESCRIPTOR MEKANİZMASININ ADIM ADIM ÇALIŞMASI 🔍
# ─────────────────────────────────────────────────────────────

class OnlyInt:
    def __get__(self, instance, owner):
        print("📥 __get__ çağrıldı")
        return instance.__dict__.get('x')

    def __set__(self, instance, value):
        print("📤 __set__ çağrıldı")
        if not isinstance(value, int):
            raise ValueError("Sadece int değer atanabilir.")
        instance.__dict__['x'] = value


# Bu sınıfta descriptor olan `OnlyInt`'i kullanıyoruz
class A:
    x = OnlyInt()  # Descriptor nesnesi, sınıf attribute'ü olarak tanımlanır


# Bir örnek oluşturuyoruz
a = A()

# Şimdi `a.x` çağrıldığında ne olur?

# 🧠 a.x → bu bir attribute erişimidir

# 🧩 Python bu işlemi çözümlerken şu sırayla çalışır:

# 1️⃣ type(a).__getattribute__(a, "x") çağrılır
#     ➤ Çünkü bu, özel bir attribute erişimidir (__getattribute__)

# 3️⃣ "x" sınıfın sözlüğünde tanımlı mı?
#     ➤ Evet, "x" = OnlyInt() gibi bir descriptor nesnesi

# 4️⃣ Descriptor kontrolü:
#     ➤ Eğer `__get__` ve `__set__` varsa → **Data Descriptor**
#     ➤ Sadece `__get__` varsa → Non-Data Descriptor

# 5️⃣ Eğer data descriptor'sa, örnek sözlüğüne (`a.__dict__`) **bakmadan** doğrudan descriptor'ın `__get__()` metodu çağrılır

# 6️⃣ Dolayısıyla: `OnlyInt.__get__(self=descriptor_obj, instance=a, owner=A)` çağrısı yapılır
#     ➤ "self" → descriptor nesnesinin kendisi (örneğin OnlyInt())
#     ➤ "instance" → descriptor'ın bağlı olduğu sınıfın örneği (a)
#     ➤ "owner" → descriptor'ın tanımlı olduğu sınıf (A)

# 🟢 SONUÇ:
# ➤ Eğer attribute bir data descriptor ise (yani hem __get__ hem __set__ varsa),
#     örneğin sözlüğündeki aynı isimde bir değer **yok sayılır**.
#     Python mutlaka sınıfın sözlüğünden descriptor'ı bulur ve __get__() çalıştırır.

print(a.x)  # output: 📥 __get__ çağrıldı → 10


# ✨ Descriptor ile tek bir attribute için kontrol uygulanabilir:
class OnlyInt:
    def __set__(self, instance, value):
        # 🔐 Sadece 'x' attribute'u kontrol ediliyor
        if not isinstance(value, int):
            raise TypeError("Sadece integer değer verilebilir!")
        instance.__dict__['x'] = value

    def __get__(self, instance, owner):
        return instance.__dict__.get('x', None)

class A:
    # 🔧 x özelliği, descriptor tarafından kontrol ediliyor
    x = OnlyInt()

a = A()
a.x = 10       # ✔️ Çalışır
# a.x = "text"  # ❌ TypeError

# ------------------------------------------------------------

# 🚨 __setattr__ kullanarak da benzer kontrol yapılabilir:
class B:
    def __setattr__(self, name, value):
        # ❗ Bu kontrol tüm attribute'lar için geçerli!
        if name == "x" and not isinstance(value, int):
            raise TypeError("x için sadece integer değer verilebilir.")
        # ⛏️ Diğer attributeları engellemeden ayarlamak için:
        super().__setattr__(name, value)

b = B()
b.x = 20        # ✔️ Çalışır
# b.x = "text"  # ❌ TypeError

# ------------------------------------------------------------

# 📌 Yorumlar:

# 1️⃣ Descriptor → sadece belirli bir attribute'ü kontrol eder (örnek: x)
# 2️⃣ __setattr__ → sınıftaki tüm attribute'lara müdahale eder
#    Bu, karmaşık ve hataya açık olabilir.
# 3️⃣ Descriptor'ler modülerdir → farklı sınıflarda tekrar tekrar kullanılabilir
# 4️⃣ Descriptor → Django, SQLAlchemy gibi framework'lerin temel taşıdır
# 5️⃣ __setattr__ daha "genel" ama "dağınık", descriptor daha "özgül" ve "temiz"




class MyDescriptor:
    def __get__(self, instance, owner):
        print(f" self >>> {self}\ninstance >>> {instance}\nowner >>> {owner}")
        return instance.ad

class Kisi:
    __slots__ = ("ad",)
    name = MyDescriptor()

# Kisi.name -> self
# kisi -> instance
# owner - Kisi
kisi = Kisi()
kisi.ad = "doruk"
print(type(kisi).__dict__["name"].__get__(kisi,type(kisi)))

print(kisi.name)

class Control:

    def __get__(self,instance,owner):
        return instance.__dict__.get("name",None).upper()

    def __set__(self, instance, value):
        if isinstance(value,str):
            instance.__dict__["name"] = value
        else:
            raise TypeError(f"{value} is not a string.")

class User:
        name = Control()
        def __init__(self,name):
            self.name = name
            print(
                type(self).__dict__["name"] # bulunur ve bu bir descriptor nesnesi (data descriptor)
            )
            print(type(self).__dict__["name"].__get__(self,type(self)))

user1 = User("demir")

print(user1.name)
print("->",user1.__dict__)

print(
    type(user1).__getattribute__(user1,"name") # -> Burda python desciptor kontrolü yapar eğer attr, data des ise ait olduğu sınıftan aramaya başlanır
)

print(
    type(user1).__dict__["name"].__get__(user1,type(user1))
)

class NonData:
    def __init__(self):
        self.attr_name = None
    def __set_name__(self,owner,name):
        self.attr_name = name

    def __get__(self,instance,owner):
        print("get çağrıldı")
        return instance.__dict__.get(self.attr_name,None)


class A:
    name = NonData()
    age =  NonData()
    def __init__(self,name):
        self.name = name

a = A("A")
print(a.name) # A
print(a.__dict__) # {'_name': 'A'}

a.__class__.__dict__["name"].__get__(a,type(a)) # get çağrıldı
"""
python bu işlemi yapmaz çünkü descriptor sınıfı Non-data descriptor'dür bu nedenle önceliği de düşüktür attribute erişiminde python bu nesnenin non-data olduğunu tespit etmesi durumunda sınıfa bakmaz doğruca örneğe gider 
"""

print(a.age)
"""get çağrıldı
None
"""
# burda sınıf attribute'su olan age'İ çağırdık ve bu isim, örnekte olmadığı için shadow olmadı doğruca __get__ çağrıldı (descriptor protokolü)