# Class

# python'da class, veriyi(attribute) ve bu veriye ait davranışları(method) aynı yapı altında toplamak için vardır
# class, aynı türden nesneleri tanımlamak için kullanılan özellik ve davranış içeren özel bir nesnedir
# bu,programlamada nesne yönelimli yaklaşımının(oop) temelidir


# Peki neden sınıf kullanırız ?

# 1) Karmaşık verileri yönetmek için: gerçek dünyadaki problemler büyüktür,sınıflar sayesinde her şeyi nesnelere bölerek daha küçük
# ve yönetilebilir bir hale getiririz

# 2) kod tekrarlarını azlatmak: aynı yapıdaki ama farklı değer taşıyan birçok nesne için yeniden kod yazmak yerine,sınıfı bir kere yazarsın ve tek yapman gereken ondan örnke oluşturmaktır

# 3) anlamlı orginazasyon: attribute + method, aynı yerde olunca kod;daha sade,anlamlı ve güvenli olur

# 4) genişlmeye açık bir yapı kurmak için: sınıflar kalıtım sayesinde başka bir sınıf tarafından donatılabilir bu onları,daha az tekrar ve daha fazla esneklik sağlar

# teknik olarak class, __new__() + __init__() metodları ile yeni bir nesne üretir

# sözdizimi;

class ClassName:

    def __init__(self):
        pass

"""
class: class,yeni bir şablon oluşturmanı sağlar(yani class -> şablon oluşturucu) bu şablon,daha sonra nesneler üretmek için kullanılır 

ClassName: ClassName,burda şablon adıdır, tip tanımıdır

def: sınıf içinde tanımlanan çağrılabililir bir bloktur bu bloğun adı __init__'idir 
varsayılan sözdiziminde __init__ kullanılmasının nedeni zaten object sınıfında bulunan __new__ metodu,mutable sınıflar için yeterlidir
__init__ ile veriyi başlatmak çoğu zaman yeterli olur 

self: self,bir sınıfın içindeki metodlarda, o sınıfın oluşturduğu nesnenin kendisini temsil eder 
self,python'un "bu işlem,hangi nesneye ait ? " sorusuna verdiği cevaptır 
aynı zamanda self,bir konvansiyonel(geleneksel) bir isimdir ama güçlü olanlarından bu nedenle çoğu zaman 
bu isme sadık kal 
"""

# Class Body(sınıf gövdesi)

# Sınıf gövdesi,python'da bir sınıf tanımı yapıldığında class anahtar kelimesi ile birlikte açılan blok içinde tanımlanan tüm kodları kapyasan bir bölümdür
# bu gövde,sınıfın oluşturulması anında bir kez çalışır ve sınıfa ait herşey(attribute,method,isimler..) burdadır


# Özellikleri

# sınıfın doğrudan bellekte oluşmasını sağlar
# içindeki değişken atamaları,class attribute'ları oluşturur ve bu attribute'lar sınıf içinde her yerde kullanılabilir

# class anahtar kelimesinden sonra yeni bir scope açılır ve bu scope içinde tanımlı olan isimler,class locals adında frame'de tutulur(stack)
# python,geçici bir namespace(local sözlük) oluşturur,bu scope içinde tanımlanan her şey bu namespace içine konur
# bu oluşturulan sözlük type ile sınıf nesnesine çevrilir
# en sonunda bir tane sınıf nesnesi oluşmuş olur ve bu sınıf adını,global scope'da tutar

class Araba:
    x = 10
    def run(self):
        ...
# 1) geçici bir local sözlük oluşturulcak
local = {} # temsili

# 2) bu local sözlüğün içine sınıfta tanımlı olan tüm arribute'lar eklencek
local["x"] = 10
local["run"] = lambda self:...

# 3) local sözlüğü, type fonksiyonu ile bir sınıf nesnesine çevrilcek
Araba_ = type("Araba_",(),local)

# 4) Araba_ adını global scope'a ekler

# Sınıf gövdesinde tanımlı herşey "sınıf tanımında " çalıştırılır mesela;

class Z:
    print("class Z tanımlandı")
# class Z tanımlandı -> ÇALIŞTI
# burda sınıfı, çağırmana gerek yoktu sınıf gövdesinde tanımlı olan nenseler,sınıf tanımlamada bir kez  çalıştırılır

# __init__() Metodu

# __init__() metodu,bir sınıftan yeni bir nesne oluşturulurken,o nesneyi başlatmak için kullanılan özel bir dunder(double underscore) metoddur


# sözdizimi
def __init___(self,param1,param2):
    self.param1 = param1
    self.param2 = param2
"""
self: nesnenin kendisi,zorunlu olarak ilk parametredir
params: kullanıcının nesneyi oluştururken vereceği değerler 
self.param1: değerleri,nesneye ait hâle getirir 
"""

# Örnek 1;

class A:
    def __init__(self):
        self.isim = "d"
        # burda "d" değeri,self yani a ismine bağlanır ve saklanır
        # aynı zamanda hiçbir parametre tanımlamadık dolasıyla hiçbir veri almadan,hard-coded yaparak nesneye,"d" adını otomatik verdik
        # bu durumda kullanıcının A() çağrı işleminde herangi bir parametre vermesine gerek kalmaz ama bu sınıftan oluşturulan tüm nesneler;
        # hepsinin isim değeri, "d" olur

a = A()
print(a.isim) # a

# Örnek 2;

class B:
    def __init__(self,nesne):
        self.nesne = "B"
        # burda nesne adında bir pozisyonel bazlı sabit isim tanımladık, bu durumda B() sınıf çağrısında
        # kullanıcının nesne parametesine,argüman vermesini zorunlu kıldık self ile de nesne parametresini, nesneye ait hâle getirdik

b = B("b") # B(),bizden bir tane zorunlu parametre'ye argüman istiyor bu nedenle değer verdik
print(b.nesne) # B

# örnek 3;

class Öğrenci:
    def __init__(self,ad,yaş,okul):
        self.ad = ad
        self.yaş = yaş
        self.okul = okul

ogrenci1 = Öğrenci("demir",20,"AÜ")

print(", ".join(f"{getattr(ogrenci1,name)}" for name in ogrenci1.__dir__() if not name.startswith("__") ))
# demir, 20, AÜ

