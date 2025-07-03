# ----------------------------
# 📌 1. `.sort()` METODU TANIMI
# ----------------------------

# `.sort()` listelere özgü bir metottur.
# Bu metodun amacı, bir listenin elemanlarını yerinde (in-place) sıralamaktır.
# Listenin kendisini değiştirir, yeni bir liste döndürmez!
# Dolayısıyla "eager evaluation" (anında işlem) mantığıyla çalışır ve daha hızlıdır.

# 🔎 SÖZDİZİMİ:
# list.sort(key=None, reverse=False)
# - key: her bir öğe için karşılaştırma yapılırken kullanılacak fonksiyonu belirtir (örn: len, str.lower vs.)
# - reverse: True verilirse büyükten küçüğe sıralama yapar.

# 🔄 KULLANDIĞI ALGORİTMA: Timsort
# - Python 3.x’te hem `list.sort()` hem de `sorted()` fonksiyonu Timsort algoritmasını kullanır.
# - Bu algoritma “merge sort” + “insertion sort” kombinasyonudur.
# - Zaten sıralı verileri çok hızlı işler (adaptive)

# 🧠 ÖZEL METODLARLA İLİŞKİSİ:
# - `.sort()` metodu, elemanlar arasında karşılaştırma yapmak için şu özel metodları (magic method) kullanır:
#   - __lt__ (küçüktür)
#   - __le__ (küçük eşittir)
#   - __gt__ (büyüktür)
#   - __ge__ (büyük eşittir)
#   - __eq__ (eşittir)
# - Eğer bu metodlar tanımlı değilse, sıralama sırasında hata alınır.

# 🧪 ÖRNEK:

class Kisi:
    def __init__(self, ad, yas):
        self.ad = ad
        self.yas = yas

    def __repr__(self):
        return f"{self.ad} ({self.yas})"

    def __lt__(self, diger):
        return self.yas < diger.yas

k1 = Kisi("Ali", 25)
k2 = Kisi("Zeynep", 30)
k3 = Kisi("Emir", 20)

kisiler = [k1, k2, k3]
kisiler.sort()  # yaşa göre sıralar (__lt__ kullanılır)
print(kisiler)
# Çıktı: [Emir (20), Ali (25), Zeynep (30)]

# -----------------------------
# 📌 2. `sorted()` FONKSİYONU
# -----------------------------

# `sorted()` her türlü iterable (liste, tuple, set, sözlük, vs.) üzerinde çalışır.
# Yeni sıralı bir liste döndürür, orijinal veriyi değiştirmez.
# Dolayısıyla "lazy evaluation" gibi davranır ve daha esnektir.

# 🔎 SÖZDİZİMİ:
# sorted(iterable, key=None, reverse=False)

# 🧠 `.sort()` gibi aynı özel metodları kullanır (__lt__ başta olmak üzere)

# 🔄 ÖRNEK:
isimler = ["ahmet", "Zeynep", "mehmet", "Fatma"]
sirali = sorted(isimler, key=str.lower)  # Büyük/küçük harf farkı göz ardı edilir
print(sirali)
# Çıktı: ['ahmet', 'Fatma', 'mehmet', 'Zeynep']

# ------------------------
# 🧾 NEDEN EAGER (İn-place)?
# ------------------------

# `.sort()` metodu listeyi yerinde değiştirir çünkü:
# - Bellek tasarrufu sağlar
# - Performans olarak `sorted()`'a göre daha hızlıdır
# - Listenin değiştirilmesinin sorun olmadığı durumlarda tercih edilir

# Ama `sorted()` fonksiyonu:
# - Girdiyi değiştirmez, çıktıyı döner (fonksiyonel programlama için ideal)
# - Her türden iterable ile çalışır (list dışı: set, tuple vs.)


# ===============================================
# 🔧 .sort() METODUNUN DÜŞÜK SEVİYE ANALİZİ
# ===============================================

# Örnek:
# lst = [3, 1, 2]
# lst.sort()

# Python içsel olarak bunu şöyle işler:
# 1. `list` türünün `sort` metodunu bulur:
#    type(lst).__dict__['sort']  →  list.__dict__['sort']

# 2. elde edilen bir bound method'dur çünkü sort() bir methoddur bu nedenle çağrılması gerekir
#   type(lst).__dict__['sort'].__call__(l,key=None, reverse=False)
#   l: sort,instance method olduğundan dolayı bir tane sınıf örneğine ihtiyaç duyar o örnek üzerinde çalışır

# 💬 Bu işlem *in-place* çalışır → listeyi yerinde sıralar
# ➕ Ek parametreler (`key`, `reverse`) varsa bunlar da doğrudan metoda gönderilir

# ===============================================
# 🧠 NOT: .sort() sadece list türünde tanımlıdır!
# ===============================================
# Çünkü bu metot sadece `list` sınıfının __dict__’inde yer alır.


# ===============================================
# 🧠 .sort() ile __lt__ (less-than) ilişkisi
# ===============================================
# Liste elemanlarını sıralarken her iki öğe arasında __lt__ (veya varsa __gt__) çağrılır.

# Örneğin: lst = [A(), A()]
# Python sıralama yaparken:
#    lst[0].__lt__(lst[1]) veya
#    type(lst[0]).__dict__['__lt__'].__call__(lst[0], lst[1])


# ===============================================
# 🧭 Sıralama Algoritması: Timsort
# ===============================================
# Python’un `.sort()` ve `sorted()` fonksiyonları **Timsort** algoritması kullanır.
# – Hızlı, kararlı ve kısmen sıralı verilerde çok etkilidir.

# ===============================================
# 🧬 sorted() FONKSİYONUNUN DÜŞÜK SEVİYE ANALİZİ
# ===============================================

# Örnek:
# sorted([3, 1, 2])

# İçsel çözümleme:
# 1. sorted fonksiyonu `__iter__` üzerinden tüm elemanları okur
# 2. Yeni bir listeye kopyalar → yeni bir liste yaratır (in-place değildir!)
# 3. Bu yeni listeye `.sort()` uygular

# Düşük seviyede:
# iterable → list(iterable) → list.sort(key=..., reverse=...) → sonucu döndür

# sorted(lst, key=..., reverse=...)
# =>
# tmp = list(lst)
# tmp.sort(key=..., reverse=...)
# return tmp


# ===============================================
# 🧠 sorted vs sort farkı:
# ===============================================
# list.sort() → listeyi yerinde sıralar, None döner (in-place)
# sorted()    → yeni sıralı bir liste döner (non-destructive)


# ===============================================
# 🔍 sorted fonksiyonunun özel metodlarla ilişkisi:
# ===============================================
# Eğer objelerin kendi karşılaştırma (__lt__) metotları yoksa TypeError verir.
# Bu yüzden kendi sınıflarında karşılaştırma tanımlamak önemlidir.

# sorted([obj1, obj2]) → obj1.__lt__(obj2)

# Tam çözümleme:
#    type(obj1).__dict__['__lt__'].__get__(obj1, type(obj1))(obj2)


# ===============================================
# 🔑 Özelleştirilmiş Sıralama İçin:
# ===============================================
# def by_len(x): return len(x)
# sorted(["a", "abc", "ab"], key=by_len)


class A:
    def __init__(self, name):
        self.name = name

    def __lt__(self, other):
        # Sıralama karşılaştırması: isimler arasında karşılaştırma
        return self.name < other.name

    def __iter__(self):
        # Sadece örnek amaçlı iterable yapmak için
        yield from self.name

    def __repr__(self):
        return f"A({self.name})"

# ---------------------------------------------------
# 🔹 sorted(a): Burada sorted, 'a' nesnesinin iterable olup olmadığını kontrol eder.
# Eğer a __iter__() metodunu tanımlamışsa, iter(a) çalışır yani a.__iter__()
# sorted(), dönen iterable'dan elemanları alıp sıralar.
a = A("zeynep")
print(sorted(a))  # A.__iter__() çalışır → 'z', 'e', ...

# ---------------------------------------------------
# 🔹 sorted((a, b)): Burada sorted, bir tuple olan (a, b) üzerinde çalışır.
# Yani iter((a, b)) → tuple.__iter__() çalışır.
# İçerideki a ve b nesneleri sırayla karşılaştırılır ama onların __iter__() metodları çağrılmaz.
b = A("ahmet")
print(sorted((a, b)))  # tuple'dan a ve b alınır, A.__lt__() ile sıralanır

# ---------------------------------------------------
# 🔹 sorted(list_of_custom_objects): Bu kullanımda da list.__iter__() çalışır.
# İçerideki her nesne __lt__, __gt__ gibi karşılaştırma metodları ile sıralanır.
l = [A("mehmet"), A("ayşe")]
print(sorted(l))  # Liste iterable olduğu için list.__iter__() çalışır

# ---------------------------------------------------
# 🔍 Özet:
# - sorted(X): Önce X'in __iter__() metoduna bakılır.
# - Eğer X iterable değilse TypeError fırlatılır.
# - X iterable ise, elemanlar alınır ve karşılaştırma yapılır.
# - Sıralama için elemanların __lt__, __gt__ gibi metodları kullanılır.
# - Eğer Sınıfta __lt__ veya __gt__ tanımlı değilse karşılaştırma yapılamaz hata alınır

