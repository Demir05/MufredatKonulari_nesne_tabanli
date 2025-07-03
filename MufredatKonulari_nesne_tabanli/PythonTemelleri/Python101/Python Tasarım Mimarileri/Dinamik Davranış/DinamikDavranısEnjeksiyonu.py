# ===========================================================================
# 🧠 DİNAMİK DAVRANIŞ ENJEKSİYONU NASIL TASARLANIR? (Teori + Pratik)
# ===========================================================================

# 🎯 AMAÇ:
# Bir sınıfa, o sınıfın kodunu değiştirmeden dışarıdan operatör/metot
# gibi davranışları otomatik ve modüler şekilde eklemek.

# ===========================================================================
# 🛠️ NASIL TASARLANIR? (GENEL ADIMLAR)
# ===========================================================================

# 1️⃣ Davranışı temsil edecek fonksiyonları bir "template" gibi tanımla
#     - closure veya factory fonksiyonları kullan (ör: def make_op(name))

# 2️⃣ Operatör/method gibi davranışları string olarak listele
#     - "__add__", "__sub__" gibi

# 3️⃣ Hedef sınıfa bu davranışları tek tek ekle
#     - setattr() veya doğrudan class üzerinde tanımla

# 4️⃣ Davranışı tanımlarken type safety’ye dikkat et
#     - Tip ipuçları, return değerleri, args/kwargs uyumu

# 5️⃣ Enjeksiyonun idempotent olmasını sağla (birden fazla eklenmesin)
#     - Önceden var mı kontrol et: `if attr in vars(cls): continue`

# ===========================================================================
# ⚠️ DİKKAT EDİLMESİ GEREKENLER
# ===========================================================================

# ❗ 1. Closure Capture Sorunu:
#     Döngü içinde fonksiyon tanımlarken değişkenin kapanış değerini yanlış
#     yakalamamak için inner function factory kullan (def make_func(op): ...)

# ❗ 2. Yan Etki (Mutability):
#     __iadd__ gibi in-place operatörler orijinal objeyi değiştirdiği için
#     dikkatli olunmalı — lambda kullanılamaz, def şart

# ❗ 3. Tip Uyumu:
#     TypeVar T kullan, hem giriş sınıfını hem çıkışı güvence altına al

# ❗ 4. Override Riskine Karşı Koruma:
#     Eğer sınıfta zaten o operatör tanımlıysa üzerine yazma!

# ❗ 5. Geriye dönük okunabilirlik:
#     Eklenen metotların açıklamaları (docstring) varsa çok daha iyi olur

# ===========================================================================
# ✅ ÖRNEK: @inject_basic_ops dekoratörü ile + ve - ekleyelim
# ===========================================================================

from typing import TypeVar, Callable, Any
import operator

T = TypeVar("T")

def inject_basic_ops(target: str, ops: tuple[str, ...]) -> Callable[[type[T]], type[T]]:
    def make_function(opfunc: Callable[[Any, Any], Any]):
        def method(self: T, other: T) -> T:
            result = opfunc(getattr(self, target), getattr(other, target))
            return type(self)(result)
        return method

    def decorator(cls: type[T]) -> type[T]:
        for opname in ops:
            if opname in vars(cls):  # override etme!
                continue
            func = make_function(getattr(operator, opname[2:]))  # "__add__" -> "add"
            setattr(cls, opname, func)
        return cls
    return decorator

# ===========================================================================
# 🧪 UYGULAMA
# ===========================================================================

@inject_basic_ops("value", ("__add__", "__sub__"))
class Point:
    def __init__(self, value):
        self.value = value

a = Point(10)
b = Point(4)
print((a + b).value)  # ➜ 14
print((a - b).value)  # ➜ 6

# ===========================================================================
# 🎯 ÖZET:
# - Sınıfa sonradan davranış ekledik
# - Tüm yapı tek bir decorator ile kontrol ediliyor
# - TypeVar, getattr, operator modülü birleşti
# - Bu, Python’un metaprogramming gücünün temiz bir örneği
# ===========================================================================
