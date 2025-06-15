# MİRAS ve __slots__ İLİŞKİSİ

# __slots__, bir sınıfın hangi attribute'lara sahip olacağını önceden belirleyip, __dict__'i devre dışı bırakmamıza yarar.
# Bu sayede bellekte tasarruf sağlanır ve yeni attribute eklenemez (eğer __dict__ açıkça eklenmemişse).

# Peki miras aldığımızda ne olur?

# Temel kurallar:
# 1. Eğer bir üst sınıf (base class) __slots__ tanımlamışsa, alt sınıf (subclass) bu attribute'lara erişebilir.
# 2. Alt sınıf ayrıca kendi __slots__'unu tanımlayabilir.
# 3. Ancak __slots__ sadece o sınıfın attribute'larını sınırladığı için, alt sınıfta yeni __slots__ tanımı yapılmazsa,
#    alt sınıfın __dict__'i yeniden oluşur ve dinamik attribute eklenmesine izin verir.
# 4. __slots__ alanları, miras olarak taşınır override edilmez subclass'da __slots__ tanımlasan bile python otomatik olarak senin yerine;
#   __slots__ = superclass.__slots__ + ("...",) yapar 

# ÖRNEK:

class UstSinif:
    __slots__ = ('x',)

    def __init__(self):
        self.x = 10

class AltSinif(UstSinif):
    __slots__ = ('y',)  # alt sınıf da kendi slotlarını tanımlar __slots__ = UstSinif.__slots__ + ('y',) -> python,bu işlemi senin yerine yapar __slots__ alanları, miras olarak taşınır override edilmez

    def __init__(self):
        super().__init__()
        self.y = 20


a = AltSinif()
print(a.x)  # 10
print(a.y)  # 20

# a.z = 30  # → AttributeError: 'AltSinif' object has no attribute 'z'
# Çünkü __dict__ yok, sadece ('x', 'y') tanımlı


# Eğer AltSinif içinde __slots__ TANIMLANMAZSA:
class AltSinif2(UstSinif):
    pass

b = AltSinif2()
b.x = 100
b.yeni = "merhaba"  # OLUR! çünkü __slots__ tanımlanmadığı için __dict__ geri gelir

# NOT:
# Eğer hem miras alınan sınıfta hem de alt sınıfta __slots__ kullanmak istiyorsan,
# her sınıf kendi __slots__'unu tanımlamalı VE python tüm slot'ları doğru bir şekilde birleştirip yönetir.

# UYARI:
# Eğer __slots__ kullandığın bir sınıfı miras alıyorsan ve alt sınıfta da __slots__ tanımlarsan,
# __weakref__ gibi özel attribute'ları da manuel olarak tanımlamalısın (örneğin GUI framework'lerinde önemli olabilir).

# ÖZET:
# - __slots__ kullanmak bellekte avantaj sağlar.
# - Miras alınan sınıfta varsa, alt sınıfta da __slots__ tanımlamak gerekebilir.
# - Alt sınıfta __slots__ yoksa, dinamik attribute tanımı yeniden açılır (__dict__ geri gelir).
# - Bu nedenle, kontrollü sınıf tasarımı için her seviyede __slots__ dikkatlice ele alınmalıdır.


# Çoklu Miras Alma:

# Üst sınıf A bir __slots__ tanımı içeriyor
class A:
    __slots__ = ("a",)  # A sadece "a" isimli attribute'u destekliyor

# Üst sınıf B de ayrı bir __slots__ tanımı içeriyor
class B:
    __slots__ = ("b",)  # B sadece "b" isimli attribute'u destekliyor

# Alt sınıf C, hem A hem B'den miras alıyor
# Her ikisi de __slots__ tanımladığı için bu çoklu miras ÇATIŞMA yaratıyor
# Çünkü Python her sınıfın nesne hafızasını farklı şekilde düzenliyor
class C(A, B):
    __slots__ = ("c",)  # C'ye "c" eklemek istiyoruz ama...

# ❌ Bu yapı TypeError ile sonuçlanır:
# TypeError: multiple bases have instance lay-out conflict

# 🧠 NEDEN?
# Çünkü hem A hem B kendi özel hafıza yapısını (__slots__) tanımlamış.
# Python bu farklı "layout"ları tek bir C sınıfında nasıl birleştireceğini bilemez.
# __slots__, method gibi miras alınamaz — belleğe fiziksel yerleşim tanımlar!

# ✅ ÇÖZÜM?
# Ya sadece bir sınıfta __slots__ kullan:
class B_no_slot:  # Bu sınıf artık çakışma yaratmaz
    pass

class C_fixed(A, B_no_slot):
    __slots__ = ("c",)  # Artık sorunsuz çalışır


# __slots__ → sınıfın bellekte nasıl yerleşeceğini tanımlar
# Zincirleme miras (tek hat): slots düzgün şekilde miras alınır
# Çoklu miras: birden fazla farklı layout çakışır → TypeError oluşur
# Python "hangi yapıyı kullanayım?" sorusunu çözemediği için layout conflict hatası verir