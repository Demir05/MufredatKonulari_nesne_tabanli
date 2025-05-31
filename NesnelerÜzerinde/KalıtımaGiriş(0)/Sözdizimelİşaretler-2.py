# Tekil Nesneler
from collections.abc import Generator,Iterable

# Runtime'da tekil nesne,program çalışırken yani runtime esnasında sadece bir tane oluşturulan nesnelerdir
# bu nesneler,veri taşımazlar önemli olan niyeti belli etmektir
# özellikleri;
# Sadece bir tane oluşturur
# her yerde aynıdır
# kimliksel olarak aynıdır dolayısıyla is kimlik operatörü kullanılabilir
# bellekten tasarruf edilir

# Ellipsis,Parameter.empty,None bu tekil nesnelere örnektirler



# Sözdizimsel işaretler, python dilinin yapısını ve bloklarını tanımlamak için kullanılan işaretlerdir
# bu işaretler herangi bir işlem yapmazlar ama programın nasıl okunacağını ve çalışacağını belirlerler


# parantez ()

# parantez,python'da oldukça esnek bir kullanım çeşitliği sunar,kullanıldığı bağlama göre parantezin görevi ve amacı değişir
# 1) parantez,callable bir objeyi çağırmak için kullanılır
# 2) parantez,bir callable obje oluşturmada ve sınıf veya fonksiyon tanımlamada parantez içleri o yapının alabilceği parametrelerin tanımlandığı yerdir
# 3) parantez,tuple yapısını tanımlamada kullanılır
# 4) parantez, generator expression oluşturmak için kullanılır
# 5) parantez,matematiksel işlemlerde ve mantıksal işlemlerde öncelik belirlemek,gruplaştırmak için kullanılır
# 6) parantez,expression işlemlerde bağlama/expression değer döndürmek için olarak kullanılır

# örnekler...;

# 1) parantezi callable bir obje çağırmak için kullanalım;

m = max([],default=0) #  burda max() fonksiyonunu çağrımak için () parantez kullandık

# 2) parantezi callable bir obje oluşturmak için kullanalım
def f(x,y,/,**kwargs): # burda f adında bir isim vereceğim ve bu isme ait çalıştırılabilir bir kod bloğu tanımlayacağım
    return m

# 3) parantezi bir tuple oluşturmak için kullanalım;

t = (1,2,3)

# 4) parantezi expression oluşturmak için kullanalım;

lazy = (x for x in range(1,20))

# 5) parantezi matematiksel işlemlerde öncelik sırası için kullanalım;

10 * (3+2) # > 50 döner

# 6) parantezi expression değer döndürmek için bağlam olarak kullanalım;

(deger := 10) # burda parantez olmasaydı syntax hatası alırdık


# köşeli parantez []

# köşeli parantez,veri yapıları tanımlamak hemde bu yapılara erişmek/değiştirmek için kullanılan kullanıldığı bağalama göre;
# gerek sözdizimsel işaret gerekse operatör gibi davranabilen bir işarettir
# 1) liste tanımlamak için kullanılır
# 2) indexleme yapmak amacıyla kullanılır
# 3) dilimleme yapmak için kullanılır,dilimleme sonucu her zaman mevcut objenin türünde oluşur yani dilimleme sonucu yeni oluşan nesnenin türü dilimlenen nesnenin türüne bağlı
# 4) mutable veri yapılarında belirli bir index'i değiştirmek için kullanılır,bu değiştirmeyi in-place yapar
# 5) list comprehension tanımlamak için kullanılır
# 6) anahtar-değer eşleşmesinde değere erişmek veya yeni bir anahtar-değer tanımlamak için kullanılır
# 7) köşeli parantez,türün içeriğini yani içindeki elemanların tipini bildirir
# örnekler...;

# 1) liste tanımlamak için kullanılır;

listem = [1,2,3]

# 2) indexleme yapmak için kullanılır;

a = listem[2]

print(a) # 3

# 3) dilimleme yapmak için kullanılır

b = listem[:1]

print(b) # [1]
# dilimlemenin sonucu mevcut objenin türüne bağlıdır dilimleme sonucu mevcut obje ile aynı türde olur

# belirli bir index'i değiştirmek için kullanılır

listem[2] = 0

print(listem) # [1, 2, 0]
# değiştirme işlemini in-place yapar

# list comprehension tanımlmak için kullanılır;

listem2 = [i*f for i,f in enumerate(listem)]
print(listem2) # [0, 2, 0]

# anahtar-değer eşleşmesinde değere erişmek veya yeni bir anahtar-değer tanımlamak için kullanılır

s = {}

s["isim"] = "demir"

print(s) # {'isim': 'demir'}

# köşeli parantez,tür bildiriminde türün içeriğini yani elemanların tiplerini bildirir;

def f(iterable:[str,str,int]): #burda iterable'daki elemanlar,sırasıyla str,str ve int olsun -> iterable:[int] de yapılabilirdi
    pass

def f(iterable:[str]):pass # burda iterable içindeki tüm elemanların string tipte beklendiğini bildirdirdik mesela böyle yazsaydık;

def f(iterable:Iterable):pass # burda iterable parametre adının,Iterable tipini beklediğini bildiririz ama o objedeki elemanların türleri hakkında herangi bir bildiri yok

def generator()-> Generator[int,None,None]: yield 1 # burda bu kullanımının sözdizimi -> Generator[yieldType,sendType,returnType]
# bu nedenle [int,None,None] dedik, bu generator,1 nesnesini yield ediyor(bu return gibi bir işlem değil) ,bu fonksiyona herangi bir değer verilmediği için sendType -> None;
# ve bu fonksiyonda return olmadığı içinde returnType -> None bildirdik

def generator2() -> Generator[str,int,None]:
    yaş = yield "demir"
    yield yaş

gen = generator2()

isim = gen.send(None)
yas = gen.send(20)

print(isim,yas) # demir 20
# süslü parantez {}

# süslü parantez,iki temel veri yapısını ki bunlar set ve dict literal veya comprehension olarak tanımlamak için kullanılır
# süslü parantezin içeriğine göre python,verinin türüne karar verir

# set literal tanımlama;

s = {1,2,3,4}

# dict literal tanımlama;

d = {"isim":"demir","yas":20}

# set comprehension tanımlama

s1 = {x for x in range(10)}

# dict comprehension tanımlama

s = {x:x**2 for x in range(5)}


# nokta .

# nokta,python'da öznitelik(attirbute) erişim işaretidir ama operatör olarak da adlandırılır çünkü bir işlem yapar ve değer döndürür
# bir nesnenin sahip olduğu özellik,metodlara erişmek için kullanılır
# nokta,nesnenin özelliklerini __getattribute__ ve __getattr__ metodları aracılığı ile getirir aslında nokta bu metodları çağırma yöntemidir
# __getattr__ ve __getattribute__ arasında farklar vardır bunlar birbirlerinin kısaltması değildir birbirlerini tamamlayan metodlardır
# getattribute,maaliyetli güçlü ama tehlikelidir çünkü her şeye müdahale eder bu durumda sonsuz döngülere yol açabilir
# bir objenin özelliğine erişirken __getattributue__ istisnasız çağrılır ama __getattr__,sadece getattribute'da nesnenin özelliği olmazsa çağrılır
# çoğu zaman __getattr__ yeterli,hafif,hızlı'dır genel olarak eksik attribute'lara özel bir davranış istiyorsan tanımlanır
# mesela bir objede adı obj olsun x adındaki bir özelliğe erişmek için > obj.x denir bu aslında arkada şöyle bir işlem yapar;
# obj.__getattribute__('x') demektir eğer burdan sonuç bulunamazsa yani AttibuteError alınırsa o zaman > x.__getattr__('x') çağrılır

isim = "demir"

print(isim.__getattribute__("upper")()) # DEMIR
# nokta aslında bu işlemi yapar


# Ellipsis ...:

# üç nokta,python'da özel bir nesneyi temsil eder bu nesneye Ellipsis denir
# ellipsis,birinci sınıf bir vatandaştır  ve tek bir örneği vardır bu nedenle is karşılaştırma operatörü  ile karşılaştırma yapmak güvenlidir
# ellipsis,yer tutucu(place holder) olarak görev yapar None'dan farklı olarak None,bilinçli bir kullanımken ellipsis yer tutma sonradan tanımlama maksatında kullanılır
# aynı zamanda ellipsis,bir işlem olarak değil bir obje olarak yorumlanır insan için ... anlamlı olsa da python, bunu ellipsis olarak yorumlar
# Not: ellipsis python'da True olarak kabul edilir None gibi bir False değer kabul edilmez

print(type(Ellipsis)) # <class 'ellipsis'>
# Ellipsis,ellipsis sınıfını temsil eder

print(...) # Ellipsis
# aynı şekilde üç nokta'da ellipsis anlamındadır

print(... is Ellipsis) # True
# Ellipsis,tek bir örneğe sahip olduğundan is ile karşılaştırma yapılması güvenlidir

isim:str =  ...
# burda isim değişkenine aslında Ellipsis objesini atadık ve bu objenin str argüman beklediğini bildirdik
# bu alan string olmalı ama şuan tanımsız demek anlamına gelir

print(isim) # Ellipsis
# bu örneği şöyle de yapabiliriz;

soy = Ellipsis
# bu örnek soy = ... ile aynı işlevi temsil eder üç nokta kullanımı daha okunabilir ve kolay olduğu için genelde o tercih edilir

print(soy) # Ellipsis

# ellipsis True olarak yorumlanır bu None nesnesinden önemli bir farkıdır

print(... and "ok") # ok
# gördüğün üzere ellipsis True olarak yorumlanır bu nedenle bu short circuit evaluation çalıştı

# listelerde belirli bir kısmın eksik olduğunu belirtmek için kullanılır;

listem = [1,2,3,...,9,10] # bu şeklinde bir tanım insan için anlamlıdır python üç noktayı işlem olarak değil, obje olarak yorumlar

print(listem)  # [1, 2, 3, Ellipsis, 9, 10]
# python ...'yı ellipsis olarak yorumlar


# İki Nokta (:)

# python'da iki nokta işareti,bir sözdizimsel yapı olarak kullanılır bir operator değildir herangi matematiksel işlem yapmaz
# iki noktanın anlamı bağlama göre değişir

# 1) dict yapısında iki nokta,gerçekten bir anahtar değer eşleşmesi yapar

# 2) fonksiyonlarda,parametrenin beklediği türü bildirir burda bir tür açıklaması yapar ama iki nokta eşleştirme yapmaz
# yani  bu zorunlu olmaz sadece bir bildiridir büyük projelerde okunaklığı,fonksiyonun ne döndürdüğünü belirtmek için kullanlır
# ve __annotations__ magic name'i ile  hint'lerin nasıl saklandığını görebilirsin
# __annotations__,bir sözlüktür ve parametrelerin adını ve türlerini anahtar-değer eşleşmesiyle saklar;
# __annotations__,sadece user-definded fonksiyonlarda bulunur built-in functionlar'da bulunmaz çünkü çoğu built-in function;
# C dilinde yazılmıştır ayrıca __annotations__, python 3.5 sürümüyle tanıtıldı

# Not: tip belirtmede lambda'da kullanılmaz lambda,basit olamsı amacıyla tanımlanmıştır bu nedenle iki nokta sözdizimsel işareti kullanılamaz
# Not: help() fonksiyonu fonksiyonda tanımlanan parametrelerin türünü gösterir

# 3) değişkenlerde de tür bildirimi yapar

# 4) kontrol yapılarında,hata yakalamada kod satırının  bittiğini ve bloğun başladığını gösterir

# 5) dilimleme yaparken kullanılır


# kullanımları;

d = {"isim":"demir"}
# burda iki nokta,anahtar ve değeri eşleştirdi

# fonksiyonlarda parametre türü belirlemede kullanılır;

def selamla(*,isim:str):
# burda isim parametresini string tür beklediğini söyledik ama zorunlı değil integer da alabilir ama mantıksal hatadır
    return f" merhaba {isim}"

print(selamla(isim='demir')) #  merhaba demir
# şimdi burda iki noktayı python değerlendirdi ve __annotations__'da saklanır

print(selamla.__annotations__) # {'isim': <class 'str'>}
# tür bildirimleri annotations'da saklanır ayırca,annotations bir sözlüktür parametre adını -> key, beklenen türü'de -> value olarak eşleştirir

# şimdi ise help() fonksiyonu ile bakalım;

print(help(selamla))
"""
selamla(*, isim: str)

None
"""
# gördüğün üzere herangi bir DocString olmadığı için metin yazmadı ama parametrelerin beklediği türü bildirdi

# değişken tanımlamada tip bildirmede kullanılır

isim : str = "demir"
# burda ise : işaretini, değişkende tür bildirimi yapmak için kullandık ama burda : işareti,bir atama veya eşleştirme yapmaz
# büyük projelerde okunaklığı arttırır

yas :int = 20
# burda yas değişkenin integer değer adlığını bildirdik

ogrenci :str = 20
# burda herangi bir hata alınmaz,ama mantıksal olarak bu işlem yanlıştır ve IDE'ler genelde buna uyarı verirler


# iki nokta burda,bu satırın artık bittiği ve bu koda ait bir bloğun başladığını bildirir,yani bir blok tanımlaycısı oalrak görev yapar
"""
if True:

    pass
#-----------------------------------------
while True:

    pass
#----------------------------------------

try:
    pass
except:
    pass
#--------------------------------------------------
"""
# iki nokta,dilimlemede başlangıç-bitiş-adım değerlerini belirtmede kullanılır

listem = [1,2,34,5]

print(listem[:2])
# burda iki noktayı,dilimleme yapmak için kullandık başlangıçtan,1.indexe kadar olan değerlerle bir liste oluşturduk
# liste dilimleme,liste döndürür



# Arrow Token -> Sözdizimsel işareti

# Arrow Token yani  -> işareti,user-definded fonksiyonlarda,fonksiyonun beklenen dönüş değerin tipini bildirir
# fonksiyonun ne tür veri döndürmesi gerektiğini,yazılımcıya aynı zamanda İDE'ya bildirmeni sağlar hem kullanıcı hemde İde bunu yorumlayabilir
# ayrıca -> işaretinin belirttiği türü python,__annotations__ sözlüğünde tutar
# Arrow Token(->) sözdizimsel işareti, kullanılması zorunlu değildir ayrıca beklenen verinin tipi; dönüşte farklı olabilir bu durumda hata alınmaz ama mantıksal olarak hata olur
# bu nedenle dikkatli tanımla
# eğer fonksiyonun herangi bir return değeri yoksa kesinlikle arrow token ile bunu bildir
# Arrow Token(->),lambda 'da kullanılamaz

def çarp(x:int,y:int,/) -> int:
    """verilen pozisyonel bazlı argümanları çarpar"""
    return x*y
# burda çarp ismine ait çalıştırılabilir bir kod bloğu tanımlıyorum,x ve y parametreleri sadece pozisyonel bazlı argüman alabilir
# ve bu pure function'numun döndürdüğü değerin türü integer olmalı

print(çarp(12,424)) # 5088

# şimdi ise annotations sözlüğüne bakalım;

print(çarp.__annotations__) # {'x': <class 'int'>, 'y': <class 'int'>, 'return': <class 'int'>}
# gördüğün üzere hem parametrelerin beklediği türleri hemde fonksiyonun geri dönüş türünü sözlükte tuttu

print(help(çarp))
"""
Help on function çarp in module __main__:

çarp(x: int, y: int, /) -> int
    verilen pozisyonel bazlı argümanları çarpar

None

"""



# burda bool döndüren bir pure funciton tanımladık;

def giriş(isim:str = None) -> bool:

    kullanıcılıar = {"aslı","ozan","doruk","demir"}
    entry = (isim in kullanıcılıar and True) or False
    return entry

# string argüman bekleyen bir sabit isimli parametre tanımladık(yani açık ismli : isim adıyla doğrudan eşleşebilir) ve varsyaılan olarak None değeri atadık
# bu fonksiyon pure function olarak tanımlanır çünkü hem dış dünyayı değiştirmiyor hem de herangi bir obje üzerinde manipülasyonu yok

print(giriş("demir")) # True