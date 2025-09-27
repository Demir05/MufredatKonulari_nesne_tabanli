# ===============================================================
# 🔧 `ast.NodeTransformer` SINIFI
# ===============================================================

# ✅ 1. Genel Tanım
# ---------------------------------------------------------------
# 🔹 `NodeTransformer`, `NodeVisitor`’dan türeyen bir sınıftır.
# 🔹 Amacı: AST üzerinde gezerken node’ları **değiştirmeye veya silmeye** izin vermek.
# 🔹 Visitor pattern + transformer mantığını birleştirir:
#     - `visit_*` metodunu override edersin.
#     - O metoddan DÖNDÜRDÜĞÜN değer yeni node olarak AST’ye yerleşir.
#     - Eğer None döndürürsen → o node ağaçtan çıkarılır (silinir).
# 🔹 Bu yüzden `NodeVisitor` “read-only” iken, `NodeTransformer` “mutable”dır.


# ✅ 2. Kullanım Alanları
# ---------------------------------------------------------------
# 🔸 Kod Dönüştürme
#     - `+` → `*` operatörlerini çevirme
#     - `print` → `logging.info` yapma
#
# 🔸 Refactoring Araçları
#     - Otomatik değişken ismi değiştirme
#     - Fonksiyon imzası değiştirme
#
# 🔸 Domain-Specific Language (DSL) / Transpiler
#     - Python üstünde başka bir sözdizimi oluşturup,
#       AST’yi dönüştürerek yeni bytecode üretme
#
# 🔍 Özet: AST’yi aktif olarak **yeniden yazmak** için kullanılır.


# ✅ 3. Miras alınabilir mi?
# ---------------------------------------------------------------
# 🔹 Evet, `NodeTransformer` da normal bir sınıftır.
# 🔹 Genellikle subclass edilerek `visit_*` metotları override edilir.
# 🔹 Pratikte `NodeVisitor` gibi direkt kullanılmaz → her zaman özelleştirilir.


# ✅ 4. Örneklenebilir mi?
# ---------------------------------------------------------------
# 🔹 Evet, instance alınabilir.
# 🔹 Ama `visit_*` metodları override edilmediyse anlamsızdır.
#
# Örn: + → * dönüştürücü
import ast

class ReplaceAddWithMult(ast.NodeTransformer):
    def visit_BinOp(self, node):
        self.generic_visit(node)  # önce alt node’ları ziyaret et
        if isinstance(node.op, ast.Add):
            node.op = ast.Mult()  # in-place değişiklik
        return node

tree = ast.parse("x = 1 + 2")
new_tree = ReplaceAddWithMult().visit(tree)
print(ast.unparse(new_tree))  # x = 1 * 2


# ✅ 5. Attribute’ları
# ---------------------------------------------------------------
# 🔹 `NodeTransformer` kendi başına sabit attribute tutmaz.
# 🔹 Subclass’lar genelde kendi state’ini ekler (örn: sayaç, liste).
# 🔹 Esas gücü method dispatch mekanizmasında.


# ✅ 6. Method’ları
# ---------------------------------------------------------------
# 🔸 `visit(node)`
#     - AST traversal’ın giriş noktası.
#     - `node` tipine uygun `visit_Foo` metodunu çağırır.
#     - Dönüş:
#         • Node → ağaçta node o şekilde değiştirilir
#         • None → node silinir
#         • Liste → mevcut node yerine listedeki node’lar eklenir
#
# 🔸 `generic_visit(node)`
#     - Varsayılan traversal davranışı.
#     - Node’un tüm alt alanlarını (children) gezer.
#     - Subclass içinde override edebilirsin, ama çoğu zaman `super().generic_visit()` çağrılır.
#
# 🔍 Önemli: `NodeVisitor`’daki `visit_*` sadece analiz içindi,
#     `NodeTransformer`’daki `visit_*` dönüş değeriyle AST’yi **değiştirir**.


# ✅ 7. Senior-level Notlar
# ---------------------------------------------------------------
# - `NodeTransformer`, AST üzerinde inplace mutasyon yapar → compile() ile tekrar çalıştırabilirsin.
# - Dönüş kuralları:
#     • Aynı node → no-op (değişiklik yok)
#     • Yeni node → AST güncellenir
#     • None → node silinir
#     • Liste → node genişletilir
# - Özellikle transpiler/refactoring araçlarında kritik rol oynar.
# - Ama dikkat: Metadata (`lineno`, `col_offset`) korunmalı; aksi halde hatalı hata mesajları çıkabilir.
#   Bunun için: `ast.copy_location`, `ast.fix_missing_locations` kullanılır.


# ✅ 8. Özet
# ---------------------------------------------------------------
# - `NodeTransformer`: AST üzerinde GEZ + DEĞİŞTİR.
# - `visit_*` metodu dönüş değeri ile ağacı günceller.
# - Kullanım: refactoring, transpiler, kod dönüştürücü.
# - `NodeVisitor` → sadece okuma, `NodeTransformer` → okuma + yazma farkı vardır.
