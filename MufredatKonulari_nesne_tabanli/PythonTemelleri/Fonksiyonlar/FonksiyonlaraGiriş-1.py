# Fonksiyonlara giriş
""" """


# fonksiyon,bir görevi gerçekleştiren,tekrar tekrar çağrılabilen çağrıldığında expression dönen,bağımsız isme sahip olan
# kod bloklarıdır
# python'da iki tip fonksiyon bulunmaktadır bunlar sırasıyla: built-in functions ve user-definded function olmak üzere ikiye ayrılır


# user-definded function: kullanıcı tarafından tanımlanan özel amaçlı fonksiyonlar

# Neden Geliştirildi;
# 1) koda modülerlik sağlamak için => karmaşık bir kod bloğunu ayırmak her işlemi ayrı oluşturmak,hata ayıklamayı-okunaklığı ve kodun
# gelecekte büyütülmesini kolaylaştırır

# 2) parametreler ile esneklik sağlama => gerek lambda gibi inline fonksiyonlar gerekse normal fonksiyonlar parametre olarak
# başka bir fonksiyonda kullanılabilir

# 3) soyutlama ve anlam katmak için => kodun amacının ne olduğu belirtmek, ne yaptığını açıkça göstermek için kullanılır

# 4) bellek ve zaman tasarrufu => bellek bir kere ayrırır ve tekrar tekrar çağrırır(her işlemde yeniden bu fonksiyon oluşturulmaz) bu durumda bellek daha optimize kullanılır
# ve kendini tekrar etmene gerek kalmaz


# fonksiyonlar hakkında bilinmes gerekenler;

# 1) fonksiyon adı identified ve key name'ler ile aynı olmamalı ve mümkünse ASCII olsun bu taşınabilirliği arttırır

# 2) bir fonksiyonun dış dünyada veya bir obje üzerinde değişiklik yapmasına side effect denir buna izin verme mümkünse pure function kullan
# pure function: aynı girdiler ile çağrılığında aynı sonucu veren hiçbir şekilde side effect'i bulunmayan fonksiyonlara pure function denir
# pure functionlar;dosya yazmaz,print etmez,global bir değişkeni değiştirmezler büyük sistemlerde genelde pure function güvenlik açısından kullanılır

# 3) her bir fonksiyon tek bir işlem yapmalı ayrıca uzunluğu 15 satırı geçmemelidir

# 4) fonksiyonun ismi ile yaptığı iş örtüşmelidir ismiyle uyumlu olmalıdır ve ismi sade,anlaşıabilir olmalı
# uzun ama anlamlı bir fonksiyon adı her zaman kısa ve anlamsız fonksiyon isminden daha anlamlıdır

# 5) bir fonksiyonu tanımlamak,çalıştırmak anlamına gelmez eğer bir fonksiyonu çağrımazsan çalışmaz

# 6) fonksiyonlar birinci sınıf vatandaştır veri gibi kullanılabilirler(veri gibi taşınabilirler,aktarılabilirler,değişebilirler)


# fonksiyon tanımlama;

# fonksiyon tanımlamak için def anahtar kelimesi kullanılır def define'nin kısaltmasıdır türkçesi ise tanımlama mânasına gelir
# python yorumlayıcısına,def anahtar kelimesini yazınca: bir isim vereceğim ve bu isme ait çalıştırılabilir kod bloğu tanımlıyorum dersin

"""def <fonksiyon_adı>():
        '''Docstring-açıklama'''
        
        <Statements>
        
        return <deger>
"""
# parantez(): fonksiyon tanımlamasında kullanılan parantezler,fonksiyonun parametre alabildiğini belirtir parametre adları parantez içine
# yazılır ayırca fonksiyonlar çağrılabilirler ve callable bir obje oluşturmak için parantez gereklidir
# Not: lambda'nın tanımlanması kolay olması açısından parantez kullanılmaz bu tasarımsaldır

# iki nokta(:): fonksiyon bloğunu başladığını gösteriyor python,girintiler sayesinde altındaki satırların bu fonksiyon
# bloğuna ait olduğunu anlayacak

# Docstring: docstring,bir fonksiyonun veya sınfın ne yaptığını açıklayan özel bir string'tir
# docstring,fonksiyonun ilk satırında tanımlanır ve üç tırnak ile yazılır fonksiyon çağrıldığında çalışmaz sadece
# help() fonksiyonunda açıklama kısmında bilgi vermesi için kullanılır
# docstring,yorum satırı ile karıştırılmamalıdır yorum satırları,python tarafından atlanır ama docstring,değerlendirilebilen bir ifadedir
# docstring,magic name ile ilişkilendirilir(__doc__) __doc__,bir string'tir

# statements: statements,birbirlerinden bağımsız işlem ifadeleridir fonksiyonlarda bu işlem türü kullanılır
# bu işlem türüne:koşul tanımlama,döngü kullanımı,içeri aktarma,fonksiyon tanımlama,değişken tanımlama,exception handling yapmak dahildir
# lambda bunların hiçbirini yapamazdı çükü expression ifade döndürürdü ama def() -> statements işlem türü içerir

# return: return,fonksiyondaki bir değeri döndürmek için kullanılan bir anahtar kelimedir return,fonksiyondaki local bir sonucu
# dışarı döndürür çoğu zaman bir işlem sonucu fonksiyonun değer döndürmesi beklenir bu durumda return kullanımı kaçınılmazdır
# return,aynı zamanda bir sonlandırıcı görevi görür return anahtar kelimesine ulaşıldığında işlemler sonlandırılır yani eğer;
# return kelimesinden sonra işlem varsa onlar çalışmaz
# bir fonksiyonda birden fazla return tanımlı olabilir bu durum karar yapılarına göre davranış değiştirme sonucu dinamik olan
# işlemlerde çok sık kullanılır ama sakın aklından çıkarma bir fonksiyonda sadece bir return çalışabilir(3 tane return olsun bunlardan sadece 1'İ çalışacak sonra işlemler bitecek)
# retrun herangi bir değer dönebilir:str,list,tuple,dict,generatır vb... ayrıca return,birden fazla nesneyi döndürebilir bu durumda ifadeleri ayırmak için virgül kullan
# return bu işlemde tuple döndürür parantez koymana gerek yok tuple tanımı için paranteze gerek yok

# return, başlı başına bir statements'dır ama expression döndürür çünkü sağ taraf,expression bir ifade olmalı ve atama veya eşleştirme yapmaz bu nedene return = .. veya return:.. gibi kullanımlar yanlıştır
# Not: nested function'larda return ile bir fonksiyonu çağırabilir ve döndürebilirsin return y() -> fonksiyonu çağır ve döndür demek iken return y -> fonksiyonun referansını döndür demektir
# fonksiyon çağrıların expression olmasını sağlayan unsur,return kelimesidir return,içteki local bir veriyi dışarı döndürür çünkü return bir expression işlem döndürür
# dolayısıyla fonksiyon çağrıldığında return,değeri döndürceği için fonksiyon çağrısı expression bir işlem olur
# return statements bir işlem olduğu için önce sağ taraf değerlendirilir

# Not2: break anahtar kelimesi bulunduğu döngüyü sonlandırır fonksiyonu sonlandırmaz eğer döngüden sonra başka bir kod yoksa fonksiyon kapanır
# ama bu kapanmanın nedeni break değil,yürütülcek olan kodların bitmesidir fonksiyonu sadece return erkenden sonlandırabilir

def selam(metin,/):
    """bu fonksiyonun amacı formatlama yaparak selamlama
    metin, sadece pozisyonel bazlı argüman alabilir
    """
    return f"Merhaba {metin} !"
# burda parantez içinde parame tanımladık aynı zamanda callable bir obje yaratmak için onlara ihtiyacımız vardı
# iki nokta ile fonksiyon bloğunun başladığını gösterdik
# amacımız formatlama yaparak değeri değiştirmek olduğundan ve bunu dış dünyaya döndürmek istediğimiz için return kullandık
# bu sayede atama yapabildik

# şimdi ise help fonksiyonu ile docstring'e bakalım;

print(help(selam))
"""
selam(metin, /)
    bu fonksiyonun amacı formatlama yaparak selamlama
    metin, sadece pozisyonel bazlı argüman alabilir

"""
# görüğün üzere fonksiyonun başında tanımladığımız docstring çalıştı aynı zamanda bu metne __doc__ile de ulaşılabilir

print(selam.__doc__)
"""
bu fonksiyonun amacı formatlama yaparak selamlama
    metin, sadece pozisyonel bazlı argüman alabilir
    
"""

x = selam('demir')

print(x) # Merhaba demir !

# return olmadan;

def selam2(metin,/):
    f"Merhaba {metin} !"

print(selam2("demir")) # None
# gördüğün üzere değer dönmedi ama içerdeki işlemler çalıştı
# bu fonksiyon,pure function'a güzel bir örnek şimdi ise bu fonksiyona side effect vererek dış dünyada değişiklik yapalım;

def selam3(metin,/):
    print(f"Merhaba {metin} !")

print(selam3("aslı")) # Merhaba aslı !
                      # None
# Bunun nedeni: bu fonksiyonda print() var ve bu dış dünyayı değiştiriyor ama return değeri olmadığı için python,otomatik olarak
# None döndürüyor çünkü varsayılan olarak fonksiyonun sonuna return None konulur ve return,bir expression işlemdir
# bu nedenle bu fonksiyon,return nedeniyle None döndürür, fonksiyon çağrıları expression'dır her türlü fonksiyonlar bir değer döndürmek zorundalardır 


# recursive(özyineli) function

# özyineli(recursive) fonksiyonlar,çözmeye çalıştığı problemin daha küçük bir versiyonunu kendi kendisine çağırarak
# çözme amacı güten bir fonksiyondur her çağrıda problem küçülür ve sonucunda bir durma şartına ulaşırak çağrı zincirini durdulur
# bazı problemler doğaları gereği kendisini tekrar eder recursive function'ların amacı bu problemleri her çağrıda küçülterek problemi bitirmek
#recursive fonksiyonlar çalışma mantığı gereği durma noktası(base case)'e ihtiyaç duyarlar eğer base case tanımlanmazsa  ve RecursionError hatası alınır

# recursive function,kendi adını kullanrak kendisini çağırır yani statements'de kendi fonksiyonumuzu çağırmamız sözkonusu
# her fonksiyon çağrısı stack'de yeni bir isim oluşturur bu isim oluşturma özelliği fonksiyonun sonuz döngüye girmemesinde önemli bir rol oynar

# Not: her tekrar eden işi recursive(özyineli) fonksiyonla yapmak mantıklı olmayabilir eğer amacın bir işlemi x kadar yapmaksa burda
# kontrol akış grupları kullanmak daha doğru olacaktır

# genel sözdizimi;
"""
def recursive_function(n):
    if <base_case>: # durma şartı
        return <sonuç>
    return recursive_function(n-1) # kendini çağıran adım     
"""
# Püf Noktası: fonksiyonun kendisini çağırmaması gereken ilk durumu bul bu durumda return ile sonuc döndür
# recursive function yazarken şunu kendine sor: hangi durumda artık kendimi çağırmam gerekmiyor

# Kullanım Alanları;
# Matematikte(faktöriyel,fibbonaci)
# veri yapılarında(ağaçlar,grafikler...)
# dosya yapılarında(klasör gezme)
# dosya formatlarında
# algoritmalar(merge sort,dfs)
# oyun/AI(hamle ağacı,tüm olası hamleleri denemek için ideal)
# dil işlemede(parser,AST çözümleme)
# dinamik programlama(yol bulma)
# kombinasyon üretimi(subset)

def merhaba(n):
    if n == 0:
        return
    print("merhaba",n)
    return merhaba(n-1)

merhaba(5)
"""
merhaba 5
merhaba 4
merhaba 3
merhaba 2
merhaba 1
"""

def factoriel(n):
    if n==0:
        return 1
    return n*factoriel(n-1) # burda factoriel fonksiyonunu çağırdık aslında ve her çağrıda yeni bir n yaratılıyor ve bu n;
# öncekinden daha küçük 3,2,1 şeklinde unutma fonksiyon çağrılarında parametre isimleri local scope'da tanımlı olurlar

print(factoriel(4)) # 24

def toplam(n):
    if n ==0:
        return 0
    return n + toplam(n-1)# burda her fonksiyon çağrısında stack'de yeni bir isim oluşturuluyor ve bu ismi yani > n
# her defasında bir ekiği olarak fonksiyona argüman olarak veriliyor bu nedenle n,her çağrıda eksiliyor

print(toplam(5)) # 15

def ters(str:str):
    if len(str) <= 1:
        return str
    return ters(str[1:]) + str[0]

print(ters("demir")) # rimed
"""
ters("demir")
↳ ters("emir") + "d"
    ↳ ters("mir") + "e"
        ↳ ters("ir") + "m"
            ↳ ters("r") + "i"
                ↳ len("r") == 1 → return "r"
"""

def duzle(lis):
    for i in lis:
        if isinstance(i,list):
            yield from duzle(i)
        else:
            yield i


print(list(duzle([1,2,3,[4,5,6],[7,8,9]])))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

def geriye_sar(n):
    if n == 0:

         return "bitti"
    print(n)
    return geriye_sar(n-1)

print(geriye_sar(5))
"""
5
4
3
2
1
bitti
None
"""
