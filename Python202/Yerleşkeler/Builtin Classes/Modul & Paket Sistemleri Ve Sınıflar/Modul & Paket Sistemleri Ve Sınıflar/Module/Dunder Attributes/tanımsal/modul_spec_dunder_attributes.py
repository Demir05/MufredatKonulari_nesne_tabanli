# name
# - Modülün tam adı (örnek: "os.path").
# - importlib bunu, import edilen isme göre otomatik set eder.
# - Elle set: spec = ModuleSpec("lib.utils", loader=..., origin=...)
# - Özel: sys.modules sözlüğünde bu ad ile saklanır.
# - Modül nesnesi etkisi: mod.__name__ bu değerle eşleşmelidir (uyum şart).

# loader
# - Bu spec üzerinden modülü yükleyecek "loader" nesnesi.
# - Örnek: SourceFileLoader("moduladi", "dosya_yolu.py").
# - Elle set: spec.loader = my_custom_loader
# - Özel: mod.__loader__ bu loader ile eşleştirilir.
# - Alternatif: Memory/namespace modüllerde loader farklı tiptedir.

# origin
# - Modülün geldiği kaynak: dosya yolu, "<built-in>", "<frozen>", "<inmemory>".
# - Elle set: spec.origin = "/abs/path/to/file.py"
# - Özel: mod.__file__ genellikle buradan türetilir (eğer disk tabanlı modülse).
# - Alternatif: built-in modüllerde "<built-in>" olur, dolayısıyla mod.__file__ bulunmaz.

# submodule_search_locations
# - SADECE paketlerde dolu olur.
# - Liste benzeri bir nesne: alt modüllerin aranacağı dizinler.
# - Özel durum: Eğer spec.is_package = True ise → bu alan otomatik bir liste ile doldurulur.
# - Modül nesnesine etkisi: mod.__path__ bu değer ile set edilir.
# - Elle set: spec.submodule_search_locations = ["/abs/path/to/pkg"]

# parent
# - Eğer bir üst modül varsa (ör. "pkg.mod" → parent = "pkg").
# - Elle set edebilirsin ama genellikle importlib hesaplar.
# - Özel: mod.__package__ değerinin belirlenmesinde kullanılır.
# - Alternatif: Parent yoksa boş string "" olur (top-level modül).

# has_location
# - Bool: Modülün fiziksel bir kaynağı var mı?
# - True → origin geçerli bir yol ya da kaynak.
# - False → built-in veya dinamik modüller.
# - Elle set: spec.has_location = False
# - Özel: importlib, mod.__file__ olup olmamasına göre karar verebilir.

# cached
# - Derlenmiş bytecode (.pyc) dosyası yolu.
# - importlib/loader tarafından doldurulur.
# - Elle set: spec.cached = "__pycache__/modul.cpython-311.pyc"
# - Modül nesnesine etkisi: mod.__cached__ genelde bu değeri alır.
# - Alternatif: in-memory veya built-in modüllerde None kalabilir.

# loader_state
# - Loader’a özel geçici veri saklama alanı.
# - Genelde custom loader’lar kendi iç bilgilerini buraya koyar.
# - Elle set: spec.loader_state = {"token": "...", "opts": {...}}
# - Modül nesnesine doğrudan bir karşılığı yoktur (sadece loader kullanır).

# is_package
# - Bool: Modül bir paket mi?
# - importlib, __init__.py dosyası üzerinden otomatik belirler.
# - Elle set: spec = ModuleSpec("pkg", loader=..., origin=".../__init__.py", is_package=True)
# - Özel: True ise → spec.submodule_search_locations otomatik listeye dönüşür.
#           ve bu da → mod.__path__ alanının oluşmasına sebep olur.
# - False ise: submodule_search_locations = None, dolayısıyla mod.__path__ olmayacaktır.
