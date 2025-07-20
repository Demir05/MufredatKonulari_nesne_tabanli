# =============================================================
# 📘 PYTHON SINIF TANIMI — METACLASS İLE OLUŞUM AŞAMALARI
# =============================================================

# 🔹 Python'da bir sınıf tanımlandığında, aşağıdaki adımlar sırayla çalışır.
# 🔹 Eğer metaclass kullanıyorsan, sınıf tanımı sırasında kontrol senin eline geçer!

# ÖRNEK:
class MyMeta(type):
    def __prepare__(name, bases):
        # 1️⃣ → (İsteğe bağlı) Sınıfın içeriğini tutacak sözlük döndürülür
        # Burada OrderedDict gibi özel yapılar döndürebilirsin
        print(f"1️⃣ __prepare__ → name={name}")
        return {}

    def __new__(mcs, name, bases, dct):
        # 3️⃣ → class body çalıştıktan sonra __new__ çağrılır
        # Yeni sınıf objesi bu metodla bellekte oluşturulur
        print(f"3️⃣ __new__ → name={name}")
        return super().__new__(mcs, name, bases, dct)

    def __init__(cls, name, bases, dct):
        # 4️⃣ → __new__ sonrasında, oluşturulan sınıf bu metodla başlatılır
        # Genelde attribute kontrolü, otomatik kayıt, validasyon burada yapılır
        print(f"4️⃣ __init__ → {name}")
        super().__init__(name, bases, dct)


class Base:
    def __init_subclass__(cls):
        # 5️⃣ → Tüm sınıf işlemleri bittikten sonra base sınıf bilgilendirilir
        # Yani bu sınıf, senden miras aldı demektir
        print(f"5️⃣ __init_subclass__ → {cls.__name__}")
        super().__init_subclass__()

# 2️⃣ → class body şu anda çalışıyor! (attr = 42 kodları işleniyor)
class MyClass(Base, metaclass=MyMeta):
    attr = 42
    def method(self):
        return self.attr

# =============================================================
# 🔄 SONUÇ:
# 🔹 Sıralı olarak çalışan aşamalar şunlardır:
#
#    1️⃣ __prepare__
#    2️⃣ class body (içerik çalışır, __dict__ doldurulur)
#    3️⃣ __new__        → class objesi oluşturulur
#    4️⃣ __init__       → class objesi başlatılır
#    5️⃣ __init_subclass__ → base class bilgilendirilir
# =============================================================

