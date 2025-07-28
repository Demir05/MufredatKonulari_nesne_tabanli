# 🧠 DOĞRU VE GÜNCELLENMİŞ METACLASS ÇATIŞMASI TANIMI

# 🔍 Python bir sınıf tanımı yaparken (örneğin: class C(A, B): ...)
# önce şunu belirlemek zorundadır:
#   "Bu yeni sınıfın metaclass'ı ne olacak?"

# 🧱 Bu kararı verirken, tüm base sınıfların metaclass'larını inceler:
# örneğin:
#   class A(metaclass=MetaA)
#   class B(metaclass=MetaB)
# ise Python, C(A, B) tanımı yapılırken MetaA ve MetaB'yi ele alır

# ✅ Hedef: MetaA ve MetaB'den türeyen "en derived" (en alt seviye) ortak bir metaclass bulmak

# 📌 Kurallar:
#   1. Eğer tüm base sınıfların metaclass'ları ortak bir ata sınıf ilişkisi içindeyse → sorun yok
#   2. Eğer metaclass'lar arasında **doğrudan veya dolaylı** bir subclass ilişkisi YOKSA → ❌ HATA!

# ❌ ÖRNEK HATALI DURUM:
class MetaA(type): pass
class MetaB(type): pass

class A(metaclass=MetaA): pass
class B(metaclass=MetaB): pass

# class C(A, B): pass  # 🔥 TypeError → MetaA ve MetaB birbirinden bağımsız!

# ✅ ÇÖZÜM:
# MetaA ve MetaB'den türeyen ortak bir metaclass yaratılır:
class MetaCommon(MetaA, MetaB): pass

class C(A, B, metaclass=MetaCommon): pass  # ✔️ Artık geçerli

# 🧩 DİKKAT:
# Sadece "ikisi de type'tan geliyor" yetmez,
# mutlaka "birbirinden türemiş veya ortak türev" olmalıdır

# ✅ Python şöyle der:
#   “Birini diğerine çevirebiliyor muyum?”
#   “Hangisi daha türetilmiş (derived)?”

# 🧠 ÖZETLE:
# 1. Tüm base sınıfların metaclass’ları alınır
# 2. Bu metaclass’lar arasında bir “en derived ortak metaclass” aranır
# 3. Eğer bulunamazsa → TypeError: metaclass conflict
