import ast
import inspect

# ------------------------------------------------------------------------------
# ast.get_docstring Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# `ast.get_docstring(node, clean: bool = True) -> str | None`
#
# Bu fonksiyon, verilen AST node’unda (örneğin Module, FunctionDef, AsyncFunctionDef, ClassDef)
# eğer bir docstring (üç tırnaklı açıklama) varsa onu döner. Yoksa None döner.
#
# “Docstring”, Python’da fonksiyon, sınıf, modül gibi yapılar için ilk ifade olarak
# kullanılan ve `"""..."""` ile yazılmış açıklamadır.
#
# `get_docstring`, AST node’unun `body` alanındaki ilk elemanı kontrol eder;
# eğer bu eleman bir `Expr` node’u ve onun `value` alanı `Constant` / `Str` türünde bir sabit
# ise (yani bir string literal), bu string literal değeri docstring olarak kabul eder.
#
# Ayrıca `clean=True` parametresi ile, indentation (girintileme)
# otomatik temizleme işlemi uygulanır (yani `inspect.cleandoc` benzeri bir temizleme).
#
# Bu fonksiyon, yorum satırları değil, **docstring literal ifadeleri** ile çalışır.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.get_docstring(node: ast.AST, clean: bool = True) -> str | None
#
# PARAMETRELER:
# - node (ast.AST):
#     Docstring’ini almak istediğin node (Module, FunctionDef, ClassDef, AsyncFunctionDef)
# - clean (bool, default=True):
#     True ise, `inspect.cleandoc` kullanılarak girintileme kaldırılır, boş satırlar düzenlenir.
#
# DÖNÜŞ:
# - Eğer docstring varsa, string türünde döner (örneğin "Bu fonksiyon …"),
# - Eğer yoksa `None` döner.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ Kod analizi esnasında fonksiyonların, sınıfların veya modüllerin dokümantasyonunu elde etmek
# ✅ Otomatik dokümantasyon üreticileri, kod tarayıcısı araçları
# ✅ Docstring’lere dayalı test araçları (örneğin “her fonksiyonda docstring olmalı” gibi kontrol)
# ✅ Kod kalite araçları (lint, style checker)
# ✅ AST tabanlı belgeleme araçları
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# ❓ Neden `get_docstring` ayrı bir fonksiyon? `walk` ya da `NodeVisitor` ile mi yapılabilirdi?
#
# - `get_docstring` sadece **belirli node türlerinde** (Module, FunctionDef, ClassDef, AsyncFunctionDef)
#   bir docstring kontrolü yapar; tüm AST üzerinde indiscriminately dolaşmaz.
# - `walk` genel bir dolaşma sağlar, her node’a bakar; ama `get_docstring` özel bir kuralla
#   docstring olan node’ları tanır ve işlem yapar. `walk` tek başına docstring çıkarmak için
#   **çok genel** kalır.
# - `NodeVisitor` ile de benzer işlem yapılabilir: `visit_FunctionDef`, `visit_ClassDef` vs. yazarsın,
#   ve her node’un body’sinin ilk elemanına bakarsın. Bu yöntem `get_docstring`’in yaptığı işi
#   esnek ama daha uzun kodla yapar.
#
# - `get_docstring` kullanımı, belirli tipte node’larda hızlı ve standart docstring çıkarımını sağlar.
#   Böylece kod analizciler vs. bu ortak işlemi kendileri yeniden yazmak zorunda kalmaz.
#
# - İçsel olarak `get_docstring`, AST node’un `body` listesine bakar, ilk elemanın
#   bir `Expr(Constant string)` olup olmadığını kontrol eder ve gerekirse `inspect.cleandoc` ile
#   girintiyi düzeltir. Bu iş mantığı doğrudan node’u inceler; dolaşma (walk) yapmaz.
#
# - `get_docstring`, yorum satırları (`# …`) ile çalışmaz çünkü AST yorumları korumaz.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

# Örnek modül docstring
mod_src = '''"""
Bu modül örneği
"""

def foo(x):
    """
    Bu fonksiyon x’i döner
    """
    return x
'''

tree = ast.parse(mod_src)

# Modülün docstring’ini al
module_doc = ast.get_docstring(tree)
print("Modül docstring:", module_doc)

# Fonksiyonun docstring’ini al
func = tree.body[1]  # FunctionDef node
func_doc = ast.get_docstring(func)
print("Fonksiyon docstring:", func_doc)

# Eğer docstring yoksa None döner
src2 = "def bar():\n    return 1"
tree2 = ast.parse(src2)
print("bar docstring:", ast.get_docstring(tree2))  # None

# --------------------------------------------------------------------------
# Bu yorumlar ve örnekler ile get_docstring’in ne iş yaptığı, hangi kriterlere
# baktığı, walk/NodeVisitor ile farkı ve kullanımı açıkça görülür.
# --------------------------------------------------------------------------
