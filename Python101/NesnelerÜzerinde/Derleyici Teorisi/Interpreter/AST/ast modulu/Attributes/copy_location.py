# ------------------------------------------------------------------------------
# ast.copy_location Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# ast.copy_location, bir AST node'unun (örneğin yeni oluşturulmuş bir Constant)
# satır ve sütun (konum) bilgilerini, başka bir node'dan kopyalamak için kullanılır.
#
# Bu işlem, özellikle bir node'u başka bir node ile DEĞİŞTİRİRKEN (refactor ederken)
# kullanılır. Yeni node, eski node'un kaynak koddaki konumuna sahip olur.
# Bu sayede hata mesajları, traceback, debug ve coverage çıktıları doğru görünür.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.copy_location(new_node: ast.AST, old_node: ast.AST) -> ast.AST
#
# PARAMETRELER:
# - new_node: ast.AST
#     Konum bilgilerini alacak olan yeni AST node'u
# - old_node: ast.AST
#     Konum bilgilerini sağlayan eski AST node'u
#
# DÖNÜŞ:
# - Aynı new_node nesnesini döner, ama lineno, col_offset gibi konum bilgileri
#   old_node'dan kopyalanmış olur.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ Mevcut bir node'un yerine yeni bir node koyuluyorsa
# ✅ Refactor, transform, transpile işlemlerinde AST node'u değiştiriliyorsa
# ✅ Yeni node’un nerede olduğunu belirtmek gerekiyorsa
# ❌ Yeni bir kod bloğu veya satır ekleniyorsa (örn: import logging),
#    copy_location kullanılmaz! Bunun yerine lineno elle ayarlanır
#    veya increment_lineno kullanılır.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# - copy_location, sadece konum bilgilerini taşır; içerik, tip, behavior değişmez.
# - new_node zaten varsa lineno bilgilerini üzerine yazar (overwrite eder).
# - old_node’da lineno/col_offset yoksa new_node’a da taşınmaz.
# - Genellikle ast.fix_missing_locations ile birlikte kullanılır.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

import ast

# -------------------------------------------------------------------
# ✅ DOĞRU KULLANIM - Mevcut node'u değiştirme (refactor durumu)
# -------------------------------------------------------------------

code = "x = 1 + 2"
tree = ast.parse(code)

# Orijinal ifade: 1 + 2
old_expr = tree.body[0].value  # BinOp node

# Yeni ifade: 3 (henüz konum bilgisi yok)
new_expr = ast.Constant(value=3)

# Konum bilgisini kopyala
ast.copy_location(new_expr, old_expr)

# Yerine koy
tree.body[0].value = new_expr

# Artık 'x = 3' oldu ve satır bilgisi korunmuş durumda
print(ast.dump(tree, include_attributes=True))

# -------------------------------------------------------------------
# ❌ HATALI KULLANIM - Yeni satır eklerken copy_location yapılmaz
# -------------------------------------------------------------------

# Yeni kod: import logging
new_import = ast.parse("import logging").body[0]  # lineno=1 by default

# Bu kodu tree.body'ye eklemek istiyorsan, başka bir node'dan konum kopyalamak GEREKSİZ
# Çünkü bu node zaten kendi başına var ve başka bir node’un yerine geçmiyor

# Eğer bu node'u kodun ortasına ekliyorsan, satır bilgilerini elle ayarlamalısın
# ya da tree.body’nin geri kalanını increment_lineno ile ilerletmelisin

# Örnek:
# ast.increment_lineno(tree, 1)
# tree.body.insert(0, new_import)

# Bu durumda import logging lineno=1 olur,
# eski kod da lineno=2’den başlar.

# -------------------------------------------------------------------
# Özet:
# copy_location → yalnızca VAR OLAN bir node’un yerine yeni bir node koyarken
# increment_lineno → yeni bir node ekliyorsan, diğer node’ların satırlarını kaydırmak için
# -------------------------------------------------------------------
