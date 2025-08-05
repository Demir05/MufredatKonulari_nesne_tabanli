# ================================================================================
# 🧩 __init__.py DOSYASI NEDİR? NE İŞE YARAR? NEDEN BU İSİMDE?
# ================================================================================
# Bu açıklama, __init__.py dosyasının Python'daki yerini, amacını, neden bu isimde
# olduğunu ve ne içerebileceğini açıklar.

# ================================================================================
# 1️⃣ TANIM: __init__.py NEDİR?
# ------------------------------------------------------------------------------

# __init__.py, bir klasörü **Python paketi** haline getiren özel bir dosyadır.

# Yani:
#   📁 bir klasör
#   +
#   📄 içinde "__init__.py" varsa
#   =
#   📦 o klasör Python için bir "paket"tir

# Bu dosya olmadan, Python 2'de klasörler modül olarak tanınmazdı.
# Python 3'te artık zorunlu değil, ama özel davranışlar tanımlamak için hala çok kullanılır.

# ================================================================================
# 2️⃣ NEDEN ADI "__init__"?
# ------------------------------------------------------------------------------

# Evet, "__init__" ismi sınıflardaki constructor ile aynıdır. Bu kasıtlıdır!

# Çünkü:
# - Sınıflarda `__init__()` nesneyi başlatır.
# - Paketlerde `__init__.py` klasörü **paket olarak başlatır.**

# Yani dosya düzeyinde bir "constructor" gibi davranır:
# - import edildiğinde çalışır
# - ayar yapabilir
# - başka şeyler import edebilir
# - ön yükleme (preload) fonksiyonları çağırabilir

# ================================================================================
# 3️⃣ NE İÇERİR?
# ------------------------------------------------------------------------------

# __init__.py dosyası boş olabilir — sadece varlığı paketi tanımlar.

# Ama doluysa şunları içerebilir:
# - Paket seviyesinde sabitler
# - Varsayılan import’lar
# - Başlatıcı kodlar
# - Kütüphane tanımı, versiyon, yapı
# - __all__ listesi (ne export edilecek)

# Örnek:
# ------------------------------------------------------------------------------
# 📁 mypkg/
#     __init__.py
#     tools.py
#     utils.py
#
# __init__.py içeriği:
#     print("mypkg paketi yüklendi")
#     from .tools import add, subtract
#     from .utils import format_string
#     __version__ = "1.0"

# Bu sayede:
#     from mypkg import add
# doğrudan çalışabilir hale gelir.

# ================================================================================
# 4️⃣ NEDEN HALA ÖNEMLİ?
# ------------------------------------------------------------------------------

# - import davranışını özelleştirmek için kullanılır
# - alt modülleri/grupları dışa aktarmak için kullanılır
# - test ortamları, plugin sistemleri, API hazırlamak için gereklidir

# Hatta advanced kullanım:
#     __init__.py içinde __getattr__ tanımlayarak dinamik import sistemi oluşturulabilir (Python 3.7+)

# ================================================================================
# 5️⃣ BONUS: BOŞ OLMASI NE ANLAMA GELİR?
# ------------------------------------------------------------------------------

# Eğer __init__.py boşsa:
# - Paket tanımlanmış olur
# - Ama ekstra bir işlem yapılmaz

# Bu çoğu zaman yeterlidir. Ama:
# - API yüzeyi oluşturulacaksa
# - Global ayar yapılacaksa
#   mutlaka dolu olmalıdır.

# ================================================================================
# ✅ ÖZET

# | Özellik           | Açıklama                                            |
# |-------------------|-----------------------------------------------------|
# | __init__.py       | Klasörü paket yapan özel dosya                      |
# | Neden "__init__"? | Sınıf gibi "başlatıcı" davranışa sahip olması       |
# | Boş olabilir mi?  | Evet                                                |
# | İçerik olabilir mi? | from .modul import x, ayarlar, __version__ vb.   |
# | Ne zaman çalışır? | Paket ilk import edildiğinde                       |

# ================================================================================






# ================================================================================
# 📦 __init__.py İÇİN ATTRIBUTE (ÖZELLİK) AÇIKLAMALARI – DETAYLI YORUMLAR
# ================================================================================
# Bu dosya bir paketin "giriş noktası" olduğundan, içine konulan her şey
# paketin genel davranışını etkiler. Aşağıda en yaygın kullanılan özelliklerin
# (değişkenlerin/fonksiyonların) ne işe yaradığını, neden kullanıldığını açıklıyoruz.

# ================================================================================
# 1️⃣ __version__
# ------------------------------------------------------------------------------
# Paket versiyonunu tanımlar.
# Bu bilgi genelde setup.py, pip, veya dış kullanıcılar tarafından kullanılır.

__version__ = "1.0.0"

# Kullanım:
#   import mypackage
#   print(mypackage.__version__)  # "1.0.0"

# ================================================================================
# 2️⃣ __all__
# ------------------------------------------------------------------------------
# Bu liste, `from mypackage import *` kullanıldığında hangi öğelerin dışa aktarılacağını belirler.

__all__ = ["add", "subtract", "format_string"]

# Eğer bu tanımlanmazsa, tüm modülde tanımlı isimler export edilir (ama bu genelde istenmez).
# Bu liste, dış API’yi kontrol altında tutmak için kullanılır.

# ================================================================================
# 3️⃣ Fonksiyon ve sınıf aktarmaları
# ------------------------------------------------------------------------------
# Genellikle modül içindeki fonksiyonlar burada tekrar dışa aktarılır.

from .tools import add, subtract
from .utils import format_string

# Bu sayede kullanıcılar:
#     from mypackage import add
# demek yerine modül yolunu bilmeden doğrudan fonksiyona erişebilir.

# ================================================================================
# 4️⃣ __path__
# ------------------------------------------------------------------------------
# Bu, sadece "namespace paketlerinde" (çok klasörlü tek paketlerde) anlamlıdır.
# Normal paketlerde nadiren değiştirilir.

# __path__ = [...]  # Liste olarak verilir. Alt paket arama yolları buradan yönetilir.

# ================================================================================
# 5️⃣ Ayarlar ve sabitler
# ------------------------------------------------------------------------------
# Paket genelinde kullanılacak ayarlar veya sabitler buraya tanımlanabilir.

DEBUG_MODE = False
DEFAULT_TIMEOUT = 30

# Diğer modüller bunu şöyle kullanabilir:
#     from mypackage import DEBUG_MODE

# ================================================================================
# 6️⃣ Başlatıcı fonksiyonlar
# ------------------------------------------------------------------------------
# Paket import edildiğinde çalışmasını istediğin kodları veya ayarları buraya yazabilirsin.

def _init_config():
    print("Config initialized")

_init_config()

# NOT: Gerçek sistemlerde genelde log, config yükleme, ENV okuma işlemleri buradan başlatılır.

# ================================================================================
# 7️⃣ __getattr__ (Python 3.7+)
# ------------------------------------------------------------------------------
# Modül içinde olmayan bir attribute çağrıldığında çalışır.
# Dinamik import, lazy loading gibi şeyler için çok kullanışlıdır.

def __getattr__(name):
    if name == "dynamic":
        return lambda: "Bu attribute dinamik olarak yaratıldı"
    raise AttributeError(f"Module has no attribute {name}")

# Kullanım:
#   import mypackage
#   mypackage.dynamic()  → Bu fonksiyon aslında modül içinde tanımlı değil ama çalışır!

# ================================================================================
# 8️⃣ __dir__
# ------------------------------------------------------------------------------
# dir(mypackage) çağrıldığında hangi öğelerin listeleneceğini özelleştirir.

def __dir__():
    return __all__ + ["__version__"]

# ================================================================================
# 9️⃣ __doc__
# ------------------------------------------------------------------------------
# Paket açıklaması. Bu string sabit, modülün docstring’idir.

__doc__ = """
MyPackage: Kullanışlı araçlar, fonksiyonlar ve yardımcı bileşenler içerir.
- tools
- utils
- config
"""
# help(mypackage) komutu bunu gösterir.

# ================================================================================
# ✅ ÖZET – __init__.py İçindeki Özellikler
# ------------------------------------------------------------------------------

# | Özellik        | Amaç                                                    |
# |----------------|----------------------------------------------------------|
# | __version__    | Paket sürümünü belirtir                                  |
# | __all__        | from X import * davranışını kontrol eder                 |
# | __doc__        | Paket açıklaması sağlar (help() içeriği)                 |
# | DEBUG, SETTINGS| Ortak sabit/ayar paylaşımı                               |
# | __getattr__    | Dinamik attribute tanımlama (3.7+)                       |
# | __dir__        | dir() fonksiyonunun ne döneceğini belirler              |
# | Fonksiyon import| Paket seviyesinden direkt kullanım sağlar              |

# ================================================================================
# 🧠 KURAL:
# __init__.py = Paket kimliği + dışa açılan arayüz + başlatıcı yapılandırma merkezi
# ================================================================================
