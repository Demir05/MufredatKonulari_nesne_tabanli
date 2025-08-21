# ================================================================================
# 📦 PYTHON'DA MODÜLLER, MODULETYPE VE SYS.MODULES – DERİNLEME YORUMLU AÇIKLAMA
# ================================================================================

# Python modülleri, programın yapı taşlarını oluşturur. Aşağıda, modüllerin
# yapısını, modül türünü (ModuleType), dinamik modül yaratmayı ve modül önbelleğini
# kontrol eden sys.modules sistemini baştan sona detaylıca ele alıyoruz.

# ================================================================================

# 1️⃣ MODÜL NEDİR?
# ------------------------------------------------------------------------------
# - Bir Python modülü, .py uzantılı bir dosyadır.
# - Fonksiyonlar, değişkenler, sınıflar ve başka modüller içerebilir.
# - Python'da `import` edilen her dosya ya da kaynak aslında bir "modül nesnesidir".

# Örnek:
#   math.py, utils.py, os (builtin) → Bunların hepsi birer modüldür.

# Bir modül import edildiğinde, arka planda Python onu RAM'e bir nesne olarak yükler.
# Bu nesneye biz "modül nesnesi" (module object) deriz ve bu nesne `ModuleType` sınıfına aittir.

# ================================================================================
# 2️⃣ MODULETYPE NEDİR?
# ------------------------------------------------------------------------------

# `ModuleType`, Python'daki tüm modül nesnelerinin sınıfıdır.
# Modülün kendisi bir `ModuleType` örneğidir.

# Nereden gelir?
#   from types import ModuleType

# Kullanımı:
#   import math
#   isinstance(math, ModuleType)  # True

# `ModuleType`, modülün bellekte nasıl temsil edileceğini tanımlar.
# Bu sınıf aslında CPython'da C ile yazılmıştır ama Python’dan erişilebilir durumdadır.

# Tüm modüller (örneğin math, os, senin yazdığın custom modül) bellekte bir ModuleType nesnesidir.

# ================================================================================
# 3️⃣ MODÜL NESNESİ NEDİR?
# ------------------------------------------------------------------------------

# Modül nesnesi, Python'da yüklü olan her modülün arkasındaki gerçek objedir.
# Modül nesnesi = bir isim alanı (namespace) gibi davranır.

# İçerdiği özel nitelikler:
# - __name__  → modülün adı
# - __file__  → dosya yolu (her zaman olmayabilir)
# - __doc__   → açıklama metni
# - __dict__  → modülde tanımlı tüm öğelerin saklandığı sözlük
# - __package__, __loader__, __spec__ vb.

# Örnek:
#   import os
#   print(os.__dict__.keys()) → modül içindeki tüm fonksiyonlar, sınıflar, sabitler

# Modül nesnesi, dinamik olarak özellik alabilir, değiştirilebilir ve okunabilir.

# ================================================================================
# 4️⃣ MODULETYPE KULLANARAK MODÜL OLUŞTURMA
# ------------------------------------------------------------------------------

# Python'da normalde modüller `import` ile yüklenir. Ama istersen program içinde
# manuel olarak da modül yaratabilirsin. Bunun için `ModuleType` sınıfını kullanırız.

# Örnek:
# ------------------------------------------------------------------------------
# from types import ModuleType
# my_mod = ModuleType("custom")
# my_mod.say_hi = lambda: "Hello!"
# print(my_mod.say_hi())  # Hello!
# ------------------------------------------------------------------------------

# Bu sayede dinamik olarak modül oluşturulabilir:
# - Plugin sistemlerinde
# - Mocking (test için sahte modül)
# - Sandbox/REPL/GUI eğitim sistemleri

# Bu modül nesnesi __name__ gibi niteliklere sahiptir ama diske yazılmış bir dosyası olmayabilir.
# İstenirse `sys.modules` içine eklenerek, gerçek bir modül gibi `import` edilebilir.

# ================================================================================
# 5️⃣ ELLE OLUŞTURULMUŞ MODÜLÜN DERİN ANALİZİ
# ------------------------------------------------------------------------------

# (1) Davranışı:
#   - Normal modül gibi davranır
#   - hasattr, dir, isinstance gibi işlemler tamamen geçerlidir
#   - `type(m)` → <class 'module'>

# (2) Performansı:
#   - Diskten yüklenmediği için ilk başta daha hızlı olabilir
#   - İçeriği sen manuel tanımlarsın → bu hem esneklik hem zahmet anlamına gelir

# (3) Attribute (özellik) kontrolü:
#   - m.hello = ...    → özellik ekleme
#   - getattr(m, "x")  → dinamik okuma
#   - setattr(m, "x", 5) → dinamik yazma
#   - del m.y          → özellik silme
#   - m.__dict__       → modülün tüm içeriği dict olarak

# (4) Diğer:
#   - sys.modules içine eklenebilir
#   - import ile çağrılabilir
#   - reload yapılabilir
#   - runtime içeriği değiştirebilir

# ================================================================================
# 6️⃣ SYS.MODULES NEDİR? NASIL ÇALIŞIR?
# ------------------------------------------------------------------------------

# `sys.modules`, Python'daki tüm yüklenmiş modüllerin kayıt altına alındığı sözlüktür.
# Her modül import edildiğinde, Python onu RAM'e yükler ve `sys.modules` içine koyar.

# Örnek:
#   import sys, math
#   print(sys.modules["math"])  # math modül nesnesi
#   print("math" in sys.modules)  # True

# Python `import` işleminde şu mantığı izler:
#   1. sys.modules içinde adı arar
#   2. Varsa, doğrudan onu kullanır
#   3. Yoksa, diske gider, dosyayı yükler, nesne oluşturur, sys.modules içine ekler

# (1) Davranışı:
#   - Bir tür önbellek (cache)
#   - Python çalışma zamanında (runtime) kullanılır
#   - import performansını artırır (aynı modül tekrar yüklenmez)

# (2) Performans:
#   - Disk erişimi yerine bellekteki nesne kullanılır → hızlıdır
#   - Sadece bir defa dosya okunur

# (3) Attribute kontrolü:
#   - sys.modules["modul_adı"] = yeni_modül → modülü değiştirme/mocklama
#   - del sys.modules["modul_adı"] → modülü sistemden silme
#   - importlib.reload(sys.modules["modul_adı"]) → yeniden yükleme

# (4) Diğer:
#   - Takip edilebilir: öncesi-sonrası karşılaştırması ile loglanabilir
#   - Dinamik analiz araçları yazılabilir
#   - Custom import sistemleri (Finder, Loader) buradan yürütülür

# ================================================================================
# 🔚 ÖZET
# ------------------------------------------------------------------------------

# ✅ Her modül bir `ModuleType` örneğidir
# ✅ `ModuleType` ile elle modül oluşturulabilir
# ✅ Bu modül RAM'de çalışır ve sys.modules içine konulursa `import` ile çağrılabilir
# ✅ `sys.modules`, import sisteminin cache tablosudur ve çok önemlidir
# ✅ Plugin, mocking, eğitim, test gibi senaryolarda bu sistemler ileri seviye kontrol sağlar

# ================================================================================


# ================================================================================
# 🧪 MODÜLLER, MODULETYPE ve SYS.MODULES – BASİT ÖRNEKLER
# ================================================================================
# Aşağıda, az önce öğrendiğin teorik bilgilerin pratikteki karşılığını göreceksin.
# Basit ve anlaşılır örneklerle modül nesnesi oluşturmayı ve sys.modules ile kullanmayı öğreneceksin.

# ================================================================================
# 📦 ÖRNEK 1 – Basit bir modül oluştur ve bir özellik ata
# ================================================================================

from types import ModuleType

# Yeni bir modül nesnesi oluşturuyoruz
my_module = ModuleType("my_first_module")

# İçine basit bir fonksiyon ekliyoruz
my_module.say_hello = lambda: "Hello from my custom module!"

# Fonksiyonu çağırıyoruz
print(my_module.say_hello())  # Çıktı: Hello from my custom module!

# ================================================================================
# 📦 ÖRNEK 2 – Modülü sys.modules'a ekle ve import ile eriş
# ================================================================================

import sys

# Elle oluşturduğumuz modül nesnesini sys.modules'a ekliyoruz
sys.modules["greeting_mod"] = my_module

# Artık bu modülü import ile çağırabiliriz
import greeting_mod

print(greeting_mod.say_hello())  # Çıktı: Hello from my custom module!

# ================================================================================
# 📦 ÖRNEK 3 – Modül içeriğini kontrol et (dict ile)
# ================================================================================

# Modülün içeriğini sözlük olarak görebiliriz
print(greeting_mod.__dict__.keys())
# Çıktı: dict_keys(['__name__', 'say_hello'])

# Yeni bir özellik daha ekleyelim
greeting_mod.version = "1.0"

print(greeting_mod.version)  # Çıktı: 1.0

# ================================================================================
# 📦 ÖRNEK 4 – sys.modules’tan modülü sil ve tekrar import et
# ================================================================================

del sys.modules["greeting_mod"]

# import greeting_mod  # HATA: ModuleNotFoundError verir çünkü artık yok

# ================================================================================
# 📦 ÖRNEK 5 – Yeni bir modül oluştur ve REPL benzeri davranış test et
# ================================================================================

sandbox = ModuleType("sandbox")
sandbox.result = eval("5 + 7")  # Kendi context'inde bir işlem

print(sandbox.result)  # Çıktı: 12

# İçine fonksiyon tanımlayabiliriz
sandbox.square = lambda x: x * x

print(sandbox.square(4))  # Çıktı: 16

# ================================================================================
# 📦 ÖRNEK 6 – sys.modules ile import edilenleri takip et
# ================================================================================

before = set(sys.modules.keys())

import math  # Yeni modül yüklendiğinde sys.modules değişir

after = set(sys.modules.keys())
new_imports = after - before

print(new_imports)  # Çıktı: {'math'} gibi

# ================================================================================
