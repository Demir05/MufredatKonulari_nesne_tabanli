def find_modul(path):
    # ============================================
    # AMAÇ:
    #  - Verilen path'i incele
    #  - Türünü bul: regular package / namespace package / düz modül (.py)
    #  - Türüne göre doğru module attribute'larını ve spec alanlarını nasıl kuracağını tarif et
    #  - Gerekirse yürütme (exec) ve sys.modules'e yazma stratejisini belirle
    # ============================================

    # 1) YOLU HAZIRLA (neden? sys.path karşılaştırmaları güvenilir olsun)
    #    - path'i mutlaklaştır (abspath): göreceli yolları düzeltmek için
    #    - platform normalize (normcase): Windows'ta büyük/küçük harf ve slash farklarını düzeltmek için
    #    - (opsiyonel) realpath: symlink varsa gerçek diske bağlamak için

    # 2) TÜR TESPİTİ (ilk çatallanma)
    #    - Eğer path bir DOSYA ise:
    #        * .py uzantılıysa → "düz modül"
    #        * değilse → "import edilemez" (bu fonksiyonun kapsamı dışında)
    #    - Eğer path bir KLASÖR ise:
    #        * path/__init__.py VARSA → "regular package"
    #        * YOKSA → namespace aday:
    #              + ebeveyn klasör sys.path altında görünüyor mu? (yani path, sys.path’teki bir kökten başlanınca erişilebilir mi)
    #              + Evetse → "namespace package"
    #              + Hayırsa → "import edilemez"

    # 3) MANTIKSAL AD (dotted name) ÜRET (neden? __name__/__package__/spec.name için şart)
    #    - sys.path içindeki "en uzun eşleşen kök"ü bul (neden? en doğru kökten relatifleşmek için)
    #    - relpath = path - kök (örn. C:\libs\a\b\pkg → a\b\pkg)
    #    - parçala ve '.' ile birleştir → full_name (örn. "a.b.pkg")
    #    - Eğer tam kökün kendisiyse (relpath boş/".") → bu durumda mantıksal ad türetilemez → import edilemez

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

    # 4) TÜRE GÖRE ATTRIBUTE/SPEC KURALLARI
    #    ----------------------------------------------------------------
    #    A) REGULAR PACKAGE (klasör + __init__.py VAR)
    #    ----------------------------------------------------------------
    #    - full_name          = "a.b.pkg"            # 3. adımda üretildi
    #    - init_file          = "<path>/__init__.py" # mutlak yol
    #    - pkg_dir            = "<path>"             # paket klasörü
    #
    #    # Modül attribute'ları:
    #    - __name__           = full_name            # modülün tam adı
    #    - __package__        = full_name            # paketlerde kendi tam adı
    #    - __file__           = init_file            # __init__.py'ye işaret etmeli
    #    - __path__           = [pkg_dir]            # DİKKAT: liste olmak zorunda
    #    - __cached__         = None                 # dinamikte genelde boş
    #    - __loader__         = None                 # gerçek loader yoksa None kalır
    #
    #    # Spec alanları (PEP 451):
    #    - __spec__.name      = full_name
    #    - __spec__.parent    = full_name.rpartition('.')[0]  # üst ad; yoksa ""
    #    - __spec__.origin    = init_file
    #    - __spec__.loader    = None                # dinamik senaryoda yok
    #    - __spec__.is_package= True
    #    - __spec__.submodule_search_locations = [pkg_dir]    # __path__ ile aynı içerik
    #
    #    # Yürütme (istersen):
    #    - __init__.py dosyasını oku ve exec et (neden? paket başlatıcı kodları çalışsın)
    #
    #    # İnvariant kontrolleri:
    #    - __path__ bir liste olmalı ve spec.submodule_search_locations ile aynı değerleri taşımalı
    #    - __file__ gerçekten __init__.py'yi göstermeli
    #    - __spec__.name == __name__
    #
    #    ----------------------------------------------------------------
    #    B) NAMESPACE PACKAGE (PEP 420)  (klasör + __init__.py YOK)
    #    ----------------------------------------------------------------
    #    - full_name   = "ns.util"        # 3. adımda üretildi
    #    - paths       = []               # çok-kök liste (aşağıda nasıl doldurulacağı yazıyor)
    #
    #    # Çok-kök toplama mantığı (neden? PEP 420 paketleri aynı ada sahip birden çok kökten oluşabilir):
    #    - full_name'i '.' ile böl → ["ns","util"]
    #    - sys.path'teki TÜM kökler için:
    #         * candidate = join(kök, *parçalar)
    #         * candidate klasör mevcutsa:
    #               - Eğer candidate/__init__.py VAR → bu ad regular pakettir → namespace geçersiz → bu dalı iptal et
    #               - Değilse → paths listesine candidate ekle
    #    - paths boşsa → namespace oluşturma → iptal (import edilemez)
    #
    #    # Modül attribute'ları:
    #    - __name__           = full_name
    #    - __package__        = full_name
    #    - __file__           = None          # DİKKAT: namespace paketlerde dosya yok
    #    - __path__           = paths         # bir veya daha çok dizin; LİSTE
    #    - __cached__         = None
    #    - __loader__         = None          # namespace'te loader yok
    #
    #    # Spec alanları:
    #    - __spec__.name      = full_name
    #    - __spec__.parent    = full_name.rpartition('.')[0]   # üst ad; yoksa ""
    #    - __spec__.origin    = None veya "namespace"          # soyut bir değer olabilir
    #    - __spec__.loader    = None
    #    - __spec__.is_package= True
    #    - __spec__.submodule_search_locations = paths
    #
    #    # Yürütme:
    #    - YOK (çalıştırılacak __init__.py yok)
    #
    #    # İnvariant kontrolleri:
    #    - __file__ mutlaka None olmalı
    #    - __path__ ve __spec__.submodule_search_locations aynı liste olmalı
    #    - Aynı adın herhangi bir kökte regular'a çakışması namespace'i geçersiz kılar (regular > namespace)
    #
    #    ----------------------------------------------------------------
    #    C) DÜZ MODÜL (.py) (paket değil)
    #    ----------------------------------------------------------------
    #    - full_name   = "a.b.module"      # 3. adımda üretildi (dosyanın bulunduğu klasörden itibaren)
    #    - file_path   = "<path>.py"       # verilen dosya
    #    - parent_name = full_name.rpartition('.')[0] or ""  # üst ad; yoksa ""
    #
    #    # Modül attribute'ları:
    #    - __name__           = full_name
    #    - __package__        = parent_name   # DİKKAT: düz modülde ebeveyn adı olmalı (relative importlar için kritik)
    #    - __file__           = file_path
    #    - (düz modülde __path__ YOK)
    #    - __cached__         = None
    #    - __loader__         = None
    #
    #    # Spec alanları:
    #    - __spec__.name      = full_name
    #    - __spec__.parent    = parent_name
    #    - __spec__.origin    = file_path
    #    - __spec__.loader    = None
    #    - __spec__.is_package= False
    #    - __spec__.submodule_search_locations = None/boş
    #
    #    # Yürütme (istersen):
    #    - .py dosyasını oku ve exec et (modülün üst düzey kodu çalışsın)
    #
    #    # İnvariant kontrolleri:
    #    - __package__ ebeveyn ad ("" olabilir); __path__ bulunmaz
    #    - __spec__.name == __name__
    #
    # 5) SYS.MODULES ENTEGRASYONU (neden? sonraki import'lar cache'ten gelsin)
    #    - sys.modules[__name__] = mod
    #    - Aynı adı ikinci kez yüklersen, yeniden çalıştırma olmaz (cache); farklı adla yüklersen alias oluşur (yan etkiler!)
    #
    # 6) HATA MESAJLARI / KENAR DURUMLAR
    #    - "dotted name türetilemedi" → path sys.path altında değilse
    #    - "namespace için katkı dizini yok" → çok-kök taramasında hiç klasör bulunamadıysa
    #    - "regular çakışması" → namespace adında bir kökte __init__.py görüldüyse
    #    - "desteklenmeyen uzantı / path yok" → dosya/klasör bulunamadıysa
    #
    # 7) NORMALİZASYON İPUÇLARI (neden? Windows/Unix farkları)
    #    - her kıyaslamada abspath + normcase kullan (case-insensitive FS'lerde sorun çıkmasın)
    #    - join/relpath ile yol parçalarını birleştir/ayır
    #
    # 8) SON DOĞRULAMA (self-check)
    #    - Paketlerde: __path__ liste, spec.submodule_search_locations aynı içerikte
    #    - Regular'da: __file__ → __init__.py
    #    - Namespace'te: __file__ → None
    #    - Düz modülde: __path__ yok; __package__ ebeveyn
    #    - Tümünde: __spec__.name == __name__, __spec__.parent doğru
    #
    # 9) (OPSİYONEL) YÜRÜTME KARARI
    #    - Regular package: __init__.py exec etmek tipik davranıştır
    #    - Düz modül: .py exec etmek tipik davranıştır
    #    - Namespace: exec YOK (çünkü dosya yok)
    #
    # NOT: Bu fonksiyonun çıktısı, pratikte "hazır bir ModuleType ve ModuleSpec nasıl kurulur"
    #      bilgisini uygular. İstersen yukarıdaki her adımı gerçek koda çevirirsin; burada
    #      'neden' ve 'nasıl' anlatıldı, böylece hatasız kurulum yapabilirsin.
    pass


import types

def module_from_spec(spec):
    """
    PEP 451'e göre, bir ModuleSpec nesnesinden modül nesnesi oluşturur.
    Eğer spec.loader içinde create_module varsa onu çağırır,
    yoksa varsayılan olarak types.ModuleType kullanılır.
    """
    # 1. Spec'e ait loader varsa ve create_module metodu tanımlıysa
    if hasattr(spec.loader, "create_module"):
        module = spec.loader.create_module(spec)
    else:
        # 2. Yoksa standart modül oluşturulur
        module = types.ModuleType(spec.name)

    # 3. Metadata'lar set edilir
    module.__spec__ = spec
    module.__loader__ = spec.loader
    module.__package__ = spec.parent
    if spec.submodule_search_locations is not None:
        module.__path__ = spec.submodule_search_locations

    return module

