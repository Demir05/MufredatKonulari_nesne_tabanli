x = 10  # global scope (main frame)

def fonksiyon():
    y = 5  # local scope (function frame)
    print(x)  # global'den erişilir
    print(y)

fonksiyon()
# print(y)  # ❌ NameError: y is not defined

"""
💡 Ne oluyor?

    x → main frame'de, global değişken

    y → function frame'de, lokal değişken

    fonksiyon() çağrıldığında geçici bir function frame oluşur

    Fonksiyon bittikten sonra y silinir → dışarıdan erişilemez ❌
"""


# global anahtar kelimesi

# Python’da global, bir isim üzerinde global scope’ta işlem yapılacağını belirtir.
# fonksiyon içinden,dış dünyada bulunan bir değişkeni değiştirmek veya global olarak bir değişken tanımlamak için global anahtar kelimesi
# kullanılması zorunludur  Not: eğer manipüle edilcek olan  obje mutable ise hata alınmaz çünkü python,mutable nesnelerde yeniden bir tanımlama işlemi yapmaz sadece in-place bir işlem yapılır
# eğer amacın sadece global bir değeri kullanmaksa global bildirmene gerek yok
# global,sadece fonksiyon içlerinde kullanılabilir Main'de kullanılamaz zaten global scope orda açıktır ve global kullanmak karışıklığa sebebiyet verir
# bu python'un basitlik ilkesine terstir bu nedenle Main'de global kullanılamaz
# global,yalnızca bir bildiridir herangi bir şekilde atama veya expression işlem yapmaz

# global birden fazla değişkenle çalışır virgül ile ifadeleri(değerler kümelerini) ayırabilirsin i

# global: bu değişkeni local scope'da değil global scope'da bir nesne olarak  kullanmak istiyorum demektir

x = 10  # global bir değişken

def f():
    x +=3

try:
    f()
except Exception as e: print(e) # cannot access local variable 'x' where it is not associated with a value
# burda f() fonksiyonunu çağırınca yeni bir x değeri oluşturmaya çalıştık ama hata aldık
"""
python,bir değişkeni scope'da şu sırayla arar: local -> enclosing -> global -> built in
burda x değişkeni global'de tanımlı yani python, bu ismi tanıyor 
ama bu değişkeni kullanması için local scope'da araması gerek(çünkü fonksiyon çağrısı local scope oluşturur)
ama local scope da bulamıyor, bu değişken tanımlı ama bulamıyor bu nedenle NameError değil UnboundLocalError hatası verir

"""

def f():
    global x # bu bir sadece bildiridir herangi bir işlem yapılmaz burda python'a global scope'da tanımlı olan x'den bahsediyoruz
    x +=3

f()
print(x) # 13

# global ile global bir değişkeni fonksiyonda oluşturabilirsin

def f1():
    global fa,f2 # birden fazla değerin global olduğunu bildirmek için değerleri ayırmak için virgül kullandık(expression seperator)
    fa = ("demir",)
    f2 = 10
# şu durumda fa ismi henüz tanımlı global'de tanımlı değil çünkü fonksiyon daha çağrılmadı

f1() # şuan tanımlandı

print(dir()) # 'fa','f2'
# mevcut scope yani Global scope'da fa isimi tanımlı :)

print(fa) # ('demir',)
print(f2) # 10

# eğer global scope'da tanımlı olan obje mutabe ise o zaman o objeyi manpüle edebilirsin;

listem = []

def a():

    listem.append(1)

a()

print(listem) #  [1]

# globals() Fonksiyonu

# globals() fonksiyonu,global scope'da tanımlı olan isimlerin ve değerlerinin bulunduğu bir dict döner.
# değişken isimleri -> key'name olurken değerleri -> value olur
# globals() fonksiyonu her yerde çağrılablilir
# globals() fonksiyonu,kapsamı görsel olarak kontrol ve manipüle edebilmeni sağlar dinamik olarak değişken oluşturma veya değiştirme yapabilirsin çünkü bir sözlük
# olarak döndüğü için işlem yapılabilir

# Not: globals ile dinamik olarak fonksiyon-değişken oluşturulabilir ama çok tavsiye edilmez pythonic bir yöntem değildir dikkatli kullanılmalı

# Not2: globals(),canlı bir sözlüktür eğer herangi bir atama veya kopyalama işlemi yapmadan üstünde gezinmek istersen hata alırsın
# çünkü viewobject bellekteki canlı görüntüsünün pencere temsilidir ve bu yapı açık(canlı) olduğu için anlık olarak izleyemezsin

print(globals()) # {'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x762926ffcbf0>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/home/demir/Documents/Python-main/MüfredatKonuları/6.0/BasitFonksiyonlardaKapsam.py', '__cached__': None, 'x': 13, 'fonksiyon': <function fonksiyon at 0x762926fda3e0>, 'f': <function f at 0x762926e1e2a0>, 'f1': <function f1 at 0x762926e1e200>, 'fa': ('demir',), 'f2': 10}
# global olarak tanımlı olan tüm isimleri anahtar-değer eşleşmesiyle döndürdü

# globals,bir sözlük olduğu için eleman manipüle edilebilir veya tanımlanabilir

globals()["f2"] = [] # f2 verisi,10 değerinin referansı idi biz şimdi yeniden bir nesne oluşturduk(integer'lar immutable);

print(f2) # []
# f2 verisi artık bir sözlüğe etiket id değerine bakıp bu sözlüğü globals ile manipüle edelim

print(id(f2)) # 131703749921600

globals()["f2"].append("demir") # burda globals() fonksiyonun sözlük olmasından fayda sağlayarak [] sözdizimsele işareti ile anahtarın değerini getirdik
# anahtarın değeri bir liste olduğu için zincirleme metod kullanımı sayesinde değer ekledik ...

print(f2,id(f2)) # ['demir'] 131703749921600
# gördüğün üzere in-place olcak bir şekilde manipülasyon yaptığımız için id değerleri aynı

# globals() ile tüm kullanıcı tarafından tanımlanmış isimleri silebilirsin ;

for name in dir() :# dir()'e argüman vermediğimiz için mevcut scope'daki isimleri döndürdec
    if not name.startswith("__"): # name magic name değilse
         del globals()[name]

print(dir()) # ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'name']
# gördüğün üzere tüm kullanıcı tarafından tanımlanmış isimler silindi

# globals ile dinamik olarak isim oluşturabilirsin;

for i,v in zip(("f","f1","f2","f3"),("demir","aslı","ozan","doruk")):
    globals()[i] = v

for k,v in globals().copy().items(): # canlı görüntüsü üstünde gezinemez(viewobject durumu) bu nedenle ilk önce copy ile
    # yeni bir nesne oluşturduk
     k.startswith("__")  or print(f"{k} -> {v}") # short circuit evaluation

"""
i -> f3
v -> doruk
f -> demir
f1 -> aslı
f2 -> ozan
f3 -> doruk

"""
# neden copy() Kullandığımızı tanımda anlattık


# locals() Fonksiyonu

# locals() fonksiyonu,geçerli local kampsamda tanımlı olan tüm isimleri ve o isimlerin değerlerini sözlük olarak döndüren bir fonksiyondur
# herangi bir kapsamdan kullanılabilir ama Main'de kullanılırsa globals() fonksiyonu gibi çalışır (global scope'da local -> global olur o mantık)
# locals() fonksiyonun döndürdüğü sözlük,canlı ve gerçek bir sözlük değildir,bir kopyasını verir locals(), sana bir sayfanın(belleğin) fotokopisini verir
# eğer üstüne yazarsan orjinal yapıyı değiştiremezsin bu nedenle sadece okunabilir
# locals genelde debug ve analizlerde kullanılır

# öncelikle bir main'de locals() kullanalım;

print(locals()) # {'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7b75d1700bf0>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/home/demir/Documents/Python-main/MüfredatKonuları/6.0/BasitFonksiyonlardaKapsam.py', '__cached__': None, 'name': 'x', 'i': 'f3', 'v': 'doruk', 'f': 'demir', 'f1': 'aslı', 'f2': 'ozan', 'f3': 'doruk', 'k': 'f3'}


def g():
    ad = "ad" # local

    s = ad in locals() and True
    return s

print(g()) # True

# locals() ile herangi bir şekilde isim oluşturma yapılamaz

def g2():
    locals()["x"] = 10
    print(x)
try:
    print(g2())

except Exception as e: print(e) # name 'x' is not defined
# burda locals(),sana sözlüğün bir kopyasını verir üstüne yazsan bile yazılan nesne gerçekten oluşturulmaz bu nedenle bu hata verir ama;

def g3() -> int:

    locals()["x"] = 10
    print(locals())
    return locals()["x"]

print(g3()) #  {'x': 10}
            #   10
# burda locals üzerinden belleğin kopyasına bir veri tanımladık gerçekten tanımlama değil(kopyasına) ama bu kopya'üzerinden döndürme yapılabilir

# locals(),belleğin kopyasını döndürdüğünden dolayı döngülerde kullanılabilir;

for k,v in locals().items():

    print(k,v) # uzun olduğu için yazmadım :) ama global tanımlı olan isimleri ve değerleri

"""
    globals() ve locals(), bellekteki veriye (heap) değil, o veriyi işaret eden isimleri (identifier) stack’inde tutulan adlara erişir.
    Ama hangi isimleri döndüreceklerini scope belirler.
"""