# collections.abc modülü:
# Python’da yerleşik olarak gelen ve birçok soyut temel sınıfı (ABC) barındıran bir modüldür.
# ABC → "Abstract Base Class" (Soyut Taban Sınıf) demektir.
# Bu soyut tabanlı temel sınıflar, Python'daki veri yapılarına (list, dict, set, etc.) benzer davranışlar tanımlamak için kullanılır.

# Amaç:
# Eğer kendi sınıfımızı built-in yapılara benzer şekilde kullanmak istiyorsak (örneğin list gibi davranan bir sınıf),
# collections.abc modülünden uygun soyut sınıfı miras alabiliriz.
# Bu sayede hem belli davranışları sağlamış oluruz hem de `isinstance(obj, Iterable)` gibi kontrollerde geçerli oluruz.

# Örnek: Iterable sınıfından miras alma

from collections.abc import Iterable, Iterator, Container

class BenimListem(Iterable):  # Iterable soyut sınıfından miras alıyoruz
    def __init__(self, veri):
        self.veri = veri

    def __iter__(self):
        return iter(self.veri)  # iterable davranışı tanımlanıyor

# Bu sınıf artık bir iterable’dır
liste = BenimListem([1, 2, 3])

# Artık `for` döngüsü içinde kullanılabilir:
for i in liste:
    print(i)

# isinstance() ile kontrol de sağlanabilir:
print(isinstance(liste, Iterable))  # True


# NEDEN SOYUT SINIFLAR?
# Bu soyut sınıflar, Python’un veri yapılarındaki temel davranışları belirlemek için kullanılır.
# Eğer __iter__, __getitem__, __len__ gibi metodları tanımlarsan;
# doğru soyut sınıftan türeyerek hem `isinstance` kontrollerinde başarılı olur hem de daha anlamlı bir yapı elde edersin.

# collections.abc modülünde bazı önemli soyut sınıflar:
# - Iterable → __iter__ gerektirir
# - Iterator → __iter__ + __next__ gerektirir
# - Container → __contains__ gerektirir
# - Sized → __len__ gerektirir
# - Sequence → __getitem__ + __len__ (ve diğerleri) gerektirir
# - Mapping → __getitem__, __iter__, __len__ (dict benzeri yapı)
# - MutableSequence, MutableMapping → mutable versiyonlar

# Bu soyut sınıflar bir interface gibi davranır: neyi yapman gerektiğini söyler, nasıl yapacağını değil.
# Ayrıca abc.ABC sınıfından türeyen sınıflar da tanımlayabiliriz (manuel olarak soyut sınıf oluşturmak için).

# ÖZETLE:
# collections.abc modülü sayesinde kendi sınıflarımıza Python’un veri yapılarına benzer davranışlar kazandırabiliriz.
# Ayrıca bu modül, daha okunabilir, kontrol edilebilir ve güvenli OOP (NYP) yapıları kurmamıza yardımcı olur.



# Bu sınıf, collections.abc.Iterator soyut sınıfından miras alıyor.
class Veri(Iterator):
    def __init__(self, veri):
        # Kendi iterable verimizi (örneğin liste, tuple) kaydediyoruz.
        # Dikkat: 'self.veri' gibi attribute'lar soyut sınıftan gelmez, biz tanımlarız.
        self.veri = iter(veri)

    def __next__(self):
        # __next__ metodu, Iterator soyut sınıfı tarafından zorunlu tutulur.
        # Çünkü @abstractmethod ile tanımlıdır.
        # Bu metodu tanımlamazsak, sınıf örneklenemez (TypeError).
        return next(self.veri)

# ✅ Şimdi neden bu sınıf hata vermez, özetleyelim:

# 1. Iterator sınıfı __next__ metodunu içeriyor GİBİ görünür,
#    ama aslında bu bir @abstractmethod'dur → sadece 'tanımlanması gerekir' demektir.
#    Gerçek bir davranış içermez, içi boştur.
#    Bu yüzden: biz bu metodu sınıfta tanımlamak ZORUNDAYIZ.

# 2. Buna karşılık __iter__ metodu, Iterator sınıfında GERÇEK olarak tanımlıdır:
#        def __iter__(self): return self
#    Bu sayede, biz tekrar tanımlamasak da nesnemiz 'iterable' kabul edilir.

# 3. Attribute konusu:
#    Soyut sınıflar metot davranışı tanımlar, attribute (örneğin self.data) sağlamaz.
#    Yani her türlü veri alanını (self.veri gibi) biz kendimiz tanımlarız.

# 4. Artık bu sınıf:
#    - for döngüsünde kullanılabilir
#    - next() fonksiyonuna verilebilir
#    - isinstance(obj, Iterator) → True sonucu verir

# Kullanım örneği:
v = Veri((1, 2, 3))
for i in v:
    print(i)  # 1, 2, 3

# Iterator kontrolü:
print(isinstance(v, Iterator))  # True

class Veri(Iterator):
    
    def __init__(self,veri):
        self.veri = iter(veri)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.veri)


verim = Veri((1,2,3,4,5,6))

print(verim.veri) #<tuple_iterator object at 0x000002480DCEB520>

#Başka bir örnek:

class A(Container):

    def __init__(self):
        self.val = ()
    

try:
    a = A()

except TypeError as t: print(t) #Can't instantiate abstract class A with abstract method __contains__
# Container soyut sınıfnda bulunan __contains__ metodu, @abstractmethod olarak tanımlanmıştır
# yani bu metod soyuttur sadece subclass'ın bu metodu override etmek zorunda olduğunu gösterir bu nedenle bu sınıf çağrısında TypeError aldık


class A(Container):

    def __init__(self):
        self.val = ()
    
    def __contains__(self, x):
        return x in self.val
    
a = A()

print(
isinstance(a,Container), # True
)
#Çünkü Container soyut sınıfı,sadece __contains__ metodu ister