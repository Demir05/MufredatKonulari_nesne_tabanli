# =====================================================================
# 📦 SYS MODÜLÜ: Python Çalışma Zamanına Erişim Kapısı
# =====================================================================

# 🔹 `sys` modülü, Python çalışma zamanına (runtime) dair bilgileri ve işlevleri içerir.
#     ➤ Örn: komut satırı argümanları, modül yükleme, stdout yönlendirme, bellek limiti, interpreter bilgisi

# 🔧 Bu modül C'de tanımlanmış olup, CPython yorumlayıcısının iç mekanizmalarına doğrudan temas sağlar.

import sys

# 🔍 Örnek:
print("Python sürümü:", sys.version)
print("Yüklü modüller:", list(sys.modules.keys())[:5])

# 🔥 Ama bizim için en önemli fonksiyon: `sys._getframe()`

# =====================================================================
# 🔍 sys._getframe(): Frame Nesnesine Düşük Seviyeli Erişim
# =====================================================================

# 📌 Tanım:
#     sys._getframe([depth]) → `types.FrameType` döner
#     (depth: int = 0)

# 🧠 Açıklama:
#     ➤ Python yorumlayıcısı her fonksiyon çağrısı için bir "execution frame" oluşturur.
#     ➤ sys._getframe(), bu frame nesnesine doğrudan erişim sağlar.
#     ➤ `depth=0` → şu anki frame
#     ➤ `depth=1` → çağıran fonksiyonun frame’i
#     ➤ `depth=2` → onun da çağıranı...

# 🧾 Sözdizimi (Syntax + Typing):

from types import FrameType
from typing import Optional

def _getframe(depth: int = 0) -> FrameType: ...

# ✅ Dönüş tipi: `FrameType` → frame.f_code, f_locals, f_globals, f_lineno... gibi alanlara sahiptir

# =====================================================================
# 📌 KULLANIM ALANLARI:
# =====================================================================

# 🔍 1. Debugging & Profiling:
#     ➤ Dinamik olarak stack trace oluşturma
#     ➤ Hangi fonksiyon, nerede çağrılmış? gibi sorulara yanıt

# 🔍 2. Logging:
#     ➤ Gelişmiş log sistemlerinde otomatik "call site" bilgisi çekmek

# 🔍 3. Decorator / Middleware sistemleri:
#     ➤ Fonksiyonun çağıranını analiz edip davranış değiştirme

# 🔍 4. Test araçları:
#     ➤ Otomatik olarak "test hangi modülden çağrıldı" çıkarımı

# 🔍 5. Debugger / Trace Framework:
#     ➤ `sys.settrace()` ile birlikte kullanılıp özel debugger'lar geliştirilebilir

# =====================================================================
# 🔬 ÖRNEK KULLANIM
# =====================================================================

def fonksiyonA():
    frame = sys._getframe(0)
    print("Benim adım:", frame.f_code.co_name)
    print("Beni çağıran:", frame.f_back.f_code.co_name if frame.f_back else "Yok")

def fonksiyonB():
    fonksiyonA()

fonksiyonB()

# =====================================================================
# ⚠️ DİKKAT EDİLMESİ GEREKENLER
# =====================================================================

# ❗ sys._getframe() düşük seviyeli bir fonksiyondur
#     ➤ CPython dışı yorumlayıcılarda çalışmayabilir (örneğin PyPy, IronPython, Jython)

# ❗ performans maliyeti olabilir:
#     ➤ Özellikle sık kullanılan kod bloklarında introspection yapmak CPU & bellek açısından pahalıya mal olur

# ❗ GC (Garbage Collector) ile uyumlu değil:
#     ➤ Elde edilen frame nesnesi, zincir halinde diğer frame'lere bağlanır (f_back)
#     ➤ Bu zincir kolay kolay çözülemez → referans döngüsü oluşabilir

# ✅ Bu yüzden kullanımdan sonra `del frame` ile temizlik yapılması önerilir

# 🔐 Bazı platformlarda bu API gizli kabul edilir:
#     ➤ Adındaki `_` (underscore), "private-like" fonksiyon olduğunu ima eder
#     ➤ Gelecekte kaldırılma riski olabilir (çok düşük ama standart dışı)

# =====================================================================
# ✅ sys._getframe() vs inspect.currentframe()
# =====================================================================

# 🔎 inspect.currentframe(), aslında `sys._getframe(0)` çağrısını sarmalayan bir fonksiyondur

# inspect.currentframe() daha güvenlidir:
#     ➤ import etmeyen sistemlerde çalışmaz
#     ➤ try/except içinde hata verir
#     ➤ Ama "gizli API" içermez, standart kütüphaneye dahildir

# 🔁 Kıyas:

import inspect
print(inspect.currentframe().f_code.co_name)  # inspect ile
print(sys._getframe(0).f_code.co_name)        # sys ile

# Her ikisi de aynı sonucu verir ✔️

# =====================================================================
# ✅ SONUÇ:
# =====================================================================

# 🔹 `sys._getframe()` CPython’un derinliklerine açılan bir kapıdır
# 🔹 Frame yapısına doğrudan erişim sağlar
# 🔹 Gelişmiş introspection, debugging, loglama gibi alanlarda kritik araçtır

# ❗ Ancak düşük seviyeli olduğu için:
#     ➤ Platform bağımlıdır
#     ➤ Performansa etki eder
#     ➤ Bellek sorunlarına yol açabilir

# ✅ Doğru kullanıldığında ise Python’un yürütme bağlamına dair inanılmaz güçlü bilgiler sağlar 🔥

