# ------------------------------------------------------------------------------
# ast.unparse Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# `ast.unparse` (Python 3.9+ ile gelen), bir AST (Abstract Syntax Tree) nesnesini
# tekrar Python kaynak kodu (string) hâline dönüştürür.
# Yani AST → kod dönüşümü sağlar (kod jenerasyonu).
# Bu sayede AST üzerinde değişiklik yaptıktan sonra kodu geri elde edebilirsin.
#
# Önemli: `unparse` ile elde edilen çıktı orijinal biçim (boş satırlar, yorumlar, özgün biçimlendirme)
# tam olarak korunmaz; AST yalnızca yapısal bilgileri içerir. :contentReference[oaicite:0]{index=0}
#
# Ayrıca bazı durumlarda `unparse` çıktısı, farklı Python sürümleri arasında tam uyumlu olmayabilir. :contentReference[oaicite:1]{index=1}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.unparse(node: ast.AST) -> str
#
# PARAMETRELER:
# - node (ast.AST):
#     Kaynağını kod hâline çevirmek istediğin AST düğümü. Genellikle bir Module, Expression, vs.
#
# DÖNÜŞ:
# - str:
#     AST’yi yansıtan Python kodu (string). Bu kod, çalıştırılabilir kod olmayabilir ama yapısal olarak eşdeğer olur.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ AST üzerinde değişiklik yaptıktan sonra kodu string olarak almak
# ✅ Kod jenerasyonu / kod transformasyonu araçlarında
# ✅ Kendi transpiler’larını yazarken
# ✅ Eğitim, analiz, test ortamında “AST → kod” adımında
# ✅ Kod yeniden üretimi gereken senaryolarda (örneğin kod refactor sonrası çıktı)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# - `unparse` yalnızca yapısal bilgileri baz alır; orijinal boş satırları, yorumları,
#   kodun tam biçimlendirmesini geri getirmez. Çünkü AST bu bilgileri tutmaz. :contentReference[oaicite:2]{index=2}
# - Bazı durumlarda `unparse`’un ürettiği kod, **f-string quote kullanımı**, **tırnak işaretleri** vs.
#   açısından farklı Python sürümleri arasında uyumsuzluk taşıyabilir. :contentReference[oaicite:3]{index=3}
# - `unparse` hata fırlatabilir (örneğin AST geçerli değilse), `ValueError`, `TypeError`, vs.
# - AST node’larının `lineno`, `col_offset` gibi konum metadata’ları `unparse` için şart değildir — `unparse` bunlara ihtiyaç duymaz; yalnızca yapısal içerik ve çocuk node’lar önemlidir.
# -  parse() fonksiyonunda Grammer/ dizininden bahsettik unparse() için bu farklıdır;
#   unparse,Cpython üzerinde bir işlem yapamaz çünkü AST'nin tekrar insan okunabilir formuna dönüştürülmesi lükstür;
#   python 3.9 ile gelen _Precedence Enum sınıfında tanımlanan semboller kullanılarak bu işlem yapılır.
#   sınıf düzeyinde tanımlı olan bu isimlerin her biri python'daki bir işareti temsil eder ve enum.auto() ile
#   dinamik olarak öncekik sırası atanır (auto kullanılmasının nedeni cpython'da ki davranışı taklit etmesi ve yeni bir işaret geldiği zaman sıraya göre değerin atanmasını sağlamak)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

import ast

# --------------------------------------------------------
# Örnek 1: Basit AST → kod
# --------------------------------------------------------
src = "x = 2 * (y + 3)\nprint(x)"
tree = ast.parse(src)

# AST üzerinde değişiklik yapmadan unparse et
code_str = ast.unparse(tree)
print(code_str)
# çıktıda şöyle bir kod beklenir (parantez, operatörlerle birlikte):
# "x = 2 * (y + 3)\nprint(x)"

# --------------------------------------------------------
# Örnek 2: AST üzerinde modifikasyon, sonra unparse
# --------------------------------------------------------
tree2 = ast.parse("a = 1 + 2")
# Orijinal ifade: 1 + 2
old = tree2.body[0].value
# Yeni ifade: 10 + 20
new = ast.BinOp(left=ast.Constant(10), op=ast.Add(), right=ast.Constant(20))
# copy_location ile üst node konumu koru
ast.copy_location(new, old)
# Alt node’ların konum bilgisi olmasa da unparse çalışır
tree2.body[0].value = new

out = ast.unparse(tree2)
print(out)
# beklenen çıktı: "a = 10 + 20"

# --------------------------------------------------------
# Örnek 3: Sınırlı biçimlendirme kaybı
# --------------------------------------------------------
src2 = """
def foo():
    # comment here
    return 5
"""

tree3 = ast.parse(src2)
out2 = ast.unparse(tree3)
print(out2)
# Not: yorum satırları kaybolabilir, boş satırlar minimalize olabilir

# --------------------------------------------------------
# Özet:
# - unparse, AST’yi kod hâline çevirir
# - yorumlar ve format bozulabilir
# ------------------------------------------------------------------------------
