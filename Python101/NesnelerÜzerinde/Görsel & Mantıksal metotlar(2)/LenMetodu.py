# __len__() METODU

# Python'da __len__() metodu, bir nesnenin uzunluğunu belirtmek için kullanılır.
# Bu metod sayesinde bir nesne, len() fonksiyonu ile birlikte kullanılabilir.
# Örneğin: len(obj) → obj.__len__()

# __len__() → nesnenin içerdiği eleman sayısını belirtir (genellikle iterable yapılar içindir)

# 🔹 Liste, tuple, set, dict, str gibi veri yapılarında bu metod tanımlıdır.
# 🔹 Kendi sınıfında da __len__() metodunu override ederek len(obj) davranışını özelleştirebilirsin.

# ===============================================
# 📌 SÖZDİZİMİ:
# def __len__(self) -> int:
#     return eleman_sayısı
# ===============================================

# NOT:x
# __len__() metodu her zaman integer döndürmelidir (int)
# Eğer float, str, None gibi bir değer döndürürsen TypeError alırsın

# ===============================================
# 📌 ÖRNEK:
class Sepet:
    def __init__(self, urunler):
        self.urunler = urunler

    def __len__(self):
        return len(self.urunler)

s = Sepet(["elma", "armut", "muz"])
print(len(s))  # 3

# ===============================================
# 🔍 __len__() METOD ÇÖZÜMLEMESİ

# Python, len(obj) ifadesini gördüğünde şu adımları izler:

# 1) len(obj) ifadesi:
#    → type(obj).__getattribute__(obj, '__len__')  # metod çözümlemesi yapılır

# 2) Eğer __len__ metodu varsa:
#    → python, type(obj).__dict__['__len__'] aranır
#    -> type.__len__'in descriptor olduğu için __get__ uygulanır
#    → bound method elde edilir: type.__len__.__get__(obj, type(obj))

# 3) Eğer __len__ metodu yoksa:
#    → TypeError: object of type 'X' has no len()

# ===============================================
# NOT:
# __len__ metodu da bir dunder metottur.
# __getattribute__ kullanılarak çözümlenir.
# → MRO (Method Resolution Order) zincirinde yukarı doğru aranabilir.


# ===============================================
# 📌 bool() ile ilişkisi:

# Eğer obj.__bool__() tanımlı değilse, Python bool(obj) çağrısında __len__() metodunu çağırır:
# → bool(obj) → __bool__() yoksa → __len__() > 0 → True

# Örnek:
class Sayilar:
    def __init__(self, liste):
        self.liste = liste

    def __len__(self):
        return len(self.liste)

s = Sayilar([])
print(bool(s))  # False → çünkü len(s) == 0


class Veri:

    def __init__(self):
        self.data = dict()

    def __len__(self):
        return len(self.data) # len(...) ifadesi,bir expression'dır python,ifade bekler bu nedenle bu metodda return ifadesi olmalıdır

v = Veri()
print(len(v))  # 0
print(bool(v))  # False → çünkü len(v) == 0

print(
    v.__class__.__getattribute__(v, "__len__").__call__(),
    type(v).__dict__['__len__'].__get__

)
