# ===============================================================
# 🌳 AST (Abstract Syntax Tree) — Soyut Sözdizim Ağacı
# ===============================================================
# Bu anlatım, AST’yi “ne, niçin, nasıl kullanılır” seviyesinde kavratmaya çalışır.

# ---------------------------------------------------------------
# ✅ 1. AST nedir?
# ---------------------------------------------------------------
# 🔹 AST, kaynak kodun (text) yapısını, programlama dilinin dilbilgisi (grammar) kurallarına
#     göre “ağaç” formunda ifade eden soyut bir modeldir.
# 🔹 Yani kodun “mantıksal yapısını” yansıtır, ama biçim (indent, boşluk, yorum satırları) gibi
#     detayları taşımaz — bu yüzden “abstract / soyut” deriz.
# 🔹 Örneğin `x = 1 + 2` kodu, AST’de şöyle görünebilir:
#     Module(
#       body=[
#         Assign(
#           targets=[Name(id='x')],
#           value=BinOp(left=Constant(1), op=Add(), right=Constant(2))
#         )
#       ]
#     )

# ---------------------------------------------------------------
# ✅ 2. AST’nin amacını bir metaforla anlatmak
# ---------------------------------------------------------------
# 🎭 Metafor: Bir binanın mimari planı gibi düşün:
#     - Kaynak kod = bina inşa edilmiş haldeki hâli (içinde detaylarla)
#     - AST = mimarın elindeki çizim (kat planları, odaların bağlantısı, fonksiyon/if blokları)
#     - Kod biçimi, boşlukları, yorumları — bunlar çatıdaki boya işleri gibi detaydır, planı bozmaz.
# AST ile sen binanın iskeletini görürsün — duvarlar, odalar, kapılar, giriş çıkış yolları.

# ---------------------------------------------------------------
# ✅ 3. AST nasıl üretilir?
# ---------------------------------------------------------------
# 1. Kod (string) → tokenize edilir (kelimelere, sembollere ayrılır)
# 2. Parser → token’lar dilin kurallarına göre hiyerarşik yapıya (parse tree / AST) dönüştürür
# 3. AST düğümleri (node’lar) Python’da `ast.AST` sınıfından türetilmiş nesnelerdir
# 4. Python’un derleyicisi bu AST’yi bytecode’a çevirdikten sonra yürütmeyi başlatır

# Python’un `ast.parse(code)` fonksiyonu bu işlemi bizim için yapar.
# Ayrıca `compile(..., flag=ast.PyCF_ONLY_AST)` ile kodu AST olarak almak mümkün.

# ---------------------------------------------------------------
# ✅ 4. AST’nin yapısı: Node’lar & alanlar
# ---------------------------------------------------------------
# 🔹 Her AST düğümü (node), bir “tip” (örneğin Assign, BinOp, If, FunctionDef) taşır.
# 🔹 Her node belirli alanlara sahiptir (örn. Assign: targets, value; BinOp: left, op, right).
# 🔹 AST node’ları ayrıca `lineno`, `col_offset` gibi dosyadaki konum bilgilerini tutar (isteğe bağlı).
# 🔹 Python’un `ast` modülü her sürüme bağlı olarak bu node tipleri ve alanlar evrimleşebilir. :contentReference[oaicite:0]{index=0}

# ---------------------------------------------------------------
# ✅ 5. AST ile ne yapabiliriz?
# ---------------------------------------------------------------
# 🔍 Kod Analizi:
#     - Hangi fonksiyon tanımlanmış, kaç if var, hangi değişkenler kullanılıyor?
#     - Linter, kalite kontrol, güvenlik analizleri bu aşamada çalışır.
# 🔄 Kod Dönüştürme / Refactoring:
#     - AST’yi al, değiştir, yeniden derle → kodu değiştir.
#     - Örn: `+` → `*`, ya da `print(...)` → `logging.info(...)`.
# 🔐 Güvenli Çalıştırma:
#     - `ast.literal_eval(...)` ile sadece sabit veri yapıları (list, dict, sayı, string) güvenle okunur; çalıştırılmaz.
# 🛠 Araç Geliştirme:
#     - IDE’ler, kod tamamlama, “go to definition”, otomatik refactor araçları AST kullanır.

# ---------------------------------------------------------------
# ✅ 6. AST’nin sınırlamaları ve dikkat edilmesi gerekenler
# ---------------------------------------------------------------
# ⚠️ Yorumlar, boşluklar, biçim (indent vs) AST’ye gelmez — kodun görünüm kısmı kaybolur.
# ⚠️ AST → kod dönüşümü (`ast.unparse`) çoğu zaman kodu “estetik biçimde” geri vermez — stil farklı olabilir.
# ⚠️ AST node’ları mutable’dur; yanlış değişiklikler syntax hatalarına ya da bozuk kodlara yol açabilir.
# ⚠️ Versiyon farkları: Python’un farklı sürümlerinde AST modelinde değişiklikler olabilir.

# ---------------------------------------------------------------
# ✅ 7. Senior seviye ipucu
# ---------------------------------------------------------------
# - AST kullanımı aslında “derleyici / kod analiz aracı” seviyesi bir iştir, her gün kullanman beklenmez.
# - Ama bir kez AST’yi kavradığında:
#     * Kod analiz araçları yazabilir,
#     * Kod dönüştürücü (transpiler / refactorer) yazabilirsin,
#     * Python’un içsel mechanizmasını anlaman derinleşir.
# - RealPython gibi kaynaklarda CPython’ın AST → compiler → execution kısmı “Interpreter süreci” içinde anlatılır. :contentReference[oaicite:1]{index=1}

# ---------------------------------------------------------------
# ✅ Özet:
# ---------------------------------------------------------------
# AST, Python kodunun mantıksal yapısını tutan soyut bir ağaç modelidir.
# Kaynak koddan derleyici sürecinde üretilir, sonra bytecode’a çevrilip yürütülür.
# `ast` modülü ile bu ara yapıyı dışarı çekip oynayabilir, analiz edebilir, yeniden derleyebilirsin.
# Yani AST, Python’un beynine uzanan bir kapı — senin manipüle edebileceğin “iç iskelet”.
