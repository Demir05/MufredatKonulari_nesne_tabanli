# 🧠 Python'da class tanımı sırasında keyword argüman geçmek mümkündür,
# ancak bu sadece sınıf başka bir sınıftan miras alıyorsa geçerlidir.

# 🔸 Örnek:
# class A(Base, debug=True):  # ✅ Geçerli
# class A(debug=True):        # ❌ SyntaxError (çünkü miras yok)

# ❗️ Bunun sebebi, bu keyword argümanlar Python tarafından
# __init_subclass__ adlı özel metoda yönlendirilir.
# Bu method ancak bir BASE sınıf varsa devreye girer.

# 📌 Eğer Base sınıfında __init_subclass__ yoksa, Python zinciri takip eder
# ve en son type.__init_subclass__'a kadar gider.
# Ancak oradaki varsayılan tanım şudur:
# def __init_subclass__(cls,/): pass
# → Yani keyword parametre kabul etmez!

# 🔥 Bu yüzden aşağıdaki kullanım HATA verir:
# class A(Base, foo=True)  → TypeError: type.__init_subclass__() takes no keyword arguments

# ✅ Çözüm: __init_subclass__ metodunu BASE sınıfında override etmektir:
# class Base:
#     def __init_subclass__(cls, **kwargs):
#         super().__init_subclass__(**kwargs)

# 💬 Peki neden genelde **kwargs kullanılır?
# Çünkü tek bir keyword yerine birden fazlası geçilebilir,
# ve gelecekte genişletilebilirlik sağlar.

# 🔧 Örnek imza farkları:
# def __init_subclass__(cls, debug):       → sadece debug alır, esnek değildir
# def __init_subclass__(cls, **kwargs):    → esnektir, plugin tasarımı gibi yerlerde tercih edilir

# 🧠 Sonuç olarak:
# - class tanımında keyword geçeceksen bir base class OLMALI
# - o base class __init_subclass__ ile bu keyword'leri karşılamalı
# - yoksa Python fallback olarak type.__init_subclass__'ı çağırır ve bu da patlar



# ---------------------------------------------------
# 📘 __init_subclass__ ve class tanımındaki kwargs
# ---------------------------------------------------

# Bu sınıf, kendisinden türeyen sınıfların tanımı sırasında verilen
# keyword argümanları (debug, strict gibi) alabilir ve işleyebilir.
class Base:
    def __init_subclass__(cls, *, debug=False):
        # debug parametresi True olarak geçirilmişse bilgi mesajı yazdır
        if debug:
            print(f"🛠️  {cls.__name__} debug modda tanımlandı!")

# 🔽 Şimdi bu sınıf Base'den miras alıyor ve debug=True parametresi ile tanımlanıyor
class Custom(Base, debug=True):
    pass

# ---------------------------------------------------
# 🧠 TEORİK AÇIKLAMALAR:
# ---------------------------------------------------

# ✔️ class Custom(Base, debug=True):
#    - Buradaki parantez normalde sadece miras için kullanılır (Base gibi)
#    - Ancak Python, class tanımlarını içsel olarak şuna çevirir:
#      → Custom = type("Custom", (Base,), {}, debug=True)

# 🔥 Bu nedenle, debug=True parametresi, Base sınıfındaki __init_subclass__ metoduna gider

# ✔️ __init_subclass__ methodunda:
#    - 'cls' parametresi → yeni tanımlanmakta olan alt sınıfı temsil eder
#    - '*' → sonraki tüm parametrelerin sadece keyword olarak verilmesini zorunlu kılar
#    - 'debug=False' → isteğe bağlı bir parametre (varsayılan False)

# ❌ Positional argüman (yani *args) class tanımında kullanılamaz!
#    class MyClass(Base, True, False) → SYNTAX ERROR oluşur
#    çünkü Python sadece tuple of base types ve keyword argümanlara izin verir

# ✔️ Ama şu geçerlidir:
#    class MyClass(Base, debug=True, strict=False)

# 🧠 Sonuç:
# __init_subclass__, class tanımı sırasında keyword argüman alabilir,
# ama sadece keyword-based olmalıdır — positional değil!

# Bu özellik, özellikle kütüphane veya plugin sistemlerinde çok esneklik sağlar.

class B:
    def __init_subclass__(cls,deneme):
        cls.deneme = deneme

class A(B,deneme="demir"):
    def __init__(self, isim):
        self.isim = isim

    @classmethod
    def f(cls):
        print(cls.deneme)

A.f()