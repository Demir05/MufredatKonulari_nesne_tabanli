# ---------------------------------------------------------------
# PYTHON'DA BOOLEAN DEĞERİ NASIL BELİRLENİR?
# ---------------------------------------------------------------

# Python'da herhangi bir nesne mantıksal bir bağlamda (örneğin if, while gibi) kullanıldığında
# bu nesnenin 'doğruluk değeri' (truthiness) değerlendirilir. Bu değerlendirme, `bool()`fonksiyonu ile yapılır.

# Bu işleyiş sırasıyla şuna bakar:
# 1. Eğer nesne `__bool__()` metodunu tanımlamışsa → bu çağrılır ve bool değeri alınır.
# 2. Eğer `__bool__` yoksa, `__len__()` metodu aranır → bu metodun sonucu sıfır ise `False`, aksi halde `True` döner.
# 3. Her iki metod da yoksa → Python varsayılan olarak nesneyi `True` kabul eder (fallback mekanizması).

# NOT: `object` sınıfında `__bool__` tanımlı değildir. Bu nedenle kendi sınıfında `__bool__` veya `__len__` tanımlamadıysan
# mantıksal bağlamda `if obj:` gibi bir kullanım her zaman `True` döner.

# Bu dosya bu mekanizmayı test etmek için kullanılır.

# ---------------------------------------------------------------
# __bool__ ve __len__ override edildiğinde nasıl çalışır?
# ---------------------------------------------------------------

class MyBool:
    def __bool__(self):
        print("==> __bool__ çağrıldı")
        return False

class MyLen:
    def __len__(self):
        print("==> __len__ çağrıldı")
        return 0

class Default:
    pass

print("MyBool örneği:")
print(bool(MyBool()))  # False, çünkü __bool__ False döner

print("\nMyLen örneği:")
print(bool(MyLen()))   # False, çünkü __len__ 0 döner

print("\nDefault örneği:")
print(bool(Default())) # True, çünkü __bool__ ve __len__ yok → fallback olarak True

# ---------------------------------------------------------------
# __getattribute__ ile doğrudan erişimde AttributeError alınması
# ---------------------------------------------------------------

# DİKKAT: Eğer `__bool__` metodunu `__getattribute__` ile almaya çalışırsan ve sınıfta bu metod tanımlı değilse,
# Python AttributeError verir çünkü `object` sınıfı bu metodu sağlamaz.

a = Default()
try:
    print(type(a).__getattribute__(a, "__bool__"))
except AttributeError:
    print("❌ __bool__ doğrudan erişimde bulunamadı (beklenen davranış)")

# Ama bool(a) çalışır çünkü Python, __bool__ yoksa __len__'e, o da yoksa fallback'e gider.
print("bool(a) sonucu:", bool(a))

# ---------------------------------------------------------------
# if a: kullanımı aslında bool(a) ile aynıdır
# ---------------------------------------------------------------

# Arka planda `if a:` → `if bool(a):` çağrısı yapılır.
# Yani mantıksal bağlamda nasıl değerlendirileceğini bool() fonksiyonu belirler.
# Bu yüzden __bool__ ya da __len__ tanımlamıyorsan, her nesne True kabul edilir.

# ---------------------------------------------------------------
# TRUTHY & FALSY NEDİR?
# ---------------------------------------------------------------

# Python'da bir nesne mantıksal bağlamda (if, while, bool() vb.) kullanıldığında
# otomatik olarak `True` ya da `False` olarak değerlendirilir.
# Bu değer, nesnenin "doğruluk değeri"dir.

# Bu doğruluk değeri şu şekilde sınıflandırılır:
# 1. TRUTHY: Mantıksal bağlamda True kabul edilen nesneler
# 2. FALSY : Mantıksal bağlamda False kabul edilen nesneler

# ---------------------------------------------------------------
# FALSY ÖRNEKLER
# ---------------------------------------------------------------
# Bu değerler bool() fonksiyonuna (ya da mantıksal bağlama) girdiğinde `False` döner:

falsy_examples = [
    False,              # Boolean False
    None,               # Boşluk değeri
    0,                  # Sayısal sıfır (int, float, complex)
    0.0,
    0j,
    "",                 # Boş string
    [],                 # Boş liste
    {},                 # Boş sözlük
    (),                 # Boş demet
    set(),              # Boş küme
    range(0),           # Boş range
]

# Test edelim:
for value in falsy_examples:
    print(f"Değer: {repr(value):<10} -> bool() sonucu: {bool(value)}")

# ---------------------------------------------------------------
# TRUTHY ÖRNEKLER
# ---------------------------------------------------------------
# Bu değerler mantıksal bağlamda True kabul edilir:

truthy_examples = [
    True,               # Boolean True
    1, 42, -7,          # Sayılar
    "hello",            # Boş olmayan string
    [0],                # Eleman içeren liste (sıfır olsa bile)
    {"a": 1},           # Eleman içeren dict
    (None,),            # Eleman içeren tuple
    {0},                # Eleman içeren set
    range(1),           # Eleman içeren range
]

for value in truthy_examples:
    print(f"Değer: {repr(value):<10} -> bool() sonucu: {bool(value)}")

# ---------------------------------------------------------------
# TRUTHY - FALSY KARŞILAŞTIRMASI
# ---------------------------------------------------------------

# `if`, `while`, `and`, `or`, `not` gibi yapılarda bool() otomatik çağrılır

if []:          # False çünkü [] Falsy
    print("Boş liste True kabul edildi!")
else:
    print("Boş liste False kabul edildi!")  # ✅ Çalışan satır

if [0]:         # True çünkü içinde eleman var
    print("Elemanlı liste True kabul edildi!")  # ✅ Çalışan satır
