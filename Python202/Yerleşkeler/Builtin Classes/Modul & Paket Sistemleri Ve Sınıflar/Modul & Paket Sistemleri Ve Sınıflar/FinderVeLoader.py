# ====================================================================
# 🧠 F I N D E R  -  Python'da Modül Bulucu Mekanizması
# ====================================================================

# Python’da "Finder", bir modülün nerede olduğunu bulan bileşendir.
# "Bulmak" = diskten, sys.path'ten, bellekten, zip dosyası içinden, vs.


# Finder'lar `sys.meta_path` listesinde tutulur
# Python, import edilen modül sys.modules içinde yoksa bu listeyi kullanır

# --------------------------------------------------------------------
# 🔹 Finder Sınıfları Ne Yapar?
# --------------------------------------------------------------------

# Bir finder, en azından `find_spec(fullname, path, target=None)` metodunu implement eder.
# Bu metod, modülün yerini belirlemeye çalışır ve eğer bulursa bir `ModuleSpec` objesi döner.

# EĞER BULAMAZSA: None döndürülür ve zincirdeki sıradaki finder denenir


# --------------------------------------------------------------------
# 🔸 Örnek: Default Finder → PathFinder
# --------------------------------------------------------------------

# PathFinder → Python’un kendi Finder'ıdır
# sys.path dizisini gezer ve .py, .pyc, .so, .pyd dosyalarını arar

# importlib.machinery.PathFinder.find_spec(...) şeklinde çalışır
# Normal import’lar genellikle buradan geçer

# --------------------------------------------------------------------
# 📌 FINDER vs LOADER
# --------------------------------------------------------------------

# Finder = "Modül NEREDE?"
# Loader = "Modülü NASIL yükleyeceğim?"

# Finder sadece spec döner
# Loader ise `exec_module(module)` ile dosya çalıştırır

# --------------------------------------------------------------------
# 🔍 Finder Ne Zaman Kullanılır?
# --------------------------------------------------------------------

# 1) sys.modules içinde modül yoksa
# 2) import edilen modül sys.path’te değilse
# 3) modül sys.path’te bulunamıyorsa, veya sys.path dışında özel bir kaynaktan yüklenmek isteniyorsa
#     (örn. zip dosyası, şifreli dosya, runtime memory, veritabanı, vs.)
#     bu durumda devreye özel Finder’lar girer

# --------------------------------------------------------------------
# 🔄 Kendi Finder’ını Yazmak İçin:
# --------------------------------------------------------------------

# 1. Bir sınıf oluştur ve `find_spec(self, fullname, path, target)` metodunu tanımla
# 2. Gerekirse `ModuleSpec` nesnesi üret ve bir Loader ata
# 3. Finder'ı sys.meta_path'e en baştan ekle

# --------------------------------------------------------------------
# 💡 Basit Kural:
# --------------------------------------------------------------------

# Finder = dedektif 👮
# Loader = taşıyıcı 🚚

# Finder "os" modülünü bulur ve "burada!" der
# Loader ise içeriği çalıştırır ve `sys.modules` içine koyar

# --------------------------------------------------------------------
# ❗ Dikkat Edilecek Noktalar
# --------------------------------------------------------------------

# - find_spec dönerken ya None ya da DOĞRU yapılandırılmış ModuleSpec dönmelidir
# - path parametresi paketlerde alt modül ararken kullanılır (submodüller için)
# - custom Finder yazarken performans kaybı olmaması için dikkatli olunmalı

# --------------------------------------------------------------------
# 🔓 Finder Kullanım Alanları
# --------------------------------------------------------------------

# - Şifreli modülleri yüklemek (örneğin .enc)
# - JSON veya YAML dosyalarını modül gibi import etmek
# - Modülleri dinamik olarak internetten yüklemek
# - Kod çalışmasını izleyen loglayıcı sistem kurmak


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                      PYTHON MODULE TYPES: FINDER & LOADER             ║
# ╠════════════════════════╦═════════════════════╦═══════════════════════╣
# ║       MODULE TYPE      ║       FINDER        ║        LOADER         ║
# ╠════════════════════════╬═════════════════════╬═══════════════════════╣
# ║ 📦 Regular Package      ║ FileFinder          ║ SourceFileLoader      ║
# ║ └ (__init__.py var)     ║                     ║                       ║
# ╠────────────────────────╬─────────────────────╬───────────────────────╣
# ║ 🧠 Namespace Package    ║ FileFinder          ║ NamespaceLoader        ║
# ║ └ (__init__.py yok)     ║                     ║                       ║
# ╠────────────────────────╬─────────────────────╬───────────────────────╣
# ║ 📄 Python Module        ║ FileFinder          ║ SourceFileLoader      ║
# ║ └ (.py dosyası)         ║                     ║                       ║
# ╠────────────────────────╬─────────────────────╬───────────────────────╣
# ║ ⚙️ Extension Module     ║ FileFinder          ║ ExtensionFileLoader   ║
# ║ └ (.pyd / .so dosyası)  ║                     ║                       ║
# ╠────────────────────────╬─────────────────────╬───────────────────────╣
# ║ 🧊 Frozen Module        ║ FrozenImporter      ║ FrozenImporter         ║
# ╠────────────────────────╬─────────────────────╬───────────────────────╣
# ║ 💻 Built-in Module      ║ BuiltinImporter     ║ BuiltinImporter        ║
# ╠────────────────────────╬─────────────────────╬───────────────────────╣
# ║ 🧪 Bytecode-only Module ║ FileFinder          ║ SourcelessFileLoader  ║
# ╠────────────────────────╬─────────────────────╬───────────────────────╣
# ║ 🧭 Custom / Meta Loader ║ MetaPathFinder      ║ (Sen belirlersin!)     ║
# ╚════════════════════════╩═════════════════════╩═══════════════════════╝

# 🧠 NOTLAR:
# - FileFinder modülü doğrudan yüklemez; uygun loader'ı çağırır (.py, .so, __init__.py vb.)
# - Builtin ve Frozen modüller için finder ve loader aynıdır (tek sınıf, çift işlev) çünkü hem find_spec hemde exec_module var
# - Namespace package'ler import sırasında __init__.py olmadığı halde çalışır.
# - Custom meta path sistemi yazarken hem finder hem loader senin elindedir.
