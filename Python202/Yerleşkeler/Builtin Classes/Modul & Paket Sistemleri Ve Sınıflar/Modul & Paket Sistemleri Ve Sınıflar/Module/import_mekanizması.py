# 🧠 PYTHON'DA MODÜL YÜKLEME MEKANİZMASI (IMPORT PROTOKOLÜ) – TAM AKIŞ

# Her `import modul_adi` ifadesi çalıştığında, Python aşağıdaki adımları sırasıyla uygular.
# Bu süreç hem esneklik hem de performans açısından oldukça özelleştirilebilirdir.

# 1️⃣ ADIM – sys.modules (CACHE) kontrolü
# ---------------------------------------
# - sys.modules bir dict’tir; daha önce yüklenmiş tüm modüller burada tutulur
# - Eğer modül burada varsa doğrudan geri döndürülür (disk erişimi yapılmaz)

# Örnek:
# if "os" in sys.modules:
#     return sys.modules["os"]


# 2️⃣ ADIM – sys.meta_path zinciri (FINDER’LAR)
# ---------------------------------------------
# - Eğer sys.modules içinde yoksa, Python `sys.meta_path` listesini tarar
# - Her eleman bir "finder" nesnesidir ve `find_spec()` metoduna sahiptir
# - Bu metot başarılı olursa bir `ModuleSpec` döner, aksi halde None döner

# NOT: meta_path → modülün *nerede olduğunu bulmaya çalışan* zinciridir


# 3️⃣ ADIM – PATHFINDER: importlib.machinery.PathFinder
# ------------------------------------------------------
# - Python’un varsayılan finder’ıdır
# - sys.path’teki dizinleri tarar

# 🔹 Önemli: Python her sys.path girdisi (her dizin) için
#            ayrı bir `FileFinder` örneği oluşturur.
# 🔹 Her `FileFinder` sadece KENDİ dizininde arama yapar.
#    Bu sayede modül araması izole, hızlı ve yönetilebilir olur.

# 🔹 Finder zinciri içinde bu örnekler sırayla denenir:
#    örn: sys.path = ["/lib1", "/lib2"]
#         → FileFinder("/lib1")
#         → FileFinder("/lib2")

# - Her dizin + fullname (örn. importlib.machinery → importlib/machinery)
#   → Bu fiziksel yolda aşağıdaki kontroller yapılır:

#   1. __init__.py dosyası varsa → regular package
#   2. .py dosyası varsa         → standalone modül
#   3. Sadece klasör varsa       → namespace package (PEP 420)

# NOT: Finder sadece dosyayı bulur, çalıştırmaz!



# 4️⃣ ADIM – ModuleSpec nesnesi oluşturulur
# ----------------------------------------
# - Başarılı finder → `importlib.machinery.ModuleSpec` döner
# - Bu nesne:
#     - `name`      : modülün adı
#     - `loader`    : hangi loader ile yüklenecek
#     - `origin`    : dosyanın yeri
#     - `is_package`: paket olup olmadığı
#     - `submodule_search_locations`: varsa iç modüller için path

#  Python bir modülü yüklemeden önce:
# 1. Önce module_from_spec(spec) fonksiyonunu çağırır
#    - Eğer Loader içinde create_module tanımlıysa onu kullanır
#    - Aksi halde varsayılan olarak types.ModuleType(spec.name) ile bir modül nesnesi oluşturur
#
# 2. Bu modül nesnesi otomatik olarak __spec__, __loader__, __package__, __path__ gibi
#    metadata'larla donatılır
#
# 3. Ardından exec_module(mod) çağrılarak modülün içeriği bu nesnenin __dict__’ine yüklenir
#    - Yani artık modülün kodu bu boş yapının içine exec() ile çalıştırılır
#
# SONUÇ:
# module_from_spec → modülün iskeletini hazırlar
# exec_module      → içine kodu yerleştirir


# 5️⃣ ADIM – Loader devreye girer
# -------------------------------
# - `spec.loader.exec_module(modul)` çağrılır
# - Loader:
#     - Dosyayı okur
#     - `exec()` ile çalıştırır
#     - Modülün `__dict__`’ine yükler

# Örnek loader'lar:
# - SourceFileLoader      → .py dosyaları için
# - ExtensionFileLoader   → .so / .pyd dosyaları için
# - BuiltinImporter       → gömülü modüller için


# 6️⃣ ADIM – Module instance oluşturulup meta veriler set edilir
# --------------------------------------------------------------
# - `module_from_spec(spec)` çağrılır
#     → spec'e göre boş bir modül objesi oluşturulur
#     → modülün __name__, __loader__, __package__ gibi meta verileri atanır
#     → KOD henüz çalışmaz! exec_module çağrısı bunu sağlar


# 7️⃣ ADIM – sys.modules güncellenir
# ---------------------------------
# - Yüklenen modül artık `sys.modules` içine yazılır
# - Böylece ikinci kez çağrılırsa yeniden yüklenmesine gerek kalmaz


# ✅ MODÜL ARTIK KULLANIMA HAZIRDIR
# ---------------------------------
# - Artık doğrudan `import modul_adi` ile kullanılabilir


# Basit gösterimi
import os  # 1: sys.modules? yoksa → 2: sys.meta_path? → 3: PathFinder → 4: ModuleSpec → 5: Loader → 6: sys.modules → 7: os kullanılabilir
