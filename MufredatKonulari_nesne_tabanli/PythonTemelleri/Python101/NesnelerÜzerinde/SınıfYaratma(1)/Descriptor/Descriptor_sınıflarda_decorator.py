# 🔷 PYTHON’DA DECORATOR & DESCRIPTOR İLİŞKİSİ (Derin ve Profesyonel Tanım)
# ------------------------------------------------------------------------

"""
📌 Tanım:
Decorator, Python’da bir fonksiyonu ya da metodu alıp onun davranışını değiştiren bir "sarmalayıcı fonksiyondur".
Descriptor ise attribute erişimlerini (__get__, __set__, __delete__) kontrol eden bir sınıf tabanlı protokoldür.

✨ Birçok yerleşik decorator (@staticmethod, @classmethod, @property), aslında özel descriptor sınıflarıdır.

👉 Yani:
  ➤ Decorator, davranış ekler
  ➤ Descriptor, davranışı kontrol eder

Ve bu iki yapı birlikte kullanıldığında:
  ➤ Fonksiyonlara özel erişim kontrolü kazandırılır (örneğin bir fonksiyon bir property haline gelir)

# ------------------------------------------------------------------------
# 🔧 1. @property gibi yerleşik decorator'lar aslında descriptor sınıflarıdır


@property = class property(object):
              def __get__(self, obj, objtype): ...
              def __set__(self, obj, value): ...
              def __delete__(self, obj): ...

@property gibi yapılar "decorator gibi görünür", çünkü syntax öyle:
    @property
    def name(self): ...
Ama aslında bu bir descriptor'dur → name = property(name)

Böylece name bir descriptor nesnesi olur ve attribute erişimi kontrol altına alınır.


# ------------------------------------------------------------------------
# ⚙️ 2. Decorator + Descriptor nasıl yazılır? Dikkat edilmesi gerekenler


Kendi descriptor'ını yazmak için __get__, __set__, __set_name__ gibi metodlar tanımlanır.
Decorator gibi kullanmak için descriptor sınıfı fonksiyonu parametre alır.


# 🔧 Descriptor nesneleri (__get__, __set__, __delete__) sınıf düzeyinde tanımlanır
# ve örnek üzerinden erişildiğinde tetiklenir.
#
# Örnek:
# class MyClass:
#     name = MyDescriptor()
#
# Burada `MyDescriptor()` bir descriptor nesnesidir ve `name` sınıf attribute'udur.

# ❓Peki decorator gibi descriptor tanımları nasıl oluyor?
# Örnek:
# class MyClass:
#     @cached_property
#     def expensive_calc(self): ...

# Bu örnek aslında:
#   def expensive_calc(self): ...
#   expensive_calc = cached_property(expensive_calc)
#   class body'ye expensive_calc isminde descriptor yerleştir
# şeklinde çalışır.

# ✅ Yani fonksiyona decorator uygulanır (func -> descriptor instance),
# ardından o descriptor, sınıfın attribute'ü haline gelir.
# Böylece descriptor protokolü (örn. __get__) yine işler.

# ================================
# 🔄 GENELLEME
# ================================
# Bir descriptor objesini fonksiyon saran (decorator) şekilde tanımlarsan:
#   - __init__(self, func) yaparsın,
#   - __get__ ile fonksiyonun çıktısını kontrol edersin.
#   - @decorator şeklinde kullanım sağlarsın
# Bu durumda:
#   ✅ Fonksiyonu wrap'leyen descriptor objesi sınıfa class attribute olarak eklenmiş olur.
#   ✅ Bu Python'un descriptor kuralı ile %100 uyumludur.

# 🧠 Bu durum, decorator'ler ile descriptor'lerin nasıl birlikte çalışabileceğini gösterir.
#   Ve aslında syntax sugar gibi görünen yapı, class attribute ilkesine uygun çalışır.



# =====================================
#  Descriptor'lerde __call__ Kullanımı
# =====================================

# 🔁 Python'daki descriptor protokolü:
#   __get__(self, instance, owner)
#   __set__(self, instance, value)
#   __delete__(self, instance)

# Bunlar sadece attribute erişimi, yazımı ve silinmesini kontrol eder.
# Dolayısıyla:
# - instance.attr  →  __get__
# - instance.attr = val  →  __set__
# - del instance.attr  →  __delete__

# 📌 Bir descriptor sınıfı genellikle bir fonksiyonu sarmak için kullanılır.
# Ancak bu sarma işlemi sonucunda o descriptor'un **__call__** metodu yoksa:
# - instance.method → sadece bir ifade olur (örneğin bir string dönebilir),
# - instance.method() → mümkün değil! Çünkü dönen şey bir fonksiyon değilse TypeError alırsın.

# 💡 Bu yüzden, bir descriptor aynı zamanda bir **decorator olarak bağımsız** şekilde kullanılmak isteniyorsa:
# ✅ O zaman __call__ metodu tanımlanmalıdır.

# Örnek:
# class Upper:
#     def __init__(self, func):
#         self.func = func
#     def __get__(self, instance, owner):
#         return self.func(instance).upper()
#     def __call__(self, *args, **kwargs):
#         return self.func(*args, **kwargs).upper()

# Bu sayede hem:
# - Sınıfa descriptor olarak tanımlanabilir (`class A: @Upper def f(self):...`)
# - Hem de dışarıda bir fonksiyonu doğrudan süsleyebilir:
#     @Upper
#     def greet(name): return name

# 🎯 SONUÇ:
# - `__call__` olmadan descriptor sadece bir attribute temsilcisidir.
# - `__call__` varsa, aynı sınıf hem descriptor hem decorator gibi davranabilir.
# - Bu tasarım, çok yönlülük (versatility) sağlar ama her zaman gerekli değildir.



Aşağıda bir decorator+descriptor birleşimi örneği var 👇
"""

class UpperProp:
    def __init__(self, func):
        self.func = func  # Süslenen fonksiyon burada tutulur
        self.__name__ = func.__name__  # Fonksiyonun adı kaydedilir (isteğe bağlı, __set_name__ alternatifi var)

    def __get__(self, instance, owner):
        if instance is None:
            return self  # Eğer sınıf üzerinden erişiliyorsa, descriptor objesinin kendisi döner
        result = self.func(instance)  # Fonksiyon örneğe uygulanır
        return result.upper()  # Dönen string upper() ile büyük harfe çevrilir

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

# ------------------------------------------------------------------------
# ⚠️ 3. Dikkat edilmesi gerekenler

"""
❗ 1. __get__ içinde instance.attr çağırırken dikkat:
    - Eğer attr, descriptor ismi ile çakışırsa → sonsuz döngü olur → RecursionError alırsın
    - Bu nedenle __set_name__ kullanarak descriptor’a özel saklama ismi tanımlanır (örn. "_name")

❗ 2. __slots__ kullanıyorsan:
    - Saklanan isim, __slots__ içinde tanımlanmalı
    - Eğer descriptor ile erişim varsa, __slots__ içindeki isim descriptor adıyla çakışmamalı

❗ 3. Decorator ile kullanılan descriptor'larda init'de alınan fonksiyonu kaybetmeyi unutma:
    - func.__name__, func.__doc__ gibi metadata’lar kaybolabilir (update_wrapper ile sarılabilir)

"""

# ------------------------------------------------------------------------
# 🔍 4. Sonuç

"""
💡 property, staticmethod, classmethod gibi yerleşik yapılar:
    ➤ Birer decorator gibi görünür
    ➤ Ama hepsi descriptor sınıfı olarak tanımlanmıştır
    ➤ Yani bu yapılar hem fonksiyonu değiştirir (decorator),
      hem de erişimi kontrol eder (descriptor)

✅ Bu birliktelik sayesinde:
    - Fonksiyonları attr gibi kullanmak mümkün olur (property)
    - Sınıf üzerinden çağrılabilir hale gelir (classmethod)
    - Nesne bağımsız erişim sağlanır (staticmethod)
    - Erişim kontrolleri şeffaf ve sade bir şekilde yazılır
"""

# ------------------------------------------------------------------------

class Cap:
    def __init__(self, func):
        self.__func = func

    def __call__(self,metin):
        return self.__func(metin).capitalize()

class A:

    @staticmethod
    @Cap
    def read(metin):
        return metin

a = A()

print(a.read("doruk"))


class Upper:
    def __init__(self, func):
        self.__func = func
        self.__name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.__func(instance).upper()

    def __set_name__(self, owner, name):
        self.__name = name

    def __set__(self, instance, value):
        setattr(instance,"name",value.upper())

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs).upper()


class User:
    def __init__(self, name):
        self.name = name
    @Upper
    def read(self):
        return self.name

user1 = User("aslı")
print(user1.read)
user1.name = "ozan"
print(user1.__dict__)

@Upper
def deneme(m):
    return m

print(deneme("merhaba"))
user1.read = "hello"
print(user1.read)
