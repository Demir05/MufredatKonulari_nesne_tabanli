# -----------------------------------------
# 📘 __init_subclass__ - Başucu Rehberi
# -----------------------------------------
from mypy import plugins


# -----------------------------
# 🧠 1. TEORİK BİLGİ
# -----------------------------

# __init_subclass__, bir sınıf başka bir sınıftan türediği anda (tanımlandığı anda) otomatik olarak çağrılan bir özel metottur.
# Bu method, "üst sınıf" (base class) tarafından tanımlanır ve "alt sınıf" tanımlandığında otomatik tetiklenir.
# Kısaca: class Sub(Base): ... → bu tanım yapılır yapılmaz Base.__init_subclass__(Sub) çağrılır.

# cls → tanımlanan alt sınıfın kendisini temsil eder
# self yoktur çünkü bu method bir "sınıf" olayına karşılık gelir, nesneye değil!
# @classmethod ile işaretlenmesine gerek yoktur çünkü Python bu özel metodu otomatik olarak cls ile çağırır.

# -----------------------------
# ⚠️ 2. DİKKAT EDİLMESİ GEREKENLER
# -----------------------------

# - __init_subclass__ Python 3.6+ versiyonlarda object sınıfına yerleşik olarak eklenmiştir
# - super().__init_subclass__ çağırmak zorunlu değildir ama çoklu kalıtım durumlarında iyi bir pratiktir
# - alt sınıfın init_subclass'ı miras almasına gerek yoktur, sadece base class tanımlar
# - kwargs parametresi opsiyoneldir, alt sınıf tanımı sırasında özel keyword argümanlar geçilebilmesini sağlar

# -----------------------------
# 🧰 3. KULLANIM ALANLARI
# -----------------------------

# ✅ Otomatik alt sınıf kaydı (plugin/handler sistemleri)
# ✅ Alt sınıfların zorunlu method veya attribute içermesini sağlama
# ✅ Tanımlanan sınıfları loglama veya debug amacıyla izleme
# ✅ Alt sınıf yapılarını introspection (cls.__dict__, cls.__annotations__) ile analiz etme
# ✅ DSL (domain-specific language) veya framework mimarisi yazarken altyapı kurma


# 🧠 __init_subclass__ nasıl çalışır? (Sade anlatım)

# 1️⃣ Python, yeni bir sınıf (örneğin Child) tanımlandığında belleğe alır
# 2️⃣ Hemen ardından __init_subclass__ isimli özel methodu çalıştırır
# 3️⃣ Bu işlem normal bir attribute araması değildir
#    → Python doğrudan çalıştırılacak metodu bilir
# 4️⃣ __init_subclass__ MRO zincirine göre ilk bulunan sınıfta çalıştırılır
#    → örnek: Base sınıfında varsa, oradaki method çağrılır
# 5️⃣ Python içsel olarak şu şekilde çağırır:
#    → Base.__init_subclass__.__get__(Child,Owner)()
#    → __get__ metodu,Child sınıfına bağlanır Owner,Base sınıfının kendisidir
#    → Yani cls = Child olarak gider
#    → bunun sonucunda bound method elde ederiz çünkü __init_subclass__,bir method'dur
# 6️⃣ Eğer method tanımlı değilse, object’teki boş hali çalışır (hiçbir şey yapmaz)

# ✅ Bu sayede Base sınıfı, ondan türeyen tüm sınıfların tanımlandığı anı yakalayabilir

# -----------------------------
# 💡 4. ÖRNEK UYGULAMA
# -----------------------------

# Base sınıf, kendisinden türeyen tüm sınıfları otomatik olarak kaydedecek
class PluginBase:
    plugins = []  # Kayıtlı plugin listesi

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)  # Çoklu inheritance için iyi alışkanlık

        print(f"📌 Yeni plugin bulundu: {cls.__name__}")  # Loglama
        PluginBase.plugins.append(cls)  # Alt sınıfı kaydet

        # Alt sınıfın 'run' methoduna sahip olup olmadığını kontrol et
        if not hasattr(cls, "run"):
            raise NotImplementedError(f"{cls.__name__} sınıfı 'run' metodunu içermeli!")

# Alt sınıf tanımlanır tanımlanmaz yukarıdaki __init_subclass__ çalışır
class MyPlugin(PluginBase):
    def run(self):
        print("Çalışıyorum!")

# Bu sınıf da geçerli çünkü 'run' metodu tanımlı
class AnotherPlugin(PluginBase):
    def run(self):
        print("Ben de çalışıyorum!")

# Şimdi kayıtlı plugin listesini görelim
print("🔍 Kayıtlı plugin'ler:", [cls.__name__ for cls in PluginBase.plugins])

# -----------------------------------------
# 🧠 SONUÇ
# -----------------------------------------

# __init_subclass__, Python'da metaprogramlama yapan geliştiriciler için güçlü bir araçtır.
# Bir sınıfın kimden türediğini izlemek, türeyen sınıfları denetlemek ve otomatik mimari kurmak için kullanılır.
# Özellikle framework, plugin altyapısı, interface gibi gelişmiş sistemlerde hayat kurtarıcıdır.

class A:
    plugins = []
    def __init_subclass__(cls, **kwargs):
        print("çağrıldım",cls.__name__)
        A.plugins.append(cls.__name__)
        super().__init_subclass__(**kwargs)


class B(A):
    def __init__(self):
        self.name = "b"
b = B()
print(A.__dict__)
b.__getattribute__("__init_subclass__").__call__()
type(b).__mro__[1].__dict__['__init_subclass__'].__get__(b,B).__call__()
try:
    type(b).__mro__[1].__dict__['__init_subclass__'].__call__(b)
except Exception as e:
    print(e)
b.__init_subclass__()
B.__mro__[1].__init_subclass__()
print(A.plugins)
A.__init_subclass__()
A.__init_subclass__.__get__(B,A).__call__()

print(A.__dict__['__init_subclass__'])