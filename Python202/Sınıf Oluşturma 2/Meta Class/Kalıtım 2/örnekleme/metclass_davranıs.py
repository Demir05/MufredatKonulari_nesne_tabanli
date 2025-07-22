# =====================================================================
# 🎓 METACLASS DAVRANIŞLARI — __init__, __setattr__, __getattribute__
# =====================================================================

# 🔹 Python'da her sınıf bir "class object"tir.
# 🔹 Bu class object'lerin nasıl oluşturulacağını, nasıl davranacağını metaclass tanımlar.

# 📌 Metaclass'ın tanımladığı dunder metodlar (örneğin __setattr__, __getattribute__)
#    "Sınıf objesinin" nasıl çalıştığını belirler, yani Model gibi bir sınıf tanımlandığında
#    artık o sınıf, metaclass'ın bir örneği olur.

# ---------------------------------------------------------
# 💡 ÖNEMLİ: Metaclass ≠ Instance class
# Model  →  MyMeta sınıfının bir örneği (yani: isinstance(Model, MyMeta) ✅)
# m = Model() → bu örnek ise normal instance → Base üzerinden kontrol edilir
# ---------------------------------------------------------

# 🔹 Bu yüzden aşağıdaki erişimlerde şu metotlar devreye girer:

# ➤ Model.foo = "x"       → MyMeta.__setattr__
# ➤ print(Model.foo)      → MyMeta.__getattribute__
# ➤ m = Model()           → MyMeta.__call__
# ➤ m.name = "ali"        → Base.__setattr__ (örnek düzeyi!)

# 🧠 Yani: Sınıf objesi üzerinde yapılan işlemleri metaclass dunder metodları yönetir
#         Örnek üzerinde yapılan işlemleri base class yönetir


class MyMeta(type):
    def __init__(cls, name, bases, dct):
        print(f"[Meta.__init__] Sınıf oluşturuldu: {name}")
        super().__init__(name, bases, dct)

    def __setattr__(cls, key, value):
        print(f"[Meta.__setattr__] Model seviyesinde attr atanıyor: {key} = {value}")
        super().__setattr__(key, value)

    def __getattribute__(cls, key):
        print(f"[Meta.__getattribute__] Model seviyesinde attr okunuyor: {key}")
        return super().__getattribute__(key)


class Base:
    def __init__(self):
        print("[Base.__init__] Örnek oluşturuluyor")

    def __setattr__(self, key, value):
        print(f"[Base.__setattr__] Örnek seviyesinde attr atanıyor: {key} = {value}")
        super().__setattr__(key, value)


class Model(Base, metaclass=MyMeta):
    pass


# ✅ Sınıf (class object) üzerinden yapılan işlemler
Model.version = "1.0"      # → MyMeta.__setattr__
print(Model.version)       # → MyMeta.__getattribute__

# ✅ Örnek (instance) üzerinden yapılan işlemler
m = Model()                # → Base.__init__
m.name = "Demir"           # → Base.__setattr__
