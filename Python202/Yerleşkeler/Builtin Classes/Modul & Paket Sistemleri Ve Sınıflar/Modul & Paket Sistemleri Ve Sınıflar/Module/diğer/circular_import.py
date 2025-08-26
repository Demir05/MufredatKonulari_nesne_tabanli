# ------------------------------------------------------
# 🔁 Circular Import (Dairesel İçe Aktarma) – Tanım ve Detaylı Açıklama
# ------------------------------------------------------

# ----------------------------------
# 📘 Tanım:
# ----------------------------------
# Circular import, iki veya daha fazla modülün birbirini doğrudan veya dolaylı olarak içe aktarmasıdır.
# Bu durum, Python'un modülleri satır satır çalıştırma doğası nedeniyle sorunlara yol açabilir.

# ----------------------------------
# 📌 Basit Örnek:
# ----------------------------------
# a.py:
#   from b import foo
#   def bar(): pass
#
# b.py:
#   from a import bar
#   def foo(): pass
#
# Bu yapı hataya yol açar çünkü:
# - a.py çalışmaya başlar → b.py'yi import eder
# - b.py çalışmaya başlar → tekrar a.py'yi import eder (ama henüz tam yüklenmemiştir)
# - a.py içinde tanımlı isimler (örn. bar) daha oluşturulmamıştır → AttributeError oluşabilir

# ----------------------------------
# 🔍 Neden Olur?
# ----------------------------------
# - Python modülleri, yüklenirken bir defalık çalıştırılır (module initialization).
# - `import` işlemi, modülü çalıştırır ve `sys.modules` içine ekler.
# - Ancak modül henüz tamamen çalışmadan başka bir modül tarafından çağrılırsa, eksik tanımlar oluşabilir.

# ----------------------------------
# 🔥 Belirtileri:
# ----------------------------------
# ❌ ImportError: cannot import name 'X' from partially initialized module 'Y'
# ❌ AttributeError: 'module' object has no attribute 'X'

# ----------------------------------
# 🛠️ Çözüm Stratejileri:
# ----------------------------------

# ✅ 1. Geç İçe Aktarma (Lazy Import):
# - `import` işlemini modülün en başında değil, ihtiyaç duyulduğu yerde yap.
# - Böylece modül tamamen yüklendikten sonra import çağrısı yapılır.

# ✅ 2. Fonksiyon İçi Import:
# - import işlemini fonksiyonun içinde tanımlayarak çalıştırmayı geciktir.
# - Bu yöntemle circular import çoğu zaman aşılabilir.

# ✅ 3. Ortak Modül Oluştur:
# - İki modülün de ihtiyaç duyduğu fonksiyonları ya da verileri ayrı bir ortak modüle taşı.
# - Her iki modül de bu ortak modülden import eder.

# ✅ 4. TYPE_CHECKING ile sadece tip kontrolü zamanında import et:
# - from typing import TYPE_CHECKING
# - if TYPE_CHECKING:
#       from other_module import SomeType

# ✅ 5. `importlib.import_module()` ile dinamik import:
# - Bu yöntem `__getattr__` ya da runtime bazlı işlemler için kullanılabilir.

# ----------------------------------
# 🔁 Kendi Kendini Besleyen Sistemlerde Durum:
# ----------------------------------

# Örneğin bir yapı, bir diğerinden konfigürasyon alırken,
# o da geri dönüp buna referans veriyorsa, bu iç içe geçiş ihtiyacı doğar.

# Bu gibi durumlarda:
# 🔹 Her iki modül, yalnızca ihtiyaç duyduğu interface'i bilmelidir.
# 🔹 Ortak veri paylaşımı bir ara katman üzerinden yapılmalıdır (örn. registry, config store).
# 🔹 Bu mantıksal bağ, fiziksel bağa (import'a) dönüştürülmemelidir.
# 🔹 Örneğin: settings.py gibi bağımlılık içermeyen bir merkezi yapı üzerinden veri akışı sağlanabilir.

# ----------------------------------
# 📌 Sonuç:
# ----------------------------------
# Python'da circular import ciddi bir yapısal sorundur.
# Ancak yazılım mimarisi düzgün planlanırsa ve modüller gevşek bağlanırsa (loose coupling),
# bu sorunlar çoğunlukla önlenebilir.

# Circular import, bir mimari uyarı niteliğindedir:
# → "Bu modüller birbirine fazla bağımlı hale geldi!"
# → Dolayısıyla çözüm, sadece teknik değil; tasarımsal düşünmeyi de gerektirir.

"""
🔁 Örnek 1 – Doğrudan Karşılıklı İçe Aktarma (En Temel Circular Import)

a.py

from b import func_b

def func_a():
    print("func_a çağrıldı")


b.py

from a import func_a

def func_b():
    print("func_b çağrıldı")


🧠 Sorun:
a.py, b.py'yi import eder → b.py, a.py'yi tekrar import eder → func_a henüz tanımlanmamışsa hata oluşur (ImportError veya AttributeError).

🔁 Örnek 2 – Sınıflar Arası Bağımlılık

models.py

from services import save_user  # ❌ Circular import

class User:
    def save(self):
        save_user(self)


services.py

from models import User  # ❌ Circular import

def save_user(user: User):
    print(f"{user} kaydedildi")


🧠 Sorun:
Hem models.py, hem services.py birbirini import eder. Modüllerden biri henüz yüklenmeden çağrıldığı için hata oluşur.

✅ Çözüm:

save_user'ı fonksiyon içinde import et.

Veya save_user fonksiyonunu utils.py gibi bağımsız bir modüle taşı.

🔁 Örnek 3 – Fonksiyon İçi Import ile Lazy Çözüm

a.py

def func_a():
    from b import func_b  # ⏳ Lazy import
    func_b()


b.py

def func_b():
    print("func_b çalıştı")


🧠 Yarar:
Fonksiyon sadece çağrıldığında func_b import edilir. Bu sayede circular import oluşmaz.

🔁 Örnek 4 – TYPE_CHECKING ile Tip Bağımlılığı Çözümü

a.py

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from b import B

def kullan(b: "B"):
    print("B örneği kullanıldı")


b.py

class B:
    pass


🧠 Yarar:
Runtime’da b import edilmez, sadece tip kontrolü sırasında alınır. Circular import önlenmiş olur.

🔁 Örnek 5 – Ortak Arabirim Modülü Kullanımı

interface.py

class ICommon:
    def process(self): pass


modul_a.py

from interface import ICommon
class A(ICommon):
    ...


modul_b.py

from interface import ICommon
class B(ICommon):
    ...


🧠 Yarar:
Her iki modül de ortak bir arabirimi kullanır ama birbirlerine doğrudan bağlı değildir.
"""