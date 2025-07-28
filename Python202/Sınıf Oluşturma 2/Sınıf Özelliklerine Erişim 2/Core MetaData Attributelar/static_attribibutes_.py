# ============================================================
# 🧠 PYTHON'DA `__static_attributes__` ATTRIBUTE'U NEDİR?
# ============================================================

# ✅ Tanım:
# -----------
# `__static_attributes__`, Python 3.13 ile birlikte gelen yeni bir attribute’dur.
# Bir sınıf içinde `self.x = ...` gibi *doğrudan* atanmış instance attribute’ları
# tanımlama anında otomatik olarak toplar ve bir tuple olarak saklar.

# ✅ Ne işe yarar?
# ------------------
# - Sınıf içinde hangi instance değişkenlerin tanımlandığını belirlemeye yarar.
# - Özellikle `__slots__`'u otomatik oluşturmak veya ORM gibi sistemlerde alan tespiti için kullanılır.
# - Kod analiz araçları (type checker, linters) bu bilgiyi kullanabilir.

# ✅ Nasıl çalışır?
# -------------------
# - Sınıf gövdesinde `self.<attr>` şeklinde yapılan atamaları analiz eder.
# - Bu attribute'ları `__static_attributes__` isminde tuple olarak sınıfın namespace’ine ekler.

# ✅ Örnek:
# ----------
class Person:
    def __init__(self):
        self.name = "Ali"
        self.age = 30

print(Person.__static_attributes__)  # ➜ ('name', 'age')

# ✅ Gerçek Hayattaki Kullanımı:
# -------------------------------
# ORM sistemlerinde, hangi field’ların olduğunu anlamak için `__static_attributes__` sayesinde
# ayrı bir decorator, field() fonksiyonu veya manuel tanımlama gerekmez.

# ------------------------------------------------------------
# 🧪 ÖRNEK: Otomatik `__slots__` Kullanımı
# ------------------------------------------------------------
class AutoSlotsMeta(type):
    def __new__(cls, name, bases, dct):
        # Eğer static attributes varsa bunları __slots__ olarak ayarla
        if '__static_attributes__' in dct:
            dct['__slots__'] = dct['__static_attributes__']
        return super().__new__(cls, name, bases, dct)

class User(metaclass=AutoSlotsMeta):
    def __init__(self):
        self.username = "user"
        self.password = "1234"

print(User.__slots__)  # ➜ ('username', 'password')
