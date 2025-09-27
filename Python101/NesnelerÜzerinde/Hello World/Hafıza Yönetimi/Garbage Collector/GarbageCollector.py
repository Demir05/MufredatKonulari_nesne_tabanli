# ===============================================================
# ♻️ PYTHON'DA GARBAGE COLLECTOR (GC) & CYCLE COLLECTOR
# ===============================================================

# 🔹 Python, bellek yönetimini otomatik olarak yapar.
#     Bu sistemin adı: Garbage Collector (GC) → "çöp toplayıcı"
#     GC, kullanılmayan objeleri silerek bellek sızıntılarını önler.

# 🔹 Python'da iki temel strateji vardır:
#     1️⃣ Referans Sayımı (Reference Counting)
#     2️⃣ Döngü Toplayıcı (Cycle Collector)

# ---------------------------------------------------------------
# 🔍 1️⃣ REFERANS SAYIMI (sys.getrefcount ile ölçülebilir)
# ---------------------------------------------------------------

# 🧠 Her obje, kaç referansla tutulduğunu bilir.
#     ➤ Eğer referans sayısı sıfıra düşerse → obje silinir.

# Örnek:
# import sys
# x = [1, 2, 3]
# print(sys.getrefcount(x))  # Genelde 2 olur (x + getrefcount argümanı)

import gc

# ===============================================================
# ♻️ PYTHON GC — NESİL (GENERATION) MANTIĞI
# ===============================================================

# 🔹 Python’un garbage collector’ı, nesneleri “yaşlarına” göre 3 nesile ayırır:
#     ➤ Gen 0 → Yeni oluşturulan objeler
#     ➤ Gen 1 → Gen 0’dan kurtulanlar
#     ➤ Gen 2 → Gen 1’den de kurtulan, uzun ömürlü objeler

# 🔍 Amaç: Her objeyi her zaman kontrol etmek yerine,
#         kısa ömürlüleri sık, uzun ömürlüleri seyrek kontrol etmek.

# ===============================================================
# ✅ NESİL 0 (GENERATION 0)
# ===============================================================

# 🔸 Yeni oluşturulan her obje önce Gen 0’a yerleştirilir.
# 🔸 Gen 0, en sık toplanan nesildir.
# 🔸 Eğer obje toplanamazsa → Gen 1’e terfi eder.

# ➤ Gen 0 tetiklenme eşiği: gc.get_threshold()[0]
# ➤ Gen 0’daki tahsis sayısı: gc.get_count()[0]

# ===============================================================
# ✅ NESİL 1 (GENERATION 1)
# ===============================================================

# 🔸 Gen 0’dan kurtulan objeler Gen 1’e geçer.
# 🔸 Gen 1 daha az sıklıkla toplanır.
# 🔸 Eğer Gen 1’de de toplanamazsa → Gen 2’ye geçer.

# ➤ Gen 1 tetiklenme eşiği: gc.get_threshold()[1]
# ➤ Gen 1 tahsis sayısı: gc.get_count()[1]

# ===============================================================
# ✅ NESİL 2 (GENERATION 2)
# ===============================================================

# 🔸 Gen 2, en uzun ömürlü nesneleri içerir.
# 🔸 Gen 2 toplaması en nadir gerçekleşir.
# 🔸 Gen 2’deki objeler genellikle sabit yapıdadır (örneğin modül düzeyindeki sabitler).

# ➤ Gen 2 tetiklenme eşiği: gc.get_threshold()[2]
# ➤ Gen 2 tahsis sayısı: gc.get_count()[2]

# ===============================================================
# 🧪 ÖRNEK: Eşik ve sayaçları gözlemleme
# ===============================================================

print("GC Eşik Değerleri:", gc.get_threshold())  # (700, 10, 10) gibi
print("GC Sayaçları:", gc.get_count())           # (Gen0, Gen1, Gen2)

# ➤ Bu sayaçlar, son toplama işleminden bu yana kaç obje üretildiğini gösterir.
# ➤ Sayaçlar eşik değerine ulaşınca ilgili nesil toplanır.

# ===============================================================
# ✅ NESİL MANTIĞININ FAYDASI
# ===============================================================

# 🔸 Kısa ömürlü objeler → hızlıca temizlenir (Gen 0)
# 🔸 Uzun ömürlü objeler → daha az kontrol edilir (Gen 2)
# 🔸 Bu sayede performans artar, gereksiz tarama yapılmaz.

# 🔍 GC, objeye doğrudan “ömür biçmez” ama yaşına göre davranışını değiştirir.
#     ➤ Gen 0 → yeni doğmuş
#     ➤ Gen 1 → orta yaş
#     ➤ Gen 2 → yaşlı ve sabit

# ===============================================================
# ✅ Elle Toplama Örnekleri
# ===============================================================

# ➤ Gen 0 toplama: gc.collect(0)
# ➤ Gen 1 toplama: gc.collect(1)
# ➤ Gen 2 toplama: gc.collect(2)

# ➤ Tüm nesiller: gc.collect()  # varsayılan olarak Gen 2’ye kadar toplar

# ===============================================================
# ✅ SONUÇ:
# ===============================================================

# ➤ GC, nesneleri yaşlandırarak daha verimli bellek yönetimi sağlar.
# ➤ Her nesil, farklı sıklıkta toplanır.
# ➤ Bu sistem sayesinde Python, hem hızlı hem akıllı temizlik yapar.

