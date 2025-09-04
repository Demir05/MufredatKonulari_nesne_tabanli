# ----------------------------------------------------------------------------------
# 📘 `with` İFADESİNİN FELSEFESİ – NEDEN VAR? NEYİ TEMSİL EDER?
#
# Python'daki "with" ifadesi, sadece teknik bir özellik değil; yazılımda
# "doğru şekilde kaynak yönetimi" ve "geçici durumların kontrolü" için geliştirilmiş,
# minimalist ve sade bir tasarım felsefesinin ürünüdür.
#
# with, geliştiriciye şunu der:
#   "Bir şeyi kullan, işin bitince onu unutma, ben senin yerine geri bırakırım."
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🌱 ANA FELSEFE: "KULLAN VE GERİ BIRAK"
#
# with ifadesi, bir nesnenin ya da kaynağın kontrollü kullanımını sağlar.
# Kaynağı belli bir bağlam (context) içinde geçici olarak kullanır ve ardından otomatik olarak temizler.
#
# Bu kaynak:
# - Bir dosya olabilir
# - Bir veritabanı bağlantısı olabilir
# - Bir kilit olabilir
# - Bir zaman ölçer olabilir
# - Ya da sadece geçici bir ayar bile olabilir
#
# Temel düşünce: "Bir işlemi başlat, kullan, ardından ortamı eski haline döndür."
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🧘‍♂️ ZEN OF PYTHON ve `with`
#
# with ifadesi, Python'un temel tasarım ilkeleriyle birebir örtüşür:
#
# - Explicit is better than implicit → Kaynağın açıkça kullanımı ve kapanışı belli
# - Simple is better than complex   → try-finally yerine tek satırla kaynak yönetimi
# - Readability counts              → Ne zaman başladığı ve bittiği açık olan kod
#
# with, bu sayede güvenli, sade ve okunabilir kod yazımını destekler.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 📦 with = "Geçici Evren"
#
# with bloğu, adeta geçici bir evren yaratır:
# - Kaynak ya da durum burada aktif olur
# - İşlem tamamlanınca evren kapanır ve her şey eski haline döner
#
# Gerçek hayattaki örneği:
#   Komşudan matkap alırsın → kullanırsın → işin bitince geri verirsin
#   Ama unutma riskin varsa? with bunu senin yerine yapar :)
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🔄 SADECE KAYNAK DEĞİL, GEÇİCİ DURUM YÖNETİMİDİR
#
# `with`, sadece dosya ya da bağlantı açmak için değil;
# her türlü "giriş-yap → işlem → çıkış-yap" yapıları için kullanılabilir.
#
# Örneğin:
# - Terminalde renk geçici olarak değiştirilebilir
# - Ortam değişkeni geçici olarak set edilebilir
# - Bir klasör içerisine geçici olarak girilebilir
# - Zaman ölçümü yapılabilir
#
# Kısacası: Geçici bir şey varsa ve sonra eski haline dönmesi gerekiyorsa,
# orada with kullanılabilir.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🧾 ÖZET
#
# `with`, Python'un temiz, açık ve güvenli yazılım geliştirme felsefesini temsil eder.
# Kaynakları unutmadan yönetmek, geçici durumları doğru şekilde sarmak
# ve hata olasılığı olan yerlerde güvenli bir yapı kurmak için ideal bir çözümdür.
#
# Bir işlem geçici ise ve sonunda toparlanması gerekiyorsa:
#     with kullanılır. Nokta.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 📘 `with` NEDİR? — SÖZEL TANIM
#
# `with` ifadesi, Python'da kaynakların güvenli ve kontrollü bir şekilde
# kullanılması için geliştirilmiş bir kontrol yapısıdır.
#
# Kaynağın kullanıldığı işlem bloğuna bir "bağlam" (context) tanımlar:
# - Girişte hazırlık yapılır (kaynak açılır)
# - Çıkışta temizlik yapılır (kaynak kapatılır)
#
# Böylece "aç-kullan-kapat" desenini daha sade, güvenli ve otomatik hale getirir.
#
# Python'un okunabilir, hataya dayanıklı ve temiz kod yazma felsefesiyle uyumludur.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🔍 `with` KENDİSİ NE TÜR BİR YAPI?
#
# `with`, Python'da yerleşik (built-in) bir **kontrol deyimi**dir (statement).
# Yani bir fonksiyon veya sınıf değildir.
#
# Ancak `with` ifadesi, kullandığı nesnenin bir **context manager** (bağlam yöneticisi)
# olmasını bekler. Bu nedenle `with` ifadesi içinde kullanılan nesne:
#
# ✅ Ya özel metotlar içeren bir sınıf (class) olmalıdır
# ✅ Ya da `contextlib.contextmanager` gibi bir araçla sarmalanmış bir fonksiyon olabilir
#
# Yani `with` ifadesinin çalışması için, "içine verilen şeyin" belirli protokolü uygulaması gerekir.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# ⚙️ GEREKEN PROTOKOL: `__enter__` ve `__exit__`
#
# with ile kullanılacak olan bir sınıf mutlaka şu iki özel (dunder) metoda sahip olmalıdır:
#
# 1️⃣ __enter__(self)
#     - `with` bloğuna girildiğinde çalışır
#     - Kaynak veya ortam hazırlanır
#     - Genellikle "as" ile atanan nesneyi döndürür
#
# 2️⃣ __exit__(self, exc_type, exc_value, traceback)
#     - `with` bloğundan çıkıldığında çalışır
#     - Normal çıkış veya hata fark etmeksizin çağrılır
#     - Kaynak kapatılır, temizlik yapılır
#     - Eğer hata olduysa, bu metodun içinde yönetilebilir
#
# Not: Bu metotlar, Python'un "context management protocol" olarak bilinen
# bir sözleşmenin parçasıdır.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🧪 GEREKLİ OLAN ATTRIBUTE'LAR (DUENDER METHODLAR)
#
# Bir nesnenin `with` içinde kullanılabilmesi için aşağıdaki özellikleri taşıması gerekir:
#
#   ➤ hasattr(obj, '__enter__') == True
#   ➤ hasattr(obj, '__exit__') == True
#
# Bu iki metot varsa, Python nesneyi context manager olarak kabul eder.
# Bu durumda:
# - `__enter__()` ile işlem başlatılır
# - `__exit__()` ile işlem sonlandırılır
#
# Bu, özel bir arayüz gibi düşünülebilir. `with`, sadece bu protokolü tanır.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# ✅ ÖZET
#
# - `with` = Python'da yerleşik bir kontrol yapısıdır (statement)
# - Kendi başına sınıf ya da fonksiyon değildir
# - Ancak içinde kullanılan nesne bir context manager olmalıdır
# - Context manager olabilmek için __enter__ ve __exit__ metotlarına sahip olmak gerekir
#
# Bu yapılar sayesinde kaynaklar:
# - Güvenli şekilde açılır ve kapatılır
# - Hatalardan korunur
# - Otomatik olarak temizlenir
#
# Bu sade ama güçlü yapı, Python'un sadelik, okunabilirlik ve güvenlik ilkeleriyle doğrudan örtüşür.
# ----------------------------------------------------------------------------------
