# ====================================================
# 🧾 PYTHON'DA __firstlineno__ ATTRIBUTE — AÇIKLAMA
# ====================================================

# ✅ __firstlineno__ nedir?
# ----------------------------
# - Bir sınıf veya fonksiyonun **tanımının başladığı satır numarasını** belirtir.
# - Bu attribute, **CPython derleyicisi** tarafından sınıf/fonksiyon oluşturulurken otomatik eklenir.
# - Değeri bir sayı (int) olup, kaynak kod dosyasındaki satır numarasını yansıtır.

# ✅ Nerede bulunur?
# ----------------------------
# - `__code__` attribute'u olan nesnelerde (fonksiyonlar gibi) `co_firstlineno` olarak bulunur.
# - Sınıf nesnelerinde doğrudan `__firstlineno__` olarak saklanabilir (örneğin bazı introspection araçlarında).

# ✅ Ne işe yarar?
# ----------------------------
# - Geliştirici araçları (IDE, debugger, profiler) bu attribute'u kullanarak
#   ilgili yapının kaynak dosyadaki konumunu tespit eder.
# - Özellikle büyük projelerde hata ayıklama (debug) ve dökümantasyon üretiminde kullanılır.

# ✅ Gerçek dünyada ne zaman önemlidir?
# ----------------------------
# - Kod analiz araçları (`inspect`, `ast`, `pdb`, `traceback`, `coverage`)
#   ilgili kodun **nerede tanımlandığını** öğrenmek için bu attribute'u kullanır.
# - Ayrıca test ve hata raporlama sistemleri için önemlidir.

# 🔹 Fonksiyon örneği:
def test_function():
    return 42

print(test_function.__code__.co_firstlineno)
# ➜ Bu fonksiyonun hangi satırda başladığını gösterir.

# 🔹 Sınıf için:
import inspect

class Sample:
    def method(self): pass

print(inspect.getsourcelines(Sample)[1])
# ➜ Bu da sınıfın başladığı satır numarasını verir (benzer bilgi).

# ✅ Sınıflarda doğrudan __firstlineno__:
# ----------------------------------------
# - Bazı meta-programlama durumlarında metaclass,
#   sınıfın başlangıç satırını özel olarak `__firstlineno__` olarak saklayabilir.
# - Bu zorunlu bir Python standardı değildir ama bazı framework'ler böyle yapar.

# 🔍 Örnek (manuel atama):
class MyMeta(type):
    def __new__(cls, name, bases, dct):
        import inspect
        frame = inspect.currentframe().f_back
        dct['__firstlineno__'] = frame.f_lineno
        return super().__new__(cls, name, bases, dct)

class Demo(metaclass=MyMeta):
    pass

print(Demo.__firstlineno__)  # ➜ Demo sınıfının tanımının başladığı satır
