# ===============================================================
# 📘 `ast.NodeVisitor` SINIFI
# ===============================================================

# ✅ # ===============================================================
# # 📘 `ast.NodeVisitor` SINIFI — DETAYLI TANIM
# # ===============================================================
#
# # ✅ 1. Genel Tanım
# # ---------------------------------------------------------------
# # 🔹 `NodeVisitor`, `ast` modülünde tanımlı bir yardımcı (utility) sınıftır.
# # 🔹 Amacı: AST ağacı üzerinde “dolaşmayı” (traversal) kolaylaştırmak.
# # 🔹 Kendi başına bir AST node’u değildir — yani kaynak kodu temsil etmez.
# # 🔹 Visitor tasarım desenine uygun olarak çalışır:
# #     - Her node için `visit_*` isimli method arar.
# #     - Örneğin: `visit_BinOp`, `visit_FunctionDef`, `visit_Assign`.
# #     - Eğer böyle bir method yoksa → `generic_visit` çağrılır.
# # 🔹 Bu sayede AST üzerinde analiz veya inceleme yaparken her node tipi için
# #     ayrı ayrı davranış tanımlayabilirsin.
#
# # ---------------------------------------------------------------
# # ✅ 2. Mekanizma nasıl çalışır?
# # ---------------------------------------------------------------
# # 🔹 Sen `visitor.visit(node)` çağırdığında:
# #     1. Node’un sınıf adı alınır → örn. BinOp
# #     2. Bu ada uygun metod adı türetilir → "visit_BinOp"
# #     3. Eğer subclass içinde bu metod tanımlıysa → o çağrılır
# #     4. Yoksa → fallback olarak `generic_visit(node)` çağrılır
# #
# # 🔍 Örneğin:
# #     - `visit_BinOp` metodun varsa → sadece BinOp node’larında çalışır
# #     - Eğer tanımlı değilse → generic_visit tüm alt node’ları gezmeye devam eder
# #
# # 🔸 Pseudo-code (aslında NodeVisitor’ın içindeki `visit` metodu şöyle çalışır):
# #     def visit(self, node):
# #         method_name = "visit_" + node.__class__.__name__
# #         visitor = getattr(self, method_name, self.generic_visit)
# #         return visitor(node)
#
# # ---------------------------------------------------------------
# # ✅ 3. `visit_*` metodları ne zaman çalışır?
# # ---------------------------------------------------------------
# # 🔹 AST üzerinde `visit()` çağrıldığında traversal başlar.
# # 🔹 Hangi node’a gelinirse, o node’un tipine uygun `visit_*` metodu tetiklenir.
# # 🔹 Eğer o node için özel metod tanımlı değilse → generic_visit çalışır.
# # 🔹 her dispatch metodunda mutlaka generic_visit olmalı aksi halde alt düğümler üzerinde gezilemez
# # Örn:
# # class MyVisitor(ast.NodeVisitor):
# #     def visit_BinOp(self, node):
# #         print("BinOp bulundu:", ast.dump(node))
# #         self.generic_visit(node)
# #
# # tree = ast.parse("x = 1 + 2")
# # MyVisitor().visit(tree)
# #
# # Çıktı:
# # BinOp bulundu: BinOp(left=Constant(value=1), op=Add(), right=Constant(value=2))
#
# # ---------------------------------------------------------------
# # ✅ 4. `generic_visit` ne yapar?
# # ---------------------------------------------------------------
# # 🔹 Varsayılan traversal davranışıdır.
# # 🔹 Node’un `_fields` içindeki tüm alt node’larını bulur → `visit()` ile gezer.
# # 🔹 Yani sen hiçbir şey override etmesen bile, generic_visit tüm AST’yi dolaşır.
# # 🔹 ayrıca alt node'ları bulduğu için recursion olmaz.
# # 🔹 gezme işleminde herangi bir düğümü değiştirmek gayesi olmadığı için side effect yoktur
# # 🔹 yani herangi bir düğüm return edilmez

# # Örn: Assign node’unun targets ve value alanları vardır.
# # generic_visit bu alanlara girerek alt node’ları da ziyaret eder.
#
# # ---------------------------------------------------------------
# # ✅ 5. `walk` ile farkı
# # ---------------------------------------------------------------
# # 🔹 `ast.walk(node)` → bir generator’dır, AST’deki tüm node’ları sırayla yield eder.
# # 🔹 Ama hiçbir dispatch yapmaz, yani `visit_*` metodlarını çağırmaz.
# # 🔹 Sadece raw node nesnelerini verir → sen kendin if isinstance ile ayrım yaparsın.
# #
# # Örn:
# # for node in ast.walk(tree):
# #     print(type(node).__name__)
# #
# # Çıktı:
# # Module
# # Assign
# # Name
# # BinOp
# # Constant
# # Constant
# # Store
# # Add
# #
# # 🔍 Yani:
# # - NodeVisitor.visit → "akıllı traversal" (uygun visit_* çağrılır)
# # - ast.walk → "kör traversal" (sadece node’ları verir, sen yorumlarsın)
#
# # ---------------------------------------------------------------
# # ✅ 6. Senior-level yorum
# # ---------------------------------------------------------------
# # 🔸 NodeVisitor = "okuyucu": sadece AST’yi dolaşır, tipine göre özel davranış uygular.
# # 🔸 walk = "ham tarayıcı": tüm node’ları verir, hiçbir özel davranış çalıştırmaz.
# # 🔸 generic_visit = "varsayılan gezgin": sen özel metod yazmadıysan bile node’ları gezer.
# # 🔸 Bu yapı Visitor tasarım deseninin tam karşılığıdır:
# #     • visit_* → özel davranış
# #     • generic_visit → default davranış
# #     • visit() → dispatch mekanizması
#
# # ---------------------------------------------------------------
# # ✅ 7. Özet
# # ---------------------------------------------------------------
# # - NodeVisitor → AST’yi tip tabanlı dispatch ile dolaşır
# # - visit_* → node tipine özel metodlar
# # - generic_visit → varsayılan traversal
# # - walk → dispatchsiz düz tarama

import ast
class MyVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print(f"Fonksiyon bulundu: {node.name} (line {node.lineno})")
        self.generic_visit(node)  # alt node’ları da gez


# ✅ 2. Kullanım Alanları
# ---------------------------------------------------------------
# 🔸 Kod Analizi
#     - Fonksiyonların, değişkenlerin, import’ların bulunduğu yerleri tespit etme.
#     - Linter, static analysis, güvenlik tarayıcıları.
#
# 🔸 Kod Metriği
#     - Bir dosyada kaç tane if var? kaç tane loop var?
#     - Hangi fonksiyon kaç satırdan oluşuyor?
#
# 🔸 IDE & Refactoring Araçları
#     - "Go to definition", "Find all functions", "AutoDoc" gibi özellikler.
#
# 🔍 Not: `NodeVisitor` AST’yi değiştirmez → sadece okur/anlamlandırır.


# ✅ 3. Miras alınabilir mi?
# ---------------------------------------------------------------
# 🔹 Evet, `NodeVisitor` normal bir Python sınıfıdır → subclass alabilirsin.
# 🔹 Pratikte zaten her zaman subclass alarak kullanılır.
# 🔹 Çünkü işlevi ancak `visit_*` methodlarını override ettiğinde ortaya çıkar.
#
# Örn:
class FuncCollector(ast.NodeVisitor):
    def __init__(self):
        self.funcs = []
    def visit_FunctionDef(self, node):
        self.funcs.append(node.name)
        self.generic_visit(node)   # alt node’ları da gez


# ✅ 4. Örneklenebilir mi?
# ---------------------------------------------------------------
# 🔹 Evet, `NodeVisitor` doğrudan instance alınabilir.
# 🔹 Ama kendi başına anlamlı değildir, çünkü `visit_*` methodları tanımlı değildir.
# 🔹 Subclass edip `visit_*` methodlarını override etmek neredeyse zorunludur.
#
# Örn:
tree = ast.parse("def foo(): pass")
collector = FuncCollector()
collector.visit(tree)
print(collector.funcs)  # ['foo']

