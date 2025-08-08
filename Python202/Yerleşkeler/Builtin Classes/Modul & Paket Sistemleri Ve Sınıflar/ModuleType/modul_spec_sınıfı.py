# 🔎-----------------------------------------------------------
#           ModuleSpec Sınıfı & __spec__ İlişkisi
# 🔎-----------------------------------------------------------

# 📌 1. Nedir?
# ----------------------------------------------------------------
# `ModuleSpec`, Python 3.4+ sürümünden itibaren gelen `importlib`
# altyapısının bir parçası olan özel bir sınıftır.
# Amacı: Bir modülün nasıl ve nereden yükleneceğine dair tüm meta bilgileri taşımaktır.
# Bu sınıfın örneği her import işleminde otomatik olarak oluşturulur
# ve yüklenen modülün `__spec__` attribute'una atanır.


# 📦 2. Nereden gelir?
# ----------------------------------------------------------------
# `importlib.machinery` modülü içindedir:

from importlib.machinery import ModuleSpec

# Bu sınıf, modülün adını, yükleyicisini (loader), kaynağını (origin),
# cache yolunu, alt modül arama yollarını, vb. içerir.


# 🧠 3. Neden `__spec__` attribute'u ile ilişkilendirilmiş?
# ----------------------------------------------------------------
# Çünkü: Python’un yeni nesil import mekanizması (PEP 451) şunu yapar:
#
# - import edilirken modül nesnesi (ModuleType) oluşturulur
# - o modülün nasıl yüklendiğini tanımlayan `ModuleSpec` nesnesi oluşturulur
# - bu nesne doğrudan `modul.__spec__` içine atanır
#
# Böylece:
# - Yükleme bilgileri her zaman modül nesnesi içinde yer alır
# - Modül üzerinde debug, reload, yeniden çözümleme işlemleri kolaylaşır

# 🔁 Örnek:
import os
print(os.__spec__)

# Çıktı:
# ModuleSpec(name='os', loader=..., origin='.../os.py')

# ☑️ Bu bilgi import sisteminin kontrol, reload ve analiz süreçlerinde kullanılır.
# ☑️ Özellikle `importlib.reload()` fonksiyonu, `__spec__` üzerinden yeniden yüklemeyi yapar.


# 🧱 4. Hangi alanları içerir?
# ----------------------------------------------------------------
# name:                        Modülün tam adı (örnek: 'os.path')
# loader:                      Hangi loader ile yüklendiğini belirtir
# origin:                      Nereden geldiğini (disk yolu, built-in vs)
# submodule_search_locations:  Eğer paket ise → alt modül dizinleri
# parent:                      Eğer varsa, ait olduğu üst modül
# has_location:                Gerçek fiziksel yolu var mı
# cached:                      .pyc dosyasının yolu
# loader_state:                Loader’a özel geçici veri taşıma alanı


# 📌 5. Elle oluşturmak mümkün mü?
# ----------------------------------------------------------------
from types import ModuleType

m = ModuleType("demo")
m.__spec__ = ModuleSpec(name="demo", loader=None, origin="manual")
print(m.__spec__)

# Böylece elle oluşturduğun modül, import sistemine daha gerçekçi görünür.
# Bu özellik sandbox, custom loader, dynamic plugin sistemlerinde çok işe yarar.


# 🔐 6. Niye bu kadar önemli?
# ----------------------------------------------------------------
# Çünkü:
# - `__spec__`, modern import sisteminin *merkezi parçasıdır*
# - reload, finder, loader, dokümantasyon, IDE tooltip gibi araçlar bu attribute'u kontrol eder
# - Özellikle modülün nereden yüklendiğini anlamak için ideal yerdir


# ✅ 7. Özet
# ----------------------------------------------------------------
# - `ModuleSpec`, modülün nasıl yüklendiğini tanımlayan özel bir sınıftır
# - import sırasında otomatik oluşturulur ve `__spec__` içinde tutulur
# - Elle modül oluşturduğunda, `__spec__` yoktur (çünkü import zinciri çalışmaz)
# - `__spec__` varsa → modül daha analiz edilebilir, reload edilebilir, incelenebilir olur

# 💡 Bonus: Sphinx gibi dokümantasyon araçları da bu attribute'a bakabilir

# ---------------------------------------------------------------


# 📌 MODÜLSPEC KULLANARAK CUSTOM MODÜL OLUŞTURMA ve IMPORT EDİLEBİLİR HALE GETİRME

# ───────────────────────────────────────────────
# 1️⃣ Amaç:
# Bellekte özel bir modül nesnesi oluşturmak (ModuleType),
# ve bu modülün, normal bir modül gibi import edilebilmesini sağlamak

# ───────────────────────────────────────────────
# 2️⃣ Kullanım Nedeni:
# Eğer sadece ModuleType(name) ile sys.modules'e eklersen:
#  → çalışır, ama introspection, reload, debugging gibi
#    sistem araçları eksik bilgiyle çalışır

# Bunun yerine:
#  → importlib.machinery.ModuleSpec kullanarak
#     modülün kimliğini (name, loader, origin) tam şekilde belirlemiş olursun

# Bu sayede:
#  - importlib.reload() ile çalışır
#  - __spec__ bilgilerinden debugger, logger, IDE faydalanabilir
#  - modül, sanki bir dosyadan gelmiş gibi davranır

# ───────────────────────────────────────────────
# 3️⃣ Adım Adım Uygulama:

from types import ModuleType
from importlib.machinery import ModuleSpec
import sys

# A. modül adı
mod_name = "my_custom_plugin"

# B. modül nesnesi oluştur
mod = ModuleType(mod_name)

# C. modül bilgilerini içeren ModuleSpec oluştur
spec = ModuleSpec(
    name=mod_name,
    loader=None,           # manuel oluşturduğumuz için yükleyici yok
    origin="in-memory"     # fiziksel dosya değil; sadece tanımlayıcı bilgi
)

# D. __spec__, __loader__ gibi alanları modüle aktar
mod.__spec__ = spec
mod.__loader__ = spec.loader
mod.__package__ = ""       # üst paket bilgisi yok
mod.__file__ = None        # fiziksel dosya yok

# E. modül içeriğini doldur
exec("def hello(): print('Hello from custom module')", mod.__dict__)

# F. sys.modules'a kaydet
sys.modules[mod_name] = mod

# ───────────────────────────────────────────────
# 4️⃣ Artık modül gerçek gibi import edilebilir:

import my_custom_plugin
my_custom_plugin.hello()  # ➤ Hello from custom module

# ───────────────────────────────────────────────
# 5️⃣ Özet:
# - Modül = modül nesnesi (ModuleType)
# - Kimlik = yükleme bilgisi (ModuleSpec)
# - İlişkilendirme = mod.__spec__ ile
# - Kayıt = sys.modules[name] = mod

# Ve böylece:
# ➤ IDE, debugger, import mekanizması tam olarak bu modülü tanır
# ➤ reload(), inspect, doc gibi sistemler çalışır

# 🔥 Profesyonel, temiz ve gerçek bir modül davranışı elde edilir
