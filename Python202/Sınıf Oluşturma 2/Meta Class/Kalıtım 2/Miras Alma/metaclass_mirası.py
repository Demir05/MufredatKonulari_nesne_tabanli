# =====================================================
# 🎓 METACLASS'LARDA MİRAS — YAPI ve UYUMLULUK SİSTEMİ
# =====================================================

# 🔹 Python'da metaclass'lar da birer sınıftır (type'dan türetilirler)
# 🔹 Bu yüzden bir metaclass, başka bir metaclass'tan MİRAS alabilir

# ➕ Amaç:
#   - Davranışları birleştirmek
#   - Ortak metotları tek bir metaclass içinde paylaşmak
#   - Büyük sistemlerde tüm metaclass ihtiyaçlarını hiyerarşik olarak çözmek

# =====================================================
# 🧠 KONU: Metaclass → Metaclass Kalıtımı (Inheritance)
# =====================================================

# 🔸 Parent metaclass → Ortak temel davranışları sağlar
# 🔸 Child metaclass → Üsttekinin davranışlarını özelleştirir ya da genişletir
# 🔸 Sonuçta: Child metaclass = Parent metaclass + ekstra yetenek

# 💡 Unutma:
#   - Sınıf: instance oluşturur
#   - Metaclass: sınıfı oluşturur
#   - Metaclass da sınıf gibi davranır = miras alabilir

# =====================================================
# 🔧 ÖRNEK: METACLASS MİRAS ZİNCİRİ
# =====================================================

# Ana metaclass — ortak davranışlar burada
class BaseMeta(type):
    def __new__(mcs, name, bases, dct):
        print(f"[BaseMeta.__new__] → {name}")
        return super().__new__(mcs, name, bases, dct)


# İkinci seviye metaclass — ekstra validasyon
class ValidateMeta(BaseMeta):
    def __init__(cls, name, bases, dct):
        print(f"[ValidateMeta.__init__] → {name}")
        if "id" not in dct:
            raise TypeError(f"{name} sınıfında 'id' attribute'u zorunlu!")
        super().__init__(name, bases, dct)


# Son metaclass — başka özel davranışlar da eklenebilir
class LoggingMeta(ValidateMeta):
    def __setattr__(cls, key, value):
        print(f"[LoggingMeta.__setattr__] → {key} = {value}")
        super().__setattr__(key, value)
    

# =====================================================
# 🧪 Bu metaclass hiyerarşisini kullanan sınıf
# =====================================================
class Model(metaclass=LoggingMeta):
    id = 123


# ✅ Burada olanlar:
# 1. LoggingMeta.__new__() çağrılır (BaseMeta'dan miras)
# 2. ValidateMeta.__init__() çağrılır → id kontrolü yapılır
# 3. LoggingMeta.__setattr__ → Model.attr = val tarzı işlemleri yakalar


# =========================================================================
# 🎓 METACLASS HİYERARŞİSİ — GERÇEK DÜNYADA KULLANIM AMACI ve FAYDALARI
# =========================================================================

# 🔷 Python'da metaclass mirası, sadece teorik bir oyun değildir.
# 🔷 Büyük framework'lerde, ORM'lerde, veri şeması yönetimlerinde çok kullanılır.

# 🔹 Amaç:
#    - Tek bir metaclass ile her davranışı yüklemek yerine
#    - Parça parça yetenekleri "katmanlara" ayırmak
#    - Bu sayede ESNEK ve YENİDEN KULLANILABİLİR bir yapı kurmak

# =========================================================================
# ✅ FAYDALARI NELERDİR?
# =========================================================================

# 1️⃣ Ayrı Sorumluluklar: Her metaclass sadece bir görevi üstlenir
#    - örneğin biri doğrulama (validation)
#    - diğeri otomatik kayıt (registry)
#    - başka biri logging veya debug
#
# 2️⃣ Katmanlı kontrol: Sistemin farklı aşamalarında davranış ekleyebilirsin
#    - örnek: ORM için alanları kayıt et
#    - örnek: eğer özel bir özellik tanımlanmamışsa hata fırlat
#
# 3️⃣ Genişletilebilirlik: Yeni ihtiyaçlar çıktığında zincire yeni bir sınıf eklersin

# =========================================================================
# 🌍 GERÇEK DÜNYA ÖRNEKLERİ
# =========================================================================

# ➤ Django ORM:
#    - Model tanımladığında arka planda bir metaclass devreye girer
#    - Alanları __new__ içinde toplar, __init__ içinde kontrol eder
#
# ➤ Pydantic (data validation):
#    - Field tanımlamalarını metaclass toplar
#    - Validasyon, sıralama, özel alan kontrolleri yapar
#
# ➤ Plugin sistemleri:
#    - Yeni bir sınıf tanımlandığında otomatik olarak bir yerlere kayıt yapılır

# =========================================================================
# 🔧 ÖRNEK: KATMANLI METACLASS ZİNCİRİ
# =========================================================================

# 1. Alan toplayıcı
class CollectFieldsMeta(type):
    def __new__(cls, name, bases, dct):
        dct["_fields"] = [k for k in dct if not k.startswith("__")]
        return super().__new__(cls, name, bases, dct)

# 2. Otomatik kayıt sistemi
class RegistryMeta(CollectFieldsMeta):
    registry = []
    def __init__(cls, name, bases, dct):
        RegistryMeta.registry.append(cls)
        super().__init__(name, bases, dct)

# 3. Doğrulama yapan metaclass
class ValidationMeta(RegistryMeta):
    def __init__(cls, name, bases, dct):
        if "id" not in dct:
            raise TypeError(f"{name} sınıfında 'id' eksik!")
        super().__init__(name, bases, dct)

# Kullanıcı sınıfı → bu zincirin tüm davranışlarını alır
class Model(metaclass=ValidationMeta):
    id = 1
    name = "Ali"

# Şimdi Model:
# → __new__: field'ları topladı
# → __init__: Registry'e eklendi
# → __init__: 'id' var mı kontrol edildi
