# ========================================================
# 🔷 mro() METODU NEDİR? NE İŞE YARAR?
# ========================================================

# ➤ Python'da çoklu kalıtım (multiple inheritance) varsa,
# bir attribute veya metot arandığında hangi sınıflara
# hangi sırayla bakılacağını belirlemek gerekir.

# İşte bu sıraya "MRO" yani Method Resolution Order denir.

# 🔹 type.mro(cls) → Bu fonksiyon, bir sınıfın MRO'sunu
# hesaplar ve döner. (hesaplama algoritması: C3 Linearization)

# 🔹 cls.__mro__ → Bu ise sınıfın MRO zincirini veren bir
# attribute'dur (hazır bir tuple gibi davranır, değiştirilemez)

# ✅ Örnek:

class A: pass
class B(A): pass
class C(B): pass

# mro() → MRO hesaplayan metot
print(type.mro(C))
# [<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>]

# __mro__ → Hazır attribute
print(C.__mro__)
# (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)

# Gördüğün gibi ikisi aynı sonucu verir — ama biri hesaplar, diğeri hazırdır.

# 🔸 NOT: type.mro(C) → override edilebilir bir metottur
# Özellikle metaclass ile özel MRO sıralaması yazmak için kullanılır:

class MyMeta(type):
    def mro(cls):
        print(f"Özel MRO hesaplanıyor -> {cls.__name__}")
        return super().mro()

class Base: pass
class MyClass(Base, metaclass=MyMeta): pass

print(MyClass.__mro__)  # mro override edildiği için log verir

# ========================================================
# 🧠 PEKİ NEDEN type.mro() VAR? __mro__ ZATEN VARKEN?
# ========================================================

# ❓ Çünkü __mro__ sadece bir attribute'dur:
#   - Değeri hazırdır, sadece okunur
#   - Hesaplama mantığı içermez
#   - Override edilemez

# ❗ Ama bazı özel durumlarda (örneğin framework veya ORM sistemlerinde)
#   - MRO'yu özel kurallara göre sıralamak istersin
#   - Bu durumda type.mro() override edilebilir
#   - Böylece Python senin belirlediğin sırayı kullanır

# ➕ Yani:
#   - __mro__ = veri
#   - mro() = mantık

# 📌 Bu separation of concerns prensibidir:
# Bir şeyin "ne olduğu" (__mro__) ile "nasıl hesaplandığı" (mro())
# ayrıdır.

# ========================================================
# 📘 SONUÇ:
# --------------------------------------------------------
# 🔸 __mro__ → hazır tuple, readonly
# 🔸 mro() → override edilebilir hesaplama mantığı
# 🔸 Çoklu kalıtımda davranışı özelleştirmek için mro() kullanılır
