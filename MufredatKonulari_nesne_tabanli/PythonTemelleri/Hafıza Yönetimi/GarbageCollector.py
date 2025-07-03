# ===============================================================
# ♻️ PYTHON'DA GARBAGE COLLECTOR (GC) & CYCLE COLLECTOR
# ===============================================================

# 🔹 Python, kullanılmayan objeleri otomatik olarak siler.
#     Bu sisteme Garbage Collector (çöp toplayıcı) denir.
#
# 🔹 Temel olarak "referans sayımı" yöntemi kullanır:
#     ➤ Bir objeye referans kalmazsa, otomatik olarak silinir.

# ---------------------------------------------------------------
# 🔁 AMA SORUN ŞU: Referans Çemberi (Cycle)
# ---------------------------------------------------------------
# 🧠 Eğer iki obje birbirine referans veriyorsa (A → B → A gibi),
#     referans sayıları sıfırlanmaz — ama aslında objeler kullanılmaz.
#
# ✅ Bu durumda Python, cycle collector’ı devreye sokar.
#     ➤ gc.collect() çağrısıyla bu döngüleri temizleyebilirsin.

# ===============================================================
# 🔍 re.purge() VE CACHE CLEAR METODLARI NEDEN GEREKLİ?
# ===============================================================

# 🔹 re modülü (regex işlemleri), derlenen desenleri cache’ler (önbellekler)
#     ➤ Performansı artırmak için yapılır.
#
# 🔥 Ancak bu cache içindeki objeler hâlâ modül içinde referanslıdır.
#     ➤ Bu yüzden GC onları temizlemez!
#
# ✅ re.purge() çağrısı ile bu cache elle temizlenebilir.

# ---------------------------------------------------------------
# 📦 functools.lru_cache gibi yapılar da aynı şekilde çalışır:
#     ➤ Bellekte tuttuğu cache’i GC göremez.
#     ➤ .cache_clear() ile elle silmek gerekir.

# ===============================================================
# 📌 NEDEN GC CACHE'İ TEMİZLEMEZ?
# ===============================================================

# | Sebep 📌                  | Açıklama                                               |
# |---------------------------|--------------------------------------------------------|
# | GC referansa bakar        | Cache hâlâ bir objeye bağlıysa, "canlı" kabul eder     |
# | Cache bilinçli tutulur    | Performans için bilinçli olarak bellekte bırakılır     |
# | GC'nin amacı farklı       | Kullanılmayan objeleri siler, ama cache’i yönetmez     |

# ✅ SONUÇ:
# ➤ GC = Otomatik bellek temizliği
# ➤ Cache = Manuel temizlik gerekir
# ➤ re.purge(), .cache_clear() gibi fonksiyonlar bu yüzden önemlidir
