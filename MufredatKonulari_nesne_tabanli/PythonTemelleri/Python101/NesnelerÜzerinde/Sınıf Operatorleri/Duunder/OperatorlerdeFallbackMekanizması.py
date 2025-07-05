# ================================================================
# 🔁 PYTHON'DA TERS VE YERİNDE OPERATÖR METODLARI (radd, iadd)
# ================================================================
#
# 🎯 a + b ifadesinde Python şu sırayı izler:
#   1️⃣ a.__add__(b)
#   2️⃣ Eğer bu metod yoksa ya da NotImplemented dönerse:
#       ➤ Python b.__radd__(a) metodunu çağırır
#
# ------------------------------------------------
# 🔹 __radd__(self, other)
# ------------------------------------------------
# ➤ "Ters toplama" operatörüdür: right-hand add.
#     ➤ `a + b` çalışmazsa → Python otomatik olarak `b.__radd__(a)` çağırır.
#
# ⚠️ `__radd__` metodunun **doğrudan bir operatörü yoktur.**
#     ➤ Yani `a + b` yazarsın, ama `__radd__()` *yedek plan* olarak çalışır.
#
# 🧠 Neden var?
#     ➤ Farklı türde nesnelerin birlikte çalışmasını sağlar.
#
# Örn:
# class A:
#     def __add__(self, other):
#         return NotImplemented
#
# class B:
#     def __radd__(self, other):
#         return f"{other} + B"
#
# A() + B()  →  A.__add__ → NotImplemented → B.__radd__(A())


## ===========================================================
# 🔁 PYTHON OPERATÖR ÇÖZÜMLEME MEKANİZMASI (Adım Adım)
# ===========================================================
#
# 🎯 Amaç: a + b / a += b gibi işlemlerde hangi metodun ne zaman çağrıldığını anlamak
#
# -----------------------------------------------------------
# 📌 ÖRNEK: a += b
# -----------------------------------------------------------
#
# 1️⃣ İlk olarak Python, a.__iadd__(b) metodunu çağırmayı dener.
#     - Bu metod tanımlıysa ve çalışırsa işlem burada biter.
#     - Eğer tanımlı değilse veya NotImplemented dönerse:
#
# 2️⃣ Python, normal sol operatörü çağırır: a.__add__(b)
#     - Bu metod çalışırsa sonucu alır, `a = a + b` gibi davranır.
#     - Eğer bu da NotImplemented dönerse:
#
# 3️⃣ Python sağ tarafa fallback yapar: b.__radd__(a)
#     - Yani ters operatörü çağırır (right-side)
#     - Bu çalışırsa sonucu alır
#
# 4️⃣ Yukarıdaki tüm adımlar başarısız olursa:
#     - Python TypeError fırlatır: unsupported operand types
#
# -----------------------------------------------------------
# 📌 ÖRNEK: a + b
# -----------------------------------------------------------
#
# 1️⃣ Python önce sol operatöre bakar: a.__add__(b)
#     - Eğer NotImplemented dönerse:
#
# 2️⃣ Sağ taraf denenir: b.__radd__(a)
#
# 3️⃣ İkisi de başarısızsa TypeError fırlatılır
#
# ===========================================================
# ✅ Notlar:
# -----------------------------------------------------------
# - Zincir yalnızca NotImplemented ile devam eder
# - Eğer herhangi bir adım TypeError fırlatırsa zincir kırılır
# - Bu sistem tüm çiftli operatörler (__, __r__) için geçerlidir
#
# 💡 Bu sıralamayı bilmek, in-place davranışları ve fallback mekanizmaları
#    tasarlarken hayati önem taşır.
# ===========================================================

# 📌 Bu yapı, Python'a yüksek esneklik ve türler arası uyum sağlar.
# ================================================================

class MyClass:
    def __radd__(self, other):
        return f"{other} + MyClass"


print(10 + MyClass())  # int.__add__(MyClass()) ➜ NotImplemented ➜ MyClass.__radd__(10)

class Alpha:
    def __init__(self,value:str):
        self.value = value

    def __radd__(self, other):
        return f"{self.value} + {''.join(str(other))}"

    def __add__(self,other):
        return NotImplemented

a1 = Alpha("demir")

print([1,2,3] + a1)

class Alpha:
    def __init__(self,value:str):
        self.value = value

    def __radd__(self, other):
        print("__radd__ çalıştı!")
        return f"{self.value} + {''.join(str(other))}"

    def __add__(self,other):
        return NotImplemented

    def __iadd__(self,other):
        return NotImplemented


a1 = Alpha("demir")

print("ozan" + a1) # __radd__ çalıştı!


class Alpha:
    def __init__(self,value:str):
        self.value = value

    def __radd__(self, other):
        print("__radd__ çalıştı!")
        return f"{self.value} + {''.join(str(other))}"

    def __iadd__(self,other):
        return NotImplemented


a1 = Alpha("demir")

print("ozan" + a1) #__radd__ çalıştı!

