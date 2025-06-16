# 🧱 __getitem__() Metodu

# __getitem__ metodu, bir nesneye köşeli parantez ([]) ile erişim yapıldığında çağrılan özel (dunder) metottur.
# Örneğin: obj[key] gibi bir erişim yapıldığında bu metod devreye girer.

# Bu metod, bir objeyi indekslenebilir (subscriptable) yapar.
# Eğer bir sınıf içinde __getitem__ metodu tanımlı değilse, obj[key] ifadesi → TypeError verir.

# 📌 __getitem__ ile __getattribute__ farkı: 
# - __getattribute__ → doğrudan attribute erişimini kontrol eder → obj.attr
# - __getitem__ → key/index bazlı item erişimini kontrol eder → obj[key]
# - __getitem__,örneğin kendisini dict gibi kullanmanı sağlar

# 🔗 Python’un Çağrı Zinciri (obj[key] için):
# obj["isim"]
# ↓
# → type(obj).__getitem__(obj, "isim")   # Python doğrudan __getitem__ metodunu çağırır
# ↓
# → Eğer sınıfta __getitem__ tanımlıysa çalıştırılır
# ↓
# → Yoksa MRO zincirine göre __getitem__ aranır Not: __getitem_ metodu,object ve type sınıfında bulunmaz bu nedenle sınıflar bu metodu manuel override etmeli
# ↓
# → Eğer hiç bulunamazsa → TypeError: 'ClassName' object is not subscriptable hatası alınır

# 🧾 Sözdizimi:
# def __getitem__(self, key: Hashable/index) -> Any:
#     return self.data[key]  self.data list/dict gibi bir yapıdır -> built olan __getitem__ metodu çağrılılır

# 🎯 Kullanım Alanları:
# - Sözlük, liste gibi indekslenebilir veri yapıları oluşturmak
# - JSON benzeri veri yapılarında erişim kontrolü yapmak
# - Nested veri yapıları üzerinden key bazlı erişim tanımlamak
# - Proxy nesneler oluşturmak (başka yapıları sarmalayan sınıflar)

class Demir:

    def __init__(self):
        self.data = "demir"
    def __getitem__(self,index: int):
        return self.data[index]

demir = Demir()
print(demir.__dict__)

print(demir.data)

print(demir.__class__.__getitem__(demir,2))
print(demir[3])
print(demir.data[2])

for i in demir:
    print(i,end=",")  # d, e, m, i, r

# 🧱 __setitem__() Metodu

# __setitem__ metodu, bir item(öğe) "indeks veya anahtar üzerinden" değer atandığında çağrılan özel (dunder) metottur.
# Örneğin: obj[key] = value  gibi bir ifade kullanıldığında bu metot devreye girer.

# Bu metot, indeksleme (indexing) ve anahtar-atama (key assignment) gibi davranışları kontrol etmemizi sağlar.
# __setitem__, __getitem__, __delitem__ gibi metodlar koleksiyon yapılarının temelini oluşturur.

# 📌 __setattr__ ile farkı:
# - __setattr__ → attribute atama işlemini kontrol eder (örnek: obj.x = 10)
# - __setitem__ → indeks/anahtar bazlı veri atama işlemini kontrol eder (örnek: obj["x"] = 10)

# 🔗 Python’un Çağrı Zinciri (obj[key] = val için):
# obj["isim"] = "Ali"
# ↓
# → type(obj).__setitem__(obj, "isim", "Ali")  # Python doğrudan __setitem__ metodunu çağırır
# ↓
# → Eğer sınıfta __setitem__ tanımlıysa o çalışır
# ↓
# → Değilse MRO sırasına göre uygun __setitem__ aranır(object ve type sınıflarında __setitem__ metodu bulunmaz)
# ↓
# → Eğer bulunamazsa → TypeError: 'ClassName' object does not support item assignment hatası alınır

# 🎯 Kullanım Alanları:
# - Sözlük gibi çalışan özel veri yapıları tanımlamak
# - Liste veya tuple benzeri özel yapılar oluşturmak
# - Anahtara özel kontrol ve validasyon kuralları yazmak
# - JSON benzeri veri manipülasyon yapıları üretmek

# 🧾 Sözdizimi:
# def __setitem__(self, key: Hashable/index: int, value: Any) -> None:
#     # özel kurallar yazılabilir
#     self.data[key] = value  # tipik bir kullanım

# ➕ Avantaj: objeyi dict gibi kullanabilmeyi sağlar, daha soyut ve esnek veri kontrolü sunar

# ⚠️ NOT: __setitem__ kullanımı, doğrudan attribute değil item (öğe) manipülasyonudur.
# Genellikle özel veri yapılarında (özellikle kapsülleme, kontrol ve veri yapısı tasarımında) kullanılır.

# Dinamik olarak __setitem__ metodunu runtime esnasında eklemek;

def __setitem__(self,key,value):
    self.__dict__[key] = value

Demir.__class__.__setattr__(Demir,"__setitem__",lambda s,k,v: __setitem__(s,k,v))

demir["data"] = "ozan"

print(demir.__dict__,end="\n\n") # {'data': 'ozan'}

class Veri:
    def __init__(self):
        object.__setattr__(self,"data",{})

    def __setattr__(self, name, value):
        raise TypeError("bu nesne değiştirilemez")

    def __setitem__(self,key,value):
        self.data[key] = value

    def __delattr__(self,name):
        if name == "data":
            raise TypeError("bu nesne silinemez")
    def __getattr__(self, item):
        print(f"{item} öğesi yok")


verim = Veri()

verim["yeni"] = "ozan"
verim["yeni2"] = "doruk"
print(verim.__dict__)
print(verim.data) #{'data': {'yeni': 'ozan', 'yeni2': 'doruk'}}

verim.__class__.__getattribute__(verim,"data")



# 🗑️ __delitem__() Metodu

# __delitem__ metodu, bir nesneden köşeli parantez ile bir eleman silinmek istendiğinde otomatik olarak çağrılan özel (dunder) metottur.
# Örneğin: del obj[key] → bu ifade çalıştığında __delitem__ devreye girer.

# Bu metodu override ederek, kendi veri yapılarında eleman silme davranışını özelleştirebilirsin.

# ❗ Eğer sınıf içinde __delitem__ tanımlı değilse → del obj[key] → TypeError: 'ClassName' object does not support item deletion

# 🔗 Python’un Çağrı Zinciri (del obj[key] için):
# del obj["isim"]
# ↓
# → type(obj).__delitem__(obj, "isim")    # Python doğrudan __delitem__ metodunu çağırır
# ↓
# → Eğer sınıfta __delitem__ tanımlıysa çalıştırılır
# ↓
# → Yoksa MRO zincirine göre __delitem__ aranır
# ↓
# → Bulunamazsa → TypeError hatası alınır

# 🧾 Sözdizimi:
# def __delitem__(self, key: Hashable) -> None:
#     del self._veri[key]

# 🎯 Kullanım Amaçları:
# - dict/list gibi yapıları temsil eden sınıflarda eleman silme davranışı tanımlamak
# - nested yapıların kontrolünü sağlamak
# - veri güncellemelerini kontrollü yapmak (örneğin: log tutmak, sınırlama koymak vs.)

# ✅ Örnek:
class VeriDeposu:
    def __init__(self):
        self._veri = {"isim": "Asya", "yaş": 25}

    def __getitem__(self, key):
        return self._veri[key]

    def __setitem__(self, key, value):
        self._veri[key] = value

    def __delitem__(self, key):
        print(f"'{key}' anahtarı siliniyor...")
        del self._veri[key]


d = VeriDeposu()
del d["yaş"]     # → __delitem__ çalışır
print(d._veri)   # → {'isim': 'Asya'}

# ✔️ Bu yapı sayesinde kendi sınıflarını dict gibi davranır hale getirirsin

# ⚠️ NOT:
# __delitem__, sadece del obj[key] işlemi için geçerlidir.
# del obj.key gibi bir attribute silme işlemi için __delattr__ kullanılır. (bu farklı bir dunder metottur!)

class Sınıfım:

    def __init__(self):
        self.data = {}

    def __delitem__(self,key):
        print(key,"silindi")
        del self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

s = Sınıfım()

s["isim"] = "Asya"

print(s.__dict__)

del s["isim"]

print(s.__dict__)

