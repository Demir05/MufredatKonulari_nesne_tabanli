# bool sınıfı:

# Python'da bool sınıfı, mantıksal değerleri temsil eder: True (doğru) ve False (yanlış)
# bool sınıfı aslında int sınıfının bir alt sınıfıdır(int sınıfından miras alır ) → Yani bool bir integer'dır: 
# True → 1, False → 0 gibi davranır → Örn: True + 1 = 2

# bool sınıfının amacı, bir nesnenin mantıksal (truthy/falsy) bağlamda ne anlama geldiğini belirlemektir

# Bu sınıf sayesinde bir nesneyi doğrudan:
# → if obj:
# → while obj:
# → bool(obj)
# gibi yapılarda kullanabiliriz


# Falsy ve Truthy:

# Python'da bazı nesneler doğrudan "False" gibi davranır → Bunlara falsy denir:
# Falsy örnekleri: None, False, 0, 0.0, "", [], {}, set(), range(0)

# Diğer tüm nesneler → truthy kabul edilir yani mantıksal bağlamda True sayılırlar

# if, while gibi kontrol yapıları truthy/falsy mantığını kullanır

# Örnek:
# if []: → False → çalışmaz
# if [1,2,3]: → True → çalışır

# Aynı şey while için de geçerlidir:
# while veri: → veri boş değilse döngü devam eder


# __bool__() metodu:

# __bool__() özel metodu, bir nesne mantıksal bağlamda değerlendirilirken çağrılır:
# Örneğin:
# → if obj:
# → while obj:
# → bool(obj)

# Bu metod, nesneye True ya da False değeri atamak için override edilir
# Eğer nesnede __bool__() metodu tanımlı değilse, Python onun yerine __len__() metodunu çağırır

# Eğer hem __bool__() hem __len__() yoksa:
# → Python: TypeError: object is not interpretable as a boolean hatasını verir

# DİKKAT: __bool__() metodu, object sınıfında tanımlı DEĞİLDİR
# Yani Python'da varsayılan bir bool davranışı yoktur → Her sınıfın ihtiyacına göre override etmesi gerekir
# type sınıfında da bulunmaz → Kullanmak istiyorsan kendi sınıfında override etmelisin

# Sözdizimi;

# def __bool__(self) -> bool:
#   return bool(self.data) -> burda loop olmaz çünkü bool(),bir sınıf çağrısıdır
#   **aynı zamanda mantıksal bağlam,bir expression(ifade) döndürür dolasıyla __bool__ metodunda mutlaka return değeri olmalı ve bool bir değer döndürmelidir


# Kullanım örneği:
class Sepet:
    def __init__(self, urunler):
        self.urunler = urunler

    def __bool__(self):
        # sepet boşsa False, doluysa True
        return bool(self.urunler)

s = Sepet(["elma"])
if s:
    print("Sepet dolu")  # Sepet dolu

# while ile kullanım:
sayilar = [1, 2, 3]
while sayilar:
    print(sayilar.pop())
# → while, sayilar listesi boşalana kadar devam eder
# → burada Python → bool(sayilar) → True/False


# Mantıksal çözümleme zinciri (method resolution order):

# 1) if obj: veya while obj: → Python bu nesne mantıksal mı diye sorar
# 2) → type(obj).__getattribute__(obj, "__bool__") 
#     → type(obj).__dict__['__bool__'] -> bound method elde ederiz çünkü __bool_, metoddur bu nedenle sonradan çağrılması gerekir
#     → type(obj).__dict__['__bool__'].__call__(obj) -> aynı zamanda __bool__, method wrapper(get-set Descriptor) değildir bu nedenle descriptor protokolü uygulanmaz 
# 3) __bool__ yoksa: → __len__() çağrılır
# 4) İkisi de yoksa: → TypeError

# NOT: __bool__ metodu, __getattribute__ ile çözülür
# MRO zincirine göre sınıf içinde bulunamazsa, miras yoluyla parent sınıflarda aranır

print(
    s.__class__.__getattribute__(s,"__bool__").__call__(), # True
    s.__class__.__dict__['__bool__'].__call__(s) #True 
)

# bool() çağrısı:

# 1) bool, bir sınıftır: <class 'bool'>
#    → bool aslında int sınıfından türetilmiştir → yani: bool ⊂ int

# 2) bool() fonksiyon gibi görünse de aslında bir sınıf çağrısıdır:
#    → bool(obj) ifadesi:
#       → type.__call__(bool, obj) demektir

# 3) Python bu sınıf çağrısını şöyle çözümler:

# → bool(obj)
# → type.__call__(bool, obj)                       # bool bir sınıf → __call__ tetiklenir
# → type.__dict__["__call__"].__get__(bool, type)  # Descriptor protokolü → bound method elde edilir,__get__ metodu, bool sınıfına bağlanır ve bound method elde ederiz çünkü __call__,bir special metoddur
# → bound_method.__call__(*args,**kwargs)          # bound_method, çağrıldığında __call__, artık Descriptor'ı değil bound_method'da bulunan __call__ metodunu çağırır bunun sonucunda bu işlemler bizi;
# → bool.__new__(bool, obj) → yeni bir bool nesnesi oluşturulur 
# → bool.__init__(bool, obj) → bu nesne başlatılır (init çoğu zaman boş bırakılır)
# Ancak...
#   bool sınıfı, int sınıfından miras aldığı için __new__ metodunu override eder
#   ve burada özel bir davranış sergiler: objeyi mantıksal olarak değerlendirir


# 4) Yani bool(obj) şunları yapar:

# 1) → type(obj).__getattribute__(obj, "__bool__")      # obj.__bool__ varsa
#    → obj.__bool__() → True / False

# 2) → Eğer __bool__ yoksa: type(obj).__getattribute__(obj, "__len__")   # yedek plan
#    → obj.__len__() > 0 → True / False

# 3) → İkisi de yoksa: TypeError fırlatılır


# Örnek:
class Kutu:
    def __init__(self, icerik):
        self.icerik = icerik

    def __bool__(self):
        return bool(self.icerik)

k = Kutu(["defter"])
print(bool(k))   # True → çünkü icerik listesi boş değil


# bool bir sınıf olduğu için:
print(type(bool))            # <class 'type'>     → çünkü bool bir sınıftır
print(bool.__class__)        # <class 'type'>     → metaclass: type
print(bool.__bases__)        # (<class 'int'>,)   → int sınıfından türetilmiş

