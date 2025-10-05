# ===============================================================
# 🧠 AST’de `None` Kavramı — Sözel + Teknik Derleme
# ===============================================================
#
# Python’da `None` tekil (singleton) bir objedir:
# - Normalde bir değişkene atanabilir (x = None)
# - Fonksiyon return etmezse default dönüş değeri olur
#
# Ama AST tarafında aynı `None` nesnesi 3 farklı bağlamda kullanılır.
# ===============================================================

# ---------------------------------------------------------------
# ✅ 1. Literal `None` (kodda gerçekten yazılmış)
# ---------------------------------------------------------------
# Kod:
#   x = None
#
# AST:
#   Assign(
#       targets=[Name(id='x', ctx=Store())],
#       value=Constant(value=None)   👈 Literal None
#   )
#
# 🔸 Burada `None`, Constant node’una gömülmüş durumda.
# 🔸 Kodda gerçekten "None" yazıldığını temsil eder.
# 🔸 Runtime’da bu node → gerçek `None` nesnesini üretir.

# ---------------------------------------------------------------
# ✅ 2. Opsiyonel Alanlarda `None` (kodda hiç yazılmamış)
# ---------------------------------------------------------------
# Kod:
#   def f(): pass
#
# AST:
#   FunctionDef(
#       name='f',
#       args=arguments(...),
#       body=[Pass()],
#       returns=None   👈 opsiyonel alan boş → None
#   )
#
# 🔸 Burada `None`, kodda olmayan bir şeyin göstergesidir.
# 🔸 Yani "bu field boş bırakılmış" demektir.
# 🔸 Örn: dönüş tipi annotation yok → returns=None
#
# Kod:
#   def f(): return
# AST:
#   Return(value=None)  👈 Return ifadesinde değer yok

# ---------------------------------------------------------------
# ✅ 3. NodeTransformer İçinde `None` (node’u silmek için)
# ---------------------------------------------------------------
# Transformer:
#   class RemoveAssign(ast.NodeTransformer):
#       def visit_Assign(self, node):
#           return None
#
# Kod:
#   x = 1
#
# AST Sonucu:
#   Assign node tamamen silinir, sanki hiç yazılmamış gibi.
#
# 🔸 NodeTransformer’da return None = "bu node’u ağaçtan çıkar"
# 🔸 Eğer alan bir listeyse (örn. Module.body) → listeden atılır
# 🔸 Eğer alan opsiyonelse → alan boş bırakılır
# 🔸 Buradaki `None` bir "silme sinyali"dir

# ---------------------------------------------------------------
# 🧩 Genel Özet — AST’de `None`’un 3 Farklı Anlamı
# ---------------------------------------------------------------
# 1) Constant(value=None) → Kodda gerçekten `None` yazılmıştır
# 2) field=None           → Opsiyonel alan boş bırakılmıştır
# 3) return None          → NodeTransformer node’u silsin
#
# 🔍 Tek bir Python nesnesi (None), ama AST içinde üç ayrı semantik taşır:
#   ➤ Değer (literal)
#   ➤ Yokluk (opsiyonel boşluk)
#   ➤ Silme sinyali (dönüşümde)
# ===============================================================
