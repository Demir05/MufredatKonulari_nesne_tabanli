# ------------------------------------------------------------------------------
# 📦 Python `typing` modülü — Tür Bildirimi İçin Temel Araç
# ------------------------------------------------------------------------------

# 🚨 Python dinamik bir dildir, yani değişkenlerin türü çalışma zamanında belirlenir.
# Bu esneklik büyük avantajlar sağlasa da, büyük projelerde karmaşıklığa neden olabilir.

# ✅ İşte bu yüzden `typing` modülü ortaya çıktı:
# 1. Kodun okunabilirliğini ve bakımını artırmak
# 2. IDE'lerin otomatik tamamlama ve hata uyarılarını geliştirmek
# 3. mypy gibi araçlarla statik analiz (run etmeden hata kontrolü) yapmak

# ------------------------------------------------------------------------------
# 🔑 `typing` modülündeki Temel Tipler ve Kullanım Amacı
# ------------------------------------------------------------------------------

from typing import (
    Any, Union, Optional,
    List, Tuple, Dict, Set,
    Iterable, Sequence, Mapping,
    Callable, TypeVar, Generic
)

# 🧠 `Any` → Her türü kabul eder. Tip güvenliği sağlamaz. Kaçınılmalı.
# Kullanıcıdan gelebilecek "ne olacağı belli olmayan" veri için kullanılır.
def identity(x: Any) -> Any:
    return x

# 🧠 `Union` → Birden fazla türden biri olabilir.
# `Optional[X]` aslında `Union[X, None]`'dır.
def notify(user: Union[str, int]) -> None:
    print(user)

def notify_safe(user: Optional[str]) -> None:
    print(user or "Anonim")

# 🧠 `List`, `Tuple`, `Dict`, `Set`
# Liste, sözlük gibi yapılar için içeriğin türü tanımlanır.
def squares(nums: List[int]) -> List[int]:
    return [x**2 for x in nums]

# 🧠 `Iterable`, `Sequence`, `Mapping`
# Iterable → Üzerinde döngü yapılabilir
# Sequence → Sıralı ve indekslenebilir (list, tuple)
# Mapping → Genelde dict gibi key-value yapılar, ama sadece okuma garantilenir
def first_item(seq: Sequence[str]) -> str:
    return seq[0]

def print_config(cfg: Mapping[str, int]):
    for key, value in cfg.items():
        print(f"{key} = {value}")

# ------------------------------------------------------------------------------
# 🔧 Fonksiyonların Tipini Tanımlamak → Callable
# ------------------------------------------------------------------------------
# `Callable[[arg1_type, arg2_type], return_type]`
# Dinamik olarak başka bir fonksiyonu parametre olarak alan yapılar
def apply(fn: Callable[[int, int], int], a: int, b: int) -> int:
    return fn(a, b)

# ------------------------------------------------------------------------------
# 🧬 TypeVar → Generic Türler
# ------------------------------------------------------------------------------
# Fonksiyon ya da sınıfın türünü esnek ama tutarlı tanımlamak için kullanılır.

# Genel Söz Dizimi:
# T = TypeVar(name, *constraints, bound=None, covariant=False, contravariant=False)

# 🔹 name: TypeVar için bir etiket. Genelde "T", "K", "V" gibi kısa harfler tercih edilir.
# 🔹 *constraints: (İ steğe bağlı) — Bu TypeVar sadece belirtilen türler ile kullanılabilir.
# 🔹 bound: (İsteğe bağlı) — TypeVar, belirli bir sınıfın alt sınıfı olmak zorundadır.
# 🔹 covariant / contravariant: (İleri düzey kullanım, genelde Generic sınıflarda kullanılır.)

# Mesela bir fonksiyon hem str, hem int alabilsin ama ne aldıysa onu döndürsün
T = TypeVar("T")  # Genellikle tek harf kullanılır: T, K, V, S

def get_first(sequence: Sequence[T]) -> T:
    return sequence[0]

# T sadece str VEYA bytes olabilir
T = TypeVar("T", str, bytes)

# Kullanım: Bir fonksiyon hem str hem bytes alabilir ama başka bir şey OLMAMALI
def echo(value: T) -> T:
    return value

echo("selam")  # ✅ OK
echo(b"merhaba")  # ✅ OK
# echo(42) ❌ mypy uyarır çünkü int yok

# T, sadece str sınıfına veya onun alt sınıfına bağlıdır
T = TypeVar("T", bound=str)

# covariant=True: Alt sınıfı, üst sınıfa atanabilir
# contravariant=True: Üst sınıfı, alt sınıfa atanabilir
# Bunlar genelde sadece Generic class yapılarında faydalıdır

T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


def upper_text(x: T) -> T:
    return x.upper()

# upper_text(123) ❌ int → str ile ilişkili değil
# upper_text("merhaba") ✅ OK



# echo(123)       ❌ Hatalı: int, A'nın izin verdiği türlerden biri değil
# echo("merhaba") ✅ Geçerli
# echo(b"merhaba") ✅ Geçerli

# 🔍 Bu kullanım genellikle sınırlı türdeki tipleri kabul eden generic fonksiyonlar/sınıflar için uygundur.
# Örn: Sadece str veya bytes türünde çalışabilen dönüştürücüler, kodlayıcılar vs.


# ✅ Generic nedir?
# Generic, `typing` modülünde bulunan soyut bir sınıftır.
# Amacı, generic yani tür parametreli (type-parameterized) sınıflar tanımlamamızı sağlamaktır.
# Bu sayede, sınıfımızı farklı veri türleriyle kullanabileceğimizi belirtiriz.

# Örnek: Box sınıfı
T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

# 🔽 Artık şu kullanımı yapabiliriz:
box_str = Box[str]("Merhaba")  # T burada str olarak belirlenmiş olur
box_int = Box          # T burada int olarak belirlenmiş olur

# ⛓️ Bu nasıl mümkün oluyor?
# Çünkü Generic sınıfı, `__class_getitem__` adında özel bir metot içerir.
# Bu metodun amacı `Box[str]` gibi `Box` sınıfına yapılan index ([]) işlemlerini yakalayıp işleyebilmektir.
# Normal sınıflarda bu olmaz çünkü bu sınıflar `__class_getitem__` metoduna sahip değildir.
# `Generic` sınıfından miras alınca bu metod sınıfa dahil olur.

# 💡 Detay: __class_getitem__ metodu ne yapıyor?
# `Box[str]` çağrıldığında, `Box` sınıfı `Generic`'den türediği için,
# `Box.__class_getitem__(str)` metodu çağrılır ve tip parametresi olarak `str` atanır.
# Bu sayede, mypy gibi statik tip denetleyicileri bu sınıfın hangi türle kullanıldığını anlayabilir.

# 🚫 Eğer Generic'ten miras almazsak:
# Aşağıdaki gibi yazarsak:
class NotGeneric:
    pass

# Şunu yapmaya çalışırsak:
# NotGeneric[int]  ❌ HATA verir çünkü sınıf indexlenemez (not subscriptable)

# 🧠 Yani, `Generic[T]` kullanımı, sınıfı türle parametrik hale getirir.
# Bu sadece tip kontrolü içindir — runtime'da etkisi yoktur (yani kodun çalışma şeklini değiştirmez).
# Ancak `mypy`, `pyright` gibi analiz araçları için çok faydalıdır.

# 📝 Kural: Her zaman Generic[T] türetirken, T bir TypeVar olmalı.
# Ayrıca Box[str] gibi kullanımlar `Generic`'in sağladığı `__class_getitem__` sayesinde olur.


# ------------------------------------------------------------------------------
# 🧱 Generic Sınıflar
# ------------------------------------------------------------------------------
# Sınıfın türünü parametreleştirmek için `Generic[T]` kalıtımı yapılır
class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

# Kullanım
int_box = Box
str_box = Box[str]("Merhaba")

# ------------------------------------------------------------------------------
# 🛠 Class Tanımlarında Tür Bildirimi
# ------------------------------------------------------------------------------
# Python'da sınıf tanımında sadece kalıtım belirtilir, tür bildirimi değil!
# Ancak sınıf içinde __init__ ve property'lerde typing çok önemlidir

class Product:
    name: str  # Bu bir tip ipucudur, init'e zorunlu değildir
    price: float

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

# ------------------------------------------------------------------------------
# 📊 mypy — Python Statik Tip Denetleyici
# ------------------------------------------------------------------------------
# Python yorumlayıcısı bu tipleri zorunlu kılmaz!
# Ama `mypy` gibi araçlar ile kontrol edilebilir:
# Terminalden çalıştır: `mypy my_script.py`

# Hatalar, eksik dönüşler, yanlış parametreler erken fark edilir
# Modern IDE'ler (VSCode, PyCharm) da `typing` ile daha verimli çalışır


def a(data:Any)-> None:
    print(data)


# ----------------------------------------------------
# 🧩 Kendi Generic Alias Yapımızı Oluşturma
# ----------------------------------------------------
#
# Amaç: Box[int], Box[str] gibi typeların
# kullanıcı tanımlı sınıflar için de çalışmasını sağlamak.

class GenericAlias:
    """
    • origin: asıl sınıf (Box)
    • args: tip argümanları (örn: (int,))
    """
    def __init__(self, origin, args):
        self.__origin__ = origin
        self.__args__ = args

    def __call__(self, *args, **kwargs):
        # alias ile çağrılsan bile asıl sınıf örneklenir
        return self.__origin__(*args, **kwargs)

    def __repr__(self):
        args = ", ".join(a.__name__ for a in self.__args__)
        return f"{self.__origin__.__name__}[{args}]"

# ----------------------------------------------------
# 🛠️ __class_getitem__ ile sınıfı subscriptable yapma
# ----------------------------------------------------

class MyGeneric:
    """
    Bu sınıfın üzerine [Type] yazıldığında,
    GenericAlias üretir.
    """
    def __class_getitem__(cls, item):
        print(cls)
        # item tek tip veya tuple olabilir
        if not isinstance(item, tuple):
            item = (item,)
        return GenericAlias(cls, item)

# ----------------------------------------------------
# 🧪 Örnek bir generic sınıf
# ----------------------------------------------------
class Box(MyGeneric):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Box({self.value!r})"

# ----------------------------------------------------
# ✅ Deneyelim
# ----------------------------------------------------
B_int = Box[int]              # alias yaratıldı
print(B_int)                  # → "Box[int]"

b = B_int("merhaba")
print(b, type(b))            # → Box('merhaba') <class '__main__.Box'>

b2 = Box[int]("test2")
print(isinstance(b2, Box))   # → True
print(isinstance(Box[int], GenericAlias))  # → True

# ----------------------------------------------------
# 🎯 Özet
# ----------------------------------------------------
# • generic sistemini MyGeneric + GenericAlias ile taklit ettik.
# • Box[int] ile çağrı yapıldığında GenericAlias nesnesi döner.
# • Bu alias, çağrıldığında Box sınıfının orijinal __init__ fonksiyonunu kullanır.
# • Böylece T türü gerçekten tutuluyor ve mypy gibi araçlar da bunu yorumlayabilir.


from typing import TypeVar, Generic

# ================================================================
# 1. COVARIANT — Alt sınıf, üst sınıf yerine kullanılabilir
# ================================================================

# 1. adım: Tip değişkeni tanımla — covariant=True
T1 = TypeVar("T1", covariant=True)

# 2. adım: Bu T1'i kullanan generic sınıf oluştur
class Superclass(Generic[T1]):
    def __init__(self, value: T1) -> None:
        self.value = value

# 3. adım: Üst ve alt sınıf oluştur
class Animal:
    pass

class Dog(Animal):
    pass

# 4. adım: Superclass[Dog] türünde bir değişkene Superclass[Animal] ata
animal: Superclass[Dog] = Superclass[Animal](Animal())

# ✅ Bu çalışır çünkü:
# T1 covariant → Alt sınıf (Dog), Üst sınıfın (Animal) yerine geçebilir


# ================================================================
# 2. CONTRAVARIANT — Üst sınıf, alt sınıf yerine kullanılabilir
# ================================================================

# 1. adım: Tip değişkeni tanımla — contravariant=True
T2 = TypeVar("T2", contravariant=True)

# 2. adım: Bu T2'yi kullanan generic sınıf oluştur
class Consumer(Generic[T2]):
    def consume(self, value: T2) -> None:
        print(f"Tüketiliyor: {value}")

# 3. adım: Consumer[Dog] türünde bir değişkene Consumer[Animal] ata
animal_consumer: Consumer[Dog] = Consumer[Animal]()

# 4. adım: Dog nesnesi gönder
animal_consumer.consume(Dog())

# ✅ Bu çalışır çünkü:
# T2 contravariant → Üst sınıf (Animal), Alt sınıfın (Dog) yerine geçebilir
# Veri içeri alınırken (parametre olarak), genel olanı kabul etmek güvenlidir


# ================================================================
# ÖZET
# ================================================================

# Covariant → Veri döndürüyorsan (getter) → Alt sınıf kabul edilir
# Contravariant → Veri alıyorsan (setter) → Üst sınıf kabul edilir

# Sadece okuma → covariant
# Sadece yazma → contravariant

# Kullanım alanları genelde API tasarımı, frameworkler, soyutlama ve tür güvencesi içindir
