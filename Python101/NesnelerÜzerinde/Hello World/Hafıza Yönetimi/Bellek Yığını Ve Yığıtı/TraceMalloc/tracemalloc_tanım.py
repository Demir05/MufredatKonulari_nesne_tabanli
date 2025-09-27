# 📦 tracemalloc — yalnızca sözel/teorik açıklama (tamamı yorum satırı)
# -----------------------------------------------------------------------------
# 🌱 NEDİR?
# tracemalloc, Python’un standart kütüphanesinde yer alan bir modüldür.
# Python nesneleri için yapılan Heap bellek tahsislerini (allocation) izler ve
# “hangi kod satırı/traceback/modül ne kadar bellek ayırdı?” sorusuna cevap verir. 🧠

# -----------------------------------------------------------------------------
# 🎯 AMACI NEDİR?
# • Bellek kullanımını görünür kılmak (şeffaflık)
# • Bellek sızıntılarını (leak) ve gereksiz tahsisleri tespit etmek
# • “Önce/Sonra” karşılaştırmalarıyla regresyon (zamanla artış) analizi yapmak 📈

# -----------------------------------------------------------------------------
# ⏰ NE ZAMAN KULLANILIR?
# • Uzun süre çalışan servislerde bellek sürekli artıyorsa
# • Büyük veri işleyen betiklerde beklenenden fazla bellek harcanıyorsa
# • Refactor/versiyon geçişi sonrası bellek farkını kıyaslamak istiyorsan
# • Kütüphane geliştirirken API çağrılarının bellek etkisini ölçmek istediğinde 🔍

# -----------------------------------------------------------------------------
# 🧩 NASIL ÇALIŞIR? (YÜKSEK SEVİYE)
# 1) İzlemeyi başlatırsın → tracemalloc, “bu andan sonra” yapılan tahsisleri kaydeder
# 2) Bir “snapshot” (anlık görüntü) alırsın → o ana kadar biriken izlerin fotoğrafı
# 3) Sonra bir snapshot daha alırsın → iki snapshot’ı karşılaştırıp farkı (delta) görürsün
# 4) Raporu; dosya adı, satır numarası veya traceback’e göre özetleyebilirsin 🗺️

# -----------------------------------------------------------------------------
# 🧱 TEMEL KAVRAMLAR
# • Tracing (izleme): start() ile açılır, stop() ile kapanır
# • Snapshot (anlık görüntü): take_snapshot() ile alınır; o ana kadarki tahsis özeti
# • Traceback: Bir tahsisin geldiği çağrı zinciri (hangi fonksiyon/satır dizisi)
# • Statistics: Snapshot’tan çıkarılan, dosya/satır/traceback’e göre gruplanmış özet tablolar
# • Filters: Belirli yolları/modülleri dahil etme/etmeme (gürültüyü azaltır) ✂️

# -----------------------------------------------------------------------------
# 🧪 NELERİ TAKİP EDER / ETMEZ?
# ✅ Python nesnelerinin bellek tahsislerini izler (pymalloc katmanı)
# ❌ Her yerel (native) C bellek tahsisini göremez (özellikle bazı 3. parti C uzantıları)
# ❌ İşletim sistemi seviyesindeki toplam süreç belleği (RSS) bilgisini doğrudan vermez
# ✅ “Python kaynaklı bellek artışı”nı anlamak için idealdir 🧭
