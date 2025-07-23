# ==========================================================
# 📘 PYTHON'DA METACLASS — “Sınıf Üreten Sınıf” Yapısı
# ==========================================================


# 🔹 GİRİŞ: NEDİR BU METACLASS?

# Python'da nesneler sınıflardan üretilir.
# Ancak sınıfların kendisi de birer nesnedir ve onların üretimi de bir "sınıf" tarafından yapılır.
# İşte bu sınıf, metaclass’tır.

# type(A) dediğinde sonuç <class 'type'> ise A sınıfı type tarafından üretilmiş demektir.


# 🔹 TEMEL TANIM:

# Metaclass: Sınıfları oluşturan sınıflardır.
# Genelde 'type' sınıfı kullanılır. Ancak kendi özel metaclass'ını yazarak bu süreci özelleştirebilirsin.


# 🔹 KULLANIM AMAÇLARI:

# - Sınıf tanımı sırasında müdahale etmek
# - Field veya metodları kontrol etmek
# - Otomatik özellikler eklemek
# - ORM/Validation/Plugin sistemleri kurmak
# - ABC gibi interface kuralları oluşturmak


# 🔹 METACLASS'IN DEVREYE GİRDİĞİ NOKTALAR:

# type veya kendi metaclass’ının override ettiği metotlar:
# __new__        → sınıfın belleğe yazılmadan önceki tanımı (yapı aşaması)
# __init__       → sınıf oluşturulduktan sonra içerik yerleşimi (başlatma aşaması)
# __call__       → sınıf çağırıldığında (örnek oluşturma)
# __setattr__    → sınıf seviyesinde özellik değiştirme
# __getattribute__/__getattr__ → sınıfın attribute erişim davranışı


# 🔹 ÖRNEK: BASİT BİR METACLASS

class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"[Meta] Sınıf Tanımlanıyor: {name}")
        return super().__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        print(f"[Meta] {cls.__name__} örnekleniyor!")
        return super().__call__(*args, **kwargs)

    def __setattr__(cls, name, value):
        print(f"[Meta] {name} attribute'u değiştiriliyor → {value}")
        return super().__setattr__(name, value)


class MyClass(metaclass=MyMeta):
    def __init__(self):
        self.x = 10

# Sınıf tanımı anında çalışır (örnek üretmesek bile):
# [Meta] Sınıf Tanımlanıyor: MyClass

obj = MyClass()
# [Meta] MyClass örnekleniyor!

MyClass.y = 20
# [Meta] y attribute'u değiştiriliyor → 20


# 🔹 METACLASS vs __init_subclass__

# __init_subclass__ sadece alt sınıf tanımlandığında çalışır.
# Metaclass ise sınıf tanımı anında çalışır ve her class için uygulanabilir.

class Base:
    def __init_subclass__(cls, **kwargs):
        print(f"[Base] Alt sınıf tanımlandı: {cls.__name__}")

class Alt(Base):
    pass
# Çıktı: [Base] Alt sınıf tanımlandı: Alt


# 🔹 UNUTMA:

# - Metaclass işlemi **runtime değil, class tanımı sırasında** çalışır
# - Sınıf üzerinde yapılan tüm işlemler (örnekleme, attr atama) aslında metaclass tarafından kontrol edilir
# - Sadece ihtiyaç duyulan yerde kullanılmalı çünkü kod karmaşıklığını artırır

# ==========================================================
# 🧠 NEDEN METACLASS'LAR `type` SINIFINDAN MİRAS ALIR?
# ==========================================================


# 🔹 1. type SINIFI, SINIF OLUŞTURMAKLA SORUMLU "FABRİKADIR"

# Normalde Python bir class bloğu gördüğünde aslında arka planda şunu yapar:

# A = type("A", (), {})
# Yani class tanımı, aslında type() fonksiyonuyla yapılır.

# Bu nedenle biz metaclass yazmak istediğimizde, type'ı özelleştirmemiz gerekir.
# type'ın yerine kendi üretim kurallarımızı koymak için ondan miras alırız.


# 🔹 2. ÖZEL METACLASS YAZMA

# Aşağıdaki gibi bir metaclass tanımlarsan:
class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"Sınıf tanımlanıyor: {name}")
        return super().__new__(cls, name, bases, attrs)

# Burada MyMeta sınıfı, type’tan türediği için artık sınıf üretme işlemlerini özelleştirebilir.


# 🔹 SONUÇ:

# Kendi metaclass’ını yazarken type’tan miras almak zorundasın çünkü:
# - Sınıf oluşturma sürecine müdahale edebilmek için type’ın altyapısını genişletiyorsun
# - Sınıf seviyesi davranışları yönetmek için gereken kontrolü elde ediyorsun


# ==========================================================
# 🧠 "metaclass=" NEDİR? — Python'da Syntactic Sugar ve Arka Plan
# ==========================================================

# 🔹 GİRİŞ:

# Python'da bir sınıf tanımı yaptığında aslında Python, bu tanımı yorumlayıp
# arka planda bir metaclass çağrısı yapar.
# Bu metaclass, varsayılan olarak "type" sınıfıdır.
# Ancak "metaclass=" ile bunu özelleştirebilirsin.

# 🔹 ÖRNEK: KLASİK metaclass TANIMI

class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"[MyMeta] Sınıf üretildi: {name}")
        return super().__new__(cls, name, bases, attrs)


# 🔹 Normal Kullanım — metaclass belirtme

class A(metaclass=MyMeta):
    x = 42

# Bu satır çalıştığında arka planda şu çağrılır:
# A = MyMeta("A", (object,), {"x": 42})


# 🔹 Manuel Kullanım — aynı işi biz yaparsak:

A_manual = MyMeta("A_manual", (object,), {"x": 42})

print(A_manual)       # <class '__main__.A_manual'>
print(A_manual.x)     # 42

# Buradaki fark: Python bunu bizim yerimize yapıyor, biz "class" sözdizimini kullanarak kolayca sınıf tanımlıyoruz


# 🔹 NEDEN "metaclass=" VAR?

# "metaclass=" bir Python keyword'ü değildir, ancak Python'un class tanımı sırasında tanıdığı
# özel bir "keyword argument"tir. Sadece "class" tanımı içerisinde geçerlidir.

# Bu sayede:
# - Daha okunabilir, sade, anlaşılır sınıf tanımları yapılabilir
# - IDE'ler, linters, dokümantasyon araçları bu sözdizimini anlayabilir
# - Geliştiriciler karmaşık sınıf üretimlerini basitçe yapılandırabilir


# 🔹 SONUÇ:

# metaclass=MyMeta ifadesi sadece bir syntactic sugar'dır.
# Python, bu syntax'ı görünce arka planda:
# → MyMeta("SınıfAdı", (BaseClass,), class_dict) çağrısını yapar

# Sen istersen bu sınıfı doğrudan da üretebilirsin, örneğin:
# MyMeta("B", (), {"x": 99}) gibi.

