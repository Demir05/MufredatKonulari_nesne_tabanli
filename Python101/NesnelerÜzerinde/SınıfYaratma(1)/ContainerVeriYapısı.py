# 📦 __contains__() metodu & Container Veri Yapısı
# 📌 Container Veri Yapısı Nedir?
# Container (taşıyıcı) veri yapısı, içinde birden fazla öğe tutabilen yapılardır.
# list, tuple, dict, set gibi yapılar → container’dır.
# Bunların ortak özelliği: __contains__, __iter__, __getitem__ gibi özel metodlarla donatılmış olmalarıdır.

# 🧠 Container olmanın temel kriterleri:
# 1. __contains__ metodunu desteklemesi: → "x in obj" ifadesine cevap verebilmesi
# 2. __iter__ veya __getitem__ gibi erişim metotlarının tanımlanmış olması
# 3. İçinde birden fazla nesne saklayabilecek yapı olması
    


# ✅ 2. collections Modülü nedir?
# -------------------------------
# "collections", Python'un standart kütüphanesindeki bir modüldür.
# İçerisinde iki tür yapı barındırır:

# 🔹 a) Gerçek veri yapıları:
# - Counter       → Eleman sayar
# - defaultdict   → Varsayılan değerli dict
# - deque         → Çift yönlü kuyruk
# - OrderedDict   → Sıralı dict
# - ChainMap      → Çoklu dict'i birleştirir

from collections import Counter, defaultdict, deque, OrderedDict, ChainMap

# 🔹 b) Soyut sınıflar (collections.abc):
# Bunlar sadece interface gibi davranır; kodun davranışını kontrol eder.
# Eğer bir sınıf bu soyut sınıflardan kalıtım alırsa, belirli metotları override etmek zorundadır.

from collections.abc import Container, Iterable, Mapping, Sequence

# Örnek:
class MyC:
    def __contains__(self, item):
        return True

print(isinstance(MyC(), Container))  # True → Çünkü __contains__ tanımlı

# ✅ 3. Fark Özeti:
# -----------------

# list bir container’dır çünkü eleman tutar ve gerekli metodları içerir.
# Ancak list, collections modülünden gelmez. C dilinde tanımlanmış yerleşik (built-in) bir türdür.

# collections modülü, ekstra veri yapıları (Counter, deque, vs.) sunar
# ayrıca soyut sınıflarla Python'da veri protokollerini standartlaştırır.

# ✅ 4. Sonuç:
# -----------------
# - list → bir container’dır (ama collections'dan gelmez)
# - Counter → bir container’dır ve collections modülünden gelir
# - collections.abc.Container → bir soyut sınıftır, sadece __contains__ metodunu kontrol eder

# 📌 collections bir veri türü değil, modül adıdır!




# 🔍 __contains__ metodu, Python'da `in` anahtar kelimesiyle(üyelik operatörü) yapılan arama işlemlerini kontrol eden özel (dunder) bir metottur.
# Bu metot bir nesne içinde bir eleman olup olmadığını kontrol eder:
# Örneğin: x in obj → __contains__ çağrılır

# __contains__ metodu sayesinde, nesnelerini `in` operatörü ile kontrol edilebilir (searchable) hale getirirsin.

# 🔗 Python'un Çağrı Zinciri (x in obj için):
# "elma" in obj
# ↓
# → type(obj).__contains__(obj, "elma")
# ↓
# → Eğer __contains__ tanımlıysa doğrudan çağrılır
# ↓
# → Yoksa, Python otomatik olarak __iter__ veya __getitem__ metodlarını denemeye başlar (fallback sistemi)
#   __contains__ metodu override edilmezse, Python sırasıyla:
#       1) __iter__ → iterasyonla bakar
#       2) __getitem__ → indeksleri sırasıyla kontrol eder
#       Bu fallback sistemini anlamak önemlidir.
# ↓
# → Eğer onlar da yoksa → TypeError

# 🧾 Sözdizimi:
# def __contains__(self, item) -> bool:
#     return item in self._veri

# ✅ Kullanım Amaçları:
# - özel sınıflarda arama/membership işlemlerini kontrol etmek
# - belirli koşullara göre erişim izni vermek
# - erişim öncesi güvenlik, filtre, kontrol gibi davranışlar eklemek

from collections import namedtuple as np

Hatalar = np("Hatalar",["Veri"])

hata = Hatalar(
    Veri= lambda value: TypeError(f"Doğrudan Özellik:{value} Manipüle edilemez")
)

class AlısverisSepeti:

    def __init__(self):
        object.__setattr__(self,"sepet",{})

    def __contains__(self, item):
        return item in self.sepet

    def __setitem__(self, key, value):
        self.sepet[key] = value
        print(f"{key} eklendi !")

    def __getitem__(self, item):
        return self.sepet[item]

    def __delattr__(self,item):
        raise hata.Veri(item)

    def __setattr__(self, name, value):
        raise hata.Veri(name)

    def __repr__(self):
        attrs= ",".join(f"{key!r}:{value}" for key,value in self.__dict__.items())
        return f"{type(self).__name__}({attrs})"

sepetim = AlısverisSepeti()

sepetim["elma"] = 5

print( "elma" in sepetim) #burda in kontrolünü __contains__ metodu sayesinde yaptık

print(dir(sepetim))

print(repr(sepetim))