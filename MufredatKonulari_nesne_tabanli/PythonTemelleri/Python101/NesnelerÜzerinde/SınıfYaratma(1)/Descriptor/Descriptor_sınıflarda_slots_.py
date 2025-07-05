 #  🔷 __slots__ ve Descriptor Kullanımı – İleri Seviye Python Nesne Modeli

# ----------------------------------------
# 🔹 __slots__ ve Descriptor İLİŞKİSİ
# ----------------------------------------
# ➤ __slots__ tanımlandığında __dict__ kaldırıldığı için descriptor nesnelerinin **attribute**'lara veri yazmak için
#     doğrudan `instance.__dict__[self.attr_name] = value` şeklindeki kodları çalışmaz!
# ➤ Bu durumda `setattr(instance, self.attr_name, value)` gibi alternatif teknikler gerekebilir.
# ➤ Alternatif olarak:
#     - __slots__ içinde descriptor'un çalışacağı **alan adını** açıkça belirtmek gerekir.
#     - __set_name__ metoduyla bu ad yakalanmalı ve sadece o slot'a veri yazılmalı.


# ───────────── Descriptor & __slots__ Uyumlu Tasarım ─────────────

# 🔹 1. Sınıf attribute adı ile örnek (instance) attribute adı çakışmamalı.
#     Çünkü:
#       - Sınıf attribute'u, descriptor olabilir (örneğin: `name = MyDescriptor()`).
#       - Aynı isimde örnek attribute (örneğin: `self.name = ...`) kullanılırsa
#         bu durum **shadowing (gölgeleme)** olarak adlandırılır.
#       - Bu, descriptor'ın devre dışı kalmasına ya da hatalı çalışmasına neden olur.

# 🔹 2. __slots__ kullanımı varsa durum daha kritiktir.
#     - __slots__ özelliği, örnek sözlüğünü (__dict__) kaldırır.
#     - Yalnızca __slots__ içinde belirtilen isimler kullanılabilir(veri,descriptorsa atlanabilir doğruca __get__,__set__çağrılabilir).
#     - Bu nedenle attribute adlarının özenle seçilmesi gerekir.

# 🔹 3. Python attribute erişiminde şu sıralamayı takip eder:
#     instance.attr  →  type(instance).__dict__['attr'].__get__(instance, type(instance))
#     - Eğer `attr` bir **data descriptor** ise (__get__ ve __set__ içeriyorsa),
#       örnek sözlüğü atlanır ve descriptor protokolü doğrudan çalışır.
#     - Non-data descriptor ise örnek sözlüğü önceliklidir.

# 🔹 4. __set_name__ metodunun rolü burada çok önemlidir.
#     - Bu metod sayesinde descriptor kendisine ait attribute ismini öğrenir.
#     - Bu bilgiyle, örnek nesne üzerinde farklı bir isim (örn: "_name") ile veri saklayabilir.
#     - Bu da sınıf attribute ismi ile çakışma riskini ortadan kaldırır.

#     Örnek:
#     def __set_name__(self, owner, name):
#         self.attr_name = "_" + name   # Örnekte '_name' olarak saklanacak

# 🔹 5. RecursionError’un nedeni: getattr(instance, self.attr_name)
#     - Eğer `self.attr_name` → `"name"` ise ve bu descriptor’ın bağlı olduğu attribute ise:
#       `getattr()` fonksiyonu yeniden __get__ tetikler → sonsuz döngü oluşur.
#     - Çözüm: Saklanan veri ismi farklı olmalı (örn: `_name`) veya doğrudan instance.__dict__ ya da __slots__ kullanılmalı.

#     getattribute / getattr davranışı özet:
#     - __getattribute__ her attribute erişiminde çağrılır → descriptor kontrolü burada olur.
#     - getattr fallback’tir → __getattribute__ başarısız olursa devreye girer.
#     - getattr içinde descriptor tetiklenebilir, dikkatli kullanılmalı.

# ✅ Doğru Tasarım: __set_name__ ile örnek içinde kullanılan veri adını farklı belirlemek
#    ve descriptor çözümlemesini Python’un beklediği şekilde yönetmek.


# 🔍 Neden __slots__ içinde tanımlı olmamasına rağmen descriptor'a yazarken hata almayız?

# ✔️ Çünkü Python'da bir attribute'a atama (örn: obj.name = "demir") yapıldığında:

# 1️⃣ İlk olarak `type(obj).__dict__['name']` kontrol edilir.
#    - Eğer bu `Data Descriptor` ise (yani hem __get__ hem __set__ tanımlıysa)
#      descriptor protokolü uygulanır, doğrudan `__set__()` çağrılır.

# 2️⃣ `__slots__` içinde `name` tanımlı olmasa  bile bu descriptor'a öncelik verilmesine engel değildir.
#    - Descriptor zaten özelleştirilmiş bir davranış tanımladığı için
#      Python slot’a değil, descriptor’a teslim eder işi.

# 3️⃣ `__set__()` metodunun içinde instance'a değer atamak için `instance._name = value` yazılırsa,
#     bu atama doğrudan `__slots__` alanına yapılır.
#     (Yani `__dict__` yoksa, Python `__slots__` üzerinden depolar.)

# 🧠 Bu sayede attribute adı `name` olsa da, descriptor bunu `_name` gibi
#     farklı bir içsel isimle slot’a yazabilir ve çakışma yaşanmaz.

# ✅ Özetle:
#     - Descriptor varsa, Python slot'a yazmaya çalışmaz.
#     - Descriptor’un `__set__()` metodu tüm kontrolü alır.
#     - Sen descriptor içinde hangi attribute'a yazılacağını belirtirsin (`_name` gibi).


# ----------------------------------------
# 🧠 SONUÇ
# ----------------------------------------
# ✔ __slots__ → bellek ve hız optimizasyonu
# ✔ Descriptor → attribute erişim kontrolü
# ✔ Birlikte → güvenli, optimize, kısıtlı ve yüksek seviyeli bir attribute yönetim sistemi!

# ----------------------------------------
# 🔷 __slots__ + Descriptor Kullanımı
# ➤ __slots__, örnek nesnelerin __dict__'e sahip olmasını engeller ve bellek kullanımını optimize eder
# ➤ Descriptor sınıfı ile birlikte kullanıldığında, veri depolama için alternatif yollar gerekir
# ➤ En iyi pratik: descriptor içinde depolama yapılır (örneğin: private dict, weakref, vs.)

class DescriptorWithSlots:
    def __set_name__(self, owner, name):
        # Sınıfa atanmış attribute ismini kaydeder
        self.attr_name = "_" + name  # private benzeri adlandırma

    def __get__(self, instance, owner):
        print(f"__get__ çağrıldı → {self.attr_name}")
        return getattr(instance, self.attr_name)

    def __set__(self, instance, value):
        print(f"__set__ çağrıldı → {self.attr_name} = {value}")
        setattr(instance, self.attr_name, value)


class User:
    __slots__ = ("_name", "_age")  # sadece bu iki alan oluşturulabilir
    name = DescriptorWithSlots()
    age = DescriptorWithSlots()

    def __init__(self, name, age):
        self._name = name  # __set__ çağrılır → _name = name
        self._age = age    # __set__ çağrılır → _age = age


# ✅ Test
u = User("demir", 28)

print(u.name)  # __get__ çağrılır
print(u.age)   # __get__ çağrılır

# 🧠 NOT:
# - __slots__ sayesinde örnek sözlüğü yok → __dict__ yok
# - Bu yüzden descriptor, veri saklamak için doğrudan örnek üzerinde tanımlı slot alanlarına yazıyor

class UpperDescriptorWithName:


    def __set_name__(self, owner, name):
        self.attr_name =  "_"+ name
        print(f"[DEBUG] name >>> {self.attr_name}")

    def __get__(self, instance, owner):
        if hasattr(instance,"__dict__"):
            print("örnekte __dict__ tanımlıdır ")
            return instance.__dict__[self.attr_name]
        print("örnekte __slots__ tanımlıdır ")
        #return super().__getattribute__( self.attr_name)

        return getattr(instance, self.attr_name) # -> owner.__dict__[self.attr_name].__get__

    def __set__(self, instance, value):
        if hasattr(instance,"__dict__"):
            print("örnekte __dict__ tanımlıdır ")
            instance.__dict__[self.attr_name] = value
        else:
            print("örnekte __slots__ tanımlıdır ")
            super().__setattr__(self.attr_name, value)

class User:
    __slots__ = ("_name",)
    name = UpperDescriptorWithName()

    def __init__(self, name):
        self._name = name

usr = User("demir")
print(usr._name)
print(type(usr).__dict__["name"].__get__(usr,type(usr)))
