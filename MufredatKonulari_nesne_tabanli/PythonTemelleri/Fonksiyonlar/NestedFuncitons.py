# Nested Functions

# bir fonksiyonun içinde başka bir fonksiyon tanımlı olabilir bu yapıya nested functions denir
# fonksiyon tanımlama sırasında fonksiyon çağrılmaz sadece nesne olarak oluşur ve tanımlama, fonksiyonun bulunduğu mevcut scope'a bağlıdır
# dıs fonksiyon kodlandığında,global scope'da tanımlı hale gelir ama ic fonksiyonlar tanımlı değillerdir python'da isimler,tanımlandıkları scope'a aittirler;
# ic fonksiyonu,dıs fonksiyonun local scope'unda yaşayan bir isimdir ve ancak dıs fonksiyon çağrıldığı zaman tanımlanır ve sonra çağrılabilir

def dis():

    print(locals())

    def ic():

        print("ben içim")

    ic()
    print(locals())
dis() # ben içim
# burda ic() fonksiyonu,dıs fonksiyonun local scope kapsamı içinde tanımlanmıştır
# ic() fonksiyonu dış dünya gözükemez sadece dıs() fonksiyonu çalıştığında görünebilir

"""
{}
ben içim
{'ic': <function dis.<locals>.ic at 0x760907f20e00>}
"""
# burda ilk önce locals boş çünkü henüz bir tanımlama yok ama ic() fonksiyonu tanımlandığı zaman local scope da bu ic() fonksiyonun
# tanımlı olduğunu görüyoruz bu fonksiyon nested functions frame'inde saklanır

"""
>>> def dıs():
...     def ic():
...             return
...     return ic()
... 
>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'dıs']"""
# mesela burda dıs fonksiyonu ve onun içinde de ic fonksiyonu tanımladık ama global scope'da sadece dıs fonksiyon tanımlı


# Stack Çalışması

def Dıs():
    print("dış")
    def Ic():
        print("ic")
    Ic()
    print("bitti")

Dıs()
"""
1. önce Dıs() fonksiyonu çağrıldı -> stack'e girdi çünkü sadece Dıs fonksiyon tanımlı şuan
2. print("dış") çağrıldı
3. Ic() fonksiyon tanımlandı ama çağrılmadı şuanda local'de isim olarak duruyor
4. Ic() fonksiyon çağrıldı -> stack'e girdi 
5. print("iç") çağrıldı
6.Ic() fonksiyon bitti -> stack'den çıkıldı silindi
7.print("bitti") çağrıldı
8.Dıs() fonksiyon biti -> stack'den çıkıldı silindi
"""


# Neden Nested Funcitons kullanılır

# sadece bir fonksiyon içinde kullanılcak yardımcı bir işlemi ayrı tanımlayıp modülerliği arttırmak için
# ic fonksiyonun yalnızca dıs fonksiyon üzerinden erişebilmesi,dış dünyadan erişilememesi için kullanılır

# Enclosing Scope Nedir: iç içe olan fonksiyonlarda,iç fonksiyonun erişim sağlayabildiği dış fonksiyonun kendi local scope'u

# Closure Nedir: bir iç fonksiyonun enclosing scope'taki değişkenleri taşıyarak dışarıya aktarılmasıdır
# bu aktarma işlemi sayesinde fonksiyon kapansa bile dışardan değişkenlere erişilebilir ve manipüle edilebilir
# Not: eğer obje mutable ise hata alınmaz çünkü python,mutable nesnelerde yeniden bir tanımlama işlemi yapmaz sadece in-place bir işlem yapılır
# python ismi aramaya: local -> enclosing -> global -> built in sırasını izleyerek bulur değişken adını enclosing'de bulur
# ama iç fonksiyonun kendi scope'unda(local) o ismi bulamadığı için ama aynı zamanda ismi tanıdığı için hata alınır


# aynı zamanda __closure__,bir fonksiyonun tanımladığı scope dışında tanımlanmış ama hâlâ bağlı kaldığı değişkenleri saklayan
# bir magic name'dir kısacası eğer bir ic fonksiyon, dış fonksiyonda tanımlanan değişkenleri kullanıyorsa __closure__ demetinde  tutulur
# eğer yoksa __closure__ None'dır;
# bu __closure__,fonksiyon tanımlarken python tarafından hemen ve tamamen(eager evaluation işlemine göre) oluşturulur sonradan ekleme yapılmaz
# ve cell eklenmesi için isimlerin aktif olarak kullanılmasına gerek yoktur ic fonksiyonun,enclosing scope aralıcığı ile erişebilmesi yeterlidir

# Closure;

def dıs():
    x = 10
    def ic():
        return  x
    return ic
# burda ic fonksiyonu tanımladıktan sonra ic fonksiyonun referansını döndürdük çünkü burda;
# dıs() fonksiyonu çağırdığımız zaman dış fonksiyon sonlancak ve bize ic fonksiyonun referansını döndürcek
# ve closure sayesinde dış fonksiyonda tanımlı olan değişkeni dış fonksiyon kapandığı halde iç fonksiyondan erişebilceğiz

f = dıs()
print(f()) # 10

# Enclosing;

def dıs():
    x = 30
    def ic():
        return x
    return ic()
# burda closure kullanılmadı çünkü ic fonkisyonu dıs fonksiyonun içinde çalıştırdığımız için enclosing scope sayesinde
# ic fonksiyon,x değişkenine ulaşabildi

print(dıs()) # 30

# eğer dış kapsamdaki bir değişkeni değiştirmeye çalışırsan hata alırsın;

def a():
    yas = 20

    def b():

            #yas += 10
            ...
    b()

try:
    a()
except UnboundLocalError as e: print(e.args) # ("cannot access local variable 'yas' where it is not associated with a value",)

# obje mutable ise hata alınmaz python,bu durumda yeniden bir oluşturma-bağlama işlemi değil bir in-place işlemi yapar sadece

def x():

    listem = []

    def y():
        listem.append(1)
    y()
    return listem

print(x()) # [1]


# nonlocal anahtar kelimesi

# nonlocal anahtar kelimesi,nested function'larda, bir dış(ama global olmayan) kapsamdaki immutable nesneyi manipüle etmek amacıyla kullanılır
# normalde immutable bir nesneyi iç fonksiyondan manipüle edemezsin çünkü;
# python o veriyi bulmak için > local->enlosing->global->built-in sırasını izler ve o nesneyi enclosing'de bulur
# ama  o veriyi değiştirmek için kendi local scope'unda tanımlı olması gerekir ve tanımlı olmadığı için ama aynı zamanda o objeyi tanıdığı için UnboundLocalError hatası alınır
# nonlocal,nested funcitonların global'i dir
# nonlocal,herangi bir işlem yapmaz veya expression döndürmez,sadece bildiridir, değişkeni local bu fonksiyon içinde local olarak değil
# bir dış(enclosing) fonksiyonunda ara demektir

def x():

    isim = "demir"

    def y():

        nonlocal isim # burda isim adlı değişkenin local olmadığını dış kapsamda tanımı bir isim olduğunu local değil unlocal olarak kullanacağımızı bildirdik

        isim = "aslı"
    y()
    return isim
print(x())  # aslı

# bir örnek;

def u():
    def u1():
        isim2 = "mwf"
        print("çalışıyorum")
        return isim2
    return u1()

print(u())

isi1 = u()

print([isi1])
"""
çalışıyorum
mwf
çalışıyorum
['mwf']
    ✅ u() fonksiyonunun içinde tanımlı u1() fonksiyonu var
    ✅ u() → return u1() der, yani u1()’i çalıştırır
    ✅ u1() içinde hem print, hem return var
    ✅ return edilen değer dış dünyaya çıkar
    ✅ u() çağrıldığında otomatik olarak iç fonksiyon da çalıştığı için çıktı tekrar oluşur
 print(u()) satırı:

    u() çağrılır

    İçinde u1() çağrılır:

        print("çalışıyorum") çalışır

        "mwf" değeri döner

    u() de bu değeri dışarı döndürür

    print() bu "mwf" değerini ekrana yazar
isi1 = u() satırı:

    Aynı u() yine çağrılır

    u1() yine çağrılır:

        Yine "çalışıyorum" yazılır

        Yine "mwf" döner ve isi1 olur
"""

# Nested function'larda parametre tanımı

def f(fon): # f ismini kullanacağım ve bu isme ait çalıştırılabilir bir kod bloğu tanımlıyorum ve bu fonksyion fon adında sabit tanımlı bir parametreye sahip
    def p(x=None,**kwargs):
        print(x,kwargs)
        return x
    return p
# f() fonksiyonu,p fonksiyonun kendisinin referansını dönecektir p() fonksiyonun aldığı argümanlar verirmiştir

p1 = f(x)

print(type(p1)) # <class 'function'>

x1 = p1("demir",aslı="anne") # demir {'aslı': 'anne'}
# burda p() fonksiyonu çalıştı çünkü çağırdık
3
print(x1) # demir
# p() fonksiyonu,x sabit tanımlı pozisyonel bazlı argümanı döndürdüğü için "demir" döndürdü

# şimdi ise f() fonksiyona verilen fon argümanını kullanalım

def x(a,**anahtarlar):
    return (a,anahtarlar)
# burda bir x adında fonksiyon tanımladık bu fonksiyon,x sabit tanımlı parametre ve anahtarlar adında bir key word only parametresi var

def f(fon): # -> bu f() fonksiyonu fon adında bir argüman alıyor...
    def p(x=None,**kwargs): # -> bu iç fonksiyon olan p() fonksiyonu,iki tane parametreye sahip x ve kwargs şeklinde
        print(x,kwargs) # -> bu parametrelerin değerlerini print ile standart kontrol akışına yazdırıyor
        return fon(x,**kwargs) # -> return ile dış fonksiyona verilen fon argümanını çalıştırıyor ve bu fon fonksiyonuna, p() fonksiyonunda tanımlanan x ve kwargs değerlerini taşıyor
    return p# en sonda da f() fonksiyonu, p() fonksiyonun kendisinin referansını döndürür ama çalıştırmaz

x1 = f(x)
print(x1("tuntunsahur",kelime=1))

"""
tuntunsahur {'kelime': 1}
('tuntunsahur', {'kelime': 1})
"""


# Dekarator

# dekarator,bir fonksiyonu alıp ona ekstra davranışlar(girişler,çıkışlar,kontroller vb.) ekleyip değiştirilmiş(modifiye) halini döndüren yapılardır
# bu yapılar özünde bir fonksiyonun dekarator şekliyle kullanılmasıdır yukarıda ki örnekte ki f() fonksiyonu dekarator gibidir
# fonksiyonun içeriğini değiştirmeden hatta hiç görmeden onun çevresine süs(fonksiyonun davranışını değiştirmeden ona ekstra özekkikler katmak demektir süsün karşılığı yukarıda ki örnekte p() fonksiyonu),
# koruma,kayıt,ölçüm gibi özellikler eklemesidir bu sayede kod tekrarlarını azaltır
# Python dekoratörleri = closure + fonksiyon döndüren fonksiyon

# dekarator,@ işareti ile gösterilir: @ işareti,dekatratorü görsel olarak ayırt etmesi kolay,kullanılmayan bir işaret olduğundan,kolay yazılabilen bir
# işaret olmasından dolayı seçilmiştir

# dekarator,tasarlarken nested function kullanılır çünkü her çağrıda çalışacak bir yapı gerekli o da ancak closure olur bu nedenle
# eğer iç yapıda fonksiyon kullanılmazsa dıştaki fonksiyon çalıştığı anda orjinal fonksiyon çalışır bu nedenle ic fonksiyonda tanımlı olan parametreleri dikkatli yönet eğer orninal fonksiyon,parametre almıyorsa bu iç fonksiyonda parametre tanımlama çünkü kullanılmayacak
# ve bu yapmak istediğimiz 'süs' işlemlerini yapamayız onlara süre yetmez çünkü fonksiyon çalıştı ve bitti

def dekerator(fonk): # temsilen dekarator koyduk
    def sarmalayıcı(): # iç yapı yani süs,artık dekerator() fonksiyonuna verilen fonksiyon bizim bu süs fonksiyonu olur her çağrıldığında çalışır
        print("sarmalayıcı çalışıyor")
        fonk() # orjinal fonksiyonu çağırır çünkü orjinal fonksiyonu hala kullanmak istiyoruz
        print("sarmalayıcı hala burda")
    return sarmalayıcı # yeni davranışlı modifiyeli fonksiyonu döndürür
# bu kod en basiti ile bir dekeratordür yukarıda ki örneğe çok benziyor aslında

def selam():
    print("merhaba :)")
# şimdi amacımız bu fonksiyonun içeriğini/davranışını değiştirmeden sadece süslemek ekstra yeni davranışlar eklemek ama işte bunları dışardan yapacağız

selam = dekerator(selam)
# dekarator aslında ^ demektir
print(selam())
"""
sarmalayıcı çalışıyor
merhaba :)
sarmalayıcı hala burda
None
"""

# ama selam = dekerator(selam) kullanımı çok büyük bir ırgatlık biz bunu istemiyoruz bu nedenle @ harfini kullanmışlar

@ dekerator
def selam():
    print("merhaba :)")
# bu kullanımı daha iyi daha net
# ama hâlâ iş bitmiş değil hatırlarsan fonksiyon tanımlamak çalıştırmak demek değil

selam()
"""
sarmalayıcı çalışıyor
merhaba :)
sarmalayıcı hala burda
"""


# şimdi ise argümanlı bir şekilde örnek yapalım 2 yukarıda ki örnekte olduğu gibi aynı mantıkla olcak;

listem = ["demir","ozan","doruk"]
def kontrol(fonk:callable) -> callable: # burda argümanın beklediği tipi callable olarak verdik ve bu fonksiyonun döndürdüğü tip olarak callable verdik
    """hedef fonksiyona verilen elemanlar listem listesinde olup olmadığını kontrol eder
    eğer tüm argümanlar listede ise hedef fonksiyonun çalışmasına izin verilir aksi halde işlemler sonra erer"""

    def sarmalayıcı(*args): # args: tüm verilen sıralı pozisyoneller burda saklancak bu args parametresini orjinal fonksiyona argüman verirken kullanacağız
        if all(kelime in listem for kelime in args):
            print("kontrol başarılı")
            return fonk(*args)
        else:
            print("geçersiz giriş")
            return
    return sarmalayıcı

@ kontrol
def giriş(*args):

   metin ="".join(map(lambda x: f"hoşgeldiniz -> {x}",args))
   return metin

print(giriş("demir"))


# stack çalışma mantığı;

def dekoratör(f):
    print("dekoratör çalıştı")

    def sarmal(*args, **kwargs):
        print("sarmal çalıştı")
        return f(*args, **kwargs)

    return sarmal

@dekoratör
def fonksiyon():
    print("fonksiyon çalıştı")

fonksiyon()

"""
1) @dekorator satırı görüldü,python bu satırı: fonksiyon=dekoratör(fonksiyon) şeklinde yorumlar
2) dekoratör() çağrılır -> stack'e gider
3) print("dekoratör çalıştı") çağrılır
4) sarmal() fonksiyonu tanımlanır ama çağrılmaz 
5) dekoratör fonksiyonu,sarmal fonksiyonun referansını döndürür ve fonksiyon biter
6) fonksiyon() satırı artık sarmal() fonksiyonu temsil eder dolasıyla sarmal() fonksiyonu çağrılır -> stack'e gideer burda closure'ın önemi kritiktir
7) print("sarmal çalıştı") fonksiyonu çağrılır
8) return ile f() fonksiyonu yani orjinal "fonksiyon" fonksiyonu çağrılır ama fonksiyon bitmez (return,statments işlemdir bu nedenle önce sağ taraf değerlendirir)
9) print("fonksiyon çalıştı") çarğılır
10) "fonksiyon" fonksiyonu() biter ve stack'den çıkılır silinir
11) sarmal fonksiyonu biter() stack'den çıkılır temizlenir
"""