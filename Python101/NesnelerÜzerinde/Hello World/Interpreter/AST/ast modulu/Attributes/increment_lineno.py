# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# ast.increment_lineno, Python'un ast (Abstract Syntax Tree) modülünde yer alır.
# Verilen bir AST node'unun ve onun tüm alt düğümlerinin `lineno` ve varsa
# `end_lineno` metadatalarını n kadar artırır.
#
# Bu, AST üzerinde kod ekleme, taşıma, dönüştürme gibi işlemler yapıldığında,
# satır bilgilerini gerçek konumla eşleştirmek için kullanılır.
# ------------------------------------------------------------------------------
# Özellikle debugging, trace, coverage gibi araçların doğru satır numarası
# göstermesi için önemlidir.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.increment_lineno(node: ast.AST, n: int = 1) -> ast.AST
#
# PARAMETRELER:
# - node (ast.AST):
#     İşlem yapılacak AST düğümüdür. Bu node ve altındaki tüm node'lar etkilenir.
# - n (int, varsayılan=1):
#     Kaç satır ileri kaydırılacağı. Pozitif bir tamsayı olmalıdır.
#
# DÖNÜŞ:
# - Girdi olarak verilen AST node'u döner, ama tüm uygun satır numaraları
#   n kadar artırılmış olur.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# - Kodun başına veya ortasına AST yoluyla yeni kod blokları eklendiğinde
# - Debugger / hata mesajlarında doğru satır gösterimi gerektiğinde
# - Test coverage araçlarında doğru analiz sağlamak için
# - Kod jenerasyonu ve transpile süreçlerinde
# - AST tabanlı refaktör araçlarında veya linters
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# - increment_lineno, verilen node ve tüm alt düğümlerini etkiler.
#   Sonradan eklenen node'lar da bu işlemden etkilenebilir.
#
# - Eğer yeni kod eklediysen, önce yeni kodu ayrı AST olarak üret,
#   sonra eski kodun satırlarını kaydır, ardından birleştir.
#
# - Python 3.8+ ile birlikte gelen `end_lineno` da artırılır.
#
# - `lineno` içermeyen node'lar bu işlemden etkilenmez (örneğin bazı `expr`’ler).
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

# 📘 Örnek 1: Basit lineno arttırma
import ast

source = "x = 1\ny = 2"
tree = ast.parse(source)

# lineno değerlerini 10 artır
ast.increment_lineno(tree, 10)

print(ast.dump(tree, include_attributes=True))
# Beklenen: x = 1 -> lineno=11, y = 2 -> lineno=12

# ------------------------------------------------------------------------------

# 📘 Örnek 2: Kodun başına satır eklemek ve satır numaralarını düzeltmek

# Orijinal kod
original_code = "def foo():\n    return 42"
original_tree = ast.parse(original_code)

# Eklemek istediğimiz kod (2 satır)
extra_code = "import logging\nlogging.basicConfig(level=logging.INFO)"
extra_tree = ast.parse(extra_code)

# Orijinal kodu 2 satır ileri kaydırıyoruz
ast.increment_lineno(original_tree, 2)

# AST'leri birleştiriyoruz
extra_tree.body.extend(original_tree.body)

# Sonuç olarak oluşan AST:
final_tree = extra_tree

print(ast.dump(final_tree, include_attributes=True))

# Beklenen:
# import logging -> lineno=1
# logging.basicConfig(...) -> lineno=2
# def foo(): -> lineno=3
# return 42 -> lineno=4

# ------------------------------------------------------------------------------

# Bu yapı, kod enjekte edilen durumlarda lineno uyumsuzluklarını düzeltir
# ve hata mesajlarının, debugger'ların, coverage araçlarının düzgün çalışmasını sağlar.
