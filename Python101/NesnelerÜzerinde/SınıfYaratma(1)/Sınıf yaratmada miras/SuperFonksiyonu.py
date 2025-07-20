# ======================================================
# 🚀 super() FONKSİYONU – DETAYLI TANIM
# ======================================================

# 🔹 `super()` fonksiyonu, Python'da miras (inheritance) yapılarında
# alt sınıfın, üst sınıftaki attribute ve metodlara güvenli şekilde erişmesini sağlar.

# 🔹 En yaygın kullanımı: override edilen bir metod içinde,
# üst sınıfın aynı isimli metodunu çağırmak için kullanılır.

# 🔹 `super()` fonksiyonu **MRO (method resolution order)** zincirine göre çözümleme yapar.
# Bu sayede Python, doğru sırayla sınıfları tarayarak en uygun metod/attribute'u bulur.

# ======================================================
# 🎯 AMACI
# ======================================================

# ✅ Kod tekrarını önlemek
# ✅ Alt sınıfın üst sınıf fonksiyonlarını genişletmesini sağlamak
# ✅ Çoklu miras durumlarında doğru metod zincirini korumak, zinciri koparmadan davranışı sürdürmek

# ======================================================
# 🧱 SÖZDİZİMİ
# ======================================================

# 1. Temel kullanım:
#     super().method(args)      → derleyici, otomatik olarak geçerli sınıfı ve örneği belirler bu python3'de geldi :)

# 2. Gelişmiş (eski stil) kullanım:
#     super(AltSınıf, self).method(args)
#     → AltSınıf: şuan bulunduğumuz sınıf,mro zincirinde aramaya hangi sınıftan başlayacağım
#     → self: örnek (instance), hangi örnek üzerinden çözümleme yapılcak

# ======================================================
# 🧪 ÖRNEK:
# ======================================================

class Canli:
    def __init__(self, ad):
        self.ad = ad
        print(f"Canli: {ad}")

class Hayvan(Canli):
    def __init__(self, ad, tur):
        super().__init__(ad)  # → Üst sınıfın __init__'i çağrıldı
        self.tur = tur
        print(f"Hayvan: {tur}")

h = Hayvan("Leo", "Kedi")

# ======================================================
# ⚙️ super() NASIL ÇALIŞIR?
# ======================================================

# Alt sınıfta super().__init__() çağrıldığında:
# 1. Python, geçerli sınıfı ve örneği belirler
# 2. MRO zincirine göre `Canli` sınıfının __init__() metodunu bulur
# 3. Bulunan metod çağrılır

# Yani şu zincir oluşur:
# type(Hayvan).__mro__ → (Hayvan, Canli, object)

# super().__init__ → MRO zincirinde Hayvan'dan sonra gelen Canli.__init__

# ======================================================
# 💡 KULLANIM ALANLARI
# ======================================================

# 🔸 1. __init__ metodunu genişletmek
# 🔸 2. __setattr__, __str__, __call__ gibi dunder metodları override edip eski davranışı korumak
# 🔸 3. Çoklu miras yapılarında MRO uyumluluğu sağlamak
# 🔸 4. Kapsamlı davranış kontrolü yapmak (örnek: GUI kütüphaneleri, ABC metaclass, vb.)

# ======================================================
# 📌 super() ve MRO
# ======================================================

# Python çoklu miraslarda C3 Linearization adı verilen bir algoritma kullanır.
# Bu algoritma sınıfların __mro__ sırasını belirler.
# super(), bu sıraya göre bir üst sınıfa gider ve metod çözümlemesi yapar. bu sayede davranış zinciri koparmadan, davranış sürdülülebilir

# ======================================================
# 🛑 super() KULLANIRKEN DİKKAT:
# ======================================================

# 🔸 super() sadece yeni-style sınıflarda çalışır (Python 3'te tüm sınıflar new-style’dır)
# 🔸 super(), method scope içinde çağrılması gerekir çünkü super():
#     hangi sınıftayım = CurrentCLass;
#     hangi nesneyle çağrıldım = self
#   super(),class body'de çağrıldığında self bilgisi olmaz ama python bu bilgiye ihtiyaç duyar: super(currentclass,self) class gövdesinde, aktif olarak hangi sınıfın içinde olduğunu çözemez
# 🔸 super(), mevcut örneği(self) otomatik olarak bağlar bu nedenle super(). -> attribute erişiminden sonra erişilen method'a, self argümanı veremezsin çünkü zaten bağlıdır 

# ======================================================
# 🧪 ALTERNATİF
# ======================================================

# super() kullanmazsan şu şekilde çağırmak gerekirdi:
#     Canli.__init__(self, ad)  → Bu, sabit referans olduğu için çoklu miraslarda güvenli değildir
#     Bu nedenle → `super()` tercih edilir.

# ======================================================

# ============================================
# 🔁 super() vs object.method(self, ...) FARKI
# ============================================

# 🎯 Amaç: Alt sınıftan üst sınıfın metoduna erişmek

# ÖRNEK:
class Base:
    def hello(self):
        print("Base'den merhaba")

class Child(Base):
    def hello(self):
        print("Child")
        super().hello()        # ✅ 1. YÖNTEM: super()
        # Base.hello(self)    # ✅ 2. YÖNTEM: doğrudan sınıf adı

c = Child()
c.hello()

# ============================================
# 🧠 super() NASIL ÇALIŞIR?
# ============================================

# 1. Python şu çözümlemeyi yapar:
#    → type(c).__mro__ → (Child, Base, object)
#    → Child sınıfındayız, MRO'da bizden sonraki ilk sınıf: Base

# 2. Python, `Base.hello()` metodunu bulur ve çağırır:
#    super().hello() → Bound method oluşturulur → Base.hello(self)

# ✅ Avantaj: MRO zincirini korur → Çoklu mirasta çok önemlidir.

# ============================================
# 🆚 object.method(self, ...) NASIL FARKLI?
# ============================================

# → `Base.hello(self)` ifadesi **sabit bir çağrıdır**.
# → Bu, MRO zincirini dikkate almaz → doğrudan Base sınıfı çağrılır.

# Bu yüzden çoklu mirasta sorun çıkabilir.

# ============================================
# 💥 ÖNEMLİ FARK: ZİNCİR DAVRANIŞI
# ============================================

# Eğer class A, class B ve class C şeklinde çoklu miras varsa:

# class A:
#     def f(self): print("A")

# class B(A):
#     def f(self):
#         print("B")
#         super().f()

# class C(A):
#     def f(self):
#         print("C")
#         super().f()

# class D(B, C):  # Çoklu miras!
#     def f(self):
#         print("D")
#         super().f()

# D().f()

# ÇIKTI:
# D
# B
# C
# A

# → Bu zinciri `super()` korur.
# → Ama her sınıf kendi üst sınıfını doğrudan çağırırsa bu zincir bozulur:
#    B.f() → A.f()
#    C.f() → A.f()
#    → C sınıfı atlanır!

# ============================================
# ✳️ super() ZİNCİRİ
# ============================================

# D().f() çağrısı → MRO zinciri çalışır:
# D → B → C → A → object

# Her `super()` çağrısı bir sonraki sınıfa geçer.
# Python'da bu zincir, C3 Linearization algoritmasıyla çözülür.

# ============================================
# 🔚 ÖZETLE:
# ============================================

# ✅ `super()`:
#     - Dinamik çözümleme yapar
#     - MRO sırasına göre çalışır
#     - Çoklu miraslarda güvenlidir
#     - Esnek ve Pythonic'tir

# ❌ `Base.method(self, ...)`:
#     - Sabit bir çağrıdır
#     - MRO zincirini atlar
#     - Çoklu mirasta zinciri koparır
#     - Yalnızca basit miras için önerilir


class Canlı:

    def __init__(self):
        self.attribute = ["tepki verme","boşaltım"]

class Omurgalı:

    def __init__(self):
        self.attribute = ["omurga"]


class Memeli(Omurgalı):

    def __init__(self):
        super(Memeli,self).__init__() # Omurgalı.__init__(self) dememiz gerekirdi bu sabit bir çağrı olur ve davranış zincirini koparıl,sürdüremezdik
        self.attribute.extend(["süt bezi","sıcak kanlı","vücut kılları"])

m = Memeli()

print(m.__dict__) #{'attribute': ['omurga', 'süt bezi', 'sıcak kanlı', 'vücut kılları']}


class Insan(Memeli,Canli): # Kalıtım burda başlar insan sınıfı hem memeli sınıfından hemde canlı sınıfından miras alır

        def __init__(self):
            super().__init__() #burda super fonksiyonu kritiktir çünkü bu sınıf birden fazla sınıfan miras alıyor yani çoklu kalıtım sözkonusu burda davrnışsal zincir kopmadan devam etmeli
            # eğer sabit kodlama -> Memeli.__init__(self) yazsaydık Canlı sınıfı atlanırdı ve o sınıfın attribute'unu alamazdık 


insancık = Insan()

print(
    insancık.__dict__ # {'attribute': ['omurga', 'süt bezi', 'sıcak kanlı', 'vücut kılları']}
)

print(insancık.__class__.__base__) #<class '__main__.Memeli'>
#doğrudan Memeli sınıfından miras alıyor birde mro 'ya bakalım sonra açıklamasını yapacağız :)

print(insancık.__class__.__bases__) # (<class '__main__.Memeli'>, <class '__main__.Canli'>) 



class Insan(Memeli,Canli): # Kalıtım burda başlar, C3 Linearization algoritması için sınıfların sırası çok kritik eğer Canlı sınıfı başta olsa idi Mro'da başta olurdu 

        def __init__(self):
            super().__init__() #burda super fonksiyonu kritiktir çünkü bu sınıf birden fazla sınıfan miras alıyor yani çoklu kalıtım sözkonusu burda davrnışsal zincir kopmadan devam etmeli
            # eğer sabit kodlama -> Memeli.__init__(self) yazsaydık Canlı sınıfı atlanırdı ve o sınıfın attribute'unu alamazdık 
            self.attribute.extend(("akıl","duygu","benzetme"))

insancık = Insan()

print(
    insancık.__dict__ #{'attribute': ['omurga', 'süt bezi', 'sıcak kanlı', 'vücut kılları', 'akıl', 'duygu', 'benzetme']}
)

print(insancık.__class__.__mro__) #(<class '__main__.Insan'>, <class '__main__.Memeli'>, <class '__main__.Omurgalı'>, <class '__main__.Canli'>, <class 'object'>)
# burda super() fonksiyonun seçeceği sınıf sırasını görüyorsun __mro__'da sınıfların sırası, C3 Linearization algoritmasına göre belirlenir 