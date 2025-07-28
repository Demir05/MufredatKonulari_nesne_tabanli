# ------------------------------------------------------
# 📖 SÖZEL + TEORİK TANIM — __mro_entries__ Mekanizması
# ------------------------------------------------------

# __mro_entries__:
# Python'da sınıf tanımı yapılırken kullanılan özel bir mekanizmadır.
# Bu mekanizma sayesinde, kalıtım listesinde görünen bir "obje",
# aslında başka bir sınıf(lar)ın kalıtılmasını sağlayabilir.

# -------------------------------------
# 🔑 NEDEN BÖYLE BİR MEKANİZMA VAR?
# -------------------------------------

# Python'da class tanımları esnasında kalıtım listesi mutlaka type objelerinden oluşmalıdır.
# Ancak zaman zaman wrapper/generic gibi class dışı nesneler bu listeye yazılmak istenebilir.
# İşte __mro_entries__ bu nesnelere "senin yerine kim kalıtılsın?" diye sorulmasını sağlar.

# -------------------------------
# 🧠 NASIL ÇALIŞIR? (ÇAĞRI ZİNCİRİ)
# -------------------------------

# Python aşağıdaki gibi bir tanım gördüğünde:
# class MyClass(Wrapper()):

# Şunları adım adım yapar:
# 1. Wrapper() çağrılır → instance döner
# 2. Python bu instance’a hasattr(x, '__mro_entries__') sorar
# 3. Varsa __mro_entries__((original_bases)) çağrılır
# 4. Döndürülen tuple, __bases__ olarak kullanılır
# 5. Wrapper objesi MRO’ya girmez, yerine dönen sınıflar girer

# -------------------------------
# ✍️ SÖZDİZİMİ VE GERİ DÖNÜŞ
# -------------------------------

# class Wrapper:
#     def __mro_entries__(self, bases: tuple) -> tuple:
#         return (GercekBase,)

# ⛳ Not:
# • self = çağrılmış base objesidir (ör: Wrapper())
# • bases = diğer base class’ların bulunduğu tuple
# • dönüş = tuple (type içeren)

# ------------------------------------
# 📦 NEREDE KULLANILIR? (KULLANIM AMAÇLARI)
# ------------------------------------

# • DSL tanımları (ör: class API(SecureRoute()))
# • ORM kalıtım enjektörleri (ör: class User(InjectDB()))
# • Typing / generic sistemleri (ör: List[int])
# • Plugin sistemleri (otomatik base injection)
# • Decorator tarzı class wrapper’lar

# ------------------------------------
# 🚫 EĞER __mro_entries__ TANIMLI DEĞİLSE?
# ------------------------------------

# • Python, base objesinin bir type olup olmadığına bakar
# • Eğer type değilse ve __mro_entries__ de yoksa:
#   🔥 TypeError: "bases must be types" hatası fırlatılır

# -------------------------
# 🧠 ÖNEMLİ KIYASLAMALAR
# -------------------------

# __mro_entries__ → class tanımı sırasında çalışır
# __bases__        → class tanımından sonra oluşan tuple
# __mro__          → method arama sırasını belirler (dinamik çözümleme)

# -------------------------
# 🧠 ÖZET TANIM
# -------------------------

# • __mro_entries__, sadece sınıf tanımı sırasında,
#   çağrılmış bir objenin yerine hangi base’lerin geçeceğini belirler
# • Bu mekanizma sayesinde, görünmeyen sınıf yapıları kalıtıma dahil edilebilir
# • Python’un derleyici düzeyinde tanıdığı bir “inheritance hook”tur

# ✅ Gereklilik: class tanımında objenin çağrılması gerekir → class A(Wrapper()) ✅
# ❌ Sadece class adı verilirse çalışmaz → class A(Wrapper) ❌


# 🔧 Bu, kalıtılacak gerçek sınıf
class Loggable:
    def log(self):
        print("📋 Logging...")

# 🎭 Bu, sadece görünür olan ama MRO'da yer almayacak olan dekoratif sınıf
class Logger:
    def __mro_entries__(self, bases):
        print(f"🔍 __mro_entries__ çağrıldı! bases={bases}")
        return (Loggable,)  # 👈 Gerçek kalıtım bu sınıftan olacak

# 🧪 Sınıf tanımı sırasında Logger() çağrılır → __mro_entries__ devreye girer
class Service(Logger()):
    def do(self):
        print("⚙️ Doing work")

svc = Service()
svc.do()
svc.log()  # 🔥 log() Loggable'dan geliyor

class E:pass

class P:
    def do(self):
        print("<UNK> Doing work")

class Z:
    def __mro_entries__(self, bases):


        return (P,)

bases = []

for base in (E,Z()):
    if hasattr(base, '__mro_entries__'):
        bases.extend(base.__mro_entries__((E,Z())))
    else:
        bases.append(base)
print(bases)

A = type("A",tuple(bases),{})

print(A.__mro__)
