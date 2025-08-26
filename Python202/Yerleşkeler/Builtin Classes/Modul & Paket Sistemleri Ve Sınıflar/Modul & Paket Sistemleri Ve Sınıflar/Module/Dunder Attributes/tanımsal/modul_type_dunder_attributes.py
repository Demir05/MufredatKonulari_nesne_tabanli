# __cached__
# - Amaç: Derlenmiş bytecode (.pyc) dosyasının tam yolu.
# - Kim set eder: importlib/loader (dosya tabanlı modüllerde otomatik).
# - Elle set: mod.__cached__ = "__pycache__/demo.cpython-311.pyc"
# - Not: Memory/URL/built-in yüklemelerde olmayabilir ya da None kalabilir.
# - Alternatif: __spec__.cached genelde aynı bilgiyi taşır (tercih edilen kaynak spec).

# __builtins__
# - Amaç: Modülün global alanında kullanılacak yerleşik isimler (print, len, ...).
# - Kim set eder: CPython, modül yürütülürken otomatik.
# - Elle set: mod.__builtins__ = builtins   # nadiren gerekir.
# - Dikkat: Değiştirirsen sadece o modülün içindeki builtins etkilenir (çok özel durumlar dışında dokunma).

# __dict__
# - Amaç: Modülün namespace’i; tüm tanım ve değerleri burada tutulur.
# - Kim set eder: Otomatik; exec/import ile kod çalıştıkça dolar.
# - Elle set: mod.__dict__["NAME"] = value (veya vars(mod)["NAME"] = value)
# - Alternatif: exec(source, mod.__dict__) ile toplu yükleme/patch mümkündür.

# __annotations__
# - Amaç: Modül seviyesindeki type hint’ler (PEP 526).
# - Kim set eder: Python, tanım yaptıkça otomatik (boş dict ile başlar).
# - Elle set: mod.__annotations__ = {"x": int}
# - İpucu: from __future__ import annotations ile stringleştirilmiş anotasyonlar görebilirsin.

# __all__
# - Amaç: from module import * davranışını sınırlar; dışa açılan API yüzeyini belirler.
# - Kim set eder: Programcı (otomatik set edilmez).
# - Elle set: mod.__all__ = ["foo", "Bar", "CONST"]
# - Alternatif: __all__ tanımlı değilse “yıldız import” isimleri, alttan çizgi ile başlayanlar hariç, modül içeriğinden türetilir.

# __path__
# - Amaç: SADECE paketlerde bulunur; alt modüllerin aranacağı dizinlerin listesi.
# - Kim set eder: importlib (paket ise __spec__.submodule_search_locations üzerinden).
# - Elle set (paket oluşturuyorsan): mod.__path__ = ["/abs/path/to/pkg"]
# - Alternatif: __spec__.submodule_search_locations ile senkron tutulur; is_package=False ise None olur.

# (Opsiyonel) __getattr__  (PEP 562)
# - Amaç: Modül düzeyinde tembel/özel attribute çözümü (name bulunamadığında çağrılır).
# - Kim set eder: Programcı (isteğe bağlı).
# - Elle set:
#       def __getattr__(name):
#           if name == "heavy": import heavy as _h; return _h.value
#           raise AttributeError(name)
# - Alternatif: Tembel import/geriye dönük uyumluluk için faydalı.

# (Opsiyonel) __dir__  (PEP 562)
# - Amaç: dir(module) çıktısını özelleştirmek (gizlemek/eklemek).
# - Kim set eder: Programcı.
# - Elle set:
#       def __dir__(): return ["public_api", "version"]
# - Alternatif: __all__ ile birlikte dışa açık yüzeyi düzenleyebilirsin.

# (Konvansiyonel) __version__
# - Amaç: Modül sürümü (resmi zorunluluk değil, topluluk konvansiyonu).
# - Kim set eder: Programcı.
# - Elle set: __version__ = "1.2.3"
# - Alternatif: importlib.metadata.version("paket-adi") ile paket sürümünü dışarıdan oku.

# (Konvansiyonel) __author__, __license__
# - Amaç: Meta bilgi (belgeleme).
# - Kim set eder: Programcı.
# - Elle set: __author__ = "Ad Soyad", __license__ = "MIT"
# - Not: Araçlar/dokümantasyon için yararlıdır, zorunlu değildir.


# __name__
# - Modülün adı. (örn: "os", "os.path", "__main__")
# - sys.modules içinde anahtar olarak kullanılacak olan string.
# - Otomatik: import sırasında set edilir.
# - Manuel: mod = ModuleType("mymod") → mod.__name__ = "mymod"
# - Önem: modül eşsiz kimlik. Farklı __name__ ile yüklenirse aynı dosya bile olsa iki ayrı modül gibi davranır.

# __package__
# - Modülün ait olduğu paket ismi (string).
# - Paket içi import mekanizmasında kullanılır (relative import için kritik).
# - Örnek: "os.path" modülünde __package__ = "os"
# - Top-level modülse: "" (boş string) olur.
# - Manuel set: mod.__package__ = mod.__name__.rpartition(".")[0]
# - Eğer yanlış set edilirse → "from . import x" gibi relative import’lar çalışmaz.

# __file__
# - Modülün kaynak dosyasının yolu (string).
# - Diskten yüklenen modüllerde otomatik set edilir.
# - Built-in modüllerde yoktur → AttributeError atabilir.
# - Manuel set: mod.__file__ = "/path/to/mymod.py"
# - Kullanım: hata ayıklama, reload, importlib introspection.

# __loader__
# - Bu modülü yükleyen loader nesnesi.
# - Örnek: <_frozen_importlib_external.SourceFileLoader object ...>
# - importlib otomatik set eder.
# - Manuel set: mod.__loader__ = my_custom_loader
# - Kullanım: tekrar yükleme, introspection, özel import mekanizmaları.

# __spec__
# - Modülün yüklenme detaylarını tutan ModuleSpec nesnesi.
# - importlib.import_module vs. otomatik doldurur.
# - Manuel set: mod.__spec__ = importlib.util.spec_from_file_location("name", "file.py")
# - Kullanım: modülün tam meta bilgisini (origin, loader, parent vs.) taşır.

# __doc__
# - Modülün docstring’i.
# - Kaynak dosyada en üstteki üç tırnaklı string alınır.
# - import sırasında otomatik set edilir.
# - Manuel set: mod.__doc__ = "Bu benim özel modülüm."
# - Kullanım: help(mod) çağrısında, IDE tooltips.
