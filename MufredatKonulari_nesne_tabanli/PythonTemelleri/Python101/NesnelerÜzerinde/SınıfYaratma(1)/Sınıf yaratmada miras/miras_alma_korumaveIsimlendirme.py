# ------------------------------------------------------------------------
# 📘 KONU: Python'da İsimlendirme Konvansiyonları ve Miras ile Koruma Mekanizması
# ------------------------------------------------------------------------

# Python'da değişken ve fonksiyon isimleri yalnızca isim değil; bazı yazım şekilleri
# özel anlamlar taşır. Bu kurallar genelde bir "konvansiyon" (gelenek) olarak işler,
# ama bazı durumlarda Python dilinin kendisi bu isimleri farklı yorumlar (örneğin: __x).

# ------------------------------------------------------------------------
# 🧩 1. _tek_altçizgi (örnek: _x)
# ------------------------------------------------------------------------

# Bu kullanım bir değişkenin veya metodun "iç kullanım" amaçlı olduğunu belirtir.
# Yani bir API, sınıf ya da modül geliştirirken şu mesajı verir:
# "Bu öznitelik iç iş mantığı için yazılmıştır, dışarıdan kullanılması önerilmez."

# Bu, yalnızca bir konvansiyondur, teknik olarak herhangi bir engel koymaz.
# Python'da her şeye erişebilirsin; bu sadece bir uyarıdır.

# Örnek:
class A:
    def __init__(self):
        self._secret = "Bu sadece iç kullanım içindir"

a = A()
print(a._secret)  # Erişebilirsin, ama erişmemen beklenir.

# ------------------------------------------------------------------------
# 🧩 2. __çift_altçizgi (örnek: __x)
# ------------------------------------------------------------------------

# Bu kullanım gerçek bir davranış farkı yaratır.
# Python bu tür isimleri sınıf adına göre "name mangling" adı verilen
# bir işlemle otomatik olarak yeniden adlandırır. bu işlem varible adını değiştirmekten ibarettir

# Bu sayede:
# - Aynı isimli değişkenlerin alt sınıflarda üst sınıfı ezmesi engellenir.
# - Sınıf içi gizliliğe yönelik basit bir koruma sağlanır (gerçek private değil).
# - Python '_SınıfAdı__isim' şeklinde içeriği yeniden adlandırır.

# Örnek:
class B:
    def __init__(self):
        self.__data = 42  # Bu aslında self._B__data olur artık __data adında bir değişken olmaz bu isim değişir dolasıyla ulaşamayız.

b = B()
# print(b.__data)       # AttributeError: 'B' object has no attribute '__data'
print(b._B__data)        # 42  → name mangling ile saklanmış

# ------------------------------------------------------------------------
# 🧬 3. Miras Durumunda __x Koruma Mekanizması
# ------------------------------------------------------------------------

# Eğer bir sınıfta __isim şeklinde bir alan tanımlarsan,
# bu alan alt sınıflarda aynı isimle tanımlansa bile çakışmaz.
# Çünkü Python her sınıfa özgü olarak __isim adını yeniden adlandırır.

# Örnek:
class Base:
    def __init__(self):
        self.__value = 100  # self._Base__value
    def show(self):
        print("Base:", self.__value)

class Sub(Base):
    def __init__(self):
        super().__init__()
        self.__value = 999  # self._Sub__value

    def show(self):
        print("Sub:", self.__value)

s = Sub()
s.show()           # Sub: 999
super(Sub, s).show()  # Base: 100

# Burada alt sınıfın __value'si, üst sınıfın __value'sini ezmemiştir.
# Çünkü Python bunları:
# - self._Base__value
# - self._Sub__value
# şeklinde ayrı saklamıştır.

# Bu, miraslı yapılarda "kapsülleme" (encapsulation) sağlar.
# Python'da private yoktur ama __ ile bu davranış emüle edilebilir.

# ------------------------------------------------------------------------
# 🧪 NOT: __x ile gizlenen alanlara hâlâ erişebilirsin
# ------------------------------------------------------------------------

# Python'da "koruma" bir yasak değil, bir engeldir.
# Erişebilirsin ama özellikle yapman gerekir:

print(s._Base__value)  # 100
print(s._Sub__value)   # 999

# ------------------------------------------------------------------------
# 🧠 4. __x__ (magic methods) → Farklı Bir Kategori
# ------------------------------------------------------------------------

# Eğer isim hem başında hem sonunda çift alt çizgiyle yazılmışsa (__init__, __call__, __str__),
# bu özel/metaprogramlama amaçlı Python'a ait isimlerdir.

# Bunlar Python dili tarafından tanınır ve otomatik olarak çağrılır.

# Örnek:
class MyClass:
    def __str__(self):
        return "Ben bir nesneyim"

print(str(MyClass()))  # __str__ otomatik olarak çalışır

# Bu isimleri kullanma! Yeniden tanımlayabilirsin (override),
# ama kendi isimlerini __x__ şeklinde yazma — Python gelecekte o ismi kullanabilir.

# ------------------------------------------------------------------------
# 🧾 5. self, cls, *args, **kwargs — Ne İşe Yarar?
# ------------------------------------------------------------------------

# self → Sınıf içindeki örneğe (instance) erişmek için
# cls → Sınıf metodlarında sınıf nesnesine erişmek için
# *args → Fazladan pozisyonel argümanları almak için (tuple olarak)
# **kwargs → Fazladan keyword argümanları almak için (dict olarak)

# Bunlar zorunlu isimler değildir ama Python topluluğunun kabul ettiği standartlardır.

# ------------------------------------------------------------------------
# 📌 Özet:
# ------------------------------------------------------------------------

# _x        → sadece konvansiyonel gizlilik
# __x       → ad çakışmasını önleyen name mangling, kapsülleme sağlar
# __x__     → Python'un özel sistem fonksiyonları (magic methods)
# self/cls  → instance/sınıf bağlamı için kullanılan parametreler
# *args, **kwargs → esnek fonksiyon tanımları için

# Miras durumlarında özellikle __x kullanımı, alt sınıfın üst sınıf verisini
# yanlışlıkla ezmesini önlediği için önemlidir. Bu sayede Python'da yapay
# bir "private" erişim katmanı oluşturulmuş olur.

# Gerçek gizlilik olmasa da Python felsefesi şudur:
# "Engellemem ama niyet belli ederim" (we are all consenting adults here)

class A:
    _s = "31"
    def __init__(self):
        self.__ID = 11111
    def give(self):
        return self.__ID

class B(A):
    def __init__(self,ID):
        super().__init__()
        self.ID = ID


b = B(31)

print(b.give())

print(b._s)





