# =========================================================
# 🧠 HEAP, STACK ve SCOPE — PYTHON'DA HAFIZA YÖNETİMİ
# =========================================================

# 🔹 HEAP (Yığın Bellek):
#    ➤ Uzun ömürlü nesneler burada saklanır (örnek: class instance'ları, list, dict, set).
#    ➤ Python'da "new" anahtar kelimesi yoktur ama her obje aslında heap'te yaratılır.
#    ➤ Garbage Collector (çöp toplayıcı) tarafından yönetilir.
#    ➤ Global erişimlidir, fonksiyonlar sona erse bile heap’teki nesneler yaşamaya devam eder.

# 🔹 STACK (Yığıt Bellek):
#    ➤ Geçici değişkenler (yerel değişkenler, fonksiyon çağrıları) burada tutulur.
#    ➤ Fonksiyon çalıştığında yeni bir stack frame oluşturulur.
#    ➤ Fonksiyon bittiğinde bu frame kaldırılır, içindekiler silinir.
#    ➤ Daha hızlıdır ama sınırlı hafızaya sahiptir (genellikle megabaytlarla sınırlıdır).

# =========================================================
# 📏 DİJİTAL BELLEK AYAK İZİ VE HEAP'İN ROLÜ
# =========================================================
#
# 💾 Bir programın RAM kullanımı (bellek ayak izi) genellikle **HEAP**'te tutulan verilerin
#     büyüklüğüne bağlıdır.
#
# 📌 Neden?
#    - Heap’te nesneler sürekli yaşamda kalır (özellikle büyük veri yapıları: list, dict, objeler)
#    - Stack daha küçük ve geçicidir, her fonksiyon bittiğinde temizlenir.
#
# 🧠 Bu yüzden büyük boyutlu veriler, resimler, dosyalar, modeller, çok elemanlı listeler vs.
#     genelde heap belleği doldurur.
#
# ✅ Hafızayı optimize etmek isteyen biri için:
#    ➤ Heap kullanımı en önemli takip kriteridir
#    ➤ Gereksiz referansları bırakmak (`del`, scope dışına çıkarmak) önemlidir