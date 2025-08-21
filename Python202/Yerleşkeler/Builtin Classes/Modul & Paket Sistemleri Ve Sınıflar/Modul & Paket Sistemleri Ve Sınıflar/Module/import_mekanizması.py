"""
PYTHON'DA MODÜL YÜKLEME MEKANİZMASI (IMPORT PROTOKOLÜ) – TAM AKIŞ

Her `import modul_adi` yazıldığında, Python aşağıdaki adımları sırayla uygular.
Bu süreç, hem performans, hem esneklik, hem de yeniden yapılandırılabilirlik açısından tasarlanmıştır.

1. 🔍 ADIM – sys.modules kontrolü (CACHE):
   - Python önce `sys.modules` sözlüğüne bakar
   - Bu sözlük, daha önce yüklenmiş modüllerin bellekteki haliyle tutulduğu yerdir
   - Eğer aranan modül burada varsa, diskten tekrar yüklenmez

   ÖRNEK:
       if "os" in sys.modules:3
           return sys.modules["os"]

2. 🔁 ADIM – sys.meta_path zinciri (FINDER’LAR):
   - Eğer modül `sys.modules` içinde yoksa, Python `sys.meta_path` listesindeki *finder* nesnelerini sırayla çağırır
   - Her finder, `find_spec(modul_adi, path, target)` metodunu implement eder
   - Bu metot ya bir `ModuleSpec` döndürür (başarılı bulma) ya da `None` döndürür (devam et)

   NOT: `meta_path` → modülün *nerede olduğunu bulmaya çalışanların* listesi

3. 📍 PATHFINDER (default finder):
   - Python’un varsayılan finder’ı: `importlib.machinery.PathFinder`
   - Bu sınıf, `sys.path` dizisini tarayarak `.py`, `.pyc`, `.pyd`, `.so` uzantılı dosyaları arar
   - Paket dizinleri varsa `__init__.py` aranır <aranan şey'in regular package olduğu varsayılır eğer import edilen dosya ise dosyanın kendisi aranır>
   - Uygun dosya bulunursa, `ModuleSpec` oluşturulur

   ÖRNEK:
       sys.path = ["/usr/lib/python", "/home/user/code"]
       PathFinder -> bu klasörleri gezer

4. 📦 ADIM – ModuleSpec oluşturulması:
   - `find_spec()` başarılı olursa `ModuleSpec` döner:
     - name
     - loader (Loader nesnesi)
     - origin (dosya yolu)
     - is_package (bool)
     - submodule_search_locations (eğer paketse)
   - Bu spec, Python’a modülün *nasıl yükleneceğini* söyler

5. 🚚 ADIM – Loader devreye girer:
   - `spec.loader.exec_module(modul)` çağrılır
   - Loader, modülün dosyasını okur ve `exec()` ile `modul.__dict__` içine çalıştırır

      ÖRNEK LOADER’LAR:
       - SourceFileLoader: .py dosyalarını yükler
       - ExtensionFileLoader: .so, .pyd dosyalarını yükler
       - BuiltinImporter: gömülü modülleri yükler

6. Module Attribute'ları set edilir

    # module_from_spec(spec):
    # → spec'e göre boş modül oluşturur, metadata'ları set eder
    # → sadece yapıyı kurar, kodu çalıştırmaz (exec_module gerekir)

6. 🧠 ADIM – sys.modules güncellenir:
   - Yüklenen modül, artık `sys.modules["modul_adi"]` içine yazılır
   - Bu sayede bir daha çağrıldığında direkt buradan alınır

7. 🔚 KULLANIMA HAZIR:
   - Artık `modul_adi` adıyla erişilebilir hale gelmiştir
"""

# Basit gösterimi
import os  # 1: sys.modules? yoksa → 2: sys.meta_path? → 3: PathFinder → 4: ModuleSpec → 5: Loader → 6: sys.modules → 7: os kullanılabilir
