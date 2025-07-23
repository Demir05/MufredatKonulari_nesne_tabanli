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

# ===============================================================
# 🧠 Metaclass İçinde `super()` Kullanımı Hakkında Notlar
# ===============================================================

# 🔹 Metaclass içindeki __new__ metodunda:
# Neden `super().__new__(cls, name, bases, dct)` şeklinde çağrıyoruz?

# Çünkü __new__, sınıf objesini oluşturacak olan metottur. Yani:
# - Bu noktada "oluşturulacak sınıf" henüz yoktur
# - Python, sınıfı oluşturabilmek için hangi sınıf üzerinden türetileceğini bilmek zorundadır

# 💡 `super()` fonksiyonu normal sınıflarda genellikle `super().__init__()` şeklinde kullanılır.
# Bu durumda self zaten mevcut olduğu için Python neyi kastedildiğini bilir.

# Ancak metaclass’ta `__new__` bir "classmethod" gibi çalışır ve
# `super()`'ın çalışabilmesi için hangi sınıfın (`cls`) oluşturulmakta olduğunu belirtmek gerekir.

# ✅ Bu yüzden: `super().__new__(cls, name, bases, dct)` yazmak zorundayız.

# Eğer cls verilmezse, Python hangi sınıfın `__new__()` metodunu çağıracağını bilemez
# ve `TypeError` hatası alırsın.

# ===============================================================
# 🧪 Örnek (Doğru Kullanım):
class MyMeta(type):
    def __new__(cls, name, bases, dct):
        print("Metaclass __new__ çağrıldı")
        return super().__new__(cls, name, bases, dct)  # cls burada zorunlu

class MyClass(metaclass=MyMeta):
    pass

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


# 📘 __prepare__ METODU NEDİR?

# __prepare__ metodu, Python'da sınıf oluşturulurken kullanılan bir metaclass hook'udur.
# Metaclass sınıflarının içinde tanımlanabilir ve sınıf gövdesi (class body)
# oluşturulmadan hemen önce çağrılır.

# Yani:
# class Foo(metaclass=Meta): yazıldığında
# 1. __prepare__ çağrılır -> bir namespace (sözlük benzeri yapı) döner
# 2. class Foo gövdesi (x = 1, def ...) bu namespace'e yazılır
# 3. sonra __new__ ile sınıf nesnesi oluşturulur
# 4. sonra __init__ ile sınıf başlatılır

class MetaExample(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        # metacls:   Metaclass'ın kendisi (örnek: MetaExample)
        # name:      Tanımlanmakta olan sınıfın adı (str olarak)
        # bases:     Miras alınan sınıfların tuple'ı (örn: (Base1, Base2))
        #
        # 📌 DÖNÜŞ:   class body'de kullanılacak sözlük (dict ya da dict-like obje)
        #            -> içine 'x = 1', 'def foo()' gibi şeyler yazılır
        #
        # 🎯 KULLANIM AMAÇLARI:
        #   - Özel attribute’lar eklemek (varsayılanlar, loglama, docstring vs)
        #   - Base sınıflara göre dinamik namespace üretmek
        #   - OrderedDict, defaultdict gibi özel dict davranışları tanımlamak

        return dict(created_by='__prepare__')


# 🧠 NEDEN __prepare__ İÇİN @classmethod KOYMASAK DA BAZEN ÇALIŞIYOR?

# 🔸 Çünkü __prepare__ Python'daki TEK magic metoddur
#     → Argüman sayısına göre "kibarca davranan" özel bir istisna içerir.

# 🔸 Python __prepare__'i çağırırken şunu yapar:
#     1. type.__dict__['__prepare__'] ile metodu doğrudan alır (yani descriptor, __getattribute__, __get__ vs çalışmaz!)
#     2. Eğer method 2 parametre alıyorsa (name, bases) → Python "metacls" argümanını geçmeyebilir
#     3. Yani şuna benzer:
#        if prepare_arg_count == 2:
#            return prepare(name, bases)
#        else:
#            return prepare(metacls, name, bases)

# 🔥 Bu dinamik çağrı şekli sadece __prepare__'e özgüdür.
#    Diğer magic metodlarda böyle bir "argüman sayısına göre çağırma esnekliği" yoktur.

# 🎩 Neden böyle yapılıyor?
# - Çünkü __prepare__ sınıf gövdesi değerlendirilmeden önce çağrılır.
# - Eğer burada hata çıkarsa class tanımı çökebilir.
# - Dolayısıyla Python, sınıf tanım sürecinde hata toleransı yüksek tutar.

# ⚠️ RİSK?
# - @classmethod olmadan çalıştırırsan:
#     • IDE seni uyarır (mypy, pyright, VSCode vs)
#     • Kodun gelecek Python versiyonlarında çalışmama ihtimali vardır
#     • Geliştirici okurluğu azalır (metacls nerede?)

# ✅ DOĞRU YAKLAŞIM:
#     @classmethod
#     def __prepare__(metacls, name, bases):
#         ...

# ❌ GEÇİCİ AMA RİSKLİ:
#     def __prepare__(name, bases):  # metacls yok
#         ...


# Python çağırma zinciri düşük seviyede şöyle işler:
# 1. prepare_fn = Meta.__dict__['__prepare__']   # bound method değil!
# 2. namespace = prepare_fn(Meta, name, bases)   # manuel çağrı
# 3. type.__new__(Meta, name, bases, namespace)
# 4. Meta.__init__(cls, name, bases, namespace)



# ----------------
# 🔬 ŞİMDİ GERÇEK UYGULAMA ÖRNEĞİ
# ----------------

from typing import Any
from collections.abc import Mapping

class MetaExample(type):
    # ✅ Pythonic ve sağlam __prepare__ tanımı
    @classmethod
    def __prepare__(metacls, name: str, bases: tuple) -> Mapping[str, Any]:
        # Bu metod class gövdesi oluşturulmadan hemen önce çağrılır
        # Burada döndüğümüz dict benzeri yapıya, class gövdesindeki tüm attribute'lar yazılır
        print(f"📦 __prepare__ called: metacls={metacls.__name__}, name={name}, bases={bases}")
        return {'created_by': '__prepare__'}

    def __new__(cls, name, bases, namespace, **kwargs):
        # Sınıf objesi oluşturulurken çağrılır
        print(f"🛠️ __new__: name={name}, namespace={namespace}")
        return super().__new__(cls, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        # Sınıf objesi belleğe yerleştirildikten sonra çağrılır
        print(f"🚀 __init__: created_by={getattr(cls, 'created_by', None)}")
        super().__init__(name, bases, namespace)

# 🔧 Bu sınıf tanımı, yukarıdaki akışı başlatır
class User(metaclass=MetaExample):
    name = "aslı"
    age = 32

# ✅ Output:
# 📦 __prepare__ called: metacls=MetaExample, name=User, bases=()
# 🛠️ __new__: name=User, namespace={'created_by': '__prepare__', 'name': 'aslı', 'age': 32}
# 🚀 __init__: created_by=__prepare__

# 🧠 Artık:
print(User.created_by)  # __prepare__
print(User.name)        # aslı
print(User.age)         # 32


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



class U(type):

    @classmethod
    def __prepare__(metacls,name: str, bases: tuple[type,...]) -> Mapping[str,Any]:
        print("metacass",metacls)
        print("bases",bases)
        print("name",name)
        return dict()

class X(metaclass=U):
    pass

attr = U.__dict__["__prepare__"].__get__(X,U).__call__("X",(object,))
X = U.__mro__[1].__dict__["__new__"].__call__(U,"X",(object,),attr)

X.__class__.__mro__[1].__dict__["__init__"].__call__(X,"X",(object,),attr)
print(X)

class U(type):


    def __prepare__(name: str, bases: tuple[type,...]) -> Mapping[str,Any]:

        print("bases",bases)
        print("name",name)
        return dict()

class X(metaclass=U):
    pass

from inspect import signature

prepare = U.__dict__["__prepare__"]
lenght = len(signature(prepare).parameters)
if lenght == 2:
    attr = U.__dict__["__prepare__"].__call__("X",(object,))
else:
    attr = U.__dict__["__prepare__"].__get__(X,U).__call__("X",(object,),attr)
X = U.__mro__[1].__dict__["__new__"].__call__(U,"X",(object,),attr)

X.__class__.__mro__[1].__dict__["__init__"].__call__(X,"X",(object,),attr)
print(X)