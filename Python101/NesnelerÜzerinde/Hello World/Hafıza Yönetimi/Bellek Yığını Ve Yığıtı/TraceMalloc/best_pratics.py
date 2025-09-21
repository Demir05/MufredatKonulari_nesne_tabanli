# ─────────────────────────────────────────────────────────────
# 📌 TRACEMALLOC BELLEK ANALİZ REHBERİ
# Bu rehber, Python'da bellek sızıntısı, gereksiz tahsis ve modül etkilerini analiz etmek için
# tracemalloc modülünü nasıl kullanabileceğini adım adım gösterir.

import tracemalloc
import gc

# ─────────────────────────────────────────────────────────────
# 1️⃣ Koddan sonra bellek artışı varsa → Sızıntı olabilir

# Amaç: Kod çalıştıktan sonra hâlâ bellek artışı varsa, bazı nesneler gereksiz şekilde bellekte kalıyor olabilir.
tracemalloc.start()
snapshot_before = tracemalloc.take_snapshot()

# 🔁 Bellek tahsisi yapan kod bloğu
# Örneğin: büyük veri listesi, cache, global referans vs.
def services():
    global b
    a = list(range(1_000_000))
    b = a.copy()
    del a

services()

snapshot_after = tracemalloc.take_snapshot()
diff = snapshot_after.compare_to(snapshot_before, 'lineno')

# Farkları yazdır: pozitif size_diff varsa → potansiyel sızıntı
for stat in diff[:5]:
    print(stat)

# ─────────────────────────────────────────────────────────────
# 2️⃣ Döngü içinde sürekli tahsis varsa → Optimize edilebilir

# Amaç: Aynı satırda tekrar tekrar nesne oluşturuluyorsa, bu bellek ve performans açısından pahalı olabilir.
snapshot = tracemalloc.take_snapshot()
stats = snapshot.statistics('lineno')

for stat in stats:
    if stat.count > 10000:  # örnek eşik
        print(f"Yoğun tahsis: {stat}")

# Bu satırda döngüsel nesne üretimi varsa, cache veya reuse önerilir.

# ─────────────────────────────────────────────────────────────
# 3️⃣ Modül yüklemesi sonrası snapshot al → Hangi modül ne kadar bellek getirmiş gör

# Amaç: import işlemi sonrası hangi modül ne kadar bellek tahsis etmiş, bunu görmek.
tracemalloc.start()

import typing  # örnek modül

snapshot = tracemalloc.take_snapshot()
stats = snapshot.statistics('filename')

for stat in stats:
    print(stat)

# Bu analizle, typing, abc, contextlib gibi modüllerin bellek yükünü görebilirsin.

# ─────────────────────────────────────────────────────────────
# 4️⃣ Testten önce/sonra snapshot al → Testin bellek etkisini ölç

# Amaç: Bir test fonksiyonu çalıştığında ne kadar bellek tüketiyor, bunu ölçmek.
def test_my_function():
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()

    # 🔁 Test edilen fonksiyon
    result = [x**2 for x in range(100000)]

    snapshot_after = tracemalloc.take_snapshot()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Anlık: {current//1024} KB, Zirve: {peak//1024} KB")

    diff = snapshot_after.compare_to(snapshot_before, 'lineno')
    for stat in diff[:5]:
        print(stat)

    tracemalloc.stop()

test_my_function()

# ─────────────────────────────────────────────────────────────
# 🎯 GENEL TAVSİYELER

# - n_frames=10 kullanarak traceback zincirini anlamlı hale getir
# - gc.collect() ile çöp toplayıcıyı tetikleyip current değerini netleştir
# - statistics('lineno') → satır bazında analiz
# - statistics('filename') → modül bazında analiz
# - compare_to() → fark analiziyle sızıntı ve yoğun tahsis tespiti

# Bu rehber, büyük projelerde bellek davranışını kontrol altında tutmak için kullanılabilir.
# Kodun sadece çalışması değil, temiz çalışması gerekir.
