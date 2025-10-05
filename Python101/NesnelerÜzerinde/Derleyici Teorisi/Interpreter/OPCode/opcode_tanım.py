# 🧩 OPCODE NEDİR? — Sade & Detaylı Tanım
# =============================================================================
# • "Opcode" (operation code), Python’ın sanal makinesine (CPython VM) verilen en temel
#   talimatın adıdır. Bytecode akışı içindeki her adım bir opcode (ve varsa argümanı) ile
#   temsil edilir: LOAD_CONST, LOAD_FAST, BINARY_ADD, RETURN_VALUE gibi. 🔧
#
# • Kaynak kodun (Python) derlenmesiyle ortaya çıkan ara temsil = "bytecode".
#   Bu bytecode, opcode + argüman baytlarının sıralı dizisidir. Yani "opcode", bytecode’un
#   atomik komutudur; interpreter bu komutları tek tek okuyup uygular. ⚙️
#
# • Her opcode’un bir "numarası" (0–255 arası), bir "adı" (opname) ve çoğu zaman bir
#   "argümanı" (arg, argval, argrepr) vardır. Örn: LOAD_CONST 1 → const havuzundaki 1. sabiti yükle.
#
# =============================================================================
# 🧠 OPCODE → CODETYPE → INTERPRETER İLİŞKİSİ (Zincir)
# -----------------------------------------------------------------------------
# Python yorumlayıcısı (CPython), kaynak kodu çalıştırmadan önce onu derleyerek bir CodeType nesnesine dönüştürür.
# Bu nesne içinde yer alan co_code alanı, fonksiyonun ham bytecode dizisidir.

# Python 3.6 ve sonrasında, CPython bytecode’u "wordcode" formatında saklar.
# Bu formatta her komut 2 bayttan oluşur:
#   - 1. bayt: opcode → yapılacak işlemi belirtir (örneğin LOAD_CONST)
#   - 2. bayt: oparg  → bu işlemin hangi veriyle çalışacağını gösterir (örneğin co_consts[oparg])

# Bytecode dizisi bir bytes nesnesidir. Örneğin:
#   b'\x64\x01\x53\x00' → [100, 1, 83, 0]
#   Burada:
#     100 → LOAD_CONST
#     1   → co_consts[1]
#     83  → RETURN_VALUE
#     0   → oparg yok (bazı opcode’lar argüman taşımaz)

# CPython’ın çekirdeğindeki yorumlayıcı döngü (eval loop), bu diziyi 2’şer baytlık bloklar halinde okur:
#   - opcode = bytecode[i]
#   - oparg  = bytecode[i+1]
#   - Ardından opcode’a karşılık gelen C fonksiyonu çağrılır (örneğin LOAD_CONST → PyEval_LoadConst)

# Bu yürütme modeli sayesinde Python kodu, opcode’lar üzerinden deterministik ve optimize biçimde çalıştırılır.

# Örneğin:
#   def f(): return 42
#   Bu fonksiyonun co_code alanı: b'd\x01S\x00'
#   Yani:
#     LOAD_CONST 1 → co_consts[1] = 42
#     RETURN_VALUE → yığındaki değeri döndür

# Bazı opcode’lar argüman taşımaz (örneğin POP_TOP), bu durumda oparg genellikle 0’dır veya yok sayılır.
# Ancak wordcode sisteminde her komut 2 bayt olduğu için oparg alanı her zaman vardır — kullanılmasa bile.

# Bu yapı, CPython’ın yorumlayıcı performansını artırmak ve opcode çözümlemesini sabit hale getirmek için tasarlanmıştır.

# İstersen bu mantığı gerçek bir BytecodeTracer sınıfına dönüştürüp, opcode’ları dis.opname ile eşleştirerek semantik analiz yapabiliriz.

#
# =============================================================================
# 🔍 OPCODE ↔ dis (Disassembler) İLİŞKİSİ
# -----------------------------------------------------------------------------
# • dis modülü, opcode’ları "insan dostu" biçimde gösterir. Ham co_code baytlarını okur,
#   her opcode'u dis.Instruction nesnesine dönüştürür (opname, arg, argval, offset, satır bilgisi).
# • dis.dis(obj) → hızlı çıktı; dis.Bytecode(obj) → daha özelleştirilebilir görünüm.
# • dis sayesinde "hangi opcode’lar üretildi?", "nerede hangi argüman kullanılmış?" gibi
#   sorulara kolayca yanıt buluruz. 🔎
#
# =============================================================================
# ⏱️ OPCODE ↔ timeit (Süre Ölçümü) İLİŞKİSİ
# -----------------------------------------------------------------------------
# • timeit, opcode’ların toplam çalıştırma süresi üzerindeki etkisini ölçmene yarar.
# • dis ile "hangi opcode’lar var?"ı görür, timeit ile "kaç saniye tuttu?"yu ölçersin;
#   birlikte kullanınca "neden yavaş/hızlı?" cevabına yaklaşırsın. ⏱️
#
# =============================================================================
# 🧭 NEDEN ÖNEMLİ?
# -----------------------------------------------------------------------------
# • Opcode’ları anlamak, Python’un çalışma zamanındaki adımlarını kavramanı sağlar:
#   - Farklı yazım şekillerinin (list(range) vs comprehension) ürettiği opcode farklarını görebilirsin.
#   - Hangi komutların doğrudan C seviyesinde "hızlandırılmış" yolları kullandığını anlarsın.
#   - Performans/bellek analizinde (dis + timeit + tracemalloc) kök neden analizi yaparsın.
#
# =============================================================================
# ⚠️ SÜRÜM FARKLARI (CPython)
# -----------------------------------------------------------------------------
# • Opcode seti CPython sürümlerinde değişebilir: yeni opcode’lar eklenir, bazıları kaldırılır
#   veya yeniden adlandırılır (3.11’de çağrı/aritmetik opcode’larında büyük değişimler gibi).
# • Bu yüzden opcode adına "katı" bağımlılık kırılgandır; sürüm yükseltmelerinde bozulabilir.
#   dis/opcode modülleriyle birlikte sürüm uyumluluğunu gözetmek gerekir. 🧱
#
# =============================================================================
# 🧩 KISA ÖZET (TL;DR)
# -----------------------------------------------------------------------------
# • Opcode = CPython sanal makinesinin çalışma talimatı.
# • CodeType.co_code = bu opcode’ların ham dizisi (bytecode).
# • Interpreter = bu opcode’ları sırasıyla okur/işler.
# • dis = opcode’ları insan-dostu görünüme çevirir (Instruction).
# • tracemalloc = bu opcode akışının bellek etkisini satır/iz düzeyinde raporlar.
# • timeit = aynı akışın süre/maliyetini ölçer.
# • Hepsi bir araya gelince: "ne oldu, neden oldu, kaça mal oldu?" üç sorusunun cevabı. ✅
