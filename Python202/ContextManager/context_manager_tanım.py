# ----------------------------------------------------------------------------------
# 📘 BAĞLAM YÖNETİCİSİ (CONTEXT MANAGER) NEDİR?
#
# Bağlam yöneticisi, bir kaynağın kullanımını belirli bir işlem bloğuyla sınırlandırmak
# ve bu kullanım sürecini güvenli ve kontrollü şekilde yönetmek için kullanılan bir yapıdır.
#
# En temel amacı, kaynakların (örneğin dosya, veritabanı bağlantısı, kilit, vb.) açılması,
# kullanılması ve ardından otomatik olarak temizlenmesidir.
#
# Python'da "with" ifadesi, bağlam yöneticilerini kullanmak için özel olarak tasarlanmıştır.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🎯 NEDEN KULLANILIR?
#
# - Otomatik Temizlik: Kaynaklar, işlem tamamlandığında otomatik olarak kapatılır.
# - Hata Güvenliği   : with bloğu içinde hata olsa bile kaynak temizlenir.
# - Okunabilirlik    : Kodun ne zaman başlayıp ne zaman bittiği net şekilde anlaşılır.
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# 🧰 KULLANIM ALANLARI
#
# - Dosya işlemleri (open)
# - Veritabanı bağlantıları
# - Thread/multiprocessing kilitleri
# - Zaman ölçümü / profiling
# - Kaynak sınırlı işlemler (örneğin GPU kullanımı)
# - Geçici değişiklikler (ortam değişkenleri gibi)
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# ⚙️ NASIL ÇALIŞIR?
#
# Bir bağlam yöneticisi, arkaplanda iki özel metodu kullanır:
#
#  __enter__() : with bloğuna girerken çalışır, kaynak açılır/hazırlanır.
#  __exit__()  : with bloğundan çıkarken çalışır, kaynak kapatılır/temizlenir.
#
# Bu iki metodu içeren herhangi bir sınıf, bir bağlam yöneticisi olarak kullanılabilir.
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# 🧾 ÖZET
#
# Bağlam yöneticileri, kaynak yönetimiyle ilgili kodları daha sade, güvenli
# ve hataya dayanıklı hale getirmek için kullanılan güçlü araçlardır.
#
# "with" anahtar kelimesiyle birlikte kullanılarak, aç-kullan-kapat desenini
# otomatikleştirir ve geliştirici hatalarını minimize eder.
# ----------------------------------------------------------------------------------
