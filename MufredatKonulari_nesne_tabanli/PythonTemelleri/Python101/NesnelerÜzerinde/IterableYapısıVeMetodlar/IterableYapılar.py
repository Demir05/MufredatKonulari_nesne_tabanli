# ============================================
# 🔄 PYTHON'DA ITERABLE YAPILAR – TEMEL BİLGİ
# ============================================

# 📌 Iterable nedir?

# Iterable, "üzerinde teker teker dolaşılabilen" (yani döngü ile okunabilen) bir yapıdır.
# Örnek: list, tuple, dict, str gibi yapılar iterable’dır.
# Bu yapıların amacı for döngüsü gibi yapılarla verileri sıralı şekilde işlemektir.

# 🔍 Peki bir nesne nasıl iterable olur?

# 1️⃣ __iter__() metoduna sahip olması gerekir.
#    → obj.__iter__() çağrıldığında bir iterator nesnesi döndürmelidir.
#
# VEYA:
#
# 2️⃣ __getitem__() metoduna sahip olması gerekir.
#    → obj[i] şeklinde indisle erişimle eleman dönebiliyorsa, Python bunu iterable kabul eder. hatırlarsan __getitem___, nesneyi indekslenebilir (subscriptable) yapar.
#    → Ancak bu durumda sıfırdan (index 0'dan) başlayarak sırasıyla deneme yapar ve
#      IndexError alana kadar devam eder.
#    → Bu yöntem modern Python'da önerilmez, ama hâlâ geçerli bir yoldur.


# 📌 Iterator nedir?

# Iterator, next() fonksiyonu ile sıradaki elemanı verebilen bir nesnedir.
# Bir iterable'ı "devam ettirebilmek" için iterator gerekir.
# Teknik olarak:
# - __iter__() metoduna sahiptir → self döndürür.
# - __next__() metoduna sahiptir → sıradaki elemanı döndürür, bitince StopIteration hatası fırlatır.


# ============================================
# 🔁 __iter__() METODU
# ============================================

# Amaç:
# Bir nesneyi iterable yapmak için kullanılır.
# Python'da bir nesne, for döngüsünde ya da iter() fonksiyonuyla kullanıldığında bu metod çağrılır.

# Ne yapar?
# → Bir "iterator" nesnesi döndürmek zorundadır.
# Bu iterator nesnesi __next__() metoduna sahip olmalıdır.

# Nerede çağrılır?
# → iter(obj) çağrıldığında
# → for x in obj: ifadesinde otomatik çağrılır
# → list(obj), tuple(obj), set(obj) gibi dönüştürmelerde

# Sözdizimi:
# def __iter__(self):
#     return Iterator

# NOT:
# Eğer bir sınıf hem __iter__ hem de __next__ içeriyorsa, kendisi bir iterator’dır.

# ===================================================
# 🔍 __iter__() METODU – ÇAĞRI ZİNCİRİ (RESOLUTION)
# ===================================================

# Örnek: iter(obj)

# 1) Python iter(obj) çağrıldığında:
#    → obj.__iter__ bir attribute erişimidir
#    → __getattribute__ metodu tetiklenir

# 2) Attribute çözümlemesi:
#    → type(obj).__getattribute__(obj, '__iter__')

# 3) bulunan '__iter__' bir descriptor :
#    → descriptor.__get__(obj, type(obj)) → bound method elde edilir

# 4) En son:
#    → bound_method() → __iter__() çağrılır, bir iterator döner


# ============================================
# 🔄 __next__() METODU
# ============================================

# Amaç:
# Iterator nesnesi üzerinde sıradaki değeri döndürmek için kullanılır.
# __iter__() metoduyla dönen nesneye ait olmalıdır.

# Ne yapar?
# → Her çağrıldığında sıradaki değeri döndürür.
# → Eleman kalmadığında StopIteration hatası fırlatır.

# Nerede çağrılır?
# → next(iterator) çağrıldığında
# → for döngüsü her adımda otomatik olarak çağırır

# Sözdizimi:
# def __next__(self):
#     return value

# NOT:
# Bir nesne iterator sayılabilmek için hem __iter__ hem de __next__ metodlarına sahip olmalıdır.


# Metod Çözümleme Zinciri (Resolution Chain):

# Örnek: next(iterator)
# 
# __next__() çağrısı bir attribute erişimidir:
# obj.__class__.__getattribute__(obj, '__next__')
#
# -> obj.__class__.__dict__['__next__'] aranır
#
# -> descriptor olduğundan dolayı __get__ uygulanır
#
# -> bound method elde edilir: obj.__class__.__dict__['__next__'].__get__(obj, obj.__class__)
#
# -> Son olarak bound method çağrılır: bound_method.__call__()


# Örnek kullanım:
class A:

    def __init__(self,value):
        self.value = iter(value)
    def __iter__(self):
        return self # zaten nesneye veri verdiğimizde bir iterator döndürdük sınıfın kendisi iterator'dır  bu nedenle return self dedik
    def __next__(self):
        return next(self.value)
    

a = A([1,2,3,4,5])

print(
    a.__class__.__dict__['__next__'].__get__(a, A),  # <bound method A.__next__ of <__main__.A object at 0x...>> __get__ metodu, a nesnesine bağlanır
    a.__class__.__dict__['__next__'].__get__(a, A).__call__()  # 1, __call__ metodu ile çağrılır

)


# ============================================
# 🔍 KISACA FARKLARI

# __iter__   → iterable başlatır, bir iterator döner
# __next__   → iterator'dan sıradaki değeri döndürür
# __getitem__→ index ile erişim sağlar, __iter__ yoksa iterable gibi çalışabilir

# Yani:
# Iterable nesne → __iter__() → Iterator nesne → __next__()
# Alternatif olarak: __getitem__(i) + IndexError → Iterable davranışı

# ============================================
# Örnek kullanım sırası (for döngüsü için):
# 1) obj.__iter__() → iterator
# 2) iterator.__next__() → eleman
#    ...
# 3) StopIteration → döngü biter

# __iter__ yoksa:
# 1) obj.__getitem__(0), obj.__getitem__(1), ...
# 2) IndexError → döngü biter


from collections.abc import Iterable, Iterator

class A:
    def __init__(self,data):
        self.data = data
        
    def __iter__(self):
        return iter(self.data)


a =A([1,2,3,4,5])

print(isinstance(a, Iterable))  # True, çünkü __iter__() var
print(isinstance(a, Iterator))  # False, çünkü __next__() yok


class B:
    def __init__(self,data):
        self.data = iter(data)
        
    def __iter__(self):
        return self

    def __next__(self):
        return next(self.data)

b =B([1,2,3,4,5])

print(isinstance(b, Iterable))  # True, çünkü __iter__() var

print(isinstance(b, Iterator))  # True, çünkü __next__() var

next(b)




# =====================================================
# 🔁 iter() BUILTIN FONKSİYONU – TANIM ve KULLANIM
# =====================================================

# 📌 iter() fonksiyonu, bir nesneden bir iterator (yineleyici) oluşturur.
# Python'da bir iterable'dan for döngüsüyle veri okumak istiyorsan önce iter() çağrılır.

# Teknik olarak:
# → iter(obj) çağrıldığında: obj.__iter__() çalıştırılır ve bir iterator nesnesi döner

# 🔍 Örnek:
# liste = [1, 2, 3]
# itr = iter(liste)
# next(itr) → 1

# =====================================================
# 📘 KULLANIM ŞEKİLLERİ
# =====================================================

# 1️⃣ iterable nesne üzerinden:
#    iter(iterable)
#    → iterable.__iter__() çağrılır

# 2️⃣ sentinel (bekçi değeri) ile:
#    iter(callable, sentinel)
#    → callable() çağrılır, sonuç sentinel olana kadar devam eder

# 🔍 Örnek:
# f = open("dosya.txt")
# for satir in iter(f.readline, ''):  # readline() '' döndürene kadar
#     print(satir)

# ➕ Bu teknik, dosya okuma veya stream verilerde oldukça kullanışlıdır.


# =====================================================
# 🔄 METOD ÇÖZÜMLEMESİ (ATTRIBUTE RESOLUTION)
# =====================================================

# Python şu zinciri izler:
# 1) iter(obj)
# 2) → type(obj).__getattribute__(obj, '__iter__')
# 3) → descriptor ise __get__(obj, type(obj)) ile bound edilir
# 4) → bound_method() → __iter__() çalışır → iterator döner

# Eğer __iter__ yoksa → __getitem__(i) denenir (i=0,1,...)


# =====================================================
# ⛓️ itertools.tee() – İKİ KOPYA OLUŞTURMA
# =====================================================

# 📌 itertools.tee(iterable, n=2)
# iterable'dan n adet bağımsız iterator oluşturur (default 2 tanedir).

# Bu iteratorlar aynı kaynak veriyi paylaşır, ancak birbirinden bağımsız ilerler.

# ⚠️ Uyarı:
# - Hafıza kullanımı artar: tee(), arka planda tampon (cache) kullanır.
# - Yani bir iterator ilerlerse, diğerleri için o değerler RAM’de tutulur.

# 🔍 Örnek:
# from itertools import tee
# itr1, itr2 = tee([1, 2, 3])
# next(itr1) → 1
# next(itr2) → 1 (bağımsız kopya)

# Yani:
# - tee(), iter() gibi iterable alır
# - ama çıktı olarak birden fazla "aynı kaynağa dayalı" iterator üretir
# - iteratorlar farklı hızda ilerleyebilir

# Kullanım yeri:
# - Aynı iterable üzerinde birden fazla for döngüsü başlatmak
# - Fonksiyonlara aynı iterable'ı paralel biçimde vermek

# 🔄 Arka planda iter() kullanır çünkü tee() de iterable'dan iterator üretir.

# Sözdizimi:
# itertools.tee(iterable, n=2) → (it1, it2, ..., itN)