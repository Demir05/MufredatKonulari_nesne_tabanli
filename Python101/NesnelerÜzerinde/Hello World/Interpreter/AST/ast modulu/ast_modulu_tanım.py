# ===============================================================
# 📘 PYTHON `ast` MODÜLÜ — TANIM
# ===============================================================

# 🔹 `ast` modülü, Python kaynak kodunu “Soyut Sözdizim Ağacı” (Abstract Syntax Tree = AST)
#     biçiminde temsil etmeye yarayan bir standart kütüphane modülüdür.
# 🔹 Kod → Tokenizer → Parser → AST → Bytecode zincirinde,
#     AST katmanını geliştiricilere açan API’dir.
# 🔹 Kullanım alanları:
#     • Kod analizi (lint, type-check, güvenlik kontrolü)
#     • Kod dönüştürme (transpiler, refactoring aracı)
#     • Güvenli değerlendirme (`literal_eval`)
#     • Eğitim / debugging (Python’un nasıl parse ettiğini görmek)
# 🔹 Önemli fonksiyonlar:
#     - ast.parse(src) → AST ağacı döner
#     - ast.dump(node) → AST yapısını yazdırır
#     - ast.unparse(node) → AST’den kaynak kod üretir (3.9+)
#     - ast.walk(node), ast.iter_child_nodes(node) → gezinme araçları
# 🔹 Bu modül, CPython’un parser’ının ürettiği AST nesnelerini Python seviyesinde
#     temsil eder ve bize API üzerinden erişim sağlar.

# ===============================================================
# 🌳 PYTHON AST YAPISI — SOYUT SÖZDİZİMİ AĞACI
# ===============================================================
# 🔹 Python kodu parse edildiğinde, yorumlayıcı onu bir AST ağacına dönüştürür.
# 🔹 Her node, ast.AST sınıfından türemiştir — ama kendi görevine göre alt sınıf olarak tanımlanır.
# 🔹 Aşağıdaki yapı, örnek bir kodun AST hiyerarşisini gösterir:
# Örnek kod: x = obj.value + 2

ast.AST
├── Module                # Programın en üst düzey kapsayıcısı
│   ├── body: [Assign, If]
│   └── type_ignores: []

├── Assign                # x = obj.value + func(3, y) - z.method("test")
│   ├── targets: [Name]   # Atama hedefi
│   └── value: BinOp      # Sağ taraf (BinOp)

├── Name                  # x
│   ├── id: 'x'
│   └── ctx: Store

├── BinOp                 # (obj.value + func(...)) - z.method(...)
│   ├── left: BinOp
│   ├── op: Sub
│   └── right: Call

├── BinOp (left)          # obj.value + func(3, y)
│   ├── left: Attribute
│   ├── op: Add
│   └── right: Call

├── Attribute             # obj.value
│   ├── value: Name(id='obj')
│   ├── attr: 'value'
│   └── ctx: Load

├── Call                  # func(3, y)
│   ├── func: Name(id='func')
│   ├── args: [Constant(3), Name(id='y')]
│   └── keywords: []

├── Call                  # z.method("test")
│   ├── func: Attribute(value=Name(id='z'), attr='method')
│   ├── args: [Constant("test")]
│   └── keywords: []

├── If                    # if x > 10: ...
│   ├── test: Compare
│   ├── body: [For]
│   └── orelse: [While]

├── Compare               # x > 10
│   ├── left: Name(id='x')
│   ├── ops: [Gt]
│   └── comparators: [Constant(10)]

├── For                   # for i in range(5): ...
│   ├── target: Name(id='i')
│   ├── iter: Call(func=Name('range'), args=[Constant(5)])
│   ├── body: [Expr]
│   └── orelse: []

├── Expr                  # print(i)
│   └── value: Call(func=Name('print'), args=[Name('i')])

├── While                 # while x < 20: ...
│   ├── test: Compare
│   └── body: [AugAssign]

├── Compare               # x < 20
│   ├── left: Name(id='x')
│   ├── ops: [Lt]
│   └── comparators: [Constant(20)]

├── AugAssign             # x += 1
│   ├── target: Name(id='x')
│   ├── op: Add
│   └── value: Constant(1)

# Operatör node’ları (sadece tip bilgisi taşır, metadata yok):
├── Add                   # + operatörü
├── Sub                   # - operatörü
├── Gt                    # > operatörü
└── Lt                    # < operatörü





# ===============================================================
# 🧠 PYTHON AST SİSTEMİ — SINIF VE ÖRNEK ADLANDIRMALARI
# ===============================================================

# 🔹 Python'da ast modülü, kaynak kodu soyut sözdizim ağacına (AST) dönüştürür.
# ➤ Bu dönüşümde her yapı bir "AST düğümü" (node) olarak temsil edilir.

# ---------------------------------------------------------------
# ✅ AST BASE CLASS
# ---------------------------------------------------------------
# 🔸 ast.AST → Tüm AST node sınıflarının temel (base) sınıfıdır.
# 🔸 Soyut bir sınıftır; doğrudan örneklenmez.
# 🔸 Tüm node sınıfları bu sınıftan miras alır.
# Örnek:
#   isinstance(ast.Assign(), ast.AST) → True

# ---------------------------------------------------------------
# ✅ AST NODE SINIFLARI (AST Node Classes)
# ---------------------------------------------------------------
# 🔸 Bunlar somut sınıflardır.
# 🔸 Her biri Python'daki bir sözdizimsel yapıyı temsil eder.
# 🔸 Örnek sınıflar:
#   - ast.Module
#   - ast.Assign
#   - ast.FunctionDef
#   - ast.Name
#   - ast.Constant
#   - ast.BinOp
# 🔸 Bunlara genel olarak "AST node sınıfları" denir.

# ---------------------------------------------------------------
# ✅ AST NODE ÖRNEKLERİ (AST Node Instances)
# ---------------------------------------------------------------
# 🔸 AST node sınıflarının çalışma zamanında oluşturulmuş örnekleridir.
# 🔸 Kodun yapısal temsili bu örnekler üzerinden kurulur.
# 🔸 Örnek:
#   node = ast.Assign(...)
#   type(node) → ast.Assign
#   isinstance(node, ast.AST) → True
# 🔸 Bu örneklere "AST düğümleri" veya "AST node örnekleri" denir.


# ---------------------------------------------------------------
# ✅ AST TRAVERSAL VE TÜRSEL KONTROL
# ---------------------------------------------------------------
# 🔸 AST üzerinde gezinmek için isinstance(node, ast.AST) kontrolü yapılır.
# 🔸 Bu sayede tüm node’lar tek bir soyut sınıf üzerinden işlenebilir.
# 🔸 Traversal sistemleri (NodeVisitor, NodeTransformer) bu mimariye dayanır.

# ---------------------------------------------------------------
# ✅ MİRAS DAVRANIŞI
# ---------------------------------------------------------------
# 🔸 ast.Assign, ast.Module gibi sınıflar → ast.AST’ten miras alır.
# 🔸 isinstance(node, ast.AST) → True
# 🔸 issubclass(ast.Assign, ast.AST) → True
# 🔸 Bu yapı, semantic profiler ve introspection zinciri için türsel bütünlük sağlar.

# ---------------------------------------------------------------
# ✅ ÖZET
# ---------------------------------------------------------------
# 🔹 ast.AST → Base class
# 🔹 ast.Assign, ast.Module → AST node sınıfları
# 🔹 node = ast.Assign(...) → AST node örneği
# 🔹 type(node).__name__ → AST node tipi (string)
# 🔹 isinstance(node, ast.AST) → Türsel kontrol

# 🔍 Bu terminoloji, semantic profiler, refactor sistemi ve DSL tasarımı için temel taşlardan biridir.


