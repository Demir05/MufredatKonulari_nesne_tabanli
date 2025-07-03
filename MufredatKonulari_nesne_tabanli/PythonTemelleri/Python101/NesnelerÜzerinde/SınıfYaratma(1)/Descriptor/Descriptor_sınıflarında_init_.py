# 📌 KONU: Descriptor sınıflarında neden __init__() override edilir?
# ─────────────────────────────────────────────────────────────

# 🔷 GENEL TANIM:
# Descriptor sınıfı, başka bir sınıfın class attribute'ü olarak görev yapar.
# Bu sayede obj.attr gibi işlemlerde, obj.__dict__ yerine __get__(), __set__(), __delete__() gibi metodlar devreye girer.
# Ama bazı descriptor'lar (örneğin property gibi) daha dinamik ve özelleştirilebilir yapı ister.
# Bu durumda descriptor sınıfı __init__() fonksiyonu ile yapılandırılır.

# 🔹 NEDEN GEREKLİ?
# Birden fazla descriptor örneği kullanıldığında, her biri farklı bir attribute için çalışır.
# Bu durumda descriptor’un hangi attribute'u yönettiğini bilmesi gerekir.
# Bunu sağlayan şey __init__()’de alınan parametrelerdir. (örn: name, type, validator vs.)

# ➤ KULLANIM AMACI:
# Her descriptor nesnesi kendi iç konfigürasyonuna sahip olur.
# Örneğin:
#   - Hangi türde değer kabul edecek?
#   - Hata kontrolü / validasyon mantığı ne olacak?

# 🔸 PROPERTY GİBİ DURUMLARDA:
# property sınıfı da bir descriptor'dur ve __init__ içinde şu parametreleri alır:
#   - fget: Getter fonksiyonu
#   - fset: Setter fonksiyonu
#   - fdel: Deleter fonksiyonu
# Bu fonksiyonlar sayesinde kullanıcıya temiz bir API sunar:
#   @property
#   def x(self): ...
#   @x.setter
#   def x(self, value): ...

# 🔸 STATICMETHOD & CLASSMETHOD NEDEN __init__ KULLANIR?
# Bunlar da descriptor’dur!
# staticmethod: Sadece fonksiyonu alır, örnek ya da sınıf bilgisi gerekmez.
# classmethod: Fonksiyonu alır ama çağrıldığında otomatik olarak sınıfı (cls) geçirir.
# Her ikisi de __init__ ile fonksiyonu alır ve __get__ ile bağlama (binding) işlemi yapar.

# 🔸 NORMAL DESCRIPTOR’LA FARKI:
# Basit descriptor'lar (örneğin sadece __get__ tanımlı olanlar) sabittir.
# Bir konfigürasyon taşımazlar.
# Ama init'li descriptor’lar **birden çok farklı amaçla ve esneklikle** kullanılabilir.

# 🔸 MÜKEMMEL FARK:
# 1️⃣ Sabit descriptor:
#     class A:
#         x = OnlyGetDescriptor()
#     ➤ Tek görev, "x" erişimi kontrol etmek. Dinamik değil.

# 2️⃣ Init'li descriptor:
#     class Field:
#         def __init__(self, name, type):
#             self.name = name
#             self.type = type
#     ➤ Bu Field sınıfı birden çok farklı attribute'u ayrı kurallar ile yönetebilir.

# 🔚 ÖZETLE:
# Descriptor'ların __init__ ile yapılandırılması,
# onları tekrar kullanılabilir, esnek ve özelleştirilebilir yapar.
# property, staticmethod ve classmethod gibi yapılar bunun doğal örnekleridir.

# 🔍 Bu yapı sayesinde:
# - Tek descriptor sınıfı = birçok attribute için özel yapı
# - DRY ve reusable design
# - Property-like API temizliği

# 💡 Sonuç:
# Python'daki descriptor mimarisi, init destekli descriptor'larla
# zenginleştirildiğinde gerçekten güçlü bir API kontrol katmanı sağlar.


class ControlDescriptor:
    def __init__(self,_type):
        self.__type = _type
        self.__atribute__name = None

    def __get__(self,instance,owner):
        return instance.__dict__.get(self,None)

    def __set__(self,instance,value):

        if isinstance(value,self.__type):
            instance.__dict__[self] = value
        else:
            raise TypeError(f"{repr(value)} is not {self.__type}")




class User:
    name = ControlDescriptor(str)
    def __init__(self,name):
        self.name = name

user1 = User("demir")


print("kullanıcı dict",user1.__dict__,sep=":") # kullanıcı dict:{<__main__.ControlDescriptor object at 0x76db17139160>: 'demir'}
print(user1.name) # demir

user1.name = "osman"

print("kullanıcı dict",user1.__dict__,sep=":") # kullanıcı dict:{<__main__.ControlDescriptor object at 0x700d98135550>: 'osman'}
print(user1.name) # osman