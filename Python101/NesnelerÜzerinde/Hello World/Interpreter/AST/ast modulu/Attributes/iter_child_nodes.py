# ------------------------------------------------------------------------------
# ast.iter_child_nodes Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# `ast.iter_child_nodes(node)` fonksiyonu, verilen bir AST düğümünün **doğrudan çocuk** node’larını iterable olarak döner.
# Yani, `node`’un tüm alt alanlarındaki (fields) AST node tipindeki değerler ve
# listelerdeki node öğeleri tek tek çıkarılır.
#
# Bu fonksiyon, AST üzerindeki hiyerarşik ilişkileri anlamak için temel yapı taşlarından biridir.
# Green Tree Snakes belgesinde, “many nodes have children in several sections … ast.iter_child_nodes will go through all of these” denir. :contentReference[oaicite:0]{index=0}
# Python dokümantasyonundaki “ast Helpers” bölümünde de `iter_child_nodes(node)`’un “direct child nodes” döndürdüğü tanımlıdır. :contentReference[oaicite:1]{index=1}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.iter_child_nodes(node: ast.AST) -> Iterator[ast.AST]
#
# PARAMETRELER:
# - node (ast.AST): Çocuklarını almak istediğin AST düğümü
#
# DÖNÜŞ:
# - Bir iterator döner. Bu iterator, `node`’un doğrudan çocuk AST node’larını sırayla verir.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ Bir node’un alt node yapılarını tek aşamada keşfetmek
# ✅ NodeVisitor / custom traversal’da `generic_visit`’in kullandığı altyapı
# ✅ `walk` gibi geniş kapsamlı traversal algoritmalarında temel yapı
# ✅ AST modifikasyonu yaparken önce doğrudan çocukları kontrol etmek
# ✅ Hiyerarşik analiz, çocuk-bağlam çözümlemesi
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# ❓ Neden `iter_child_nodes` / neden tek başına `walk` yeterli değil?
#
# - `iter_child_nodes` yalnızca **doğrudan çocukları** verir, **derin alt ağacı değil**.
#   Bu sayede, sadece bir adım derinlikteki ilişkileri hızlıca inceleyebilirsin.
#
# - `walk` ise, tüm ağacı (tümü) dolaşır, yani `iter_child_nodes`’un çıktısını
#   kullanan bir algoritmanın sürekli çok derine gitmesini sağlar — yani `walk` = iter + recursion / queue üzerine kurulu.
#
# - `walk` sırasıyla genişlik öncelikli (yatay önce) dolaşır, sonra derinliğe iner.
#   Ama `iter_child_nodes` yalnızca tek seviye çocukları döndürür.
#   Dolayısıyla `iter_child_nodes`, `walk` gibi global bir sıralama sunmaz;
#   sadece o anki node’dan bir seviye aşağı iner.
#
# - `iter_child_nodes` kullanmak, daha kontrollü traversal yapabilmeni sağlar. Örneğin:
#     ```python
#     for child in iter_child_nodes(node):
#         # sadece bir seviye çocuk ile işlem yap
#     ```
#
# - Ayrıca `NodeVisitor.generic_visit` içinde `iter_child_nodes` kullanılır, bu yüzden
#   kendi traversal'ını özelleştirirken doğrudan `iter_child_nodes` kullanmak doğal bir yaklaşımdır.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

import ast

# Örnek: Basit bir AST ve iter_child_nodes kullanımı
src = """
def foo(x):
    return x * 2
"""

tree = ast.parse(src)

# Module node’un çocuklarını al
for child in ast.iter_child_nodes(tree):
    print("Child of Module:", type(child).__name__)

# Bu muhtemelen:
# Child of Module: FunctionDef

# Örnek: FunctionDef node’un doğrudan çocukları
func = tree.body[0]
for c in ast.iter_child_nodes(func):
    print("Child of FunctionDef:", type(c).__name__)
# Örneğin:
# Child of FunctionDef: arguments
# Child of FunctionDef: Return
# Child of FunctionDef: decorator_list (liste ama iter_child_nodes bunu filtreleyip node’lar verir)

# Örnek: iter_child_nodes ile kendi DFS traversal’ını yazmak
def my_dfs(node):
    yield node
    for child in ast.iter_child_nodes(node):
        yield from my_dfs(child)

print("DFS via iter_child_nodes + recursion:")
for n in my_dfs(tree):
    print(type(n).__name__, getattr(n, "lineno", None))

# Bu `my_dfs`, `walk`’un yaptığı gibi tüm node’ları gezer, ama traversal sırayı sen belirlersin.

# --------------------------------------------------------------------------
# Bu yorumlar ve örnekler `iter_child_nodes` fonksiyonunun mantığını,
# `walk` ile ilişkisini, kullanım senaryolarını ve dikkat edilmesi gerekenleri
# tam olarak anlatır.
# --------------------------------------------------------------------------
