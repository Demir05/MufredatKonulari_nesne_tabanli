# ----------------------------------------
# 🧠 METACLASS vs CLASS DECORATOR
# ----------------------------------------

# 🎯 AMAÇLARI ORTAK: Sınıf davranışını değiştirmek
# 🔁 Ancak bunu farklı zamanlarda ve farklı güç seviyeleriyle yaparlar

# ========================================
# 1️⃣ TEORİK FARKLAR
# ========================================

# 🧬 METACLASS:
# --------------------------
# • Sınıfı oluşturacak "sınıftır"
# • type yerine özelleştirilmiş bir sınıf üreticidir
# • Sınıf tanımı anında devreye girer (compile-time gibi davranır)

# 🔧 CLASS DECORATOR:
# --------------------------
# • Sınıf tanımı tamamlandıktan sonra uygulanır
# • Var olan sınıfı alır, değiştirir veya sarmalar
# • Sınıf objesi belleğe geldikten sonra çalışır

# ========================================
# 2️⃣ KOD AKIŞINDAKİ ZAMANLAMA
# ========================================

# class MyClass(metaclass=MyMeta):
#     pass

# class MyClass: ...
# MyClass = decorator(MyClass)

# 🔁 Metaclass → class statement çalışırken çağrılır
# 🔁 Decorator → class statement bittikten sonra çağrılır

# ========================================
# 3️⃣ GÜÇ DENGESİ
# ========================================

# ✅ Metaclass:
# • __slots__, __new__, __init__, __prepare__
# • __mro__ değiştirme, attribute validation
# • DSL & framework kuralları tanımlamak için ideal

# ✅ Decorator:
# • __init__ override, method ekleme
# • logging, metrics, metadata inject gibi hafif işlemler
# • Sınıfı sararak proxy oluşturabilir (class wrapper)

# ========================================
# 4️⃣ GERÇEK DÜNYA KULLANIMLARI
# ========================================

# 🔧 Metaclass Kullanım Örnekleri:
# • ORM altyapısı (Django Models)
# • Interface zorlaması (abc.ABCMeta)
# • Auto __slots__, auto __init__, field extraction
# • Singleton, immutable class üretimi

# 🎨 Class Decorator Kullanım Örnekleri:
# • @dataclass → methodları otomatik üretir
# • @total_ordering → ordering methodlarını tamamlar
# • logging, caching, register decorators
# • @singleton, @timed, @debug gibi kolay yapılandırıcılar

# ========================================
# 5️⃣ ORTAK NOKTALAR
# ========================================

# ✅ Her ikisi de sınıf davranışını değiştirebilir
# ✅ Her ikisi de reusable abstraction sağlar
# ✅ Her ikisi de plugin, registry, validation gibi yapılara uygundur
# ✅ İkisi birlikte bile kullanılabilir

# ========================================
# 6️⃣ HANGİ DURUMDA HANGİSİ?
# ========================================

# 🔹 Hafif davranışlar (logging, annotation, override) → Decorator
# 🔹 Yapısal değişim (__slots__, inheritance check, MRO) → Metaclass
# 🔹 Sadece o sınıfı etkilesin → Decorator
# 🔹 Tüm alt sınıfları da kapsasın → Metaclass
# 🔹 Kod okunabilirliği öncelikliyse → Decorator

# ========================================
# 7️⃣ PEKİ YA BİRLİKTE?
# ========================================

# @log_methods
# class MyClass(metaclass=ValidatedType):
#     pass

# ➕ Metaclass ile yapı kontrol edilir
# ➕ Decorator ile davranış eklenir

# İdeal bir sistem bu ikisini birlikte, katmanlı şekilde kullanır

# ========================================
# 8️⃣ GÖZDEN KAÇMAMASI GEREKENLER
# ========================================

# • Decorator, sınıfı sarmalayabilir (proxy gibi çalışır)
# • Metaclass, __classcell__ gibi düşük seviyeli detaylara müdahale edebilir
# • __slots__ gibi özellikler sadece metaclass ile kontrol edilebilir

# ========================================
# ✅ SONUÇ: TANIM
# ========================================

# 🧬 METACLASS = “Sınıfın nasıl doğacağını belirler”
# 🎨 DECORATOR = “Doğmuş sınıfı güzelleştirir, süsler, geliştirir”

# 🎯 Metaclass yapısal
# 🎯 Decorator davranışsal

# Birlikte kullanıldığında: hem güçlü hem esnek bir Python mimarisi kurarsın

# 🎨 DECORATOR — sınıfa meta bilgi ekler
def model(cls):
    cls.__is_model__ = True  # Ekstra bilgi
    print(f"🎨 {cls.__name__} modeli işaretlendi")
    return cls

# 🧬 METACLASS — yapısal işlemler
class ModelMeta(type):
    def __new__(mcs, name, bases, dct):
        print(f"🔧 {name} sınıfı metaclass tarafından işleniyor")

        # Field extraction
        annotations = dct.get("__annotations__", {})
        dct["__slots__"] = tuple(annotations)

        # Otomatik repr üretimi
        def __repr__(self):
            attrs = ", ".join(f"{key}={getattr(self, key)!r}" for key in annotations)
            return f"{name}({attrs})"
        dct["__repr__"] = __repr__

        return super().__new__(mcs, name, bases, dct)

# ✅ Kullanım:
@model
class User(metaclass=ModelMeta):
    name: str
    age: int

# 🔍 Test:
u = User()
u.name = "Ali"
u.age = 30
print(u)  # 👉 User(name='Ali', age=30)
print(User.__is_model__)  # ✅ True
print(User.__slots__)     # ✅ ('name', 'age')
