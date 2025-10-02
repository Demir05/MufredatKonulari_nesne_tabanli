# 🧩 opcode MODÜLÜ NEDİR?
# =============================================================================
# • opcode modülü, Python’un sanal makinesinde kullanılan bütün OPCODE’ların (operation code)
#   numaralarını, isimlerini ve yardımcı tablolarını barındırır.
# • Bu modül, "dis" gibi kullanıcı-dostu araçlara altyapı sağlar ama doğrudan senin de erişimine açıktır.
# • Yani opcode = Python VM’in sözlüğü, opcode modülü = bu sözlüğün resmi kaynağı. 📚

# -----------------------------------------------------------------------------
# 📌 Neden Böyle Bir Modüle İhtiyaç Duyuldu?
# • Çünkü CPython yorumlayıcısı, bytecode çalıştırırken *sayısal opcode değerleri* kullanır.
#   (ör: LOAD_CONST = 100, RETURN_VALUE = 83)
# • Biz insanlar isimleriyle (LOAD_CONST) okumak isteriz, makine ise numaralarıyla (100) çalışır.
# • opcode modülü bu iki dünya arasında köprü kurar → isim <-> sayı eşlemesi yapar. 🌉
# • Ayrıca Python’un kendi içinde, disassembler ve optimizer’lar da bu tabloları kullanır.

# -----------------------------------------------------------------------------
# 📌 Erişilebilir Olmasının Amacı
# • Normal kullanıcıların doğrudan opcode numaralarıyla uğraşması gerekmez.
# • Ama özel durumlarda (ör: bytecode manipülasyonu, kendi derleyicini yazma, eğitim/analiz)
#   opcode modülünü kullanmak faydalıdır.
# • CPython çekirdeğinde var olan opcode.h dosyası derleme sürecinde otomatik olarak
#   opcode.py’ye dönüştürülür → böylece Python seviyesinde de erişilebilir hale gelir.

# -----------------------------------------------------------------------------
# 📌 Kullanım Alanları
# • dis modülü gibi araçların arka planı.
# • Eğitim: "hangi opcode hangi numaraymış?" öğrenmek.
# • Bytecode üretimi veya manipülasyonu (ileri düzey → örn: kendi compiler/VM denemeleri).
# • Python sürüm farklarını analiz etmek: hangi opcode yeni eklenmiş, hangisi silinmiş.
# • Performans analizinde: "bu fonksiyon kaç opcode ile çalışıyor?"

# -----------------------------------------------------------------------------
# 📌 opcode MODÜLÜNDEKİ TEMEL NESNELER
# 1) opcode.opmap     → {'LOAD_CONST': 100, 'RETURN_VALUE': 83, ...}
#    - İsimden numaraya sözlük (string → int)
#
# 2) opcode.opname    → ['<0>', '<1>', ..., 'LOAD_CONST', ..., 'RETURN_VALUE']
#    - Numaradan isme liste (index = int → string)
#
# 3) opcode.HAVE_ARGUMENT
#    - 90 gibi bir eşik değer → bu numaradan büyük opcode’lar argüman taşır.
#
# 4) opcode.hasconst, opcode.hasname, opcode.haslocal, opcode.hasjrel, opcode.hasjabs ...
#    - Belirli opcode kategorilerini listeler:
#      * hasconst → sabit yükleyen opcode’lar (LOAD_CONST gibi)
#      * hasname  → isimle ilgili opcode’lar (LOAD_NAME, STORE_NAME)
#      * haslocal → yerel değişkenlerle ilgili opcode’lar (LOAD_FAST, STORE_FAST)
#      * hasjrel  → relatif atlama yapan opcode’lar (JUMP_FORWARD)
#      * hasjabs  → mutlak atlama yapan opcode’lar (JUMP_ABSOLUTE)
#
# Bu koleksiyonlar bytecode analizinde çok işe yarar. 🔍

# -----------------------------------------------------------------------------
# 📌 Örnekler
import opcode

print("LOAD_CONST numarası:", opcode.opmap["LOAD_CONST"])  # 100
print("100 numaralı opcode adı:", opcode.opname[100])      # LOAD_CONST

print("Argüman taşıyan opcode'lar:", [opcode.opname[i] for i in range(len(opcode.opname)) if i >= opcode.HAVE_ARGUMENT])

print("Sabit kullanan opcode'lar:", [opcode.opname[i] for i in opcode.hasconst])

# -----------------------------------------------------------------------------
# 🎯 Özet
# • opcode modülü = CPython’ın opcode setinin Python’daki resmi yansımasıdır.
# • Gerektiğinde opcode numaralarını/isimlerini/özelliklerini öğrenmek için buraya bakılır.
# • dis, opcode modülünü kullanarak sana insan-dostu çıktılar üretir.
# • Sen de eğitim, analiz veya ileri seviye bytecode hack’leri için doğrudan kullanabilirsin.
