# Python fonksiyonları derlendiğinde, içlerinde kullanılan opcode’lar CPython yorumlayıcısı tarafından yürütülür.
# Her opcode’un yürütme maliyeti farklıdır; bazıları çok hızlıdır, bazıları ise yorumlayıcıda ciddi yük oluşturur.

# 🚀 Hızlı opcode’lar:
# - LOAD_CONST: Sabit bir değeri yığına yükler. co_consts havuzundan alınır. Çok hızlıdır.
# - RETURN_CONST: Python 3.11+ ile gelen optimize dönüş komutu. Sabit bir değeri doğrudan döndürür.
# - POP_TOP, DUP_TOP, ROT_TWO: Yığın üzerinde basit manipülasyonlar yapar. Minimal işlem içerir.

# ⚡ Orta hızlı opcode’lar:
# - LOAD_FAST / STORE_FAST: Lokal değişkenlere erişim sağlar. Bellek erişimi vardır ama hızlıdır.
# - LOAD_GLOBAL / STORE_GLOBAL: Global isim çözümlemesi yapar. __globals__ ve __builtins__ içinde arama yapar.
#   Bu çözümleme işlemi daha maliyetlidir çünkü isim zinciri (LEGB) içinde dolaşılır.

# 🐢 Yavaş opcode’lar:
# - CALL / PRECALL / MAKE_FUNCTION: Fonksiyon çağrısı başlatır. Yeni bir frame oluşturur, argümanlar bağlanır.
#   Bu işlem yorumlayıcıda en maliyetli adımlardan biridir.
# - RAISE_VARARGS / SETUP_EXCEPT: Hata yönetimi opcode’larıdır. Kontrol akışını keser, stack’i boşaltır.
# - JUMP_FORWARD / POP_JUMP_IF_FALSE: Kontrol akışını değiştirir. Yürütme sırasını etkiler, koşullu dallanma içerir.

# 🧠 Mimari çıkarım:
# Bir fonksiyonda yavaş opcode’lar ne kadar fazlaysa, o fonksiyonun çalışma süresi potansiyel olarak o kadar uzar.
# Özellikle CALL, LOAD_GLOBAL, RAISE gibi opcode’lar sık kullanılıyorsa, yorumlayıcı overhead artar.

# 🔍 Performans analizi için:
# - co_code dizisi analiz edilerek hangi opcode’lar kullanıldığı çıkarılabilir.
# - dis.dis(...) çıktısı incelenerek opcode profili oluşturulabilir.
# - Yavaş opcode’ların sayısı ve sıklığı, fonksiyonun potansiyel yavaşlığını gösterir.

# 📦 Özet:
# - Opcode’lar sadece işlevsel değil, performanssal olarak da farklıdır.
# - CPython yorumlayıcısı her opcode’u C düzeyinde bir fonksiyonla işler; bazıları sabit veriyle çalışır (hızlı),
#   bazıları isim çözümlemesi veya frame geçişi gerektirir (yavaş).
# - Bu nedenle, bir fonksiyonun performansını analiz etmek için opcode profili incelenmelidir.
