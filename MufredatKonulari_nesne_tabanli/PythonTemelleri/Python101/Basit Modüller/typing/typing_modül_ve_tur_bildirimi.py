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
# Mesela bir fonksiyon hem str, hem int alabilsin ama ne aldıysa onu döndürsün
T = TypeVar("T")  # Genellikle tek harf kullanılır: T, K, V, S

def get_first(sequence: Sequence[T]) -> T:
    return sequence[0]

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
