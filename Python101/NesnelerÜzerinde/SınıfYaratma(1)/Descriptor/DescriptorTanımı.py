""""# 1. Önce nesnenin sınıfı belirlenir
cls = type(obj)  # Çünkü descriptor'lar sınıfa tanımlanır, bu nedenle davranışları sınıf belirler

# 2. MRO sırasına göre sınıf zincirinde attribute aranır
for base in cls.__mro__:  # MRO sayesinde çoklu kalıtımda doğru sıralı arama yapılır
    if "attr" in base.__dict__:
        descriptor = base.__dict__["attr"]  # Sınıf sözlüğünde attribute bulundu
        break
else:
    descriptor = None  # Hiçbir sınıfta attribute bulunamazsa None olur

# 3. Eğer attribute bir data descriptor ise (get + set var)
if descriptor and hasattr(descriptor, "__get__") and hasattr(descriptor, "__set__"):
    result = descriptor.__get__(obj, cls)  # Data descriptor her zaman önceliklidir, obj.__dict__'i bile ezer
    return result

# 4. Data descriptor yoksa, objenin kendi __dict__'inde attribute aranır
if "attr" in obj.__dict__:
    return obj.__dict__["attr"]  # Instance dictionary varsa, kullanılır

# 5. Hâlâ bulunamazsa ve attribute bir non-data descriptor ise (sadece get varsa)
if descriptor and hasattr(descriptor, "__get__"):
    result = descriptor.__get__(obj, cls)  # Non-data descriptor, instance'de bulunmadığı sürece çalıştırılır
    return result

# 6. Hâlâ bulunamazsa, descriptor olmayan sınıf attribute'u döndürülür
if descriptor:
    return descriptor  # Bu durumda attribute normal bir sınıf değeri gibi davranır

# 7. En son olarak __getattr__ çalıştırılır
if hasattr(cls, "__getattr__"):
    return cls.__getattr__(obj, "attr")  # Fallback olarak tanımlı __getattr__ devreye girer

# 8. Hiçbir yerde bulunamazsa, AttributeError yükseltilir
raise AttributeError(f"{cls.__name__} object has no attribute 'attr'")

"""
from typing import Optional


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


class UpperCase:
    def __get__(self,instance,owner) -> Optional[str]:
        if owner.__name__ == "Name":
            return instance._name.upper()
        return None
class Name:
    name = UpperCase()
    def __init__(self, name):
        self._name = name

demir = Name("demir")
print(demir.name)
print(demir.__dict__)

class A:
    name = UpperCase()
    def __init__(self, name):
        self._name = name
ozan = A("ozan")
print(ozan.name)