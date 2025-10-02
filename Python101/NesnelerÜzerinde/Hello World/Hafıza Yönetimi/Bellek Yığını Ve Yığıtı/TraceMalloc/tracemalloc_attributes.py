# tracemalloc modülü: Python'da bellek tahsislerini izlemek için kullanılır.
# Özellikle hangi satırın ne kadar bellek kullandığını görmek, sızıntı tespiti yapmak ve optimizasyon için idealdir.

import tracemalloc

# ------------------------------------------------------------
# 📌 start(n_frames=1)
# Bellek izlemeyi başlatır.
# n_frames: her tahsis edilen nesne için kaç adet traceback karesi tutulacağını belirler.
# ─────────────────────────────────────────────────────────────
# 🎯 n_frames Ne İşe Yarar?
# - Bellek tahsisi sırasında oluşan çağrı zincirinin kaç adımını saklayacağını belirler.
# - Daha fazla n_frames → daha derin analiz (fonksiyon zinciri görünür)
# - Daha az n_frames → daha az bellek tüketimi, ama yüzeysel analiz

# ─────────────────────────────────────────────────────────────
# 🔢 Bellek Tüketimi Üzerindeki Etkisi (Yaklaşık)
# Her nesne için tutulan traceback karesi başına bellek artışı olur.
# Aşağıdaki değerler nesne başına tahmini ek bellek maliyetidir:

# n_frames = 1   → ~200–300 byte (sadece son satır tutulur)
# n_frames = 5   → ~1.2–1.5 KB   (orta seviye analiz)
# n_frames = 10  → ~2.5–3 KB     (derin analiz için yeterli)
# n_frames = 25  → ~6–8 KB       (tam çağrı zinciri, büyük projelerde önerilir)

# Örnek: 10.000 nesne tahsis edildiğinde
# n_frames = 1   → ~2–3 MB
# n_frames = 10  → ~25–30 MB
# n_frames = 25  → ~60–80 MB

# ─────────────────────────────────────────────────────────────
# ✅ Ne Zaman Yeterli?
# - Basit tahsisler (örneğin: data = list(range(10000))) → n_frames = 1 yeterlidir.
# - Derin fonksiyon zincirleri varsa → n_frames = 10+ önerilir.

# ─────────────────────────────────────────────────────────────
# ⚠️ Dikkat Edilmesi Gerekenler
# - Çok yüksek n_frames → daha fazla bellek ve işlem maliyeti
# - Çok düşük n_frames → analiz gücü azalır (sadece son satır görünür)
# - Genelde n_frames = 10 iyi bir başlangıçtır; derin sistemlerde 25+


# Traceback karesi: Bellek tahsisi sırasında çağrı zincirindeki fonksiyon/satır bilgileri.
# Örn: A → B → C → tahsis → traceback = [A, B, C]
# Bu sayede hangi kod parçasının bellek tahsisine neden olduğunu anlayabiliriz.
tracemalloc.start(n_frames=10)

# ------------------------------------------------------------
# 📌 is_tracing()
# Bellek izleme aktif mi? True/False döner.
print("İzleme açık mı?", tracemalloc.is_tracing())  # True

# ------------------------------------------------------------
# 📌 get_traceback_limit()
# start() ile belirlenen traceback derinliğini döner.
print("Traceback derinliği:", tracemalloc.get_traceback_limit())  # 10

# ------------------------------------------------------------
# 📌 get_traced_memory()
# Anlık ve maksimum bellek kullanımını verir (byte cinsinden).
# Anlık kullanım: izleme başladığı itibaren tahsis edilen tüm python nesnelerin toplam bellek kullanımı
# Peak: izleme başladığından beri görülen rekor bellek kullanımı miktarı
current, peak = tracemalloc.get_traced_memory()
print(f"Anlık: {current} byte, Zirve: {peak} byte")

# ------------------------------------------------------------
# 📌 reset_peak()
# Maksimum bellek kullanımını sıfırlar (Python 3.9+).
# Yeni ölçüm için temiz başlangıç sağlar.
tracemalloc.reset_peak()

# ------------------------------------------------------------
# 📌 take_snapshot()
# O anki bellek durumunun snapshot'ını alır.
# Snapshot: bellekteki tüm tahsis edilmiş nesnelerin izini tutan bir veri yapısıdır.
snapshot = tracemalloc.take_snapshot()

# ─────────────────────────────────────────────────────────────
# 📌 snapshot.statistics(...) metodu nedir?
# Bu metod, tracemalloc ile alınan snapshot içindeki bellek tahsislerini gruplar.
# Parametreye göre farklı gruplama yapılır: satır, dosya, traceback zinciri veya domain bazlı.
# Her gruplama sonucu bir Statistic nesnesi döner: size, count, average gibi bilgiler içerir.

# ─────────────────────────────────────────────────────────────
# 1️⃣ 'lineno' → Satır bazında gruplama
# Her tahsisi, dosya adı + satır numarasına göre gruplar.
# En çok kullanılan ve en detaylı analiz sağlayan seçenektir.
# Örnek çıktı:
# C:\projeler\orm.py:25: size=8237 KiB, count=99745, average=85 B
# → Bu satırda 99.745 nesne oluşturulmuş, toplamda 8237 KB bellek tahsis edilmiş.

# Bu gruplama sayesinde:
# - Hangi satır en çok bellek tahsis ediyor?
# - Döngü içinde aşırı nesne üretimi var mı?
# - Bellek sızıntısı hangi satırdan kaynaklanıyor?

# ─────────────────────────────────────────────────────────────
# 2️⃣ 'filename' → Dosya bazında gruplama
# Satır numarasını dikkate almaz, sadece dosya adına göre gruplar.
# Örnek çıktı:
# C:\projeler\orm.py: size=12000 KiB, count=100000
# → Bu dosyada toplamda 100.000 nesne oluşturulmuş, 12 MB bellek tahsis edilmiş.

# Bu gruplama sayesinde:
# - Hangi dosya genel olarak daha fazla bellek kullanıyor?
# - Modül bazlı bellek analizi yapılabilir.

# ─────────────────────────────────────────────────────────────
# 3️⃣ 'traceback' → Tam traceback zinciriyle gruplama
# Bellek tahsisine neden olan çağrı zincirini (fonksiyonlar arası geçişleri) dikkate alır.
# Bu, n_frames > 1 ile anlamlı hale gelir.
# Örnek çıktı:
# File "main.py", line 42
# File "utils.py", line 18
# File "core.py", line 7
# → Bu zincir, bellek tahsisine neden olan çağrı yolunu gösterir.

# Bu gruplama sayesinde:
# - Derin fonksiyon zincirlerinde bellek davranışı analiz edilebilir.
# - Karmaşık sistemlerde hangi çağrı dizisi bellek tüketiyor görülebilir.

# ─────────────────────────────────────────────────────────────
# 4️⃣ 'domain' → Domain bazlı gruplama
# Genellikle C uzantılı modüller veya özel tahsis alanları için kullanılır.
# Python kodu için nadiren anlamlıdır.
# Örnek kullanım: farklı modüllerin bellek alanlarını ayırmak.

# ─────────────────────────────────────────────────────────────
# 📊 Her Statistic nesnesi şu bilgileri içerir:
# - .traceback → hangi dosya/satır(lar)da tahsis olmuş
# - .size → toplam tahsis edilen bellek miktarı (byte cinsinden)
# - .count → kaç nesne tahsis edilmiş
# - .average → ortalama nesne boyutu (size / count)

# Bu bilgiler sayesinde:
# - Bellek yoğun satırlar/dosyalar tespit edilir
# - Sızıntı veya gereksiz tahsisler bulunabilir
# - Performans darboğazları analiz edilebilir

# ─────────────────────────────────────────────────────────────
# 🎯 Sonuç:
# snapshot.statistics(...) metodu, bellek tahsislerini farklı açılardan gruplayarak analiz etmeni sağlar.
# 'lineno' → satır bazında en detaylı analiz
# 'filename' → dosya bazında genel bakış
# 'traceback' → çağrı zinciri bazlı derin analiz
# 'domain' → modül/alan bazlı ayrıştırma

# Bu parametreleri doğru seçerek, bellek davranışını çok daha net görebilir ve optimize edebilirsin.


# ------------------------------------------------------------
# 📌 compare_to(other_snapshot, 'lineno')
# İki snapshot arasındaki farkı gösterir.
# Bu, bellek sızıntısı tespiti için çok kullanışlıdır.
import time

# Örnek: iki snapshot arasında fark ölçümü
time.sleep(0.1)  # biraz zaman geçsin
snapshot2 = tracemalloc.take_snapshot()
diff = snapshot2.compare_to(snapshot, 'lineno')

print("\nSnapshot farkları:")
for stat in diff[:5]:
    print(stat)

# ------------------------------------------------------------
# 📌 clear_traces()
# İzleme verilerini temizler ama izlemeyi durdurmaz.
# Yeni snapshot'lar sıfırdan başlar.
tracemalloc.clear_traces()

# ------------------------------------------------------------
# 📌 stop()
# İzlemeyi tamamen durdurur.
# Bellek izleme verileri silinir, snapshot alınamaz hale gelir.
tracemalloc.stop()



import tracemalloc

# ===============================================================
# 📘 tracemalloc.Filter — Bellek İzlerini Filtreleme Rehberi
# ===============================================================

# 🔹 Filter sınıfı, tracemalloc modülünde snapshot içindeki bellek izlerini
#     dosya adı, satır numarası, domain ve stack derinliği gibi kriterlere göre
#     filtrelemek için kullanılır.
#
# Not: Filter sınıfına filename parametresi için mutlak konum verilmelidir. Lib,\Lib gibi kullanımlar geçersizdir
# ---------------------------------------------------------------
# ✅ SÖZDİZİMİ:
# ---------------------------------------------------------------

# tracemalloc.Filter(inclusive, filename_pattern, lineno=None, all_frames=False, domain=None)

# ---------------------------------------------------------------
# ✅ PARAMETRELERİN AÇIKLAMASI:
# ---------------------------------------------------------------

# 🔸 inclusive (bool)
#     - True → eşleşen izleri dahil eder
#     - False → eşleşen izleri hariç tutar
#     - Bu, filtre mantığının temelidir

# 🔸 filename_pattern (str)
#     - Dosya adı, yol veya yol deseni
#     - Örneğin: "my_script.py", "/usr/lib/", "site-packages"

# 🔸 lineno (int veya None)
#     - Belirli bir satır numarasına göre filtreleme
#     - None → tüm satırlar dahil edilir

# 🔸 all_frames (bool)
#     - False → sadece en üstteki frame kontrol edilir
#     - True → tüm stack frame’leri kontrol edilir
#     - Derin analiz için kullanılır

# 🔸 domain (int veya None)
#     - Bellek domain’i (Python 3.6+)
#     - Genellikle None bırakılır

# ---------------------------------------------------------------
# ✅ ÖRNEKLER:
# ---------------------------------------------------------------

# 🔹 Örnek 1: Belirli dosyadan gelen izleri dahil et
filter1 = tracemalloc.Filter(True, "my_script.py")

# 🔹 Örnek 2: Belirli klasörden gelen izleri hariç tut
filter2 = tracemalloc.Filter(False, "/usr/lib/")

# 🔹 Örnek 3: Sadece belirli satırdan gelen izleri dahil et
filter3 = tracemalloc.Filter(True, "my_script.py", lineno=42)

# 🔹 Örnek 4: Stack’in tüm frame’lerinde dosya adı geçen izleri dahil et
filter4 = tracemalloc.Filter(True, "my_script.py", all_frames=True)

# 🔹 Örnek 5: Belirli domain için filtreleme (genellikle kullanılmaz)
filter5 = tracemalloc.Filter(True, "my_script.py", domain=0)

# ---------------------------------------------------------------
# ✅ Filtreyi snapshot’a uygulama
# ---------------------------------------------------------------

# 🔸 Snapshot al
tracemalloc.start()
# ... kod çalışır ...
snapshot = tracemalloc.take_snapshot()

# 🔸 Filtre uygula
filtered_snapshot = snapshot.filter_traces([filter1, filter2])

# 🔸 İstatistikleri al
stats = filtered_snapshot.statistics("lineno")
for stat in stats[:5]:
    print(stat)

# ---------------------------------------------------------------
# ✅ SONUÇ:
# ---------------------------------------------------------------

# ➤ Filter sınıfı, bellek izlerini dosya, satır, domain ve stack derinliği gibi
#     kriterlere göre filtrelemeni sağlar.
# ➤ Bu sayede sadece ilgilendiğin kod parçalarının bellek davranışını analiz edebilirsin.
# ➤ Büyük projelerde gürültüyü azaltmak ve net analiz yapmak için vazgeçilmezdir.


# ===============================================================
# 📘 tracemalloc.Snapshot.filter_traces() — Bellek İzlerini Filtreleme
# ===============================================================

# 🔹 Bu metot, bir Snapshot nesnesi içindeki bellek izlerini filtreler.
# 🔹 Filtreleme, kod tabanlı (Filter) veya bellek alanı tabanlı (DomainFilter) olabilir.
# 🔹 Geriye yeni bir Snapshot döner → sadece filtreye uyan izleri içerir.

# ---------------------------------------------------------------
# ✅ İMZA:
# ---------------------------------------------------------------

# def filter_traces(self, filters: Sequence[DomainFilter | Filter]) -> Snapshot

# 🔸 self → bir tracemalloc.Snapshot nesnesi
# 🔸 filters → Filter veya DomainFilter nesnelerinden oluşan bir liste
# 🔸 dönüş → filtrelenmiş yeni bir Snapshot nesnesi

# ---------------------------------------------------------------
# ✅ PARAMETRELERİN AÇIKLAMASI:
# ---------------------------------------------------------------

# 🔹 filters (Sequence[Filter | DomainFilter]):
#     - Birden fazla filtre içerebilir
#     - Her filtre, bellek izlerini dahil etme veya hariç tutma mantığına göre çalışır

# 🔸 tracemalloc.Filter:
#     - Kod tabanlı filtreleme sağlar
#     - Parametreleri:
#         • inclusive (bool): True → dahil et, False → hariç tut
#         • filename_pattern (str): dosya adı veya yol deseni
#         • lineno (int, optional): belirli satır numarası
#         • all_frames (bool, optional): tüm stack frame’lerinde arama
#         • domain (int, optional): bellek domain’i

# 🔸 tracemalloc.DomainFilter:
#     - Bellek alanı (domain) bazlı filtreleme sağlar
#     - Parametreleri:
#         • inclusive (bool): True → dahil et, False → hariç tut
#         • domain (int): bellek domain numarası

# ---------------------------------------------------------------
# ✅ KULLANIM AMACI:
# ---------------------------------------------------------------

# 🔸 Büyük projelerde sadece kendi kodunu analiz etmek
# 🔸 Üçüncü parti modülleri hariç tutmak
# 🔸 Belirli satır veya modülün bellek davranışını izlemek
# 🔸 Gürültüyü azaltmak ve net analiz yapmak

# ---------------------------------------------------------------
# ✅ ÖRNEK KULLANIM:
# ---------------------------------------------------------------

import tracemalloc

tracemalloc.start()

# Bellek tüketen örnek kod
data = [str(i) * 1000 for i in range(1000)]

# Snapshot al
snapshot = tracemalloc.take_snapshot()

# Filtre tanımla
filters = [
    tracemalloc.Filter(True, "my_script.py"),         # sadece bu dosyadan gelen izleri dahil et
    tracemalloc.DomainFilter(True, domain=0)          # sadece Python yorumlayıcısının alanını dahil et
]

# Filtreyi uygula
filtered_snapshot = snapshot.filter_traces(filters)

# İstatistikleri al
stats = filtered_snapshot.statistics("lineno")
for stat in stats[:5]:
    print(stat)

# ---------------------------------------------------------------
# ✅ SONUÇ:
# ---------------------------------------------------------------

# ➤ filter_traces(), bellek izlerini filtreleyerek daha hedefli analiz yapmanı sağlar.
# ➤ Filter ve DomainFilter ile dosya, satır, domain ve stack derinliği bazlı filtreleme mümkündür.
# ➤ Bu yapı, bellek sızıntılarını tespit etmek ve performans analizleri için çok güçlüdür.
