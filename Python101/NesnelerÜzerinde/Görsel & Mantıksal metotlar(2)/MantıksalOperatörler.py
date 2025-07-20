# ======================================
# 🔹 Mantıksal Operatörler (Logical Ops)
# ======================================
from typing import Any


# Python'da 3 temel mantıksal operatör vardır:
# ------------------------------------------
# 1) and  → VE
# 2) or   → VEYA
# 3) not  → DEĞİL

# Bunlar "bağlaç" (connector) gibi çalışır, mantıksal zincirler kurar.
# Ancak klasik matematikteki gibi zincirleme sadeleştirme (simplify) yapmaz.

# ÖRN: a < b < c  gibi zincirli ifadeler → sadece karşılaştırma (comparison) için geçerlidir
# and / or ile: (a and b and c)  gibi ifadeler "sadeleşmez", sırayla değerlendirilir

# -----------------------------------------
# ⚙️ Değerlendirme Kuralları (short-circuit)
# -----------------------------------------

# 1. and → soldan sağa, ilk False'da durur
# bool(a and b) → önce bool(a), a False → b'ye bakılmaz
# bool(a and b) → a True → bool(b) gerekir

# 2. or → soldan sağa, ilk True'da durur
# bool(a or b) → a True ise → b'ye bakılmaz
# bool(a or b) → a False → bool(b) gerekir

# 3. not → tek operand alır, bool(not x) = True ise False döner

# Bu operatörler sonucu bool değil, operandın kendisini döner

# -------------------------------
# 🎯 __bool__ İLE NASIL ÇALIŞIR?
# -------------------------------

# Tüm bu operatörler operand'ları bool(...) içine geçirerek değerlendirir:
# örn: if a and b:
# → bool(a) → True ise → bool(b) kontrol edilir

# if yapısı gibi, "mantıksal bağlam" oluşturur
# → burada obj.__bool__() çağrılır (veya __len__ fallback)

# ------------------------------------
# 🧮 Öncelik Sırası (Operator Precedence)
# ------------------------------------

# 1. not      (en yüksek)
# 2. and
# 3. or       (en düşük)

# Bu yüzden:
# not a or b → (not a) or b  olarak çalışır
# a or b and c → a or (b and c)

# ------------------------------------
# 🧠 İfade Değil, Değer Dönerler
# ------------------------------------

# a = True or 5  → sonuc = True
# a = [] or 5     → sonuc = 5  (çünkü bool([]) = False → diğer değeri alır)
# a = {} and 8    → sonuc = {}  (çünkü False → kısa devre)

# Bu operatörler bool sonucu değil, operand döndürür.
# Yani:
# - x or y → x True ise x, değilse y
# - x and y → x False ise x, değilse y

# ------------------------------------
# ✅ Örnek
# ------------------------------------
class A:
    def __bool__(self):
        print("bool çalıştı")
        return False

a = A()
b = "devam"

sonuc = a and b  # sadece bool(a) çalışır, b'ye geçilmez
# Çıktı: bool çalıştı
# sonuc: <__main__.A object at ...> (yani False olduğu için A nesnesi döner)

class C:
    
    def __bool__(self):
        return True

class D:

    def __bool__(self):
        return False
    
c = C()
d = D()

(d and c) or print("ok")

# mantıksal kontrol; 

print(type(d).__dict__['__bool__'].__call__(d) ) # d-> False, mantıksal kavramda falsy 

print(type(c).__dict__['__bool__'].__call__(c)) # c -> True, mantıksal kavramda truhty 

# True and False -> False 
# False or ... -> print("ok")

def extended_and(operand:Any,operand2:Any,return_value:Any,fallback:Any=None,logic_not:bool=False) -> Any:
    """Bu fonksiyon,and mantıksal operatörünün geliştirilmiş versiyonudur.
    eğer operand ve operand2 sonucu True dönerse return value döner
    eğer operand ve operand2 sonucu False ise ve fallback girili ise fallback döner aksi halde operand ve operand2'Nin sonucu döner
    logical_not, operand ve operand'nin sonucunu tersine çevirir."""

    if logic_not:
        return return_value if not(operand and operand2) else fallback
    return return_value if (operand and operand2) else fallback

def extended_or(operand:Any,operand2:Any,return_value:Any,fallback:Any=None,logic_not:bool=False) -> Any:

    if logic_not:
        return return_value if not (operand or operand2) else fallback
    return return_value if (operand or operand2) else fallback

def extended_xor(operand:Any,operand2:Any,return_value:Any,fallback:Any=None,logic_not:bool=False) -> Any:

    result = bool(operand) ^ bool(operand2)
    return return_value if result ^ logic_not else fallback