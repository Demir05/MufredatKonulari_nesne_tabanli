# ---------------------------------------------------------
# 📦 PYTHON'DA `import` ve `from ... import ...` MEKANİZMALARI
# ---------------------------------------------------------

# -----------------------------------
# 1️⃣ `import x`
# -----------------------------------
# 🔹 Amaç: Bir modülün tamamını içeri aktarmak.
# 🔹 Etki: `x` ismini *bulunduğu scope*'a (genellikle modülün global scope'u) ekler.
# 🔹 Teknik olarak: `globals()["x"] = <module x>`
# 🔹 Yükleme: Tüm modül belleğe alınır (sys.modules’e eklenir)
# 🔹 Erişim: `x.something` şeklinde dot notation ile yapılır.

# ✔️ Örnek:
# import math
# math.sqrt(9)

# 📌 `import x` ifadesi, arka planda `__import__("x")` fonksiyonunu tetikler.
#     Bu sayede Finder → Loader zinciri çalışır ve modül yüklenir.


# -----------------------------------
# 2️⃣ `from x import y`
# -----------------------------------
# 🔹 Amaç: Modül içindeki belli bir öğeyi (y) doğrudan içeri aktarmak.
# 🔹 Etki: `y` ismini *bulunduğu scope*'a ekler.
# 🔹 Teknik olarak: `globals()["y"] = getattr(__import__("x", fromlist=["y"]), "y")`
# 🔹 Yükleme: `x` modülünün tamamı belleğe alınır (tüm modül yüklenir!)
# 🔹 Erişim: Direkt `y` ile yapılır. (modül ismine gerek kalmaz)

# ✔️ Örnek:
# from math import sqrt
# sqrt(9)

# 📌 Yani `from` ifadesi, sadece `y`'yi yüklemez — önce `x` modülünü tam olarak yükler,
#     sonra `y` nesnesini o modülün içinden çeker ve yerleştirir.


# -----------------------------------
# ⚖️ Karşılaştırma: import vs from-import
# -----------------------------------
# import x                 → isim: x         → erişim: x.something
# from x import y          → isim: y         → erişim: y (doğrudan)
#                          → Ama yine de `x` modülü yüklenmiş olur

# -----------------------------------
# 🧠 Bellek ve Scope
# -----------------------------------
# 🔹 `import` veya `from` ifadeleri, bulundukları scope’a göre çalışır:
#    - Modül düzeyinde ise → modülün global namespace’ine eklenir
#    - Fonksiyon içinde ise → fonksiyonun local scope’una eklenir

# ✔️ Fonksiyon içi örnek:
# def f():
#     import math       # sadece bu fonksiyona özel
#     print(math.pi)

# -----------------------------------
# 🔍 Arka Plan: Stack ve Heap
# -----------------------------------
# - Modül nesnesi: Heap bellekte tutulur
# - Modül adı (örn. math): Scope içindeki değişken (stack/register) olarak referanslanır
# - Yani: `math` ismi stack’te, `math` modülü heap’tedir

# -----------------------------------
# 🛠️ fromlist Parametresi (advanced)
# -----------------------------------
# `__import__()` fonksiyonunda `fromlist=["..."]` parametresi verildiğinde:
# → modülün altındaki öğe(ler) yüklenir
# → nokta (".") verilmesi → modülün `__name__`’ini koruyarak alt modül ithal eder

# Örnek:
# __import__("package.module", fromlist=["."]) → sadece "module" kısmını getirir

# -----------------------------------
# ✅ Performans
# -----------------------------------
# 🔹 `import` ve `from` ifadeleri performans açısından benzer yük getirebilir
# 🔹 Çünkü `from x import y` de modülün tamamını yükler
# 🔹 Ama `import x` daha okunabilir ve hataları azaltır (örneğin circular import riskinde)

# -----------------------------------
# 🧪 PEP Bağlantıları
# -----------------------------------
# PEP 302 – Import hook mekanizması
# PEP 451 – ModuleSpec tabanlı import sistemi
# PEP 562 – Modül düzeyinde `__getattr__` ve `__dir__`



# --------------------------------------------------------
# 🧠 Fonksiyon İçi `import` Kullanımı – Avantajları ve Riskleri
# --------------------------------------------------------

# -------------------------------------
# ✅ Avantajları:
# -------------------------------------

# 1. Bellek Tasarrufu:
#    - `import` işlemi fonksiyon içinde yapıldığında, sadece o scope içinde yaşar.
#    - Fonksiyon bittiğinde bu isim referans dışı kalır ve GC tarafından temizlenebilir.
#    - Bu, özellikle büyük kütüphaneler için bellek tüketimini azaltır.

# 2. Başlangıç Süresi Optimizasyonu:
#    - Uygulama başlatılırken import yapılmaz, sadece gerektiğinde yapılır.
#    - Bu, "soğuk başlangıç" süresini azaltır (CLI araçları veya mikro servisler için kritik olabilir).

# 3. Dairesel Import Sorunlarını Azaltır:
#    - Modüller sadece ihtiyaç anında import edildiğinden, modül düzeyindeki `circular import`'lar önlenebilir.

# -------------------------------------
# ❌ Dezavantajları:
# -------------------------------------

# 1. Kod Okunabilirliği Azalır:
#    - Fonksiyon içinde `import` görmek alışılmadık olabilir.
#    - Geliştirici kodun dışına bakmadan hangi modüllerin kullanıldığını göremez.

# 2. IDE Desteği Sınırlanır:
#    - PyCharm gibi IDE'ler fonksiyon içindeki `import`’ları statik analizle çözemez.
#    - Otomatik tamamlama (autocomplete) ve hata denetimi zayıflar.

# 3. Mikro Maliyetler:
#    - Her çağrıda `import` satırı tekrar çalışır (ama modül tekrar yüklenmez).
#    - `sys.modules`'den referans alınır. Bu işlem hızlıdır ancak çok sık çalışıyorsa etki yaratabilir.

# -------------------------------------
# 📌 Ne Zaman Kullanılmalı?
# -------------------------------------

# ✅ Modül büyük ve nadiren kullanılıyorsa
# ✅ Başlangıç performansı kritikse (örn. CLI araçları)
# ✅ Circular import riski varsa
# ❌ Küçük yardımcı modüllerde gerek yoktur
# ❌ Performans kritik fonksiyonlarda tekrar maliyeti yaratabilir
# ❌ IDE entegrasyonu önemliyse (geliştirici deneyimi için)

# -------------------------------------
# 📝 Sonuç:
# -------------------------------------

# Python `import` işlemi genelde düşük maliyetlidir.
# Ancak LIFO mantığıyla (kullan-çıkart) çalışan sistemlerde,
# `import`’u fonksiyon içinde yapmak daha hafif bir runtime deneyimi sunar.
# Karar verirken okunabilirlik, bellek, performans ve IDE desteği birlikte değerlendirilmelidir.


