# ===============================================================
# 🌳 PYTHON `ast.AST` SINIFI — DERLENMİŞ REHBER
# ===============================================================

# ✅ 1. Genel Tanım
# ---------------------------------------------------------------
# 🔹 `ast.AST`, Python’daki tüm AST node’larının taban (base) sınıfıdır.
# 🔹 Her node tipi (Assign, BinOp, FunctionDef, If, vb.) buradan türetilmiştir.
# 🔹 Python kaynak kodunun soyut yapısının “ortak atasıdır”.
# 🔹 Normal bir Python sınıfıdır → instance alınabilir, miras alınabilir.

import ast
node = ast.AST()
print(isinstance(node, ast.AST))  # True

# Ama tek başına anlamlı değildir:
# - `_fields` tanımlı değil
# - compile() bunu işleyemez
# - Yani “boş iskelet” gibidir


# ✅ 2. Metadata Alanları (Node’ların Konum Bilgileri)
# ---------------------------------------------------------------
# - lineno           → node’un başladığı satır numarası
# - col_offset       → satır içindeki sütun (karakter) offset’i
# - end_lineno       → node’un bittiği satır (3.8+)
# - end_col_offset   → node’un satırda bittiği sütun (3.8+)
# - type_ignores     → sadece Module node’larında, `# type: ignore` satırlarını saklar
# - ctx              → değişkenin bağlamı (Load, Store, Del)
# - decorator_list   → FunctionDef / ClassDef için decorator’lar
# - name, args, body → bazı node’lara özgü ek alanlar
#
# 🔍 Metadata, kodun AST üzerinde “nereden geldiğini” tutar.
#     → hata raporları, IDE işaretlemeleri, transpiler çıktıları bu sayede doğru olur.


# ✅ 3. Mirasa İzin Verir mi?
# ---------------------------------------------------------------
# 🔹 Evet, ast.AST’den miras alabilirsin.
# 🔹 Ama CPython compiler sadece kendi node setini bilir → custom node’ları yürütmez.
# 🔹 Yani compile() → TypeError verir.
# 🔹 Buna rağmen:
#     - Analiz araçlarında (lint, güvenlik tarayıcı) ek bilgi taşıyabilirsin
#     - Transpilerlerde “ara node” olarak kullanabilirsin
#     - Framework / DSL yazarken faydalıdır

class MyNode(ast.AST):
    _fields = ("value", "extra")

n = MyNode()
n.value, n.extra = 42, "custom"
print(isinstance(n, ast.AST))  # True


# ✅ 4. Pratik Örnek: Kara Liste Node’u
# ---------------------------------------------------------------
# 🔹 os.system çağrılarını özel bir `DangerousCall` node’una dönüştürme
class DangerousCall(ast.AST):
    _fields = ("func_name", "lineno")

class BlacklistTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        if (isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr == "system"):
            return DangerousCall(func_name="os.system", lineno=node.lineno)
        return self.generic_visit(node)

code = "import os; os.system('rm -rf /')"
tree = ast.parse(code)
new_tree = BlacklistTransformer().visit(tree)

for n in ast.walk(new_tree):
    if isinstance(n, DangerousCall):
        print(f"🚨 Kara liste: {n.func_name} @ line {n.lineno}")


# ✅ 5. Senior-level Notlar
# ---------------------------------------------------------------
# - ast.AST: herkesin üst sınıfı ama kendi başına boş bir kabuk
# - Metadata mutable’dır → değiştirirsen compile() çıktısı da değişir
# - end_lineno / end_col_offset 3.8 ile geldi → artık daha hassas konum bilgisi var
# - Miras almak dilin kendisine katkı yapmaz → sadece analiz/dönüştürme araçlarına esneklik sağlar
# - “Extended AST” oluşturmak mümkündür ama CPython derleyicisi bunu bilmez

# ===============================================================
# ✅ ÖZET
# ===============================================================
# - `ast.AST`: tüm node’ların base class’ı
# - Instance alınabilir ama anlamsızdır
# - Metadata: lineno, col_offset, end_lineno, end_col_offset, ctx vb.
# - Miras alınabilir → custom node yaratabilirsin
# - Compiler bunları çalıştırmaz → analiz ve araçlar için kullanılır
# - Güçlü kullanım alanı: DSL, transpiler, static analysis, security tools
