# =============================================================
# 📌 ÇOKLU MİRASDA METACLASS ÇAKIŞMASI — TypeError Açıklaması
# =============================================================

# 🔷 Python'da birden fazla sınıftan kalıtım yapılırken, her base class farklı bir metaclass kullanıyorsa
# 🔥 Python bu durumda hangi metaclass'ı seçeceğini bilemediği için bir çakışma hatası verir

# 💥 Hata:
# TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases

# ➤ Bu şu anlama gelir:
# Yeni oluşturulacak sınıfın metaclass'ı, tüm base sınıfların metaclass'larının **alt sınıfı (subclass)** olmak zorundadır

# 🔍 NEDEN?
# Çünkü Python sınıf oluşturma işlemini `metaclass.__new__()` ile yapar.
# Eğer birden fazla metaclass varsa ve bunlar uyumsuzsa, hangi `__new__` çağrılacak bilemez!

# ============================================================
# 🔧 ÖRNEK: UYUŞMAYAN METACLASS'LAR
# ============================================================

class MetaA(type):
    pass

class MetaB(type):
    pass

class A(metaclass=MetaA):
    pass

class B(metaclass=MetaB):
    pass

# ❌ Bu durumda Python hata verir çünkü MetaA ve MetaB birbirinden bağımsız
# ve Python ikisini aynı anda birleştirip ortak bir metaclass oluşturamaz

# class C(A, B):    # → 💥 HATA: metaclass conflict
#     pass

# ============================================================
# ✅ ÇÖZÜM: Ortak veya Uyarlanabilir Metaclass Kullanımı
# ============================================================

# 🔧 MetaA ve MetaB'nin ortak bir üst metaclass'ı olmalı veya birleştirilmeli

class BaseMeta(type): pass

class MetaA(BaseMeta): pass
class MetaB(BaseMeta): pass

class A(metaclass=MetaA): pass
class B(metaclass=MetaB): pass

# ✅ Artık Python C'yi oluştururken her iki metaclass'ın ortak noktası olan BaseMeta'yı kullanabilir
class C(A, B): pass  # ✔️ Sorunsuz
