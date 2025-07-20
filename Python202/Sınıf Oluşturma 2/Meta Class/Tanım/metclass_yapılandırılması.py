# ================================================
# 🧠 METACLASS YAPILANDIRMASI: __new__ METODU
# ================================================

# Metaclass'ta __new__ metodu, Python'da bir sınıf oluşturulmadan
# hemen önce devreye girer ve sınıfın yapısal bütünlüğünü denetler veya değiştirir.

# Örneğin: ORM sistemlerinde field'ların toplanması, validasyon yapılması gibi işlemler burada olur.

# Tam İmza:
# def __new__(metacls, name, bases, namespace, **kwargs):

# Parametreler:
# - metacls: Yeni oluşturulacak sınıfın metaclass'ı (örn: MyMeta)
# - name: Oluşturulacak sınıfın adı (örn: 'User')
# - bases: Sınıfın miras aldığı base class'ların tuple hali
# - namespace: Sınıf gövdesi (class body) içinde yazılmış tüm isimlerin bulunduğu sözlük
# - kwargs: Ek parametreler (__classcell__ gibi)

class MyMeta(type):

    # 🔸 __new__ metodu → sınıf oluşturulmadan önce çağrılır
    def __new__(cls, name, bases, namespace):
        """
        cls    → Metaclass’ın kendisi (örn: MyMeta)
        name   → Oluşturulacak sınıfın adı (str)
        bases  → Sınıfın miras aldığı üst sınıflar (tuple)
        namespace    → Sınıf gövdesindeki tüm tanımların tutulduğu dict (metod, alan, descriptor, vs.)
        """

        # ✨ dct → sınıf gövdesinde yazılan her şey burada toplanır (henüz sınıf oluşturulmamıştır!)
        # Bu dictionary doğrudan değiştirilebilir, sınıfa yeni özellikler buradan eklenebilir

        # Örnek kontrol: 'name' adlı bir attribute zorunlu olsun
        if "name" not in namespace:
            raise TypeError(f"{name} sınıfında 'name' attribute'u zorunludur.")

        # ✔️ Sınıfı oluştur ve geri dön
        return super().__new__(cls, name, bases, namespace)


# ================================================
# 🚀 Bu metaclass’ı kullanan bir sınıf tanımlayalım
# ================================================

class Model(metaclass=MyMeta):
    name = "örnek"

# Eğer 'name' attribute'u tanımlanmasaydı, TypeError fırlatılacaktı
# Bu sayede sınıfın tanımı sırasında yapısal validasyon yapılmış olur.

# ================================================
# ⚠️ cls.__dict__ vs dct farkı
# ================================================

# cls.__dict__ → mappingproxy → salt okunur, sınıf oluşturulduktan sonra erişilir
# dct          → dict → değiştirilebilir, sınıf oluşmadan hemen önce içerikleri temsil eder



# =============================================================
# 📘 METACLASS __init__ METODU — DERİNLEME ANALİZ
# =============================================================

# 🔹 Normal sınıflarda `__init__` → bir nesne örneği oluşturulduğunda çalışır
# 🔹 Metaclass'ta `__init__` → bir sınıf tanımlandığında çağrılır!

# 📌 Metaclass'ta tanımlanan `__init__`, yeni bir sınıf (class objesi) oluşturulurken,
#    o sınıf üzerinde son ayarlamaları yapmamıza olanak tanır.
#    Genellikle doğrulama (validation), otomatik kayıt, class-level attribute manipülasyonu gibi işler için kullanılır.

# Tam İmza:
# def __init__(cls, name, bases, namespace, **kwargs):

# Parametreler:
# - cls: Artık oluşmuş olan sınıf objesinin kendisi
# - name: Sınıfın adı
# - bases: Sınıfın miras aldığı sınıflar
# - namespace: Sınıf içeriğini belirten attribute sözlüğü
# - kwargs: Ek argümanlar (__classcell__ gibi, çoğu zaman otomatik iletilir)


# =============================================================
# ❓ NEDEN NORMAL __init__’ten FARKLI?
# =============================================================

# 🔹 Normal sınıf `__init__(self)` → sadece örnek başlatmak için
# 🔹 Metaclass `__init__(cls, name, bases, dct)` → sınıf objesini başlatmak için

# Çünkü metaclass, sınıfları **üreten** sınıftır.
# Yani `Model` sınıfı bir örnek değildir, bir sınıf objesidir.
# Dolayısıyla metaclass onunla bu şekilde konuşur.

# =============================================================
# 🧩 Diğer Dunder Metodların Parametreleri (metaclass içinde)
# =============================================================

# 🔸 __setattr__(cls, name, value)
#     - Model.x = 5 dediğimizde çağrılır
#     - `cls` → sınıf objesi (örneğin Model), çünkü metaclass'tayız

# 🔸 __getattribute__(cls, name)
#     - x = Model.y gibi sınıf attr erişiminde çağrılır

# 🔸 __call__(cls, *args, **kwargs)
#     - Model(...) yazıldığında çağrılır
#     - Burada sınıf objesi callable hale gelir → instance yaratılır
#     - Genellikle __new__ + __init__ zinciri başlatılır

# 🔸 __delattr__(cls, name)
#     - del Model.attr gibi sınıf seviyesinde attr silinirse çağrılır

# Bu metodların parametreleri, metaclass’ın yönettiği “sınıf objesi” üzerinden çalışır.
# Yani self yerine cls, instance yerine class davranışları göz önündedir.

# =============================================================
# 🎯 ÖRNEK:
# =============================================================

class MyMeta(type):
    def __init__(cls, name, bases, dct):
        print(f"[INIT] Sınıf Adı: {name}")
        print(f"[INIT] Base Sınıflar: {bases}")
        print(f"[INIT] Üyeler: {list(dct.keys())}")
        super().__init__(name, bases, dct)

    def __setattr__(cls, name, value):
        print(f"[SETATTR] {name} = {value}")
        super().__setattr__(name, value)

    def __getattribute__(cls, name):
        print(f"[GETATTR] {name}")
        return super().__getattribute__(name)

    def __call__(cls, *args, **kwargs):
        print(f"[CALL] Sınıf çağrıldı → {cls.__name__}")
        return super().__call__(*args, **kwargs)


class MyModel(metaclass=MyMeta):
    x = 5

    def __init__(self, value):
        print("Instance başlatıldı")
        self.value = value

# Sınıf tanımı anında:
# → __init__ (metaclass) çalışır

# Sınıf üzerinde işlem yapınca:
MyModel.new_attr = "test"    # __setattr__ (metaclass)
print(MyModel.x)             # __getattribute__ (metaclass)

# Sınıfı çağırınca:
obj = MyModel(42)            # __call__ (metaclass) → sonra örnek init çalışır


# ===================================================================
# 🧠 PYTHON'DA METACLASS → __prepare__ METODU (Nihai Açıklama)
# ===================================================================

# 🔹 __prepare__ metodu, Python'da bir sınıf tanımı yapılmadan hemen önce
#    çalıştırılan özel bir metoddur.
# 🔹 Amacı: class body (sınıf gövdesi) yazılırken, hangi "sözlük benzeri"
#    yapıya yazılacağını tanımlamaktır.

# 🔧 Sözdizimi:
# def __prepare__(cls_name:str, bases:Tuple[type,...]) -> Mapping:
#     return dict / OrderedDict / custom mapping...

# 🔹 Genelde `dict` veya `collections.OrderedDict` döndürülür.
# 🔹 Dönen mapping yapısı, sınıf gövdesi yazılırken `key=value` şeklinde
#    tanımlanan tüm öğeleri (metotlar, değişkenler vs.) toplar.

# -------------------------------------------------------------------
# 📋 Analoji:
# -------------------------------------------------------------------
# Düşün ki bir sınıf oluşturmak bir kitap yazmak gibi.
#   1️⃣ __prepare__ → "Boş bir kağıt ver" der, ve özel kağıt döndürür
#   2️⃣ class body → "Bu kağıda x, y, greet fonksiyonu yaz" der
#   3️⃣ __new__ → "Yazdıklarını al ve kitap haline getir" der

# -------------------------------------------------------------------
# 🎯 Kullanım Amaçları:
# -------------------------------------------------------------------
# ✅ Tanım sırasını korumak için (OrderedDict)
# ✅ class body’ye yazılanları önceden işlemek/filtrelemek
# ✅ class body’ye default değerler eklemek
# ✅ sınıf tanımında dekoratör veya özel notasyonları yakalamak

# -------------------------------------------------------------------
# 🔎 Örnek:
# -------------------------------------------------------------------

from collections import OrderedDict

class MyMeta(type):
    # 1️⃣ Sınıf yazılmadan önce çağrılır
    def __prepare__(name, bases):
        print(f"[__prepare__] → class '{name}' hazırlanıyor...")
        return OrderedDict()

    # 3️⃣ Class body yazıldıktan sonra çağrılır
    def __new__(cls, name, bases, class_dict):
        print(f"[__new__] → class '{name}' oluşturuluyor...")
        print("✏️ Tanım sırası:")
        for attr in class_dict:
            print(f"   → {attr}")
        return super().__new__(cls, name, bases, dict(class_dict))

# 2️⃣ Class body: Bu içerikler, __prepare__'in döndürdüğü OrderedDict'e yazılır
class MyClass(metaclass=MyMeta):
    a = 1
    b = 2
    def greet(self): return "hi"
