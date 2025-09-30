# ===============================================================
# 📘 PYTHON `ast` MODÜLÜ — MODÜL DÜZEYİ ATTRIBUTE & FONKSİYONLAR
# ===============================================================
# 🔹 Bu dosya, ast modülünde pratikte en çok kullanılan fonksiyonların
#     tanımını, imzasını, kullanım alanını ve dikkat edilmesi gereken noktaları içerir.
# 🔹 NodeVisitor, NodeTransformer, AST gibi sınıflar ayrı ele alındı;
#     burada sadece "modül düzeyi fonksiyonlar" var.
# 🔹 Referans: https://docs.python.org/3/library/ast.html

import ast

# ---------------------------------------------------------------
# ✅ parse
# ---------------------------------------------------------------
# 🔹 Kaynak kodu (string) AST ağacına dönüştürür.
# 🔹 İmza: ast.parse(source, filename="<unknown>", mode="exec", type_comments=False, feature_version=None)
# 🔹 Kullanım alanı:
#     - Bir Python kodunu parse ederek AST üzerinde analiz yapmak
#     - Refactoring ve transpiler yazmak
# 🔹 Dikkat:
#     - "mode" parametresi "exec", "eval" veya "single" olabilir.
#       • exec → script/multi-line
#       • eval → tek bir ifade
#       • single → tek satırlık interaktif ifade
tree = ast.parse("x = 1 + 2")
print(type(tree))  # <class 'ast.Module'>


# ---------------------------------------------------------------
# ✅ dump
# ---------------------------------------------------------------
# 🔹 AST nesnesini string olarak "debug friendly" biçimde döndürür.
# 🔹 İmza: ast.dump(node, annotate_fields=True, include_attributes=False, indent=None)
# 🔹 Kullanım alanı:
#     - AST’yi okunabilir biçimde görmek
#     - Debugging ve eğitim amaçlı
# 🔹 Dikkat:
#     - include_attributes=True dersek lineno/col_offset gibi metadata da görünür.
print(ast.dump(tree, indent=4))


# ---------------------------------------------------------------
# ✅ unparse (Python 3.9+)
# ---------------------------------------------------------------
# 🔹 AST’yi tekrar Python kaynak koduna dönüştürür.
# 🔹 İmza: ast.unparse(node)
# 🔹 Kullanım alanı:
#     - AST üzerinde yapılan değişiklikleri tekrar kaynak koda dökmek
#     - Kod dönüştürücü / transpiler yazmak
# 🔹 Dikkat:
#     - Yorum satırları, whitespace, format gibi görsel detaylar korunmaz.
print(ast.unparse(tree))  # "x = 1 + 2"


# ---------------------------------------------------------------
# ✅ walk
# ---------------------------------------------------------------
# 🔹 Bir AST ağacındaki tüm node’ları generator olarak dolaşır (depth-first).
# 🔹 İmza: ast.walk(node)
# 🔹 Kullanım alanı:
#     - Bir AST’deki tüm node’ları düz bir liste halinde taramak
#     - Filtreleme ile "tüm FunctionDef node’larını bul" gibi sorgular
for node in ast.walk(tree):
    print(type(node).__name__)


# ---------------------------------------------------------------
# ✅ iter_child_nodes
# ---------------------------------------------------------------
# 🔹 Bir node’un doğrudan alt node’larını iterasyonla döner.
# 🔹 İmza: ast.iter_child_nodes(node)
# 🔹 Kullanım alanı:
#     - Yalnızca immediate children üzerinde gezinmek
#     - walk kadar derine gitmez → daha kontrollü traversal
for child in ast.iter_child_nodes(tree):
    print("Child:", type(child).__name__)


# ---------------------------------------------------------------
# ✅ fix_missing_locations
# ---------------------------------------------------------------
# 🔹 AST node’larının eksik lineno/col_offset bilgilerini doldurur.
# 🔹 İmza: ast.fix_missing_locations(node)
# 🔹 Kullanım alanı:
#     - AST üzerinde değişiklik yaptıysan ve compile() edeceksen
#     - Metadata eksikse hata almamak için
# 🔹 Dikkat:
#     - Konum bilgisi olmayan node’lara en yakın üst node’un konumunu kopyalar.
tree_fixed = ast.fix_missing_locations(tree)


# ---------------------------------------------------------------
# ✅ increment_lineno
# ---------------------------------------------------------------
# 🔹 Node’ların satır numaralarını belli bir offset kadar artırır.
# 🔹 İmza: ast.increment_lineno(node, n=1)
# 🔹 Kullanım alanı:
#     - Bir node’u başka bir dosyadan/konumdan taşıyorsan satır numaralarını kaydırmak
# 🔹 Dikkat:
#     - Orijinal metadata üzerine yazılır.
tree_shifted = ast.increment_lineno(tree, n=10)


# ---------------------------------------------------------------
# ✅ copy_location
# ---------------------------------------------------------------
# 🔹 Bir node’a başka bir node’un konum bilgilerini (lineno, col_offset, end_lineno, end_col_offset) kopyalar.
# 🔹 İmza: ast.copy_location(new_node, old_node)
# 🔹 Kullanım alanı:
#     - Yeni üretilmiş bir node’u compile edilebilir hale getirmek için
# 🔹 Dikkat:
#     - Metadata doğru taşınmazsa hata mesajları yanlış satırda çıkar.
binop = tree.body[0].value
new_node = ast.Constant(value=99)
new_node = ast.copy_location(new_node, binop)


# ---------------------------------------------------------------
# ✅ get_docstring
# ---------------------------------------------------------------
# 🔹 Bir sınıf, fonksiyon veya modülün docstring’ini döner.
# 🔹 İmza: ast.get_docstring(node, clean=True)
# 🔹 Kullanım alanı:
#     - AST üzerinden docstring çıkarmak
#     - Otomatik dokümantasyon araçları
# 🔹 Dikkat:
#     - clean=True → common indentation temizlenir
code = '''\
def foo():
    """Benim docstring"""
    return 1
'''
tree = ast.parse(code)
func = tree.body[0]
print(ast.get_docstring(func))  # "Benim docstring"


# ---------------------------------------------------------------
# ✅ literal_eval
# ---------------------------------------------------------------
# 🔹 Sadece literal veri yapıları içeren bir ifadeyi güvenli şekilde değerlendirir.
# 🔹 İmza: ast.literal_eval(node_or_string)
# 🔹 Kullanım alanı:
#     - JSON benzeri string → Python objesine çevirme
#     - Güvenlik amacıyla eval yerine kullanılabilir
# 🔹 Dikkat:
#     - Yalnızca str, bytes, numbers, tuples, lists, dicts, sets, booleans, None izinlidir.
print(ast.literal_eval("[1, 2, 3]"))  # [1, 2, 3]


# ===============================================================
# ✅ Özet
# ===============================================================
# - parse → string koddan AST
# - dump → AST’yi string olarak gör
# - unparse → AST → kaynak kod
# - walk → tüm node’ları dolaş
# - iter_child_nodes → sadece alt node’ları dolaş
# - fix_missing_locations → eksik lineno/col bilgilerini doldur
# - increment_lineno → satır numaralarını kaydır
# - copy_location → node’a başka node’un metadata’sını kopyala
# - get_docstring → docstring çek
# - literal_eval → güvenli literal değerlendirme
