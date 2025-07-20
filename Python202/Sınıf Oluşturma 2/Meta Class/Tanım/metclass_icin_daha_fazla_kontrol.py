# ===============================================================
# 🧠 METACLASS → __call__ METODU (Sınıf Çağrıldığında Ne Olur?)
# ===============================================================

# 🔷 Metaclass'larda tanımlanan __call__ metodu, sınıf örneği oluşturulurken çalışır.
# 🔹 Normal sınıflarda __call__ = nesneyi çağrılabilir yapmak içindir.
# 🔹 Ama metaclass'taki __call__, doğrudan sınıf çağrıldığında devreye girer.
# 🔸 Yani: MyClass() → aslında MyMeta.__call__ ile kontrol edilir.

# 🔧 Amaç:
# - Örnek oluşturulurken özel kontrol ve işlem eklemek
# - Singleton gibi desenleri uygulamak
# - Factory logic yazmak (hangi instance'ı vereceğini belirlemek)
# - Loglama, zamanlayıcı, erişim engeli gibi işlemler

# 🔁 __call__ metodu zinciri şöyledir:
# 1️⃣ Sınıf çağrılır:        MyClass()
# 2️⃣ Metaclass.__call__ çalışır (örn: MyMeta.__call__)
# 3️⃣ İçeride:
#     - cls.__new__ çağrılır
#     - ardından cls.__init__
#     - ardından örnek return edilir

# -----------------------------------------------------------
# ✅ ÖRNEK: Metaclass içindeki __call__ ile loglama yapmak
# -----------------------------------------------------------

class MetaLogger(type):
    def __call__(cls, *args, **kwargs):
        print(f"[Metaclass] {cls.__name__} örnekleniyor...")
        # Normal örnekleme zinciri
        instance = super().__call__(*args, **kwargs)
        print(f"[Metaclass] Oluşturulan örnek: {instance}")
        return instance

# Bu sınıf MetaLogger metaclass'ına sahiptir
class Model(metaclass=MetaLogger):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Model name={self.name}>"

# 🔽 Sınıf çağrıldığında → metaclass __call__ devreye girer
m = Model("deneme")
# Çıktı:
# [Metaclass] Model örnekleniyor...
# [Metaclass] Oluşturulan örnek: <Model name=deneme>

# 🧠 Artık öğrendik:
# - __call__, sınıf örneği oluşturulurken çalışır
# - Metaclass’ın kontrolü ile instance oluşturma davranışları özelleştirilebilir


# ======================================================================
# 🧠 NİHAİ TANIM — __instancecheck__ & __subclasscheck__ METACLASS'DA
# ======================================================================

# 🔷 __instancecheck__(self, instance)
# → isinstance(obj, Class) çağrıldığında çalışır
# → obj'nin sınıfa "uygun" olup olmadığını kontrol etmek için kullanılır
# → Bu metot metaclass içinde tanımlanır (type tabanlı)

# 🔷 __subclasscheck__(self, subclass)
# → issubclass(Sub, Class) çağrıldığında çalışır
# → alt sınıfın bu sınıfa "benzer" olup olmadığını kontrol etmek için kullanılır
# → Bu da metaclass içinde tanımlanır

# 🔶 AMAÇ:
# - Gerçek kalıtım olmasa bile, bir sınıf veya nesneyi "o sınıf gibi" değerlendirmek
# - Özellikle: ABC (Abstract Base Class), interface sistemleri, plugin detection için kullanılır

# ==============================================================================
# 🛠️ YÜKSEK SEVİYE ÇAĞRILAR → isinstance() ve issubclass() NASIL ÇALIŞIR?
# ==============================================================================

# 1️⃣ isinstance(obj, Class)
#    - obj.__class__ → A (örnek sınıf)
#    - A'nın metaclass'ı varsa → onun __instancecheck__ metodu çağrılır
#    - Yoksa normal miras zinciri (__mro__) kontrol edilir

# 2️⃣ issubclass(Sub, Class)
#    - Sub.__mro__ zincirinde Class var mı kontrol edilir
#    - Eğer Class'ın metaclass'ı __subclasscheck__ içeriyorsa, o çağrılır

# ==============================================================================
# ⚠️ ÖNEMLİ: __instancecheck__ / __subclasscheck__ içinde kendini çağırma TUZAĞI
# ==============================================================================

# Eğer bu metotların içinde tekrar isinstance() / issubclass() çağrısı yaparsan
# Python tekrar bu metodu çağırır → Sonsuz döngü oluşur → RecursionError alırsın

# Yanlış kullanım örneği (sonsuz döngü yaratır):
class MetaLoop(type):
    def __instancecheck__(cls, instance):
        return isinstance(instance, cls)  # 💥 Sonsuz döngü

# Doğru kullanım — temel type metodunu çağırarak:
class SafeMeta(type):
    def __instancecheck__(cls, instance):
        return type.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        return type.__subclasscheck__(cls, subclass)

# ==============================================================================
# ✅ DOĞRU VE YARARLI ÖRNEK
# ==============================================================================

class DuckMeta(type):
    def __instancecheck__(cls, instance):
        # 'quack' metodu olan her şeyi örnek olarak kabul et
        return callable(getattr(instance, "quack", None))

class Duck(metaclass=DuckMeta):
    pass

class Dog:
    def quack(self): return "havquack"

print(isinstance(Dog(), Duck))  # ✅ True — DuckTyping'in güzel örneği

# ==============================================================================
# 💬 ÖZET:
# - __instancecheck__ → isinstance özelleştirmesi
# - __subclasscheck__ → issubclass özelleştirmesi
# - Gereksiz yere kullanma, dikkatli ve kontrollü kullan
# - Recursion tuzağından kaçınmak için super() veya type.method() ile çağır




