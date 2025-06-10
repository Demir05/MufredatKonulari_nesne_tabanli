# Bir Sınıfın Özelliklerini Manipüle Etmek

# Python'da bir sınıf tanımladıktan sonra o sınıfa, ait Attribute'ları runtime esnasında manipüle edebilirsin buna: "sınıfı,dinamik olarak manipüle etmek denir"
# Sınıf özelliklerini manipüle etmek", Python’un esnekliğini ortaya koyan en güçlü özelliklerden biridir.
#Runtime'da sınıfın iç yapısını değiştirebilirsin
#Bu, güçlüdür ama dikkatli kullanılmalıdır
#Framework'lerin çoğu bu esnekliği kullanarak seni büyüler

# Ne Tür İşlemlerden Bahsediyoruz

# 1) Yeni Attribute eklemek: sınıf.ozellik = deger

# 2) attibute değerini değiştirmek: sınıf.ozellik = yeni_deger

# 3) attribute silmek: del sınıf.ozellik

# 4) dinamik metod eklemek: metod = lambda self: ...


# Kullanım Alanları

# Test amaçlı:
# → Geçici olarak sınıfa davranış eklemek veya düzeltmek

# Plugin / modül sistemleri:
# → Dış kodlar sınıfları değiştirebilir

# Performans optimizasyonu veya debug kolaylığı:
# → Belirli durumlarda özellikleri geçici olarak kaldırmak veya değiştirmek istenebilir



# __setattr__() Metodu

# __setattr__ metodu, bir nesneye bağlı bir attribute'a değer atandığında otomatik olarak çağrılan özel bir dunder (çift alt çizgili) metottur.

# obj.x = y gibi örnek (instance) düzeyinde yapılan her atama işleminde __setattr__ metodu çağrılır.
# Eğer sınıf içinde __setattr__ override edilmemişse, Python metod çözümlemesi (MRO) yapar ve object.__setattr__ metoduna ulaşarak doğrudan onu çağırır. aynı zamanda type sınıfında da bulunur ! 

# Bu durum, __init__() metodu içinde yapılan self.x = y gibi atamalar için de geçerlidir;
# çünkü bu da bir attribute atama işlemidir ve __setattr__ tetiklenir.

# __setattr__ metodu override edilebilir, fakat bu dikkatli yapılmalıdır.
# Eğer override içinde tekrar self.attr = val gibi bir atama yapılırsa sonsuz döngü oluşur.

# Örneğin bu hatalıdır:
# def __setattr__(self, name, value):
#     self.name = value  # ❌ sonsuz döngü oluşur

# Doğru kullanım:
# def __setattr__(self, name, value):
#     super().__setattr__(name, value)

    # 📌 Bu bir STATEMENT'tır → Python burada herhangi bir değer beklemez.
    # Bu yüzden __setattr__ içinde return kullanmak gerekmez, hatta anlamsızdır.
    
    # Eğer return yazarsan, Python bunu yoksayar (görmezden gelir).


# 🧠 NESNE ÜZERİNDEN ATTRIBUTE ATAMASI
# -------------------------------------
# obj.x = val işlemi çalıştığında:

# 1. Python şu çağrıyı yapar:
#    type(obj).__setattr__(obj, 'x', val) çünkü bu bir davranışsal işlemdir attribute atama,objenin ait olduğu sınıf tarafından kontrol edilir

# 2. Buradaki type(obj) → obj'nin sınıfıdır
#    Bu sınıf içinde __setattr__ override edilmiş mi diye bakılır

# 3. Eğer yoksa, MRO (Method Resolution Order) üzerinden aranır
# 4. Hiçbiri override edilmemişse:
#    → object.__setattr__(obj, 'x', val) çağrılır


# 🧠 SINIF ÜZERİNDEN ATTRIBUTE ATAMASI
# -------------------------------------
# Class.x = val işlemi çalıştığında:

# 1. Python şu çağrıyı yapar:
#    type(Class).__setattr__(Class, 'x', val)

# 2. Buradaki type(Class) → Class'ın metaclass'ıdır
#    (genelde 'type' ama özel bir metaclass da olabilir)

# 3. Eğer metaclass __setattr__ metodunu override ettiyse, o çalışır

# 4. Override yoksa:
#    → type.__setattr__(Class, 'x', val) çağrılır


# Not: type sınıfında bulunan __setattr__,descriptor değildir ve herangi bir geri dönüş değeri yoktur.  


# 🔁 ORTAK NOT:
# - __setattr__ bir davranışsal (behavioral) özel metottur
# - Bu yüzden Python onu __getattribute__ gibi attribute lookup zinciriyle değil,
#   doğrudan type(obj) üzerinden çözümleyerek çağırır
# ========================================
# ✅ SONUÇ

# ✔️ __setattr__ çağrısı → doğrudan davranış olarak sınıfa gider (type(obj))
# ✔️ descriptor varsa ve __set__ içeriyorsa → doğrudan descriptor.__set__(...) çağrılır
# ✔️ __getattribute__ devreye girmez (çünkü bu bir erişim değil, atamadır)
# ✔️ Python doğal olarak __dict__ üzerinden descriptor protokolünü uygulamaz – ama biz uygulayabiliriz.

# örnek ;

class Öğrenci:
    def __init__(self,isim):
        self.__class__.__setattr__(self,"isim",isim) # -> self.isim = isim işleminin aynısı

ogrenci = Öğrenci("demir")
print(ogrenci.isim) # demir

# __setattr__() metodu, yeni bir python nesnesi oluşturur bu durumda artık eski nesnenin referansı kaldırılır(GC temizler)
# ve yeni bir nesne oluşturulur;

class Terminator:

    specs = ["T800"]

t800 = Terminator()
print(id(t800.specs)) # 137214660482688

Terminator.__class__.__setattr__(Terminator,"specs",["T800"])

print(id(t800.specs)) # 137214660482688


ogrenci.__class__.__setattr__(ogrenci,"durum",True) # bu işlem -> ogrenci.__setattr__... işlemin tam halidir
print(ogrenci.__dict__) # {'isim': 'demir', 'durum': True}




# Attribute Türleri


# Class Attribute

# class attribute,bir sınıfın gövdesinde tanımlanan ve sınıfın örnekleri(instance) tarafından paylaşılan bir özelliktir
# bu tür attribute'lar,sınıfın kendisine aittirler ve sınıfta bulunan __dict__ mapping proxy sözlüğünde tutulurlar
# bu attribute'lar sınıfın örnekleri tarafından okunabilirler( ama bu attribute'lar,sınıfa attir örneğe değil) ve manipüle edilebilirler bu durumda shadow(gölgelendirme) olur


# Özellikleri

# 1) Sınıf tanımı yapılırken belleğe alınırlar yani bellekte tutulmaları için sınıfın çağrılamsı,bir örnek oluşturulmasına gerek kalmaz

# 2) sınıfta bulunan __dict__ mapping proxy nesnesi içinde tutulurlar

# 3) örnek tarafından okunabilir ve değiştirilebilir

# Değiştirme işlemi nasıl olur: bu attribute'lar örneğe ait değiller öncelikle bu nedenle örnekte bulunan __dict__ içinde yer almazlar
# eğer bir örnek üzerinden sınıfta bulunan attribute değiştirilirse bu değiştirilen özellik artık nesnenin,__dict__ içine eklenmiş olur
# sadece o örneğe ait bir attribute oluşmuş olur ama sınıfta bulunan orjinal attribute,bundan etkilenmez
# Attribute erişiminde __getattribute__() metodu,özelliği nesne içinde aramaya başlayacağı için artık sınıftaki özelliğe shadow nedeniyle erişilemez çünkü;
# aynı özellik,örnekte bulunur

# Örnek...

class A:
    isim ="demir" # -> Class Attribute
    yas = 20 # -> Class Attribute
    def run(self): # -> Class Attribute
        print(self.isim,self.yas)

a = A()
b = A()

print(a.isim) # demir
# örnekler,sınıf attribute'larına erişebilirler ama örneğin kendisinde herangi bir Attribute tanımlı değildir
print(a.__class__.__dict__['__dict__'].__get__(a,A)) # {}

a.isim = "aslı"
# burda aslında şu işlemi yaptık;
a.__setattr__("isim","aslı")
# ve bu işlemde bir attribute atama işlemi olur -> a.__dict__["isim"] ="aslı"

#print(a.__dict__) # {'isim': 'aslı'}

# nesne düzeyinde en temel işlem; -> objenin sahip olduğu __dict__,normal python sözlüğü olduğu için doğrudan manipüle edebiliriz
a.__dict__['Yaş'] = 55
print(a.Yaş) # 55

# Tüm bu işlemlerden sonra sınıfı kontrol edelim

print(A.__class__.__dict__['__dict__'].__get__(A,type)['isim']) # demir -> A.__getattribute__('isim') metodunun yaptığı işlem
# Gördüğün üzere orjinal sınıfta bulunan attribute,aynı değişmedi

print(b.isim) # demir
# bu attribute'lar sınıfa aittir şuan isim verisinin tuttuğu değer,sınıfta tanımlı olan "demir" değeridir


# Instance Attribute

# Instance Attribute,genellikle __init__(...) gibi örnek başlatıcı metodlar içinde self üzerinden tanımlanan ve yalnızca o nesneye ait olan bir özelliktir
# İnstance Attribute'da,her nesne kendisine özgü özelliğe sahiptir bu özellik,diğer nenseleri veya kendi sınıfını ilgilendirmez

# __init__ ile tanımlanan attribute'lar, doğrudan örneğe ait olurlar ve örnekte bulunan __dict__ sözlüğüne yerleşirler dolasıyla Attribute erişiminde shadow olmaz


# 🔸 Class Attribute vs Instance Attribute

# ➤ Class Attribute:
# - Sınıf gövdesinde tanımlanır (class body içinde)
# - Sınıfa aittir, tüm örnekler tarafından paylaşılır
# - Sınıf oluşturulduğunda belleğe alınır
# - Sınıfın __dict__ sözlüğünde saklanır
# - Örnek üzerinden erişilebilir, ama değiştirilirse örneğe özel olur (shadowing)
# - Ortak sabit veriler için uygundur

# ➤ Instance Attribute:
# - Genellikle __init__ içinde self üzerinden tanımlanır
# - Her bir örneğe (instance) özeldir
# - Her nesne oluşturulduğunda yeniden oluşturulur
# - Nesnenin __dict__ sözlüğünde saklanır
# - Değeri sadece o nesneyi etkiler
# - Örnek başına özelleştirilmiş veri tutmak için kullanılır


# Örnek...

class Araba:
    tekerlek:int= 4 # Class Attribute

    def __init__(self,marka):
        self.__setattr__("marka",marka) # Instance Attribute

a1 = Araba("BMW")
a2 = Araba("Mercedes")

print(a1.__class__.__dict__['__dict__'].__get__(a1,Araba))  # {'marka': 'BMW'}
# Gördüğün gibi örnekte "marka" adında bir attribute tanımlanmıştır bu __init__() metodu sayesinde oldu ama farkettiysen;
# örnekte,tekerlek adında bir attribute yok çünkü bu Sınıfa ait örneğe değil

print(a1.tekerlek) # 4
# örnekler,CLass Attribute'lara erişebilirler

a1.__setattr__("tekerlek",5)
# artık a1 nesnesinde __dict__'e yeni bir attribute eklendi

print(a1.__class__.__dict__['__dict__'].__get__(a1,Araba)) # {'marka': 'BMW', 'tekerlek': 5}

print(a2.__class__.__dict__['__dict__'].__get__(a2,Araba))#  {'marka': 'Mercedes'}

Araba.__class__.__setattr__(Araba,"tekerlek",6) # Araba.tekerlek = 6
# sınıf nesnesi olan Arabaya,"tekerlek" adında bir attribute'u tanımlar ve 6 değerini atar


# __setattr__ OVERRİDE ETME

# örnek 1;

class A:

    def __setattr__(self,name,value):
        print(f"Yapılan İşlem: setattr,attribute adı: {name} değeri: {value}")
        object.__setattr__(self,name,value) # Loop'a girmemek için object sınıfındaki __setattr__() metodunu çağırdık

a = A()
a.isim = "demir" # Yapılan İşlem: setattr,attribute adı: isim değeri: demir

# örnek 2;

class Terminator:
    models = ["t800","t1000","t600","t850"]

    def __setattr__(self,name,value):
        if name == "model": # bu aslında t.model= "t800"'deki "model" olur çünkü: t.__setattr__("model","t800")
            # eğer örneğe model adına bir attribute ekleniyorsa kodlar çalışır bu durumda nesneye,model harici bir attribute eklenemez
            if value in self.models:
                object.__setattr__(self,name,value)
            else:
                print(f"Yeni model eklendi: {value}")
                self.models.append(value)
                object.__setattr__(self,name,value) # burda amacımız olmayan bir modeli listeye ekledikten sonra artık bu yeni modeli,örneğe atamak idi
                # aksi halde model listeye atansa bile örnekte "model" adına bir attribute olmayacaktı onun için: tekrar aynı işlemi yapmamız gerekirdi

        else: # Eğer kullanıcı,"model" yerine başka bir attribute eklemeye çalışırsa bu blok çalışır
            print(f"geçersiz model adı: {name}")

t = Terminator()
# → type.__call__(Terminator, ...)              # sınıfın __call__'ı
# → type.__dict__['__call__'].__get__(...)      # descriptor çözümleme
# → bound_method.__call__(*args, **kwargs)      # normal callable objeye dönüş
# → Terminator.__new__(...)                     # yeni örnek oluşturulur
# → Terminator.__init__(...)                    # örnek başlatılır

t1 = Terminator()

t.model = "t800"
print(t.model) # t800

# Olmayan bir model eklemesi yapalım;

t1.model = "t3000" # Yeni model eklendi: t3000
print(t1.model) # t3000

t1.guns = "lazer" # geçersiz model adı: guns


# örnek 3;
class Terminator:
    models = ["t800","t1000","t600","t850"]

    def __setattr__(self,name,value):
            if value in self.models:
                object.__setattr__(self,name,value)
            else:
                print(f"Yeni model eklendi: {name} değeri: {value}")
                self.models.append(value)
                object.__setattr__(self,name,value) # burda amacımız olmayan bir modeli listeye ekledikten sonra artık bu yeni modeli,örneğe atamak idi
                # aksi halde model listeye atansa bile örnekte "model" adına bir attribute olmayacaktı onun için: tekrar aynı işlemi yapmamız gerekirdi

    def __getattr__(self,name): #  burda amaç attribute erişiminde, olmayan bir özelliği eklemek ve varsayılan değer atamak
        # bunu __setattr__ yardımıyla yapıyoruz
        print(f"{name} adlı özellik bulunamadı ama eklendi")
        self.__setattr__(name,None)

t1 = Terminator()

t1.gun = "lazer" # Yeni model eklendi: gun değeri: lazer

print(t1.__dict__) # {'gun': 'lazer'}

print(Terminator.__dict__["models"]) # ['t800', 't1000', 't600', 't850', 'lazer']

t1.system
# system adlı özellik bulunamadı ama eklendi
# Yeni model eklendi: system değeri: None



# örnek 4;

class Terminator:
    models = ["t800","t1000","t600","t850"]

    def __setattr__(self,name,value):
            if value in self.models:
                object.__setattr__(self,name,value)
            else:
                print(f"Yeni model eklendi: {name} değeri: {value}")
                self.models.append(value)
                object.__setattr__(self,name,value) # burda amacımız olmayan bir modeli listeye ekledikten sonra artık bu yeni modeli,örneğe atamak idi
                # aksi halde model listeye atansa bile örnekte "model" adına bir attribute olmayacaktı onun için: tekrar aynı işlemi yapmamız gerekirdi

    def __getattr__(self,name): #  burda amaç attribute erişiminde, olmayan bir özelliği eklemek ve varsayılan değer atamak
        # bunu __setattr__ yardımıyla yapıyoruz
        print(f"{name} adlı özellik bulunamadı ama eklendi")
        self.__setattr__(name,None)

    def __dir__(self) -> list:
        return self.models
    #  # __dir__ metodu, dir(obj) fonksiyonu çağrıldığında devreye girer.
        # Normalde Python, obj.__dict__, class attribute'ları ve MRO zincirine göre bir liste üretir.
        # Ancak bu metod override edilirse, dir() çıktısını tamamen sen kontrol edebilirsin.

        # Bu örnekte, dir(t) çağrıldığında:
        # sadece models listesindeki öğeler döndürülür (örneğin: ['t800', 't1000', ...])
        # Yani standart __init__, __class__, model gibi attribute'lar bu listede görünmez.

        # Bu sayede, kullanıcıya veya geliştiriciye daha özel, sınırlı veya anlamlı bir dir() çıktısı sunulur.

t1 = Terminator()

print(Terminator.__dict__['__dir__'](Terminator)) # ['t800', 't1000', 't600', 't850']

print(t1.__class__.__dict__['__dir__'](t1)) # ['t800', 't1000', 't600', 't850']
# burda t1.__class.. kullandık çünkü t1 örneğinde __dir__() metodu tanımlı değil ve biz manuel çağırdığımızda python,
# otomatik olarak metod çözümleme yapmaz(__getattribute__ kullansaydık olurdu ama)



# örnek 5;

class Terminator:
    models = ["t800","t1000","t600","t850"]

    def __setattr__(self,name,value):
            if value in self.models:
                object.__setattr__(self,name,value) # ->
            else:
                print(f"Yeni model eklendi: {name} değeri: {value}")
                self.models.append(value)
                object.__setattr__(self,name,value) # burda amacımız olmayan bir modeli listeye ekledikten sonra artık bu yeni modeli,örneğe atamak idi
                # aksi halde model listeye atansa bile örnekte "model" adına bir attribute olmayacaktı onun için: tekrar aynı işlemi yapmamız gerekirdi

    def __getattr__(self,name): #  burda amaç attribute erişiminde, olmayan bir özelliği eklemek ve varsayılan değer atamak
        # bunu __setattr__ yardımıyla yapıyoruz
        print(f"{name} adlı özellik bulunamadı ama eklendi")
        self.__setattr__(name,None)

    def __dir__(self) -> list:
        return self.models
    #  # __dir__ metodu, dir(obj) fonksiyonu çağrıldığında devreye girer.
        # Normalde Python, obj.__dict__, class attribute'ları ve MRO zincirine göre bir liste üretir.
        # Ancak bu metod override edilirse, dir() çıktısını tamamen sen kontrol edebilirsin.

        # Bu örnekte, dir(t) çağrıldığında:
        # sadece models listesindeki öğeler döndürülür (örneğin: ['t800', 't1000', ...])
        # Yani standart __init__, __class__, model gibi attribute'lar bu listede görünmez.

        # Bu sayede, kullanıcıya veya geliştiriciye daha özel, sınırlı veya anlamlı bir dir() çıktısı sunulur.

    def __getattribute__(self, item):
        print(f"özellik erişimi: {item}")
        return Terminator.__bases__[0].__getattribute__(self, item)

t1 = Terminator()

t1.model = "t800" # özellik erişimi: models
# Çünkü __setattr__ metodunda,biz if value in self.models -> burda attribute Erişimi var burda value = models oluyor bu nedenle



# __delattr__() Metodu

# __delattr__, bir nesneden (instance) bir attribute (özellik) silinmek istendiğinde
# Python tarafından otomatik olarak çağrılan dunder (double underscore) bir metottur.
# Bu metod, attribute silme davranışını kontrol etmek ya da özelleştirmek için override edilir.
# Örneğin: bir attribute silinirken loglama yapmak, sınır koymak, değerleri arşivlemek vs.

# Söz dizimi:
# __delattr__(self, name:str) self:hangi örnek için çağrılcağı, name: silinmek istenilen attribute adı ve string türde olmalı

    # 📌 Bu da bir STATEMENT'tır → Python yine bir değer beklemez.
    # Bu nedenle return etmek gerekmez, hatta anlam taşımaz.


# 🔥 __delattr__() METODU – ÇAĞRI ZİNCİRİ

# ========================================
# 🧍🏻 1. INSTANCE (Nesne) DÜZEYİNDE
# ========================================

# Örnek: del obj.x

# → Python bunu aşağıdaki adımlarla gerçekleştirir:

# 1) obj.__delattr__('x')  çağrılır (çünkü del obj.x bir davranıştır)
# 2) Bu, örneğin ait olduğu sınıf üzerinden çözülür:
#      → type(obj).__delattr__(obj, 'x')
# 3) Eğer sınıfta override edilmiş __delattr__ metodu yoksa:
#      → object.__delattr__(obj, 'x') çalıştırılır (default silici)

# 4) Eğer obj.x bir descriptor ise ve descriptor.__delete__ varsa:
#      → descriptor.__delete__(obj) doğrudan çağrılır
#      → __delattr__ hiç devreye girmez

# ========================================
# 🏗️ 2. CLASS (Sınıf) DÜZEYİNDE
# ========================================

# Örnek: del A.attr

# → Python bu işlemi şu adımlarla yapar:

# 1) A.__delattr__('attr') çağrılır
# 2) A, bir sınıf olduğundan aslında:
#      → type(A).__delattr__(A, 'attr') çalışır, type sınıfında __delattr__ bulunur çağrılırır
# 3) Eğer attr bir descriptor ise ve __delete__ metodu varsa:
#      → descriptor.__delete__(A) doğrudan çalıştırılır

# ========================================
# 📝 NOT – EL İLE YAPILAN DESCRIPTOR ÇÖZÜMLEMESİ
# ========================================

# Eğer biz bu zinciri elle kontrol etmek istersek:

# 1) __dict__ üzerinden descriptor’a erişiriz:
#    descriptor = type(obj).__dict__['__delattr__']

# 2) Ardından descriptor protokolünü elle uygularız:
#    bound_method = descriptor.__get__(obj, type(obj))

# 3) Ve çağırırız:
#    bound_method('x')

# Bu yöntem:
#    - Python’un doğal olarak yaptığı zincir DEĞİLDİR.
#    - Sadece descriptor’ları doğrudan elle çözümlemek için kullanılır.
#    - Eğitimsel veya ileri seviye kontrol amaçlıdır.

# ========================================
# ✅ SONUÇ

# ✔️ Python davranışsal işlemleri (__setattr__, __delattr__) doğrudan sınıf üzerinden çözümler.
# ✔️ descriptor içeriyorsa __get__ değil, __delete__ uygulanır.
# ✔️ __getattribute__ çözümlemede kullanılmaz (çünkü bu erişim değil, davranıştır).
# ✔️ Manuel __dict__ çözümlemesi sadece özel bir tekniktir – Python bunu kendi yapmaz.

# -----------------------------------------------
# UYGULAMA SENARYOSU
# -----------------------------------------------
# __delattr__ override edilerek:
# - Bazı attribute'ların silinmesi engellenebilir
# - Silme işlemi sırasında özel bir işlem yapılabilir
# - Tüm silinen özellikler arşivlenebilir
# - Runtime kontrol mekanizmaları uygulanabilir,

class C:
    
    def __init__(self,isim):
       self.isim = isim

    ozellik = "hayatta"

c = type.__dict__["__call__"].__get__(C,type).__call__("demir") # ->  c = C.__new__(C) ->   C.__init__(c)

c.__init__("demair") # -> type(c).__getatribute__(c,"__init__") -> C.__init__(c,"demair")

print(c.__dict__)

type(C).__delattr__(C,"ozellik")

print(vars(C))



