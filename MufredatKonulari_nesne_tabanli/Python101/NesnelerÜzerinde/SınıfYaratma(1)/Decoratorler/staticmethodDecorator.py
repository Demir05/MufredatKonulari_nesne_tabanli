# -----------------------------------------------------------------------
# @staticmethod Decorator'ü
# -----------------------------------------------------------------------

# @staticmethod, bir sınıf içinde tanımlanan ancak sınıfın örneğiyle (self)
# ya da sınıfın kendisiyle (cls) ilgisi olmayan metodları tanımlamak için kullanılır.
# Bu metodlar, normal bir fonksiyon gibi davranır ama mantıksal olarak sınıf içinde yer alır.

# -----------------------------------------------------------------------
# Neden Var? Amacı Nedir?
# -----------------------------------------------------------------------

# 1. Bir fonksiyon, sınıfa bağlı olarak tanımlanmak isteniyor ama sınıfın
#    ne örneğiyle (self) ne de sınıfın kendisiyle (cls) ilgili değilse
#    bunu staticmethod yaparız.
#    Böylece: fonksiyon → sınıfın bir özelliği olur ama örneğe bağımlı olmaz.

# 2. Kodun organizasyonunu sağlar: Sınıfla ilgili olan ama doğrudan veriyle 
#    işlem yapmayan yardımcı fonksiyonları sınıf içinde tutarız.

# 3. Sadece işlevsel (fonksiyonel) bir mantık sunar; sınıfın içeriğine erişmez.

# -----------------------------------------------------------------------
# Sözdizimi:

# class SınıfAdı:
#     @staticmethod
#     def fonksiyon_adı(...):
#         ...

# Çağrılma:
# SınıfAdı.fonksiyon_adı(...)
# veya
# örnek.fonksiyon_adı(...)

# -----------------------------------------------------------------------
# Örnek:

class Matematik:

    @staticmethod
    def kare_al(x):
        return x * x

# Static method hem sınıf üzerinden hem örnek üzerinden çağrılabilir:
print(Matematik.kare_al(4))  # → 16

m = Matematik()
print(m.kare_al(5))          # → 25

# Bu metotlar, sınıfın durumuna (self) ya da yapısına (cls) erişemez.

# -----------------------------------------------------------------------
# Önemli Notlar:

# - Static method'lar override edilebilir, miras alınabilir.
# - MRO zincirinde çözülür; örnekte __getattribute__ ile sınıfın __dict__’inde aranır.
# - Diğer decorator'lar gibi Descriptor protokolü uygulanmaz çünkü data descriptor değildir.
# - örnek veya class  üzerinden çağrılma staticmetod'lara özgü değildir ama self ve cls parametreleri verilmemesi, staticmethod'lara özgüdür

# @staticmethod:
#  - Ne self ne cls alır.
#  - Sınıf veya örnek üzerinden çağrılabilir.
#  - Sınıf içeriğine doğrudan erişmez, açıkça "Sınıf.özellik" yazmak gerekir.

# -----------------------------------------------------------------------
# Teknik olarak:

# Sınıf tanımlanırken:
# Matematik.__dict__['kare_al'] → staticmethod objesi
# Çağırıldığında:
# Matematik.__dict__['kare_al'].__get__(None, Matematik) → gerçek fonksiyon döner
# Artık bu fonksiyon çağrılabilir hale gelir: fonksiyon(4)

# -----------------------------------------------------------------------
# Ne Zaman Kullanılır?

# - Yardımcı fonksiyonlar tanımlarken
# - Sınıfa ait bir bağlamda gruplanmak istenen, ama sınıf verisini kullanmayan işlemlerde
# - Daha düzenli ve okunabilir kod yazmak için


# -----------------------------------------------
# STATICMETHOD VE DESCRIPTOR MANTIĞI
# -----------------------------------------------

# @staticmethod bir built-in DECORATOR'dur.
# Ama aslında bir DESCRIPTOR sınıfıdır.
# Descriptor nedir? __get__, __set__, __delete__ gibi metodları olan nesnelerdir.

# staticmethod davranış olarak:
# - self veya cls gibi bağlama ihtiyaç duymaz.
# - sınıftan veya instance'dan erişildiğinde aynı şekilde çalışır.
# - asıl fonksiyon nesnesine doğrudan erişim sağlar.

# Basit bir staticmethod descriptor sınıfı aşağıdaki gibidir:

class MyStaticMethod:
    def __init__(self, func):
        # Fonksiyonu alıp saklıyoruz (örneğin: def foo(): ...)
        self.__func__ = func

    def __get__(self, instance, owner=None):
        # __get__ metodu sınıf.attribute veya instance.attribute şeklinde erişildiğinde otomatik çalışır
        # Burada instance = obj (örnek), owner = class (sınıf) (kullanılmaz burada ! )
        # Biz sadece fonksiyonu döndürmek istiyoruz, bu yüzden fonksiyonun kendisini döneriz
        return self.__func__

# Bu sayede staticmethod gibi çalışır:

class Arac:
    # normalde @staticmethod kullanırdık, biz onun yerine descriptor sınıfımızı kullanıyoruz
    bilgi = MyStaticMethod(lambda: print("Merhaba!"))

# Artık hem sınıf hem de nesne üzerinden çağırabiliriz:
Arac.bilgi()  # Merhaba!
a = Arac()
a.bilgi()     # Merhaba!

# -----------------------------------------------
# ÖZET:
# staticmethod gibi decorator'lar aslında descriptor'dır.
# Descriptor protokolü (__get__) sayesinde özel davranış sergilerler.
# self veya cls gönderilmediği için bağımsız, bağsız işlevler için idealdir.
# -----------------------------------------------

class A:
    isimler = ("demir","asli")
    
    def __init__(self):
        self.isim =  "demir"
    
    @staticmethod    
    def merhaba():
            print(A.isimler)
            
    def merheba2(self):
        print(self.isimler)
        print(self.isim) 
        
    def merhaba3(*args):
        print(A.isimler)

a = A()

a.merhaba() # ('demir', 'asli')
a.__class__.__dict__['merhaba'].__get__(a,type(a)).__call__() # bu kod geçerli çünkü staticmethod descriptor'da __get__ metodunda instance parametresi bu a objesini alır ama kullanılmaz ! 
a.__class__.__dict__['merhaba'].__get__(None,type(a)).__call__() # burda __get__().__call__() yapamazdık __get__metodu, argüman ister bu nedenle instance parametresine, None verdik

A.merhaba() # ('demir', 'asli')
 
a.merheba2() # 
a.__class__.__dict__['merheba2'].__get__(a,type(A)).__call__()  
"""
('demir', 'asli')
demir
"""

A.merheba2(a)
"""
('demir', 'asli')
demir
"""

a.merhaba3() #('demir', 'asli')
A.merhaba3() #('demir', 'asli')