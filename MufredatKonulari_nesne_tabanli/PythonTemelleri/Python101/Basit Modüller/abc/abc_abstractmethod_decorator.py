# ================================================================
# 📘 PYTHON: @abstractmethod NEDİR? NEDEN KULLANILIR? NASIL ÇALIŞIR?
# ================================================================

# 🔧 TANIM
# ---------------
# @abstractmethod → Python'da bir methodun "zorunlu olarak override edilmesi" gerektiğini belirtir.
# Bu methodun **alt sınıflarda mutlaka tanımlanması** beklenir.

# 🧱 Nereden gelir?
#   from abc import abstractmethod

# Bu decorator, sadece `abc.ABC` sınıfından türeyen sınıflar içinde kullanılabilir.
# Çünkü `abstractmethod` tek başına bir işe yaramaz, onun çalışması için ABC yapısına ihtiyacı vardır.

# =======================================================================
# 🔍 Neden @abstractmethod sadece ABC sınıfından türeyenlerde işe yarar?
# =======================================================================

# 🔧 @abstractmethod, methoda özel bir işaret koyar:
#    method.__isabstractmethod__ = True
#
# 🧠 Ancak bu işareti görecek olan sistem, Python’un özel metaclass’ı olan:
#    ➤ ABCMeta'dır (ABC sınıfının arkasındaki yapı)
#
# ✅ Eğer sınıf ABCMeta (yani ABC) kullanıyorsa:
#    - Sınıf tanımlanırken __abstractmethods__ isimli bir set oluşturulur
#    - Bu sette @abstractmethod ile işaretlenen methodlar listelenir
#    - Bu set boş değilse → sınıfın örneği oluşturulamaz → TypeError
#
# ❌ Eğer sınıf ABC değilse (yani ABCMeta kullanılmıyorsa):
#    - @abstractmethod sadece bir süs gibi durur
#    - Python bu işareti dikkate almaz
#    - Sınıf örneklenebilir, method tanımlanmasa da hata alınmaz
#
# 🎯 Bu nedenle: @abstractmethod tek başına hiçbir kontrol sağlamaz!
#    Kontrol mekanizması sadece ABCMeta içindedir.

# =======================================================================
# ✅ Sonuç:
#   - @abstractmethod = "Bu methodu alt sınıf yazmalı" işareti
#   - ABCMeta      = Bu işareti ciddiye alıp kontrol eden yapı
# =======================================================================


# ---------------------------------------------------------------
# 🎯 AMACI
# ---------------------------------------------------------------
# • Alt sınıfların belirli methodları **kesinlikle uygulamasını** sağlamak
# • Soyut sınıfın eksik tanımlı olduğunu göstermek
# • O sınıfın **örneklenmesini engellemek**

# ---------------------------------------------------------------
# 📛 EĞER KULLANILMAZSA NE OLUR?
# ---------------------------------------------------------------
# • Alt sınıflar o methodu tanımlamasa da hata alınmaz
# • Taban sınıfın örneklenmesine izin verilir
# • "Yarısı eksik sınıflar" çalışma anında fark edilmez — bu da hatalara neden olabilir

# ---------------------------------------------------------------
# 🔐 EĞER KULLANILIRSA:
# ---------------------------------------------------------------
# • En az bir @abstractmethod varsa:
#   1. Taban sınıf artık örneklenemez → TypeError
#   2. Alt sınıf, bu methodları tanımlamak zorundadır
#   3. Aksi halde o alt sınıf da örneklenemez

# ---------------------------------------------------------------
# 📌 ÖRNEK
# ---------------------------------------------------------------

# from abc import ABC, abstractmethod

# class Shape(ABC):
#     @abstractmethod
#     def area(self):
#         pass

# class Circle(Shape):
#     def area(self):
#         return 3.14 * 5 ** 2

# s = Shape()     ❌ HATA: abstractmethod tanımlı → örneklenemez
# c = Circle()    ✅ area() tanımlı → örneklenebilir

# ---------------------------------------------------------------
# 💡 ÖNEMLİ DETAY
# ---------------------------------------------------------------
# @abstractmethod sadece class methodu değil, staticmethod veya property ile de birlikte kullanılabilir:
#
# @abstractmethod
# @classmethod
# def foo(cls): ...
#
# @abstractmethod
# @property
# def bar(self): ...
#
# Bu sayede soyut property veya soyut class method da tanımlayabilirsin.

# ================================================================
# 🧠 SONUÇ:
#   - abstractmethod = methodu zorunlu kılar
#   - ABC = bu yapıyı destekler
#   - Birlikte kullanıldığında, Python'da "interface benzeri" yapı elde edilir
# ================================================================


from abc import ABC, abstractmethod

# 🔧 Bu sınıf soyut bir taban sınıf (ABC → Abstract Base Class)
class BaseMessage(ABC):

    # ----------------------------------------
    # 🧱 Bu method soyuttur — gövdesi yok
    #    Bu methodu kullanan alt sınıf, bunu override ETMEK ZORUNDA
    # ----------------------------------------
    @abstractmethod
    def send(self, recipient, message):
        pass

    # Bu soyut methodun amacı bir “sözleşme” oluşturmak:
    # “Eğer bu sınıftan türeyen biri varsa, send metodunu kesinlikle yazmalı.”

# ----------------------------------------
# ✅ Geçerli Alt Sınıf: Gerekli method tanımlandı
# ----------------------------------------
class EmailMessage(BaseMessage):
    def send(self, recipient, message):
        print(f"[Email to {recipient}]: {message}")

# ----------------------------------------
# ❌ Geçersiz Alt Sınıf: send() tanımlanmadı
# ----------------------------------------
class BrokenMessage(BaseMessage):
    pass

# ----------------------------------------
# ✅ Bu örnek çalışır
email = EmailMessage()
email.send("user@example.com", "Merhaba!")

# ❌ Bu örnek hata verir
# çünkü send() override edilmedi
# TypeError: Can't instantiate abstract class BrokenMessage with abstract method send
# broken = BrokenMessage()


class Car(ABC):
    @abstractmethod
    def car(self):
        pass

    def __str__(self):
        return f"Car: {self.car()}"



class BMWCar(Car):
    def car(self):
        return f"Bmw!"


araba = BMWCar()
print(araba.car())
print(araba)

try:
    c = Car()
# Car sınıfında @abstractmethod tanımlı olduğu için **taban sınıf** soyutlanamaz
except Exception as e:
    print(e) # Can't instantiate abstract class Car with abstract method car


class A:

    @abstractmethod
    def t(self):
        pass

class SubA(A):
    pass


a1 =A()
a2 = SubA()

"""
Burda A sınıfı,ABC sınıfından miras almadığı için @abstractmethod'un süsten farkı kalmaz 
python bu işateti,yorumlamaz..
çünkü abstractmethod ABC ile kullanıldığı zaman  sadece ABC sınıfının metaclass'ı olduğu ABCMeta tarafından
yorumlanabilen bir metoda işaret koyar bu işaret ABCmeta metaclass'I içinde bir küme(set) yapısında tutulur 
ve eğer bu küme boş değilse taban sınıfın örneği oluşturulamaz aynı şekilde alt sınıflarda da belirtilen metod,
override edilmezse o sınıfın'da örneği oluşturulamaz sonuç olarak @abstractmeethod, tek başına hiçbir kontrol sağlamaz
asıl kontrol mekanizması ABCmeta'nın içindedir 
"""