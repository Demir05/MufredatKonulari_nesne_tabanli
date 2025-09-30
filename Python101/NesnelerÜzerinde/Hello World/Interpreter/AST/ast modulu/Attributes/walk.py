# ------------------------------------------------------------------------------
# ast.walk Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# `ast.walk(node)` fonksiyonu, verilen AST node’unun kendisi dahil olmak üzere
# tüm alt düğümlerini **rekürsif olarak** dolaşır ve her bir node’u sırayla
# “yield” eder (iterator mantığında). :contentReference[oaicite:0]{index=0}
#
# Yani, AST ağacını gezmek istediğinde, `walk` sana ağacın tüm node’larını
# tek bir iterable üzerinden verir. Context (yani hangi alt ağaçtan geldiği)
# bilgisi taşımaz, sadece node’lar gelir.
#
# Dikkat: `walk`’un dolaşım sırası **belirtilmemiştir** (dokümantasyonda “no specified order”) :contentReference[oaicite:1]{index=1}
# Yani derleyici bir BFS ya da DFS kullanabilir; bu değişebilir. :contentReference[oaicite:2]{index=2}
# Bu yüzden `walk`’un sıraya dayalı mantığı güvenilemez.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.walk(node: ast.AST) -> Iterator[ast.AST]
#
# PARAMETRELER:
# - node (ast.AST): AST ağacının herhangi bir kök düğümü (örneğin Module,
#   Expression, vb.)
#
# DÖNÜŞ:
# - Bir iterator (genellikle generator) döner; bu generator, `node`’u ve
#   onun tüm alt node’larını yield eder.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ AST üzerindeki her node’u hızlıca görmek / incelemek
# ✅ Belirli tipte node’ları (örneğin ast.Assign, ast.Call) toplamak
# ✅ Basit modifikasyonlar, analizler (ama context gerekmezse)
# ✅ AST transform işlemlerinde, özellikle context önemsizse
# ✅ Hızlı gezinti; karmaşık ziyaret yapıları olmayan senaryolarda
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# - `walk` sırası belirtilmemiştir; yani node’lar herhangi bir sırayla gelebilir. :contentReference[oaicite:3]{index=3}
# - Eğer bağlam (hangi parent’tan geldiği) önemliyse, `walk` kötü seçim olabilir
# - `walk` subtree’leri “atlama” olanağı vermez: her node’u gezer
# - `NodeVisitor` / `NodeTransformer` sınıfları ile karşılaştırıldığında `walk` daha basit,
#   ama esneklik ve kontrol açısından sınırlıdır
# - Bazı kaynaklar, `walk`’un pratikte breadth-first (yatay) dolaşım gerçekleştirdiğini söyler, ama bu davranış garanti değildir :contentReference[oaicite:4]{index=4}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

import ast

# Örnek 1: Basit walk kullanımı
src = """
def foo(a):
    return a + 1

b = foo(5)
"""

tree = ast.parse(src)

# ast.walk ile tüm node’ları yazdır
for node in ast.walk(tree):
    print(type(node).__name__, getattr(node, "lineno", None))

# Bu çıktıda Module, FunctionDef, arguments, arguments içindeki arg, Return, BinOp, Name, Constant, Assign, Call, vb. node’lar görünür.

# Örnek 2: Belirli bir tip için filtreleme (örneğin tüm Assign’ler)
assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
for a in assigns:
    print("Found Assign at lineno:", a.lineno)

# Örnek 3: walk sırasının belirsizliği örneği
#
# Metin:
# def foo():
#   if cond:
#       return 1
#   else:
#       return 2
#
# Bu yapıda `walk` çıktısındaki `Return` node’larının sırası garanti edilmez:
# Belki önce `return 2` sonra `return 1` gelebilir, ya da tersine — dokumentasyonda bu belirsiz olarak geçer. :contentReference[oaicite:5]{index=5}

# --------------------------------------------------------------------------
# Bu yorumlar ve örnekler, ast.walk’un ne iş yaptığı, ne zaman kullanılması
# gerektiği ve dikkat edilmesi gereken özellikleri tam biçimde açıklar.
# --------------------------------------------------------------------------
