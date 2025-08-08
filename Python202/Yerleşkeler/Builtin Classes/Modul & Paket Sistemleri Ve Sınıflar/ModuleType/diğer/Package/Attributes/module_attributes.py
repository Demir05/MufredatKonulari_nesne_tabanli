# ──────────────────────────────
# 🧠 PYTHON MODÜL ATTRIBUTE'LARI
# ──────────────────────────────

# __name__ 📛
# Modülün ismini belirtir (örn. 'os', 'myapp.utils').
# Bu isim, modülün import edildiği tam yolu gösterir.
# Genellikle import işlemi sırasında atanır.
# → Farkı: __name__ sadece tanımlayıcıdır, modülün fiziksel konumu veya dosyası hakkında bilgi vermez.

# __doc__ 📘
# Modülün en üst kısmında tanımlanan docstring burada tutulur.
# Eğer docstring yoksa None olur.
# → Farkı: Tamamen açıklama amaçlıdır; programın davranışını etkilemez.

# __dict__ 🧰
# Modül içeriğindeki tüm isimleri ve değerleri tutan sözlüktür (fonksiyonlar, sınıflar, değişkenler...).
# Bu dictionary, modülün *namespace’idir*.
# → Farkı: Diğer attribute'lar meta veri tutarken, __dict__ modülün gerçek içeriğini barındırır.

# __file__ 📂
# Modülün kaynak kodunun bulunduğu dosyanın tam dosya yoludur.
# Derlenmiş modüllerde .pyc dosyasını da gösterebilir.
# → Farkı: origin gibi konumu belirtir ama bu attribute sadece dosya sistemi ile ilgili fiziksel referanstır.
# → __file__ != origin her zaman; çünkü origin mantıksal kaynak olabilir ("built-in", "frozen" gibi).

# __package__ 🎁
# Modülün ait olduğu paket adını belirtir.
# Bu, relative import’ların düzgün çalışması için kullanılır.
# → Örnek: 'myapp.utils.parser' modülünde, __package__ = 'myapp.utils'
# → Farkı: __name__ tam yolken, __package__ modülün ait olduğu üst seviye paket yoludur.

# __loader__ 📦
# Modülü nasıl yükleyeceğimizi belirleyen objedir.
# Bu, SourceFileLoader, FrozenImporter gibi bir sınıf olabilir.
# → Farkı: __file__ ve origin konumu gösterirken, __loader__ bu konumdan nasıl yükleneceğini belirtir.

# __spec__ 🧬
# importlib.machinery.ModuleSpec nesnesidir.
# Bu, modülün import sürecine dair tüm detayları içerir:
# → name, origin, loader, is_package, loader_state vs.
# → __spec__.origin → modülün kaynak yeri (dosya, built-in vb.)
# → __spec__.loader → yükleyici nesnesi
# → __spec__.is_package → True/False
# → Farkı: Tüm import metadata’sını kapsayan merkezi yapıdır.
# Diğer birçok attribute (__file__, __loader__, __package__) bu yapının içinden türetilir.

# __cached__ 💾
# Derlenmiş bytecode dosyasının (.pyc) yolu.
# Yalnızca .py dosyası varsa ve import edildiğinde oluşur.
# → Farkı: runtime performansı için kullanılır, modülün kendisiyle doğrudan bağlantılı değildir.

# __path__ 🛣️
# Sadece paketlerde tanımlanır (__init__.py varsa).
# Bu, alt modüllerin nerelerde aranacağını gösteren liste.
# Örn: ["./myapp/utils"]
# → Farkı: __file__ tek bir dosya iken, __path__ birden fazla dizin içerir.
# → __package__ → mantıksal bağ, __path__ → fiziksel dosya arama yolları.

# __builtins__ 🧱
# Built-in fonksiyonların bulunduğu sözlük ya da modül.
# import edilen her modülde bulunur; runtime tarafından atanır.
# → Farkı: Global değil, lokal scope’da atanır ama Python tarafından otomatik eklenir.


# ──────────────────────────────
# 🧠 ModuleSpec ALANLARI
# ──────────────────────────────

# name 🔤
# Tam modül ismi ('myapp.utils.parser')
# → __name__ ile aynı gibi görünse de __spec__.name her zaman string olarak import mekanizması içindir.

# loader 🔄
# Modülün nasıl yükleneceğini belirleyen nesnedir.
# Aynı zamanda modülün __loader__ attribute’una atanır.

# origin 📍
# Modülün geldiği fiziksel konum veya kaynak tanımı.
# Örn: '/home/user/code/utils.py', 'built-in', 'frozen'
# → __file__ ile benzer görünür ama __spec__.origin, daha mantıksal bir işlev görür.
# → Örneğin __spec__.origin = "built-in" olabilir ama __file__ yoktur.

# is_package ✅
# True ise, bu modül bir pakettir (__init__.py içerir).
# __spec__.is_package sayesinde __path__ atanabilir hale gelir.

# submodule_search_locations 🔍
# Eğer modül bir paket ise, içindeki alt modüller için taranacak klasörler.
# Bu genelde __path__ olarak modül objesine atanır.

# loader_state 🧬
# Yükleme sırasında kullanılan özel state bilgisi.
# Örn: Bytecode cache bilgisi, analiz verisi vs.

# has_location 📌
# origin varsa True olur. Dosya sistemine bağlı olmayan modüller (built-in gibi) için False.

# cached 🗃️
# Derlenmiş modül (pyc) varsa, onun dosya yolu buraya yazılır.
# Genelde __cached__ attribute’una atanır.

