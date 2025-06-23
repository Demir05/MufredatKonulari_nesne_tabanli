# 🔷 __set_name__ METODU – NİHAİ TANIM
#
# __set_name__(self, owner, name)
# ➤ Descriptor sınıflarının opsiyonel ama güçlü bir özel metodu.
# ➤ Python tarafından otomatik olarak çağrılır; geliştirici manuel çağırmaz!
#
# ⏱️ NE ZAMAN ÇAĞRILIR?
#   - Descriptor, bir sınıfın Class attribute'su olarak tanımlandığında (örneğin name = Control()),
#     o sınıfın tanımı tamamlandıktan hemen sonra Python tarafından __set_name__ çağrılır.
#
# 🎯 PARAMETRELERİ:
#   - self   → Descriptor nesnesinin kendisi
#   - owner → Descriptor'ün tanımlı olduğu sınıf (örneğin: class User)
#   - name   → Descriptor'ün bağlı olduğu attribute ismi(etiketinin adı) (örneğin: "name")
#   -          name, <class 'str'> türünde döner bu nedenle string işlemlerini destekler
#
# 🚀 NE İŞE YARAR?
#   - Descriptor'ün bağlı olduğu attribute ismini öğrenmesini sağlar.
#   - Böylece descriptor kendi __dict__ içinde anahtar olarak attribute adını tutabilir.
#   - __get__ / __set__ içinde bu isme göre erişim/atama yapılabilir.
#   - Birden fazla descriptor kullanılan sınıflarda büyük kolaylık sağlar.
#
# 🔄 __init__ metodunun alternatifi değildir, tamamlayıcısıdır!
#   - __init__ → parametre kontrolü / tür kontrolü gibi şeyler yapılır
#   - __set_name__ → descriptor’un hangi attribute’a bağlı olduğunu öğretir


class DescriptorWithName:
    def __init__(self):
        self.attr_name = None  # Başta hangi attribute'a bağlanacağını bilmiyor

    def __set_name__(self, owner, name):
        print(f"🔧 __set_name__ çağrıldı >> owner: {owner.__name__}, name: {name}")
        self.attr_name = name  # Artık descriptor 'name' gibi bir attribute'a bağlı olduğunu biliyor

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.attr_name)

    def __set__(self, instance, value):
        instance.__dict__[self.attr_name] = value


class Person:
    name = DescriptorWithName()
    age = DescriptorWithName()  # Birden fazla descriptor kullanımı

    def __init__(self, name, age):
        self.name = name
        self.age = age


p = Person("demir", 27)
print(p.name, p.age)


#-----------------------------------
def control_type(attr_type) -> bool:
    if isinstance(attr_type, type):
        return True
    return False

class Field:

    def __init__(self,attr_type):
        self.__attr_type_ = attr_type if control_type(attr_type) else None
        self.__attr_name = None

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __set__(self,instance,value):
        if isinstance(value, self.__attr_type_):
            instance.__dict__[self.attr_name] = value
        else:
            raise TypeError(f"{value} is not -> {self.__attr_type_}")

    def __get__(self,instance,owner):
        return instance.__dict__[self.attr_name]


class User:
    name= Field(str)
    age= Field(int)
    def __init__(self, name,age):
        self.name = name
        self.age = age
"""
Burda Data Descriptor kullanıldığı için python,self.name = name statements işleminde ilk olarak sınıfta name adında bir attribute olup olmadığını kontrol eder
class'da name adında bir attrtibute var! ve bu attribute, bir Data Descriptor bu nedenle python descriptor bu nedenle python,__setattr__ yerine __set__ metodunu otomatik
çağrılır
"""

user1 = User("demir",20)

print(user1.__dict__)
user1.name = "ozan"
try:
    user1.age = "demir"
except TypeError as e:
    print(e)
