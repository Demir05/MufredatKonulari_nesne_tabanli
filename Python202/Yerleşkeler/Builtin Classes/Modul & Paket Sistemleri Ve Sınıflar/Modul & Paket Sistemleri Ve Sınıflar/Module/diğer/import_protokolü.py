
# # 🐍 PYTHON MODÜL SİSTEMİ: TARİHÇE, FARKLILIKLAR VE NEDENLERİ
#
# # ------------------------------
# # 📦 1. TRADITIONAL MODULE (Pre-3.3)
# # ------------------------------
# # - Her modül .py dosyasına denk gelir.
# # - Her package klasöründe __init__.py dosyası bulunmak zorundadır.
# # - import sırasında sys.path sırasına göre ilk bulunan dosya yüklenir.
# # - Basit ama esnek olmayan bir sistemdir.
#
# # ------------------------------
# # 🌐 2. NAMESPACE PACKAGES (PEP 420 - Python 3.3)
# # ------------------------------
# # - __init__.py olmadan da package olabilir.
# # - Birden fazla klasör tek bir package altında birleşebilir.
# # - Özellikle plugin sistemleri veya pip editable install için idealdir.
# # - Bu esneklik yeni tür "Loader" ihtiyacını doğurdu (NamespaceLoader)
#
# # ------------------------------
# # 🔍 3. FINDER + LOADER AYRIMI (PEP 302 - Python 2.3)
# # ------------------------------
# # - import süreci artık Finder (ne, nerede?) ve Loader (nasıl?) olarak ayrıldı.
# # - Böylece .zip dosyasından, veri tabanından, ağdan modül yüklenebilir hale geldi.
# # - `sys.meta_path`, `sys.path_hooks` eklendi.
#
# # ------------------------------
# # 📄 4. SPEC Tabanlı Yükleme (PEP 451 - Python 3.4)
# # ------------------------------
# # - find_module() yerine find_spec() geldi.
# # - ModuleSpec nesnesi modülün tüm detaylarını taşır (ad, yol, loader, origin...)
# # - Tek merkezden kontrol, daha sağlam ve test edilebilir sistem
#
# # ------------------------------
# # 🎛️ 5. ÇEŞİTLİ FINDER ve LOADER TÜRLERİ
# # ------------------------------
# # 🔹 BuiltinImporter        => C ile gömülü modüller (sys, time, etc.)
# # 🔹 FrozenImporter         => Python içine dondurulmuş modüller
# # 🔹 FileFinder             => Dosya sistemindeki modülleri bulur
# # 🔹 SourcelessFileLoader   => .pyc dosyası varsa, doğrudan onu yükler
# # 🔹 ExtensionFileLoader    => .so / .pyd gibi C uzantılı modülleri yükler
# # 🔹 NamespaceLoader        => __init__.py olmayan klasörler için
#
# # ------------------------------
# # 🧠 NEDEN BU KADAR ÇEŞİT VAR?
# # ------------------------------
# # ✔️ Platform bağımsız çalışmak için
# # ✔️ Performans optimizasyonları için
# # ✔️ Dosya sisteminden bağımsız modül sistemleri kurmak için
# # ✔️ Zip, ağ, bellek, veritabanı gibi alternatif kaynaklardan modül yüklemek için
# # ✔️ Eski kodları bozmadan yeni esneklikler sunmak için
#
# # ------------------------------
# # 🚀 SEN NEDEN KENDİNİNKİNİ YAZARSIN?
# # ------------------------------
# # - Eğitim amaçlı
# # - Debug / analiz için
# # - Özelleştirilmiş plugin sistemi kurmak için
# # - .json, .yaml gibi farklı türleri import edebilmek için
# # - Dinamik veya sandbox ortamlar için

# ----------------------------------------
# 📦 PYTHON MODÜL YÜKLEME ÖNCELİK SIRASI
# ----------------------------------------

# 1. Built-in Modules (Gömülü Modüller)
#    - 'sys', 'math', 'time' gibi C ile gömülü gelenler
#    - importlib.machinery.BuiltinImporter ile bulunur

# 2. Frozen Modules (Donmuş Modüller)
#    - Derlenmiş, embed edilmiş modüller (örn. zipapp, exe, frozen dist)
#    - importlib.machinery.FrozenImporter ile bulunur

# 3. Source File (.py)
#    - Düz Python kaynak dosyaları (örn. /modul.py)
#    - importlib.machinery.SourceFileLoader ile yüklenir

# 4. Bytecode File (.pyc)
#    - Derlenmiş bytecode dosyaları (__pycache__)
#    - Source yoksa ama pyc varsa bu kullanılır

# 5. C Extension (.so / .pyd)
#    - Native C uzantı dosyaları
#    - importlib.machinery.ExtensionFileLoader ile yüklenir

# 6. Regular Package (Klasör + __init__.py)
#    - Klasör varsa ve içinde __init__.py varsa paket kabul edilir
#    - Bu durumda import edilen ad = klasör adı

# 7. Namespace Package (Klasör, __init__.py yok)
#    - Aynı adla birden fazla kökte klasör olabilir
#    - Ancak __init__.py yoksa namespace kabul edilir (PEP 420)
#    - Sadece diğer her şey başarısız olursa çalışır

# ----------------------------------------
# 🔄 Bu işlemlerin tamamı artık PEP 451 ile
#     importlib.machinery.FileFinder üzerinden
#     spec tabanlı (ModuleSpec) yapılır
# ----------------------------------------

# 🔥 ÖNEMLİ: Namespace (PEP 420), sadece tüm diğer dosya/dizin eşleşmeleri başarısız olursa devreye girer.
# Bu yüzden dosya temelli çözüm varsa (py, pyc, so, pyd, __init__.py) → namespace göz ardı edilir.
