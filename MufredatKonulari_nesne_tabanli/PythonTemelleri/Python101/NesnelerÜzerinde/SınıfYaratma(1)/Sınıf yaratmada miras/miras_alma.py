# ===============================================
# 🧬 MİRAS (INHERITANCE) - DETAYLI TANIM
# ===============================================

# Python'da **miras**, bir sınıfın başka bir sınıfın özelliklerini (attribute) ve davranışlarını (method) devralmasını sağlar.

# 🔗 Temel Amaç:
# Kod tekrarını azaltmak, soyutlama yapmak ve yapıların yeniden kullanılabilirliğini artırmaktır.

# 🔄 Kalıtım sayesinde:
# - Alt sınıf (child/subclass), üst sınıfın (base/superclass) sahip olduğu her şeye otomatik olarak sahip olur.
# - Ek olarak kendi özelliklerini ve davranışlarını da tanımlayabilir.
# - Gerekirse üst sınıftaki davranışları değiştirebilir (override).

# ===============================================
# 🧱 SÖZDİZİMİ
# ===============================================
#
# class ÜstSınıf:
#     ...

# class AltSınıf(ÜstSınıf):   # <-- Kalıtım burada sağlanır
#     ...

# ===============================================
# 🧩 TEKNİK OLARAK NASIL ÇALIŞIR?
# ===============================================
# Python'da her sınıfın `__bases__` adında bir niteliği vardır.
# Bu tuple, sınıfın hangi sınıflardan doğrudan miras aldığını gösterir.

# ================================
# 1) c = Child() satırı görüldü
#    → Yani: Child.__call__(*args, **kwargs)
#    → Ama Child bir sınıftır, sınıflar da type sınıfının örneğidir

# 2) Python, type sınıfının __call__ metodunu çağırır:
#    → type.__call__(Child, *args, **kwargs)

# 3) type.__call__'ın iç mantığı şöyledir:
#    a) obj = cls.__new__(cls, *args, **kwargs)  -> MRO çözümlemesi başlar
#    b) cls.__init__(obj, *args, **kwargs)

# ======================================
# 4) cls = Child olduğundan şu zincir oluşur:

# → Child.__new__()  çağrılır
#    (çünkü sınıfın kendisinde varsa öncelik ondadır)
#    → super().__new__() → bu da Base sınıfında arar → oradan object'e gider

# → sonra Child.__init__() çağrılır
#    → burada da super().__init__() diyerek Base.__init__ çağrılabilir (isteğe bağlı)

# ======================================
# 📌 Dikkat: __new__ metodu nesneyi oluşturur
#    → Bu nedenle orada return etmek zorundayız (yeni nesne)

# 📌 __init__ metodu nesneyi başlatır
#    → Return etmez, sadece içini doldurur

# ======================================
# 👣 MRO Zinciri:
# → type(c).__mro__ = (Child, Base, object)

# Eğer Child sınıfında __new__ tanımlı olmasaydı:
# → Base.__new__ → object.__new__ zinciriyle devam ederdi

# ===============================================
# 🎯 MİRASIN FAYDALARI
# ===============================================

# ✅ KOD TEKRARINI AZALTIR:
# Ortak özellikleri ve metodları bir üst sınıfta toplarsın → tekrar tekrar yazmak zorunda kalmazsın.

# ✅ KODU ORGANİZE EDER:
# Karmaşık sistemleri, küçük ve anlamlı yapılarla yönetilebilir hale getirir.

# ✅ DAVRANIŞI GENİŞLETEBİLİRİZ:
# Alt sınıf, üst sınıftan gelen metodları geçersiz kılarak (`override`) veya genişleterek yeni davranışlar ekleyebilir.

# ===============================================
# 🎓 ÖNEMLİ TERİMLER
# ===============================================

# - base class (üst sınıf, super class): miras veren sınıf
# - derived class (alt sınıf, sub class): miras alan sınıf
# - override: alt sınıfta, üst sınıftaki aynı isimli metodun yeniden tanımlanması
# - super(): alt sınıfın üst sınıf metodlarına erişmesini sağlar

# ===============================================
# 🔬 BİLİNMESİ GEREKENLER
# ===============================================

# 🔸 Python'da tüm sınıflar varsayılan olarak `object` sınıfından miras alır.
#     → Bu nedenle tüm sınıflar aslında `object` sınıfının alt sınıfıdır.
#
# 🔸 `__mro__` zinciri sayesinde bir attribute/metod aranırken:
#     - İlk olarak sınıfın kendisine bakılır
#     - Ardından sırasıyla base class'lara çıkılır

# 🔸 Çoklu miras mümkündür: class A(B, C): ...
#     → Python C3 linearization algoritması ile çözüm sırasını belirler.

# 🔸 Miras, sadece attribute/metod devralmaz:
#     Aynı zamanda `__init__`, `__str__`, `__call__` gibi tüm özel metodlar da devralınır.

# ===============================================


class Canlı:
    
    def __init__(self):
        self.kalp = "kalp"
        self.beyin = "beyin"


class Insan(Canlı): #-> kalıtım burda başlar

    pass
# Insan sınıfında, __init__ tanımlı olmasa bile miras aldığı sınıfta tanımlı olduğu için sınıf çağrsında o sınıftan alcak

insan = Insan()
canli = Canlı()

print(
    insan.__dict__ # {'kalp': 'kalp', 'beyin': 'beyin'}
    # __dict__,nesneye özgü olan attribute'ları gösterir
)


print(
    insan.beyin # beyin
)

###################### cozumleme:

print(
    type(Canlı).__dict__['__call__'].__get__(Canlı,type).__call__()
)

# __call__ çözümlemesi;

print(
    type(Canlı).__getattribute__(Canlı,"__new__").__call__(Canlı)
)

# __init__ çözümlemesi:


sınıfım = Insan.__new__(Insan)


print(sınıfım.__dict__) #{} -> boş dict döner çünkü, __new__ metodunu manuel çağırdığımız için herangi bir nesneye veri eklenmedi

try:
    sınıfım.__class__.__dict__['__init__']

except KeyError:# Insan sınıfında __init__ metodu yoktur

    print("Insan sınıfında __init__ metodu yoktur")

#Mro kullanılır:

sınıfım.__class__.__mro__[1].__dict__['__init__'].__call__(sınıfım) # burda Canlı sınıfında bulunan __init__ metodu çağrılırır 

print(sınıfım.__dict__) # {'kalp': 'kalp', 'beyin': 'beyin'}




# override etme;

class Canlı:
    
    def __init__(self):
        self.kalp = "kalp"
        self.beyin = "beyin"


class Insan(Canlı): #-> kalıtım burda başlar

    def __init__(self):
        Canlı.__init__(self) # __init__, bir class atrribute olduğundan dolayı çağırabiliriz
        self.bilinc = "bilinc"
        self.dna = "insan"


insan2 = Insan()

print(
    insan2.__dict__ # {'kalp': 'kalp', 'beyin': 'beyin', 'bilinc': 'bilinc', 'dna': 'insan'}
)

# bases ile kontrol edelim;

print(
    insan2.__class__.__bases__ # (<class '__main__.Canlı'>,) -> doğrudan Canlı sınıfından miras alıyor
)

print(
    insan2.__class__.__base__ # <class '__main__.Canlı'> 
)
