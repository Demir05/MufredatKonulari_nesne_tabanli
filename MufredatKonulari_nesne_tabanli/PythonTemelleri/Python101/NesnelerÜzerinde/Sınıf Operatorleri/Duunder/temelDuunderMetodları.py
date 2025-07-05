

# ================================================================
# ❓ NEDEN BAZI OPERATÖRLER BAZI SINIFLARDA KULLANILMAZ?
# ================================================================
# ➤ Python'da +, -, *, == gibi operatörler aslında özel metodlara bağlıdır:
#     a + b  →  a.__add__(b)
#
# ❌ Eğer bu metod tanımlı değilse → TypeError oluşur.
#
# 🎯 Çünkü her sınıf için her operatör anlamlı değildir.
#     Örn: dict + dict → çakışan anahtarlar ne olacak?
#
# ✅ Bu yüzden Python: "Kendin tanımla, ben karışmam" der.
#
# ------------------------------------------------
# ⚡ PERFORMANS AÇIKLAMASI:
# ------------------------------------------------
# ✔️ Operatörler Python’un çekirdeğinde (C dilinde) yazılmıştır.
# ✔️ Bytecode düzeyinde optimize çalışır → çok hızlıdır.
# ✔️ __add__ gibi metodlar da operatörlerle aynı işi yapar ama + daha hızlıdır.
# ================================================================


# 💡 TEMEL DUUNDER OPERATÖRLER:
# +   -> __add__(self, other)
# -   -> __sub__(self, other)
# *   -> __mul__(self, other)
# /   -> __truediv__(self, other)
# //  -> __floordiv__(self, other)
# %   -> __mod__(self, other)
# **  -> __pow__(self, other)

# +=  -> __iadd__(self, other)
# -=  -> __isub__(self, other)
# *=  -> __imul__(self, other)
# /=  -> __itruediv__(self, other)


# ✅ __add__(self, other)
# + operatörünün davranışını belirler.
# İki nesneyi toplamak için kullanılır.
class AddOnly:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return AddOnly(self.value + other.value)

    # ➤ Toplama işlemi sonucunda yeni bir A nesnesi oluşturuyoruz.
    # ✔ Böylece 'a + b' ifadesi yine bir A nesnesi döner.
    # ➤ Bu sayede işlemler zincirlenebilir hale gelir: (a + b + c)
    # ➤ Aynı zamanda orijinal nesneler değişmez → immutability korunur.

    def __repr__(self):
        return f"AddOnly({self.value})"

# a + b → a.__add__(b)
# Eğer __add__ NotImplemented dönerse → b.__radd__(a) denenir.


# ✅ __sub__(self, other)
# - operatörünün davranışını belirler.
# İki nesne arasında farkı hesaplamak için kullanılır.
class SubOnly:
    def __init__(self, value):
        self.value = value

    def __sub__(self, other):
        return SubOnly(self.value - other.value)

    def __repr__(self):
        return f"SubOnly({self.value})"


# ✅ __mul__(self, other)
# * çarpma işlemi için kullanılır.
# Sayıların veya nesnelerin tekrarlı işlemleri için kullanılabilir.
class MulOnly:
    def __init__(self, value):
        self.value = value

    def __mul__(self, other):
        return MulOnly(self.value * other.value)

    def __repr__(self):
        return f"MulOnly({self.value})"


# ✅ __truediv__(self, other)
# / işlemi için kullanılır. Ondalıklı bölme işlemi yapar.
class TrueDivOnly:
    def __init__(self, value):
        self.value = value

    def __truediv__(self, other):
        return TrueDivOnly(self.value / other.value)

    def __repr__(self):
        return f"TrueDivOnly({self.value})"


# ✅ __floordiv__(self, other)
# // işlemi için kullanılır. Tam sayı bölme işlemi yapar (küsurat atılır).
class FloorDivOnly:
    def __init__(self, value):
        self.value = value

    def __floordiv__(self, other):
        return FloorDivOnly(self.value // other.value)

    def __repr__(self):
        return f"FloorDivOnly({self.value})"


# ✅ __mod__(self, other)
# % işlemi için kullanılır. Kalan hesaplaması yapar.
class ModOnly:
    def __init__(self, value):
        self.value = value

    def __mod__(self, other):
        return ModOnly(self.value % other.value)

    def __repr__(self):
        return f"ModOnly({self.value})"


# ✅ __pow__(self, other)
# ** işlemi için kullanılır. Üs alma (power) işlemi.
class PowOnly:
    def __init__(self, value):
        self.value = value

    def __pow__(self, other):
        return PowOnly(self.value ** other.value)

    def __repr__(self):
        return f"PowOnly({self.value})"


class A:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return A(self.value + other.value)

class B:
    def __init__(self, value):
        self.value = value


a = A(20) ; b = B(23)

print(a.__add__(b).value)

class C:
    def __init__(self, value):
        self.value = value
    def __truediv__(self, other):
        return C(self.value / other.value)

c = C(0)

print(c.__truediv__(b).value)