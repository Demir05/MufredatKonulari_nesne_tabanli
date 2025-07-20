# ================================================================
# 🔁 IN-PLACE OPERATÖRLER (`__iadd__`, `__imul__`, `__isub__`, ...)
# ================================================================
#
# ❓ NEDİR BU OPERATÖRLER?
# ➤ Python’da `+=`, `-=`, `*=`, `/=`, `//=`, `%=` gibi işlemler için
#     özel metodlar tanımlanabilir:
#     - __iadd__()  →  += için
#     - __imul__()  →  *= için
#     - vs.
#
# ------------------------------------------------
# 🧠 NEDEN VARLAR?
# ------------------------------------------------
# ➤ Bu metodlar, "yerinde değiştirme" (in-place) yapar.
# ➤ Eğer nesne **mutable** (değiştirilebilir) ise:
#     - Yeni bir nesne oluşturmak yerine, mevcut nesne değiştirilir.
# ➤ Eğer nesne **immutable** (değiştirilemez) ise:
#     - Yeni bir nesne döner (tıpkı `__add__` gibi davranır).
#
# ------------------------------------------------
# 📌 FARK:
# ------------------------------------------------
#   x += y  →  x.__iadd__(y) çağrılır
#            → Eğer tanımlı değilse → x = x + y  → __add__
#
#   ✅ Mutable → orijinal nesne güncellenir
#   ❌ Immutable → yeni nesne oluşur, referans değişir
#
# Örn:
#   lst = [1, 2];  lst += [3]   →  aynı liste değişir (in-place)
#   s = "hi";      s += "!"    →  yeni string oluşur (immutable)
#
# ================================================================
# 🔧 IN-PLACE OPERATOR METODLARI – SADE TANIMLAR
# ================================================================

# ✅ __iadd__(self, other)
# += operatörünü kontrol eder. Toplamı yerinde yapmaya çalışır.
# Mutable nesnelerde `self` doğrudan değiştirilebilir.
class MyList:
    def __init__(self, data):
        self.data = data

    def __iadd__(self, other):
        self.data.extend(other)
        return self

# ✅ __isub__(self, other)
# -= operatörünü kontrol eder. Farkı yerinde çıkarır.
class Counter:
    def __init__(self, val):
        self.val = val

    def __isub__(self, other):
        self.val -= other
        return self

# ✅ __imul__(self, other)
# *= için kullanılır. Çarpımı self'e uygular.
class Scale:
    def __init__(self, value):
        self.value = value

    def __imul__(self, factor):
        self.value *= factor
        return self

# ✅ __itruediv__(self, other)
# /= operatörü için. Float bölme yapılır.
class Divider:
    def __init__(self, val):
        self.val = val

    def __itruediv__(self, other):
        self.val /= other
        return self

# ✅ __ifloordiv__(self, other)
# //= işlemi için. Küsurat atılır.
class Floor:
    def __init__(self, v):
        self.v = v

    def __ifloordiv__(self, other):
        self.v //= other
        return self

# ✅ __imod__(self, other)
# %= işlemi için. Kalan hesaplaması yapar.
class Modulus:
    def __init__(self, v):
        self.v = v

    def __imod__(self, other):
        self.v %= other
        return self

# ✅ __ipow__(self, other)
# **= işlemi için. Üs alma.
class Power:
    def __init__(self, base):
        self.base = base

    def __ipow__(self, exp):
        self.base **= exp
        return self

# ================================================================
# 🧠 İPUCU:
# - In-place operatörler, özellikle büyük veri yapılarıyla çalışırken
#   daha performanslıdır çünkü yeni nesne oluşturmazlar (mutable ise).
# - Eğer tanımlı değillerse, Python otomatik olarak `x = x + y` gibi
#   `__add__`'ı çağırır (veya `__sub__`, `__mul__`, ...)
# ================================================================
