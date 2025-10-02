# -----------------------------------------------
# 1) TANIM
# -----------------------------------------------

# 🔁 ast.walk(node)
# Verilen bir AST node'dan başlayarak, o düğüm ve tüm alt düğümlerini sırayla dolaşır.
# Bu dolaşım genişlik öncelikli (BFS tarzı) gibi görünür çünkü deque kullanılarak yapılır.
# Ancak resmi olarak belirli bir sıralama garantisi vermez.
# Kullanımı basittir, tüm ağacı düz biçimde verir.

# 🌿 ast.iter_child_nodes(node)
# Verilen AST düğümünün **yalnızca doğrudan alt çocuk düğümlerini** döndürür.
# Liste içinde olan (örneğin `body`, `orelse`) alanlardaki AST nesnelerini de otomatik çözer.
# Genellikle traversal sınıflarında (`NodeVisitor`, `NodeTransformer`) kullanılır.

# 🧩 ast.iter_fields(node)
# Verilen AST düğümündeki tüm alanları (field name, value) çiftleri şeklinde döndürür.
# Alanlar `AST`, `list`, `str`, `int`, `None` gibi türlerde olabilir.
# AST'yi analiz etmek, modifiye etmek veya daha detaylı işlem yapmak için idealdir.

# -----------------------------------------------
# 2) SÖZDİZİMİ
# -----------------------------------------------

# ast.walk(node: AST) -> Generator[AST, None, None]
# ast.iter_child_nodes(node: AST) -> Generator[AST, None, None]
# ast.iter_fields(node: AST) -> Generator[Tuple[str, Any], None, None]

# Parametre: node → ast.AST türünde bir kök düğüm
# Dönüş tipi: generator → üzerinde for döngüsüyle gezilebilir

# -----------------------------------------------
# 3) KULLANIM ALANLARI
# -----------------------------------------------

# ✅ walk:
# - Hızlıca AST üzerinde tüm düğümleri dolaşmak istenirse
# - Yüzeysel analiz veya node türlerini tespit etmek için
# - Örneğin: tüm `ast.Call` veya `ast.Assign` node’larını bulmak

# ✅ iter_child_nodes:
# - Traversal sınıfları (`NodeVisitor`, `NodeTransformer`) içinde
# - DFS traversal yazmak için temel yapı
# - Yapıyı daha kontrollü gezmek istiyorsan ideal

# ✅ iter_fields:
# - Her bir alanı adlarıyla birlikte görmek istiyorsan
# - AST node’unu debug etmek, yapı çözümlemek
# - AST modifikasyonu (yeni node ekleme, silme) gibi durumlarda

# -----------------------------------------------
# 4) EKSTRA — KARŞILAŞTIRMA & HANGİSİ NE ZAMAN?
# -----------------------------------------------

# 🔄 walk vs iter_child_nodes:
# - walk tüm ağacı dolaşır (BFS gibi)
# - iter_child_nodes yalnızca bir düğümün çocuklarını verir
# → Eğer düğümleri derinlemesine kontrol etmek istiyorsan: iter_child_nodes + recursive traversal

# 🧠 iter_child_nodes vs iter_fields:
# - iter_child_nodes sadece AST türü objeleri döndürür
# - iter_fields tüm alanları döndürür (AST olmayanlar dahil)
# → AST değiştiriyorsan veya detaylı analiz istiyorsan: iter_fields

# 🎯 Hangi Durumda Hangisini Seçmeliyim?

# ✔️ Tüm AST’yi hızlıca gezmek istiyorum → ast.walk
# ✔️ Kendi recursive traverserımı yazacağım → ast.iter_child_nodes
# ✔️ AST node’un alanlarını adlarıyla görmek istiyorum → ast.iter_fields
# ✔️ NodeVisitor gibi sınıflar yazacağım → ast.iter_child_nodes (zaten default)
# ✔️ AST’yi modifiye edeceğim → ast.iter_fields + setattr

# -----------------------------------------------
# 5) ÖRNEK
# -----------------------------------------------

import ast

tree = ast.parse("x = 1 + 2")

# 🎯 walk
for node in ast.walk(tree):
    print("walk:", type(node))

# 🎯 iter_child_nodes
for child in ast.iter_child_nodes(tree):
    print("child:", type(child))

# 🎯 iter_fields
for name, value in ast.iter_fields(tree.body[0]):
    print("field:", name, "→", value)


def iter_fields(node):
    """
    Yield a tuple of (fieldname, value) for each field in node._fields
    that is present on node.
    """
    for field in node._fields:
        try:
            yield field, getattr(node, field)
        except AttributeError:
            pass


def iter_child_nodes(node):
    """
    Yield all direct child nodes of *node*, that is, all fields that are nodes
    and all items of fields that are lists of nodes.
    """
    for name, field in iter_fields(node):
        if isinstance(field, AST):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, AST):
                    yield item


def walk(node):
    """
    Recursively yield all descendant nodes in the tree starting at *node*
    (including *node* itself), in no specified order. ...
    """
    from collections import deque
    todo = deque([node])
    while todo:
        node = todo.popleft()
        todo.extend(iter_child_nodes(node))
        yield node
