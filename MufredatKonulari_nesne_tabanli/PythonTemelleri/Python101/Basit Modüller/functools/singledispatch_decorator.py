# 📘 @singledispatch — SÖZEL TANIM
# -------------------------------------
# `@singledispatch`, Python'da bir fonksiyonu "generic function" haline getirir.
# Yani: aynı isimdeki bir fonksiyon, çağırılan argümanın türüne göre farklı şekilde çalışabilir.
# Bu yapı, 'type-based polymorphism' sağlar.
# Fonksiyonun davranışı, sadece **ilk argümanın türüne göre** belirlenir.
# Eğer belirli bir tür için özel bir versiyon tanımlanmazsa, varsayılan (decorated) versiyon çalışır.
import functools




# -------------------------------------
# ⚙️ ÇALIŞMA MANTIĞI (adım adım):
# 1) `@singledispatch` fonksiyonu sarar ve bir dispatcher nesnesi döner.
# 2) Bu dispatcher, `.register(cls)(func)` ile yeni türleri kaydeder.
# 3) `dispatcher(obj)` çağrıldığında:
#    - obj'nin türü kontrol edilir.
#    - En uygun (doğrudan ya da MRO zincirinde en yakın) kayıtlı tür aranır.
#    - O türe bağlı fonksiyon çağrılır.
#    - Eğer tür kayıtlı değilse, varsayılan decorated fonksiyon çalıştırılır.

# -------------------------------------
# 🧩 ATTRIBUTE'LARI / METOTLARI:
# dispatcher.register(cls)(func) :
#     - cls türüne özel fonksiyon tanımlar. cls bir class (int, str, list vs.) olabilir.
#     - func argüman isimleri önemli değildir, çünkü dispatcher türden eşleştirir.
#     - Aynı dispatcher’a farklı türler için farklı fonksiyonlar tanımlayabilirsin.
#
# dispatcher.dispatch(cls) :
#     - Belirtilen tür için hangi fonksiyonun çalıştırılacağını döner (fonksiyon objesi).
#     - Bu, fonksiyonu gerçekten çalıştırmaz.
#
# dispatcher.registry :
#     - Tüm kayıtlı tür-fonksiy on eşleşmelerini içeren bir sözlük (mappingproxy).
#     - {type: function}
#
# dispatcher.__wrapped__ :
#     - Orijinal (dekoratör uygulanmamış) fonksiyonun kendisini döner.
#
# dispatcher.__annotations__, __doc__ :
#     - Tanımlıysa, orijinal fonksiyonun docstring'i ve tür ipuçlarıdır.

# -------------------------------------
# 🎯 Nerede Kullanılır?
# - Farklı veri tiplerinde aynı fonksiyon adıyla ama farklı işlem yapılmak istenirse.
# - JSON serileştirme, özel string temsilleri, kontrol akışları vb.
# - İf-elif-else zincirlerinden kaçınmak için.
# - API tasarımlarında temiz genişletilebilirlik için.

# -------------------------------------
# 🚫 Nerede KULLANILMAZ?
# - İlk parametresi olmayan fonksiyonlarda (çünkü type kontrolü için 1 parametre gerekir)
# - Sınıf metotlarında doğrudan kullanılamaz (onun için: @singledispatchmethod vardır)
# - Performans kritik yerlerde uygun değildir çünkü arka planda tür araması yapılır.

# -------------------------------------
# 🧠 Ekstra Bilgi:
# - MRO: dispatch işlemi sırasında, Python sınıfının Method Resolution Order'ı (MRO) göz önünde bulundurulur.
#   Bu, kalıtım yapısında en uygun eşleşmeyi bulur.

# 📦 Temsili @singledispatch decorator mimarisi
class SingleDispatchFunction:
    def __init__(self, default_func):
        # 🎯 Varsayılan fonksiyon (type fallback)
        self.default_func = default_func
        self.registry = {}  # 🗃️ Tip -> Fonksiyon eşlemesi

    def register(self, typ):
        # 🧩 Yeni bir tip için özel fonksiyon kaydeder
        def wrapper(func):
            self.registry[typ] = func
            return func
        return wrapper

    def dispatch(self, typ):
        # 🔍 İlgili tip için hangi fonksiyonun çağrılacağını verir
        return self.registry.get(typ, self.default_func)

    def __call__(self, arg, *args, **kwargs):
        # 🚀 Çağırılınca: tip’e göre uygun fonksiyon çalıştırılır
        fn = self.dispatch(type(arg))
        return fn(arg, *args, **kwargs)

# 🎨 Kullanım (real-life usage gibi)
@SingleDispatchFunction
def describe(x):
    return f"Generic: {type(x).__name__}"

@describe.register(int)
def _(x):
    return f"Tam sayı: {x}"

@describe.register(str)
def _(x):
    return f"Metin: {x}"

# 🎬 Deneme
print(describe(42))         # ➜ Tam sayı: 42
print(describe("merhaba"))  # ➜ Metin: merhaba
print(describe(3.14))       # ➜ Generic: float



from functools import singledispatch

# 🌟 1. Adım: Generic bir fonksiyon tanımlanıyor
@singledispatch
def describe(obj):
    """Verilen objenin tipine göre açıklama döndürür"""
    return f"Genel nesne: {type(obj).__name__}"

# 🌟 2. Adım: Belirli türler için özel fonksiyonlar kaydediliyor
@describe.register(int)
def _(obj):
    return f"Tam sayı: {obj}, karesi: {obj ** 2}"

@describe.register(str)
def _(obj):
    return f"Metin: '{obj}', uzunluğu: {len(obj)} karakter"

@describe.register(list)
def _(obj):
    return f"Liste: {len(obj)} öğe içeriyor, ilk öğe: {obj[0] if obj else 'Boş'}"

# 🌟 3. Adım: Kullanım
print(describe(5))          # int
print(describe("merhaba"))  # str
print(describe([1, 2, 3]))   # list
print(describe(3.14))       # float → default function

# 🌟 4. Adım: dispatcher metadata kullanımı
print("\n--- METADATA ---")
print("Registered Types:", list(describe.registry.keys()))  # ➤ kayıtlı türler
print("float için fonksiyon:", describe.dispatch(float))    # ➤ dispatch sonucu
print("Original func:", describe.__wrapped__)               # ➤ orijinal fonksiyon
print("Docstring:", describe.__doc__)                       # ➤ dokümantasyon



@singledispatch
def duzle(obj):
    """duzler işte."""
    return (f"Bilinmeyen tür -> {obj.__repr__()}",).__iter__()

@duzle.register(tuple)
def _(obj):
    for i in obj:
        if isinstance(i,tuple):
            yield from _(i)
        else:
            yield i

@duzle.register(list)
def _(obj):
    for i in obj:
        if isinstance(i,list):
            yield from _(i)
        else:
            yield i

gen= duzle("a")

for i in gen:
    print(i)

print(duzle.__doc__) # doğrudan -> __wrapped__ fonksiyonun __doc__'unu döndürür.

class Mydispatch:
    def __init__(self, func):
        self.func = func
        self.registry = {}

    def register(self,*types):
        @functools.wraps(self.func)
        def wrapper(new_func):
            self.registry[types] = new_func
            print(self.registry)
        return wrapper

    def dispatch(self,*types):
            if any(type(_type) is self.registry for _type in types):
                return self.registry.get(types)
            return self.func

    def __call__(self,types:tuple= None , *args, **kwargs):
        fonk = self.dispatch(types)
        return fonk(*args, **kwargs)

@Mydispatch
def main():
    return "nope."

@main.register(int,str)
def _():
    return "ok"

print(main((1,"d")))