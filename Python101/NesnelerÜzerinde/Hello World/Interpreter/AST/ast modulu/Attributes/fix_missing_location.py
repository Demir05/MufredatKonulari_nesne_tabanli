# ------------------------------------------------------------------------------
# ast.fix_missing_locations Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# ast.fix_missing_locations, Python AST yapılarında eksik olan konum bilgilerini
# (lineno, col_offset, varsa end_lineno ve end_col_offset) otomatik olarak
# tamamlayan bir fonksiyondur.
#
# Özellikle elle oluşturulmuş AST node’larında veya node içine sonradan eklenen
# alt düğümlerde bu konum bilgileri eksik olabilir. Bu eksiklik `compile()` gibi
# işlemler sırasında hataya yol açar.
#
# Bu fonksiyon, AST ağacını gezerek her düğümün eksik konum alanlarını, ilgili üst
# düğümden miras alarak doldurur. Bu sayede AST geçerli ve derlenebilir hale gelir.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.fix_missing_locations(node: ast.AST) -> ast.AST
#
# PARAMETRELER:
# - node (ast.AST):
#     Konum bilgileri eksik olan AST ağacının kök düğümüdür.
#
# DÖNÜŞ:
# - Aynı AST node’unu geri döner. Ancak artık tüm alt node’larda eksik konum
#   bilgileri tamamlanmıştır.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ Elle oluşturulan AST node’larında
# ✅ AST içerisine yeni alt node’lar eklendiyse
# ✅ copy_location kullanılsa bile alt node’larda eksik bilgi varsa
# ✅ AST compile() edilmek isteniyorsa (zorunludur)
# ✅ Debug / traceback / IDE analiz desteği gerekiyorsa
# ✅ Derlenebilirlik testlerinde
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------

# ❓ Neden copy_location yeterli değil?
# - Çünkü copy_location sadece hedef node’un konum bilgilerini kopyalar.
# - Ancak bu node’un altında başka node’lar varsa (örneğin BinOp, Call),
#   bu alt node’lar lineno / col_offset bilgilerini içermez.

# ➕ Bu durumda:
# - Sadece üst node’un konumu doğru olur
# - Alt node’lar eksik kalırsa:
#   • compile() → TypeError verir
#   • traceback → yanlış/boş yer gösterir

# ❓ Peki fix_missing_locations ne yapar?
# - Bu fonksiyon, tüm AST’yi recursive olarak dolaşır
# - Eksik konum bilgilerine sahip node’lar için yukarıdaki (ebeveyn) node’un
#   konum bilgilerini alıp aynen aktarır
# - Yani AST’yi “konumsal olarak tamamlar” (miras verir)

# 🧠 Miras Mekanizması:
# - AST node’ları içinde eksik `lineno`, `col_offset`, `end_lineno`, `end_col_offset`
#   varsa, bu alanlar üst node’un aynı alanlarıyla doldurulur
# - Bu işlem recursive (önce üst, sonra alt) şekilde gerçekleşir
# # - Her alt node, bulunduğu üst node ile aynı yerdeymiş gibi varsayılır
# # - Çünkü bu node’ların orijinal kaynak kodda nerede oldukları bilinmez
# # - Dolayısıyla "aynı değerin aynen aktarılması" mantıklı ve güvenli bir yaklaşımdır

# Örnek:
# FunctionDef (lineno=10, col_offset=0)
# └── Return (lineno eksik)     → alır → lineno=10
#     └── BinOp (eksik)         → alır → lineno=10
#         ├── Constant (eksik)  → alır → lineno=10
#         └── Constant (eksik)  → alır → lineno=10

# ✅ Sonuç: Eksik tüm alanlar tamamlanır, compile() sorunsuz çalışır
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

import ast

# -------------------------------------------------------------------
# ✅ ÖRNEK 1 - Eksik konum bilgisi olan bir AST node'unu düzeltmek
# -------------------------------------------------------------------

expr = ast.Expr(
    value=ast.Call(
        func=ast.Name(id='print', ctx=ast.Load()),
        args=[ast.Constant(value='Hello')],
        keywords=[]
    )
)

# Şu anda expr ve alt node'larda konum bilgileri eksik
fixed = ast.fix_missing_locations(expr)

mod = ast.Module(body=[fixed], type_ignores=[])
compiled = compile(mod, filename="<ast>", mode="exec")
exec(compiled)  # Çıktı: Hello

# -------------------------------------------------------------------
# ✅ ÖRNEK 2 - copy_location + fix_missing_locations birlikte
# -------------------------------------------------------------------

source = "x = 1 + 2"
tree = ast.parse(source)

new_expr = ast.BinOp(
    left=ast.Constant(3),
    op=ast.Add(),
    right=ast.Constant(4)
)

# Sadece üst node'a konum kopyalanır
ast.copy_location(new_expr, tree.body[0].value)

# Alt node'larda konum eksik → fix_missing ile tamamla
ast.fix_missing_locations(new_expr)

tree.body[0].value = new_expr

compiled = compile(tree, filename="<ast>", mode="exec")
exec(compiled)  # x = 7

# -------------------------------------------------------------------
# Özet:
# - copy_location: sadece üst node’a konum verir
# - fix_missing_locations: alt node’ların tüm eksiklerini recursive olarak düzeltir
# -------------------------------------------------------------------
