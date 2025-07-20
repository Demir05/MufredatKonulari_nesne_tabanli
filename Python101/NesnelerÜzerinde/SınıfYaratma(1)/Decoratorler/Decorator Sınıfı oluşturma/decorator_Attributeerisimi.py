# -----------------------------------------------
# 🤔 Amaç: Sınıf İçinde Birden Fazla Decorator Tanımlamak
# -----------------------------------------------

# 🎯 Bu yaklaşım, decorator'ları organize etmek, gruplaştırmak, bir çatı altında tutmak için kullanılır.
# Örneğin loglama, otorizasyon, cache gibi farklı işlevleri tek bir "Decorator" sınıfında toplamak mantıklıdır.

# ✅ Sınıf, merkezi bir "dekoratör yöneticisi" olur.
# ❗ Bu sınıfın kendisi de bir decorator olabilir (via __call__), ama aynı zamanda içinde farklı decorator fonksiyonları da barındırabilir.

# -----------------------------------------------
# 📌 Teorik Tanım:
# -----------------------------------------------
# - @ işareti sadece bir fonksiyon çağrısıdır:  @x → x(func)
# - "x" burada: bir fonksiyon, bir sınıf, bir instance, bir static method, bir decorator vs olabilir.
# - Eğer sınıfın kendisini değil de içinde tanımlı metodunu decorator olarak kullanmak istiyorsan dikkat etmelisin:
#     👉 Eğer metoda "sınıf veya örnek" gerekmesin diyorsan: @staticmethod ile tanımlamalısın

# Çünkü:
#   - Instance method (self alır) = sadece nesne üzerinden çağrılabilir (@d.x)
#   - Static method (self almaz) = sınıf üzerinden çağrılabilir (@Decorator.x)

# -----------------------------------------------
# 🏗️ Örnek Yapı Kurulumu:
# -----------------------------------------------

class Decorator:
    def __init__(self, prefix):
        self.prefix = prefix  # Bu sadece __call__'da kullanılacak

    def __call__(self, func):
        # Bu, sınıfın kendisini bir decorator gibi kullanmamıza olanak tanır
        def wrapper(*args, **kwargs):
            print(f"[__call__] {self.prefix} - {func.__name__}")
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def log(func):
        # ✅ Bu method, sınıfla ya da self'le ilgilenmiyor
        # ✅ Bu yüzden @staticmethod olarak tanımlandı
        # ❗ Böylece @Decorator.log şeklinde kullanılabilir
        def wrapper(*args, **kwargs):
            print("[LOG] Fonksiyon çağrılıyor...")
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def auth(func):
        # ✅ Yine sınıfla ilgisi olmayan, doğrudan bağımsız bir decorator fonksiyonu
        def wrapper(*args, **kwargs):
            print("[AUTH] Yetki kontrolü...")
            return func(*args, **kwargs)
        return wrapper

    def custom(self, func):
        # ❗ Bu method 'self' alıyor, yani sınıfa bağlı
        # ❗ O yüzden sadece bir örnek üzerinden kullanılabilir: @d.custom
        def wrapper(*args, **kwargs):
            print(f"[CUSTOM] {self.prefix} kullanıldı")
            return func(*args, **kwargs)
        return wrapper

# -----------------------------------------------
# ⚙️ Kullanım Örnekleri:
# -----------------------------------------------

d = Decorator("🔥")

@d  # ⬅️ Sınıfın __call__ metodu çağrılır
def func1():
    print("func1 çalıştı")

@Decorator.log  # ⬅️ static method, sınıf üzerinden direkt çağrılır
def func2():
    print("func2 çalıştı")

@Decorator.auth  # ⬅️ yine static method
def func3():
    print("func3 çalıştı")

@d.custom  # ⬅️ instance method, bu yüzden 'd' nesnesi üzerinden çağrılır
def func4():
    print("func4 çalıştı")

# -----------------------------------------------
# 🚀 Çalıştırma
# -----------------------------------------------

func1()
# 🔸 __call__ içindeki wrapper çalışır

func2()
# 🔸 log decorator çalışır

func3()
# 🔸 auth decorator çalışır

func4()
# 🔸 instance üzerinden erişilen custom decorator çalışır

# -----------------------------------------------
# 🧠 Sonuç ve Hatırlatmalar:
# -----------------------------------------------

# ✅ __call__ varsa sınıf doğrudan decorator gibi kullanılabilir
# ✅ static method varsa sınıf üstünden direkt decorator çağırılabilir
# ✅ instance method varsa sadece örnek (nesne) üstünden kullanılabilir

# 🧱 Bu yapı özellikle:
# - Ortak temalı decorator’ları gruplayıp modüler hale getirmek için
# - Web framework’lerde (route, middleware, vs)
# - Configurable decorator kütüphaneleri üretmek için çok uygundur



# -----------------------------------------------------
# 📘 KONU: @decorator.x Kullanımı (Sınıf ve Fonksiyon Düzeyi)
# -----------------------------------------------------

# Bu kullanımda decorator bir nesne (sınıf, örnek, modül vs.) olur.
# 'x' ise bu nesne üzerinde tanımlanmış bir decorator fonksiyonudur.

# ----------------------------------------
# 1️⃣ Sınıf içinde tanımlandığında:
# ----------------------------------------

# class Decorators:
#     @staticmethod
#     def x(func):
#         def wrapper(...):
#             ...
#         return wrapper

# Kullanım:
# @Decorators.x
# def f(): ...

# 🔍 ÇÖZÜMLEME:
# - Python, önce Decorators.x ifadesini çözer.
# - Bu, aslında sınıf üzerinde bir attribute erişimidir:
#       Decorators.__getattribute__('x')
# - 'x' fonksiyonu @staticmethod olduğu için doğrudan döner.
# - Sonra decorator çağrısı yapılır:
#       f = x(f)
# - Böylece f, wrapper fonksiyonuyla süslenmiş olur.

# ----------------------------------------
# 2️⃣ Modül veya nesne içinde fonksiyonlar:
# ----------------------------------------

# class deco:
#     @staticmethod
#     def y(func):
#         def wrapper(...):
#             ...
#         return wrapper

# Kullanım:
# @deco.y
# def g(): ...

# 🔍 ÇÖZÜMLEME:
# - deco nesnesi üzerinden 'y' fonksiyonuna erişilir:
#       deco.__getattribute__('y')
# - y callable olduğu için doğrudan çalıştırılır:
#       g = y(g)
# - g artık süslenmiş haldedir.

# ----------------------------------------
# ✅ ORTAK SONUÇ:
# @decorator.x kullanımı, basit bir attribute erişimi + decorator çağrısıdır.
# Değişen hiçbir özel kural yoktur.
# Bu yapı sadece decorator fonksiyonlarını sınıf/modül içinde gruplamaya yarar.
# Hem okunabilirliği artırır hem modüler yapılar kurmaya izin verir.

# ----------------------------------------
# 🧠 TEMEL FORMÜL:
# @decorator.x
#   ↳ decorator.x → attribute (fonksiyon) erişimi (__getattribute__)
#   ↳ decorator.x(func) → gerçek decorator uygulaması
#   ↳ func = wrapper → fonksiyon sarılır ve süslenmiş olur


class Decorators:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.func = func
            print(f"[__call__] {self.prefix} - {self.func.__name__}")
            return self.func(*args, **kwargs)
        return wrapper
    @staticmethod
    def decorator1(func):
        def wrapper(*args, **kwargs):
            print(f"[decorator1] - {func.__name__}")
            return func(*args, **kwargs)
        return wrapper

    def decorator2(self, func): # instance method
        def wrapper(*args, **kwargs):
            print(f"[decorator2] - {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
d = Decorators("demir")  # burda decorator nesnesi oluşturduk ve "demir" -> prefix'i verdik

@ Decorators("demir") # a = Decorators("demir")(a) -> self.__call__(a)
def a(*args, **kwargs):
    ...

@Decorators.decorator1
def b(*args, **kwargs):
    ...

@d.decorator2
def c(*args, **kwargs):
    ...


a()
b()
c()


def deneme(*args, **kwargs):
    ...


deneme = type(Decorators).__dict__["__call__"].__get__(Decorators,type(Decorators)).__call__("demir")

deneme = Decorators.__dict__["decorator1"].__get__(Decorators,type(Decorators)).__call__(deneme)

d = Decorators.__new__(Decorators)
d.__init__(deneme) ; print(d)
