# ------------------------------------------------------------
# 🔎 KARŞILAŞTIRMA (ORDERING) OPERATÖRLERİ: GENEL TANIM
# ------------------------------------------------------------

# Python'da '<', '>', '<=', '>=', '==', '!=' gibi karşılaştırma operatörleri,
# aslında nesneler arasında mantıksal bir ilişki kurar.
# Bu ilişki, sınıflar içinde özel metotlarla özelleştirilebilir.

# Bu işlemlerin asıl amacı şudur:
# - Nesneler arası sıralama yapabilmek (örneğin `sorted`)
# - Mantıksal karşılaştırmalarla akış kontrolü sağlamak (örneğin: `if a < b`)
# - Veri yapılarında (set, dict) benzersizlik kontrolü yapmak (`__eq__`, `__hash__` kombinasyonu)
# - Öncelik sıralaması gereken durumlarda (priority queue vs.)

# Örneğin:
#   - Öğrencileri notlarına göre sıralamak
#   - Ürünleri fiyata göre karşılaştırmak
#   - Tarih nesnelerini zaman açısından karşılaştırmak

# ------------------------------------------------------------
# 🧠 PYTHON KARŞILAŞTIRMA ALGORİTMASI NASIL ÇALIŞIR?
# ------------------------------------------------------------

# Python, karşılaştırma işlemlerini şu sırayla ve mantıkla yapar:

# 1️⃣ Önce türler arasında karşılaştırma yapmaya çalışır.
#    Örneğin int ile float doğrudan karşılaştırılabilir:
#    3 < 5.5 → True

# 2️⃣ Farklı veri tipleri (örneğin str ile int) karşılaştırılamaz:
#    "abc" < 123 → TypeError

# 3️⃣ Bazı veri türleri leksikografik karşılaştırma kullanır.
#    Bu, sözlük sırası gibidir (dictionary order):
#    - string'lerde karakter karakter karşılaştırma yapılır.
#    - list, tuple gibi dizilerde eleman bazlı karşılaştırma yapılır.

# Örnek:
#   "ali" < "ayşe"     → True   ('l' < 'y')
#   [1, 2] < [1, 3]     → True   (ilk elemanlar eşit → ikinci elemanlar karşılaştırılır)
#   (1, "ali") < (1, "ayşe") → True

# 4️⃣ Eğer karşılaştırma özel sınıflarda yapılacaksa, Python bu sınıfta tanımlı olan:
#    __lt__, __le__, __gt__, __ge__, __eq__, __ne__ metotlarını çağırır.

# ------------------------------------------------------------
# 🔩 HANGİ METOT HANGİ OPERATÖRÜ TEMSİL EDER?
# ------------------------------------------------------------

#   __lt__(self, other)  → less than          → a < b
#   __le__(self, other)  → less than or equal → a <= b
#   __gt__(self, other)  → greater than       → a > b
#   __ge__(self, other)  → greater or equal   → a >= b
#   __eq__(self, other)  → equal              → a == b
#   __ne__(self, other)  → not equal          → a != b

# Bu metotlar boolean döndürmelidir: True ya da False

# ------------------------------------------------------------
# 🧙‍♂️ SÜPER GÜÇ: functools.total_ordering
# ------------------------------------------------------------

# Eğer sadece __eq__ ve bir tane karşılaştırma (örn. __lt__) tanımlarsak,
# diğer karşılaştırmaları otomatik üretmek için @total_ordering dekoratörünü kullanabiliriz.

# Bu, hem kod tekrarını azaltır hem de karşılaştırma mantığını sadeleştirir.

# ------------------------------------------------------------
# 🛠️ KULLANIM ALANLARI
# ------------------------------------------------------------

# 🔹 Öğrencileri notlara göre sıralamak
# 🔹 Ürünleri fiyata göre filtrelemek
# 🔹 Dosyaları tarihe göre sıralamak
# 🔹 Müzik listelerini puanlara göre sıralamak
# 🔹 Arama algoritmalarında (örneğin: binary search)

# ------------------------------------------------------------
# ŞİMDİ: Bu temel kavramları anladıysan bir sonraki adımda
# bu özel metotları örneklerle detaylıca inceleyebiliriz!



# ------------------------------------------------------------
# 🔹 __lt__  → "less than" → Küçüktür karşılaştırması ( < )
# ------------------------------------------------------------
# Sözdizimi:
# def __lt__(self, other): ...

# Amaç:
# self < other ifadesi çağrıldığında çalışır

class Student:
    def __init__(self, grade):
        self.grade = grade

    def __lt__(self, other):
        return self.grade < other.grade

# Kullanım:
s1 = Student(80)
s2 = Student(90)
print(s1 < s2)  # True → çünkü 80 < 90


# ------------------------------------------------------------
# 🔹 __le__  → "less than or equal" → Küçük eşit ( <= )
# ------------------------------------------------------------
# def __le__(self, other): ...

class Student:
    def __init__(self, grade):
        self.grade = grade

    def __le__(self, other):
        return self.grade <= other.grade

s1 = Student(85)
s2 = Student(85)
print(s1 <= s2)  # True → çünkü 85 <= 85


# ------------------------------------------------------------
# 🔹 __gt__  → "greater than" → Büyüktür ( > )
# ------------------------------------------------------------
# def __gt__(self, other): ...

class Student:
    def __init__(self, grade):
        self.grade = grade

    def __gt__(self, other):
        return self.grade > other.grade

s1 = Student(95)
s2 = Student(90)
print(s1 > s2)  # True → çünkü 95 > 90


# ------------------------------------------------------------
# 🔹 __ge__  → "greater than or equal" → Büyük eşit ( >= )
# ------------------------------------------------------------
# def __ge__(self, other): ...

class Student:
    def __init__(self, grade):
        self.grade = grade

    def __ge__(self, other):
        return self.grade >= other.grade

s1 = Student(90)
s2 = Student(80)
print(s1 >= s2)  # True → çünkü 90 >= 80


# ------------------------------------------------------------
# 🔹 __eq__  → "equal" → Eşittir ( == )
# ------------------------------------------------------------
# def __eq__(self, other): ...

class Student:
    def __init__(self, grade):
        self.grade = grade

    def __eq__(self, other):
        return self.grade == other.grade

s1 = Student(70)
s2 = Student(70)
print(s1 == s2)  # True → çünkü 70 == 70


# ------------------------------------------------------------
# 🔹 __ne__  → "not equal" → Eşit değil ( != )
# ------------------------------------------------------------
# def __ne__(self, other): ...

class Student:
    def __init__(self, grade):
        self.grade = grade

    def __ne__(self, other):
        return self.grade != other.grade

s1 = Student(60)
s2 = Student(70)
print(s1 != s2)  # True → çünkü 60 != 70


# ===============================================
# 💡 Python'da Karşılaştırma Operatörlerinin (>, <, >=, <=, ==, !=) Altyapısı
# ===============================================

# Python'da karşılaştırma operatörleri (>, <, ==, ...) özünde özel metotlar (dunder methods) ile çalışır.
# Bu metotlar, davranışsal kontrolün ilgili sınıf tarafından yapılmasını sağlar.
# Örneğin: a > b ifadesi aslında a.__gt__(b) anlamına gelir.

# ✅ Bu yöntemler object sınıfı içinde tanımlıdır fakat:
# ❗ object.__lt__, object.__gt__ gibi metotlar **anlamlı bir karşılaştırma yapmaz**
# Bunlar sadece **fallback (yedek) davranışı olarak NotImplemented döner**.

# ❗ object.__eq__(self, other)
# Eğer self ve other aynı nesne (id) değilse False döner (basit karşılaştırma yapar)
# Daha gelişmiş veri karşılaştırmaları yapmaz. nesnenin bellekte olması gerek (hardcoded olarak kullanılamaz)

# ❗ object.__ne__ ise genellikle __eq__'in değili olarak tanımlanır
# 💬 Daha da düşük seviyeye inersek:

# ===============================================
# 1️⃣ type(obj) → obj'nin sınıfını alır
# ===============================================
# Neden? Çünkü davranış tanımı sınıfta bulunur, örnek nesnede değil!
# Örnek:
#   type(a) = sınıfA → davranışlar (method resolution order - MRO) burada aranır.

# ===============================================
# 2️⃣ type(obj).__dict__ → sınıf sözlüğünü getirir
# ===============================================
# Burada sınıfın tanımladığı tüm nitelikler (metotlar dahil) saklanır.

# ===============================================
# 4️⃣ .__call__(b) → metodu çalıştırır
# ===============================================
# En sonunda çağrılır ve gerçek kıyaslama yapılır.

# ===============================================
# 🔁 Genel Düşük Seviyeli Şablon:
# ===============================================

# type(a).__dict__['__gt__'].__call__(a,b)
# object.__dict__['__gt__'].__get__(a,A).__call__(b) -> NotImplemented
# Bu ifade a > b anlamına gelir.

# ===============================================
# 🧪 Tüm Karşılaştırmalar İçin Altyapı
# ===============================================

# a > b  →  type(a).__dict__['__gt__'].__get__(a, type(a))(b)
# a < b  →  type(a).__dict__['__lt__'].__get__(a, type(a))(b)
# a >= b →  type(a).__dict__['__ge__'].__get__(a, type(a))(b)
# a <= b →  type(a).__dict__['__le__'].__get__(a, type(a))(b)
# a == b →  type(a).__dict__['__eq__'].__get__(a, type(a))(b)
# a != b →  type(a).__dict__['__ne__'].__get__(a, type(a))(b)

# 🔁 Not:
# Eğer __gt__ tanımlı değilse, Python `b.__lt__(a)` gibi simetrik alternatifleri de dener.

# ===============================================
# 🧠 Alternatif Kısa Yol:
# ===============================================
# import operator
# operator.gt(a, b) → a > b
# operator.eq(a, b) → a == b
# ...

# ===============================================
# 🔐 Bu düzeyde bilgi, ileri seviye metaprogramlama, debug veya descriptor kullanımlarında işine yarar
# ===============================================

