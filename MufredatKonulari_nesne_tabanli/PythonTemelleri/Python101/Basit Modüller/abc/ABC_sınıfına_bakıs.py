# ================================================================
# 📘 PYTHON: Soyut Sınıflar (ABC), @abstractmethod ve ABC Türemleri
# ================================================================

from abc import ABC
# 🧠 TEMEL KAVRAMLAR
# ------------------
# ▶️ ABC: Abstract Base Class
#   - Soyut sınıf anlamına gelir.
#   - Sınıfın doğrudan örneklenmemesi gerektiğini ve tamamlanması gereken bazı bölümler olduğunu ifade eder.
#   - abc.ABC sınıfı, Python'da soyut sınıf tanımlamak için kullanılır.

# ▶️ abstractmethod:
#   - Bir methodun sadece tanımının yapıldığını, **içeriğinin alt sınıf tarafından yazılmak zorunda** olduğunu belirtir.
#   - Bir sınıfta en az bir @abstractmethod varsa, o sınıf örneklenemez.

# ▶️ collections.abc:
#   - Python'da yaygın koleksiyon yapılarının (dict, list, set vs.) davranışlarını tanımlayan **hazır abstract base class**’ları içerir.
#   - `Iterable`, `Mapping`, `Sequence`, `MutableMapping` gibi arayüzler içerir.
#   - Bu soyut sınıflar bazı davranışları otomatik olarak sağlar ve eksik methodları yazmanı zorunlu kılar.

# ---------------------------------------------------------------
# 🎯 NEDEN KULLANILIR?
# ---------------------------------------------------------------
# - Kodun mimarisini netleştirmek (interface gibi davranır)
# - Alt sınıfların belli davranışları mutlaka tanımlamasını zorlamak
# - Büyük projelerde tutarlılığı artırmak
# - Polimorfik davranışı (farklı sınıfların aynı methodu farklı yorumlaması) garanti altına almak

# ---------------------------------------------------------------
# 🧱 abc.ABC KULLANIMI
# ---------------------------------------------------------------

# 1. ABC sınıfı tanımlanır:
#     from abc import ABC, abstractmethod
#
#     class MyBase(ABC):
#         @abstractmethod
#         def must_define(self):
#             pass
#
# 2. Alt sınıf tanımlar:
#     class Concrete(MyBase):
#         def must_define(self):
#             print("Implemented")

# Bu yapı sayesinde:
#   - `Concrete` örneklenebilir.
#   - `MyBase` örneklenemez.
#   - `must_define()` tanımlanmamışsa TypeError fırlatılır.

# ---------------------------------------------------------------
# 🧩 collections.abc ARAYÜZLERİ
# ---------------------------------------------------------------

# Örnek:
#     from collections.abc import MutableMapping
#
#     class MyDict(MutableMapping):
#         def __getitem__(self, key): ...
#         def __setitem__(self, key, value): ...
#         def __delitem__(self, key): ...
#         def __iter__(self): ...
#         def __len__(self): ...

# Bu durumda:
# - Python otomatik olarak bu sınıfın bir dict gibi davrandığını bilir
# - Eksik methodlar varsa TypeError oluşur

# ---------------------------------------------------------------
# 🎁 ÖZET
# ---------------------------------------------------------------
# ✅ abc.ABC → soyut sınıf altyapısını kurar
# ✅ @abstractmethod → alt sınıfların zorunlu olarak implement etmesi gereken methodları belirler
# ✅ collections.abc → hazır interface’ler sunar, genellikle koleksiyon tipleri için

# Bu yapılar, Python'da **sağlam, ölçeklenebilir ve güvenli** nesne yönelimli programlama yapmak için vazgeçilmezdir.


class Mylist(ABC):
    print("merhaba")
"""
Burda ABC'den miras alınmış ama bu sınf içersinde herangi bir soyutlama yapılmadığı için bu miras gereksizdir
bir sınıf,ABC'den miras alıyorsa amacı: soyutlama yapmak olmadıdır
"""

print(Mylist.__mro__) # (<class '__main__.Mylist'>, <class 'abc.ABC'>, <class 'object'>)
print(Mylist.__bases__) # (<class 'abc.ABC'>,)