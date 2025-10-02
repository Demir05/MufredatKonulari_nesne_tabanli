# ------------------------------------------------------------------------------
# AST Yapılarında `_fields`, `_attributes` ve `body` Üzerine Tam Tanım
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------

# ✅ _fields:
# Her bir AST düğümünün içerdiği temel alanların (field) adlarını tuple olarak içerir.
# Yani bu düğümün hangi alt bileşenleri barındırdığını tanımlar.
# Örn: ast.FunctionDef._fields → ('name', 'args', 'body', 'decorator_list', 'returns')

# ✅ _attributes:
# Konum bilgisi gibi teknik ancak derleme açısından gerekli olan metadata alanlarını belirtir.
# Bunlar çoğunlukla: ('lineno', 'col_offset', 'end_lineno', 'end_col_offset')

# ✅ body:
# Fonksiyon, sınıf, modül, if, for gibi blok yapılı node’ların içindeki ifade listesini içerir.
# Genellikle liste (List[ast.AST]) olarak gelir ve yürütülecek kod bloklarını barındırır.

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------

# - _fields: Tuple[str, ...]
# - _attributes: Tuple[str, ...]
# - body: List[ast.AST]

# Not:
# Bu alanlar genellikle düğüm sınıfı tanımı sırasında C veya Python tarafında otomatik tanımlanır.
# Doğrudan değiştirilmezler ama inceleme/işleme için okunur.

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------

# ✅ AST'deki düğüm yapısını çözümlemek için kullanılır
# ✅ Bir node'un hangi bilgileri içerdiğini belirlemek için
# ✅ AST traversal (gezinme) fonksiyonları için temel referans sağlar
# ✅ AST modifikasyonu sırasında hangi alanların ziyaret edileceğini belirlemek için
# ✅ Docstring tespiti, function/assign gibi yapıları ayırmak için
# ✅ Özel ziyaretçiler (NodeVisitor) ve transformer'lar (NodeTransformer) bu alanlara güvenir

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------

# ⚠️ Neden bu kadar önemli?

# - _fields, düğümün yapısal şemasını temsil eder: Traversal fonksiyonları örn: iter_fields, iter_child_nodes bu alanı temel alır.
# - _attributes, derleme için zorunludur: lineno gibi metadata’lar eksikse → compile() TypeError verir.
# - body, kod bloğu barındıran her düğümde içeriklerin nerede olduğunu gösteren temel referanstır.

# 📌 AST analiz, refactor ve kod üretiminde bu 3 alanın bilinmesi şarttır.
# - fix_missing_locations, bu metadata bilgilerini _attributes'a göre doldurur.
# - get_docstring gibi fonksiyonlar doğrudan body[0] üzerinden işlem yapar.
# - NodeVisitor sınıfı, _fields içindeki her alanı gezer.

# Bu yapılar, AST sisteminin iskeleti gibidir 🧱

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEK
# ------------------------------------------------------------------------------

import ast

source = '''
def greet(name):
    """Says hello"""
    print("Hello", name)
'''

tree = ast.parse(source)
func_node = tree.body[0]

print(func_node._fields)
# Çıktı: ('name', 'args', 'body', 'decorator_list', 'returns', 'type_comment')

print(func_node._attributes)
# Çıktı: ('lineno', 'col_offset', 'end_lineno', 'end_col_offset')

print(func_node.body)
# Çıktı: [Expr(...), ...]  ← fonksiyonun içindeki kod satırları (AST node’ları)

# ------------------------------------------------------------------------------
# Bu yapılar olmadan ne traverse yapılabilir, ne konum bilgisi atanabilir, ne de
# kod anlamlandırılabilir.
# ------------------------------------------------------------------------------
