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
# Özellikle manuel olarak oluşturulmuş AST node’larında veya node içine eklenen
# alt node’larda bu bilgiler eksik olabilir. Bu eksiklik `compile()` gibi işlemleri
# bozar. Bu fonksiyon, tüm alt ağaçta eksik konumları doldurarak AST’yi derlenebilir
# hale getirir.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.fix_missing_locations(node: ast.AST) -> ast.AST
#
# PARAMETRELER:
# - node (ast.AST):
#     Konum bilgileri eksik olan AST ağacının kök düğümü
#
# DÖNÜŞ:
# - Aynı AST node’unu geri döner, ancak tüm alt node’larda eksik konum
#   bilgileri tamamlanmış olur.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ Elle oluşturulan AST node’larında
# ✅ AST içine yeni alt node’lar eklenmişse
# ✅ copy_location kullanılsa bile alt node’lar eksikse
# ✅ AST compile() edilmek isteniyorsa (zorunludur)
# ✅ Debug / traceback / analiz araçlarının düzgün çalışması için
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# ❓ Neden copy_location yeterli değil?
#
# Çünkü:
# - copy_location sadece 1 node’un (üst düğümün) konumunu başka bir node’dan alır
# - Eğer bu node’un içinde başka alt düğümler varsa (örneğin BinOp, Call, vs.),
#   bu alt düğümler genelde lineno/col_offset içermez
#
# Bu durumda sadece üst node’un konumunu ayarlamak yetmez.
# Alt node’lar eksik kalırsa:
# - compile() → hata verir
# - traceback → yanlış yer gösterir
#
# fix_missing_locations bu eksik bilgileri alt düğümlere miras vererek düzeltir.
# Bu yüzden copy_location genellikle fix_missing_locations ile birlikte kullanılır.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

import ast

# -------------------------------------------------------------------
# ✅ ÖRNEK 1 - Eksik konum bilgisi olan bir AST node'unu düzeltmek
# -------------------------------------------------------------------

# Elle oluşturulmuş AST
expr = ast.Expr(
    value=ast.Call(
        func=ast.Name(id='print', ctx=ast.Load()),
        args=[ast.Constant(value='Hello')],
        keywords=[]
    )
)

# Şu anda expr ve alt node'larda lineno bilgisi yok

# Konumları otomatik dolduralım
fixed = ast.fix_missing_locations(expr)

# Artık derlenebilir hale geldi
mod = ast.Module(body=[fixed], type_ignores=[])
compiled = compile(mod, filename="<ast>", mode="exec")
exec(compiled)  # Çıktı: Hello

# -------------------------------------------------------------------
# ✅ ÖRNEK 2 - copy_location + fix_missing_locations birlikte
# -------------------------------------------------------------------

source = "x = 1 + 2"
tree = ast.parse(source)

# Yeni ifade: 3 + 4
new_expr = ast.BinOp(
    left=ast.Constant(3),
    op=ast.Add(),
    right=ast.Constant(4)
)

# Sadece üst node'a konum kopyalanır
ast.copy_location(new_expr, tree.body[0].value)

# Alt node'larda konum eksik → tamamla
ast.fix_missing_locations(new_expr)

# Node'u değiştir
tree.body[0].value = new_expr

# AST artık çalıştırılabilir
compiled = compile(tree, filename="<ast>", mode="exec")
exec(compiled)  # x = 7

# -------------------------------------------------------------------
# Özet:
# - copy_location: sadece TEK node için geçerli
# - fix_missing_locations: tüm AST alt ağacında eksik konumları düzeltir
# -------------------------------------------------------------------
