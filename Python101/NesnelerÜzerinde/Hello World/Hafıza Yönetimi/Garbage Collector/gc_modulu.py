# ♻️ gc — Çöp Toplayıcı (Garbage Collector) Modülü — Sade & Detaylı Rehber
# ============================================================================

# 🧠 NEDİR?
# • gc modülü, CPython’daki referans sayımı sistemini tamamlayan **döngü tespitli
#   çöp toplayıcıyı** (cyclic GC) kontrol etmeni ve gözlemlemeni sağlar.
# • Amaç: **Referans döngülerini** (A→B→A gibi) yakalayıp bellekten temizlemek,
#   toplayıcının davranışını ayarlamak ve bellek tanı/diagnostik bilgisi vermek. 🧰

# ----------------------------------------------------------------------------
# 🎯 NEDEN VAR? (Kısa teori)
# • CPython’da her nesnenin referans sayısı vardır; sayı sıfırlanınca anında yok edilir.
# • Ancak **döngüler** (cycle) varsa, sayılar sıfıra hiç inmez → **GC devreye girer**.
# • gc modülüyle bu toplayıcıyı **aç/kapa**, **tetikle**, **eşiklerini ayarla**,
#   **istatistik al** ve **sızıntı analizi** yap. 🔍

#import gc

# ===============================================================
# ♻️ PYTHON GARBAGE COLLECTOR (GC) — TAM AÇIKLAMALI
# ===============================================================

# 🔹 Python’da bellek yönetimi otomatik yapılır.
# 🔹 GC iki temel strateji kullanır:
#     1️⃣ Referans Sayımı → objeye referans kalmazsa silinir.
#     2️⃣ Cycle Collector → referans çemberlerini tespit edip temizler.

# ===============================================================
# 🧠 NESİL (GENERATION) MANTIĞI NEDİR?
# ===============================================================

# 🔸 GC, nesneleri "yaşlarına" göre 3 nesile ayırır:
#     - Gen 0 → Yeni oluşturulan objeler (en sık toplanan)
#     - Gen 1 → Gen 0’dan kurtulanlar (orta sıklıkta toplanır)
#     - Gen 2 → Uzun ömürlü objeler (nadiren toplanır)

# 🔸 Mantık: Yeni objeler daha sık silinir, yaşlılar daha az kontrol edilir.
# 🔸 Bu sayede performans artar → her objeyi her zaman taramak gerekmez.

# ===============================================================
# ✅ gc.enable() / gc.disable() / gc.isenabled()
# ===============================================================

# ➤ gc.enable() → GC’yi aktif hale getirir.
# ➤ gc.disable() → GC’yi geçici olarak kapatır.
# ➤ gc.isenabled() → GC açık mı diye kontrol eder.

# 🔍 Ne zaman kullanılır?
#     - Mikro benchmark’larda (ölçüm yaparken)
#     - Çok kısa ömürlü objelerin yoğun üretildiği yerlerde
#     - GC’yi geçici kapatıp sonra tekrar açmak için

# ⚠️ Dikkat: Uzun süre kapalı tutarsan bellek şişebilir!

# ===============================================================
# ✅ gc.collect(generation: int = 2) -> int
# ===============================================================

# ➤ Elle çöp toplama tetikler.
# ➤ Parametre: 0, 1 veya 2 → hangi nesil toplanacak?
# ➤ Dönen değer: Toplanan nesne sayısı

# 🔍 Ne zaman kullanılır?
#     - Büyük işlem sonrası bellek temizliği
#     - Döngüsel referansları manuel temizlemek için

# ⚠️ Dikkat: Senkron çalışır → yavaş olabilir, her yerde çağrılmaz!

# ===============================================================
# ✅ gc.get_threshold() / gc.set_threshold()
# ===============================================================

# ➤ get_threshold() → (t0, t1, t2) eşik değerlerini verir
# ➤ set_threshold(t0, t1, t2) → tetikleme eşiklerini ayarlar

# 🔍 Mantık:
#     - Gen 0 için t0 tahsis sayısı → t0’a ulaşınca Gen 0 toplanır
#     - Gen 1 ve Gen 2 için benzer mantık

# 🔍 Ne zaman kullanılır?
#     - Yük profiline göre GC davranışını ayarlamak için

# ⚠️ Dikkat: Yanlış ayar → ya fazla CPU tüketimi ya da bellek sızıntısı

# ===============================================================
# ✅ gc.get_count() -> tuple[int, int, int]
# ===============================================================

# ➤ Her nesil için tahsis–yıkım farkını verir
# ➤ Yani: Son toplama sonrası kaç yeni obje üretildi?

# 🔍 Ne zaman kullanılır?
#     - Eşiklerin neden tetiklendiğini anlamak için
#     - Bellek ritmini izlemek için

# ===============================================================
# ✅ gc.get_stats() -> list[dict]
# ===============================================================

# ➤ Her nesil için istatistik döner:
#     - collections: kaç kez toplandı?
#     - collected: kaç obje silindi?
#     - uncollectable: silinemeyen kaç obje var?

# 🔍 Ne zaman kullanılır?
#     - GC davranışını zaman içinde izlemek
#     - Bellek regresyonlarını tespit etmek

# ===============================================================
# ✅ gc.garbage : list
# ===============================================================

# ➤ Toplanamayan objeler buraya atılır (DEBUG_SAVEALL aktifse)
# ➤ Özellikle __del__ içeren döngülerde kullanılır

# 🔍 Ne zaman kullanılır?
#     - “Neden bu obje silinmedi?” sorusunun cevabını ararken

# ===============================================================
# ✅ gc.set_debug(flags) / gc.get_debug()
# ===============================================================

import gc

# ===============================================================
# 📘 PYTHON GC LOG OKUMA REHBERİ — YORUM SATIRLARIYLA
# ===============================================================

# 🔹 Bu rehber, gc.set_debug() ile etkinleştirilen GC loglarının
#     ne anlama geldiğini ve nasıl yorumlanacağını açıklar.

# ---------------------------------------------------------------
# ✅ 1. DEBUG BAYRAKLARI — gc.set_debug(flags)
# ---------------------------------------------------------------

# ➤ gc.DEBUG_STATS
#     → Her toplama işlemiyle ilgili istatistikleri yazdırır.
#     → Nesil, süre, kaç obje silindi gibi bilgiler içerir.

# ➤ gc.DEBUG_COLLECTABLE
#     → Toplanabilir objeleri listeler (isteğe bağlı detay).

# ➤ gc.DEBUG_UNCOLLECTABLE
#     → Silinemeyen objeleri listeler (örneğin __del__ içeren döngüler).

# ➤ gc.DEBUG_SAVEALL
#     → Tüm objeleri gc.garbage listesine koyar (silinmeyenler dahil).

# ➤ gc.DEBUG_LEAK
#     → DEBUG_SAVEALL + DEBUG_UNCOLLECTABLE → sızıntı analizi için ideal.

# ---------------------------------------------------------------
# ✅ 2. LOG ÇIKTISI ÖRNEĞİ — SATIR SATIR AÇIKLAMA
# ---------------------------------------------------------------

# gc: collecting generation 2...
#     → Gen 2 için çöp toplama işlemi başladı.

# gc: objects in each generation: 1682 5195 0
#     → Gen 0: 1682 obje
#     → Gen 1: 5195 obje
#     → Gen 2: 0 obje
#     → Bu, toplama öncesi izlenen obje sayılarıdır.

# gc: objects in permanent generation: 0
#     → gc.freeze() ile dondurulmuş nesne sayısı (kalıcı nesiller)

# gc: done, 0 unreachable, 0 uncollectable, 0.0007s elapsed
#     → Toplama tamamlandı.
#     → 0 unreachable → referanssız obje yok → silinecek bir şey yok
#     → 0 uncollectable → silinemeyen obje yok (örneğin __del__ içeren)
#     → 0.0007s → toplama süresi (milisaniye cinsinden)

# ---------------------------------------------------------------
# ✅ 3. FARKLI BİR LOG ÖRNEĞİ — SİLİNENLER VAR
# ---------------------------------------------------------------

# gc: collecting generation 2...
# gc: objects in each generation: 82 0 6335
# gc: objects in permanent generation: 0
# gc: done, 1287 unreachable, 0 uncollectable, 0.0009s elapsed

# ➤ 1287 unreachable → bu kadar obje artık referanssız → silindi
# ➤ 0 uncollectable → hepsi başarıyla temizlendi
# ➤ 0.0009s → hızlı temizlik

# ---------------------------------------------------------------
# ✅ 4. gc.get_debug() → Aktif bayrakları gösterir
# ---------------------------------------------------------------

# ➤ gc.get_debug() → int değeri döner (örneğin 1, 3, 5 gibi)
#     → Bu sayı, aktif bayrakların bitmask toplamıdır.

# ---------------------------------------------------------------
# ✅ 5. gc.garbage → Silinemeyen objeler burada birikir
# ---------------------------------------------------------------

# ➤ Eğer DEBUG_SAVEALL aktifse, toplanamayan objeler buraya atılır.
# ➤ Bu listeyi inceleyerek hangi objelerin neden silinmediğini görebilirsin.

# ---------------------------------------------------------------
# ✅ 6. Kullanım Örneği
# ---------------------------------------------------------------

# gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_UNCOLLECTABLE)
#     → Hem istatistikleri yazdırır hem de silinemeyenleri gösterir.

# gc.collect(2)
#     → Gen 2 toplama tetiklenir → loglar stderr’e yazılır.

# ---------------------------------------------------------------
# ✅ SONUÇ:
# ---------------------------------------------------------------

# ➤ GC logları, bellek yönetimini anlamak ve sızıntıları tespit etmek için güçlü bir araçtır.
# ➤ Bayraklar sayesinde hangi bilgilerin yazılacağını kontrol edebilirsin.
# ➤ Log çıktıları, nesil bazlı temizlik, silinemeyen objeler ve süre gibi kritik verileri içerir.


# ===============================================================
# ✅ gc.get_objects([generation]) -> list[object]
# ===============================================================

# ➤ GC’nin izlediği tüm objeleri döndürür
# ➤ Parametre: nesil → sadece o nesildeki objeleri verir

# 🔍 Ne zaman kullanılır?
#     - Bellek sızıntısı avı
#     - “Ortada biriken ne var?” sorusuna cevap

# ⚠️ Dikkat: Çok büyük liste dönebilir → üretimde kullanma!

# ===============================================================
# ✅ gc.get_referrers(*objs) / gc.get_referents(*objs)
# ===============================================================

# ➤ get_referrers → kim bu objeye referans veriyor?
# ➤ get_referents → bu obje kimlere referans veriyor?

# 🔍 Ne zaman kullanılır?
#     - Döngüsel referansları ve bağlantıları analiz etmek için

# ⚠️ Dikkat: Bu fonksiyonlar kendileri de referrer oluşturabilir!

# ===============================================================
# ✅ gc.is_tracked(obj) -> bool
# ===============================================================

# ➤ Bu obje GC tarafından izleniyor mu?
# ➤ Basit immutable’lar (int, str) genelde izlenmez
# ➤ Kapsayıcılar (list, dict, set) izlenir

# 🔍 Ne zaman kullanılır?
#     - GC’nin bu objeyi tarayıp taramadığını öğrenmek için

# ===============================================================
# ✅ gc.freeze() / gc.unfreeze()
# ===============================================================

# ➤ Kalıcı nesil mantığı:
#     - Uzun ömürlü objeleri dondur
#     - GC onları artık taramaz → performans artar

# 🔍 Ne zaman kullanılır?
#     - Servislerde, startup sonrası sabit objeleri dondurmak için

# ===============================================================
# ✅ gc.callbacks : list[callable]
# ===============================================================

# ➤ GC başladığında ve bittiğinde çağrılan fonksiyonlar
# ➤ İmza: callback(phase, info)
#     - phase: "start" veya "stop"
#     - info: nesil ve toplanan sayılar

# 🔍 Ne zaman kullanılır?
#     - Telemetri, metrik toplama
#     - GC sürecini izlemek

# ⚠️ Dikkat: Callback’ler hafif olmalı → GC’yi yavaşlatmasın!

# ============================================================================
# 🧭 NE ZAMAN KULLANILIR? (Pratik kılavuz)
# ----------------------------------------------------------------------------
# • Bellek artışı/sızıntı şüphesi: set_debug + collect + garbage ile iz sür.
# • Mikro-performans: kısa kritik bölümde disable → iş biter bitmez enable + (gerekirse) collect.
# • Tanı/izleme: get_stats, get_count ile davranışı kayda al; prod telemetri için callbacks.

# ----------------------------------------------------------------------------
# 🚧 DİKKAT / ANTİ-PATTERN’LER
# • Sürekli manuel collect çağırmak → gereksiz dur-kalk ve CPU tüketimi.
# • gc.disable ile toplayıcıyı **unutmak** → bellek şişer; daima tekrar enable et.
# • get_objects / get_referrers’i sık ve üretimde kullanmak → çok ağır ve çarpıtıcı sonuçlar.
# • DEBUG_SAVEALL açık unutmak → gc.garbage büyür, bellek kaçırır gibi görünür. 🧯

# ----------------------------------------------------------------------------
# ✨ KISA ÖZET (TL;DR)
# • gc modülü, **döngü tespitli** toplayıcıyı yönetir: aç/kapa, tetikle, eşiğini ayarla, istatistik al.
# • Sızıntı avı için: set_debug + collect + garbage + (gerekirse) get_referrers/referents.
# • Performans için: kısa süreli disable/enable, ölçerek (profil) karar ver.
# • Ağır introspeksiyon API’lerini tanı amaçlı ve ölçülü kullan. 🔍♻️
