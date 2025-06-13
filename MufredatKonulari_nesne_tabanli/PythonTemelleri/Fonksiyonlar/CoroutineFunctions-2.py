
# yield
""""""
# yield:python'da bir fonksiyonun çalışmasını geçici olarak durduran çift veri akışı sayesinde o anda üretilen değeri dış dünyaya veren aynı zamanda dış dünyadan veri alınmasını sağlayan ama fonksiyonun çalışmasını
# tamamlanmadan duraklatan ve ileride kaldığı yerden devam ettiren bir anahtar kelimedir

# yield,bir fonksiyonu lazy generator haline getirir ve fonksiyon çağrıldığından hemen çalışmaz sadece generator döndürür
# yield içeren bir fonksiyon artık bir veri üretici olur yield,fonksiyonlara üretim gücü kazandırır ama bu üretim hafif değil
# kontrollü,dinamik ve modüler bir üretim sunar

# yield,o anki değeri döndürür tüm local değişkenleri ve çalışan satırı hafızada tutar ve python beklemeye geçer sonradan kaldığı yerden devam eder

# yield,fonksiyonun kontrol akışını duraklatır,bir durak görevi görür bu sayede bellek gereksiz kullanılmaz ayırca bu duraklama sayesinde generator,konumunu tutar ve
#dışardan veri alabilir ayrıca yield'in değerini dış dünyaya döndürebilir aksi halde fonksiyon çalışırken dış dünyaya veri döndüremez veya alamaz yield,bunu sağlar

# yield,lazy evaluation mantığı ile çalışır ve itarator'de eleman kalmadıysa __next__() metodu,StopIteration hatası fırlatır

# yield,sadece fonksiyon içlerinde kullanılabilir nonlocal ve global gibidir main'de kullanılamaz

"""
generator expression VS yield
generator expression tek satır olurken yield,çok satırlı olabilir 
generator expression,kısıtlı bir kontol akışı sunar ama yield'de for while try gibi kontrol akış grupları kullanılabilir 
generator expression'da parametre tanımlanamaz ama yield'de parametre tanımlanabilir 
generator expression'un okunaklığı karmaşık yapılarda düşer ama yield,bu tip karmaşık yapılar için birebirdir 
"""

# Kullanım Alanları;

# büyük verilede çalışırken,veriyi parça parça üretirken,işlem maaliyetini zamana yayarken(bir işlemi hemen ve tamamen yapmak yerine
# ihtiyaç duyuldukça yapılmasına denir lazy evaluation,bu felsefeye göre çalışır),
# dallanmış yapıları düzleştirirken,bellek hassasiyeti olan işlemlerde kullanılır
# yield,sonsuz veri akışlarını  kontrol etmenin tek seçeneğidir

def gen(n):
    for i in range(n):
        yield i # burda i değerini dışarı döndürdü sonra beklemeye geçti döngü tekrar geldiğinde tekrar değer  döndürdü

print(gen(5)) # <generator object gen at 0x7c49b83ea5a0>
# gördüğün üzere fonksiyon yield içerdiği için artık bir veri üreticisine dönüştü
# ve fonksiyonu çağırdığımız için generator object döndürdü

generator = gen(5)
# burda bir generator döndürdü yield,hemen elemanı döndürmez önce çağrılması gerek

print(next(generator))  # 0
print(next(generator)) # 1

for i in generator: print(i)
"""
2
3
4
"""
# gördüğün üzere,yield local değişkenleri ve çalışan satırı hatırlar bu nedenle değerleri baştan yazmadı


# yield'i counter olarak kullanabilirsin

def counter():
    i = 0
    while True:
        i +=1
        yield i # burda i değerini dışarı döndürdü sonra bekemeye geçti yani tekrar döngü başına gelmedi
        # zaten bu kontrol akışını duraklatma özelliği sayesinde döngülerde kullanılabilir yoksa loop'a girerdi

counter = counter()

print(next(counter)) # 1

# bu counter'ı daha dinamik kullanabilirsin

for _ in range(10) : print(next(counter))
"""
2
3
4
5
6
7
8
9
10
11
"""
# böyle bir kullanımı generator expression'da yapamazsın

# yield,dış dünyaya o anda üretilen değeri dış dünyaya fonksiyonu duraklatarak döndürür bu durumda birden fazla yield kullanabilirsin

def f1():
    yield 1
    yield "demir"
    yield "doruk"

f1 = f1()

for _ in range(3):
    print(next(f1))
"""
1
demir
doruk
"""

# yield from

# yield from,bir iterable içindeki tüm öğeleri tek tek yield etmeyi otomatikleştiren bir ifadedir
# normal olarak for i in iterable: yield i > yerine çok daha kısa,optimize(C dilinde optimize edilmiştir bu nedenle %10-%30 daha performanslıdır)
# onun dışında aslında yield ile tamamen aynıdır
# yield from içeren bir fonksiyon artık bir veri üreticisi olur ve çağrıldığında eleman dönmez bir iterator döner

# Not: bir fonksyionda yield tanımlıysa o fonksiyon artık veri üreticisi olur  ve çağrıldığında bir iterator döner
# bu nedenle yield from ile bir fonksiyonu(iterator'ü) kombine edebilirsin

def f(lst):
    yield from lst

gen = f([1,2,3,4])

for i in gen: print(i)
"""
1
2
3
4
"""

# bu örnekte bir fonksiyonu yield from ile kombine edeceğiz

def a():
    yield "demir"
    yield "aslı"
    yield "ozan"


gen = f(a())

for i in gen: print(i)
"""
demir
aslı
ozan

"""

# yield from,özellikle özyineli(recursive) fonksiyonlarla çok sık kullanılır

def flatten(iterable):

    for i in iterable:
        if isinstance(i,(list,tuple)):
            yield from flatten(i)
        else:
            yield i


f = flatten((1,2,3,4,(5,6,7,(8,9)),10))

print(list(f)) # 10

# bu örnekte ise bir fonksiyonu üretilcek olan verinin yalnızca bir kısmınu üretecek şekilde kullandık

def alt():
    yield 1
    yield 2
    yield 3

def ust():
    yield from alt()
    yield 4
    yield 5

print(list(ust())) # [1, 2, 3, 4, 5]


def sayac(n,r):
    yield n
    if n < r-1:
        yield from sayac(n+1,r)
    else:
        return

print(list(sayac(0,10))) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Coroutine fonksiyonlarda yield ve yield from kullanımı

# x = yield,iki yönlü generator iletişimidir
# x = yield ifadesi,generatorü dışarı döndürürken aynı zamanda da dışardan veri almaya hazır hale getirir
# bu veri alma işlemini send() metodu aracılığı ile yaparız

def f():
    yield 1 # birinci durak
    x = yield # burda fonksiyon bekler ve solda değer olmadığı için None döndürür send() metodu ile değer veririz.from
    yield print("bitti") # burda tekrar bir yield kullanımı yaptık çünkü;
# python'da bir generator tükendiğinde(ki bu fonksiyonda artık başka yield kalmaması demek) __next__() fonksiyonu,StopIteration Hatasını vermekle yükümlüdür
# bu artık o generator'ün bittiğini sana bildirir
# eğer bu fonksiyonda sonda yield yerine return kullansaydık,send() metodu kullanınca hata alırdık çünkü return anahtar kelimesi;
# generator fonksyionlarda hem bir sonlandırıcıdır ama aynı zamanda artık generator'ün bittiğini ifade eder bu nedenle bu generator bittiği içinde python;
# StopIteration hatası verir


# send() Metodu

# send() metodu,bir generator'ün dışardan veri almasını ve kendi içinde üretilen verinin dışarıya döndürürmesini sağlayan bir metoddur;

# sözdizimi: generator.send(value) generator: yield içeren bir generator nesnesi, value: generator'e gönderircek olan değer

# send() metodu,fonksiyonu ilerlertir bir sonraki yield ifadesine taşır
# send() metodunun dönüş değeri,generator içinde o anda yürütülen yield ifadesinin değeridir yani yield ifadesinin sağındaki değeri;
# send() metodu döndürebilir
# corotine fonksiyonlarda değer beklenirken illa değer vermene gerek yoktur python,değere otomatik olarak None atar

# Neden direkt send() metodu kullanılamaz ?;
# bir generator'ün dışardan veri alması ve veriyi dışarı döndürebilmesi için fonksiyonun kontrol akışı duraklatılmalıdır
# bir fonksiyondaki durak noktaları ise yield veya yield from'dur fonksionumuz,sadece bu noktalardan alışveriş yapabilir bu durumda bu anahtar kelimelere;
# alışveriş noktası demek yanlış olmaz
# bir generator fonksyionunda direkt send() kullanılamaz çünkü fonksiyon daha başlamamıştır şu anki konum yield değildir
# bu nedenle eğer kullanılırsa TypeError hatası alınır bunun önüne geçilmek için next() veya send(None) kullanılır bu iki fonksiyon/metod'da fonksiyonu;
# mevcut konumadan bir sonraki yield(alışveriş) noktasına taşır

# Çok Kritik Not: y = yield bir Statements işlemidir bu nedenle python ilk sağ taraftaki yield Expression'nı değerlendirir bu durumda;
# 1) Durur ve Dışarıya None döndürür
# 2) beklemeye geçer
# 3) bir sonraki send() çağrısıyla dışardan verilen değeri x'e atar yani kod bloğu next() metodu veya send(None) ile ,x = yield satırına geldiğinde hemen değeri x'e atmaz
# sonraki işlem olarak send() kullanılmalı işte -KOD-> y = yield ; send(20) denilmesi gerek
# şimdi yield et sonra değeri, x değişkenine atama tap


# örnek 1;

def f():
    print("yield 1")
    yield 1
    print("yield 2")
    yield 2
    print("bekleniyor: x = yield")
    x = yield
    print("x değeri:", x)
    yield x * 3
# bu fonksiyon çağrıldığında bir generator döner

gen = f()

# şimdi bu generator'e veri göndermek için bizim x = yield satırına göndermemiz gerek;

gen.send(None)
gen.send(None)
gen.send(None)
# 3.tane kullandık bunun sebebini tanımda açıkladık şuan x = yield satırındaki yield çalıştı ve x değer bekliyor
"""
yield 1
yield 2
bekleniyor: x = yield
"""

işlem =gen.send(10)  # x değeri: 10
# burda send() metodu,10 değerini x değişkenine atadı ve bir sonraki yield noktasına fonksiyonu taşıdı
# ve send() metodunun döneceği değer,yield ifadesine bağlı olduğundan ve yield'in de ifadesi olduğu için send(),veri döndürcek

print(işlem) # 30

print(işlem) # 30

# örnek 2;

def f():
    x = yield 1
    yield x

gen = f()

print(gen.send(None) )# x = yield 1 satırının yield ifadesini atladık şuan fonksiyon,beklemede # 1
# aynı zamanda yield 1 olduğu için send(),1 değeri döndürdü

print(gen.send(2)) # 2
# burda send() metodu,fonksiyonu ilerletti sonraki yield ifadesinde değer olduğu için send(),değer döndürdü


# next(gen) VS send(None) arasındaki fark;

# next(gen) ve send(None) aynı işlevi yerine getirirler ancak send(None) kullanımı,generator'ün veri alışverişine hazır bir coroutine
# olduğunu vurgular bu nedenle coroutine tarzı fonksiyonlarda kodun niyetini daha iyi belli etmek,kodun okunaklığını arrtırmak için send(None) kullanılır
# eğer sadece veri döndüren bir generator fonksiyonun varsa zaman next(gen) kullanmak daha pythonic olur
# next(gen) generatorü,pasif başlatırken,send(None) generatörü,etkileşimli başlatır

# next(gen) basit üreticilerde tercih edilir;

def Sayac():
    i = 0
    while True:
        yield i
        i += 1

# bu fonksiyonun amacı sadece basit bir şekilde veri üretmek olduğu için burda send() kullanılmasına gerek yok çünkü
# fonksiyonun alabilceği bir durak,yield noktası yok

sayac =Sayac()

print(next(sayac))
print(next(sayac))
print(next(sayac))
"""
0
1
2

"""

for i in sayac:
    if i > 20:
        break
    print(i)
# burda for kullandık çünkü for döngüsü zaten arka planda next() fonksiyonunu kullanacağı için
# basit üretici olarak kullanma için çok iyi bir örnektir

def dinleyici():
    print("hazırlık...")
    x = yield "dinliyor..."
    print("gelen",x)

gen = dinleyici()

print(gen.send(None) )# burda next kullanmadık çünkü bu fonksiyon coroutine gibi davranan bir fonksiyon yani veri alışverişine hazır durumda
"""
hazırlık...
dinliyor...
"""

try:
    gen.send(20) # gelen 20
except StopIteration: # bitti Çalıştı
    print("bitti")

# çünkü dinleyici fonksiyonunda ...yield "dinliyor" ifadesinden sonra başka bir yield yok demek oluyorki generator bitti
# bu durumda __next__() fonksiyonu StopIteration hatası döndürmek zorundadır eğer burda print("gelen"..'den sonra yield kullansaydık hata almazdık çünkü generator hala bitmemiştir
# kontrol edelim;

def dinleyici():
    print("hazırlık...")
    x = yield "dinliyor..."
    print("gelen",x)
    yield "bitti"
gen = dinleyici()

print(gen.send(None))
print(gen.send(10)) # burda send() metodu,hem dışarıdaki değere x'e atadı sonra bir sonraki yield noktasına gitti ve oraki değeri döndürdü
# bu durumda artık bu fonksiyonda başka bir yield kalmadığı için bu fonksiyon bitti

"""
hazırlık...
dinliyor...
gelen 10
bitti
"""
# burda hata almadık çünkü send() en son satırda bulunan yield ifadesini döndürdü ve orda bitti
# yield yerine return olsaydı,send() metodu,fonksiyonu ilerleteceği için ve başka bir yield kalmadığı için StopIteration hatası verirdi

# örnek 3;

def toplayacı():
    toplam_değer = 0
    while True:
        inpu = yield toplam_değer
        toplam_değer += inpu

toplama = toplayacı()

print(toplama.send(None)) # 0 -> toplam_değer => 0 olduğu için
print(toplama.send(1)) # döngüden dolayı send(),fonksiyonu ilerletti ve sonraki yield ifadesine kadar çalıştırdı
# yield'in ifadesi olduğu içinde  toplam_değer'i döndürdü

print(toplama.send(2)) # 3