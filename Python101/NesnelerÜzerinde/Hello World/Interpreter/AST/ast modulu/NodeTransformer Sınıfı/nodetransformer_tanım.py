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


import ast

code = "x = 1 + 2"
tree = ast.parse(code)

import ast


class MyVisitor:
    def visit(self, node):
        """ Dispatcher mekanizması """
        if node is None:
            return
        method_name = "visit_" + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Alt node'ları recursive ziyaret eder """
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
        return None  # dönüş değeri dikkate alınmaz


class MyTransformer(MyVisitor):
    def generic_visit(self, node):
        """ Alt node'ları recursive ziyaret eder ve dönüş değerini uygular """
        for field, old_value in ast.iter_fields(node):
            if isinstance(old_value, list):
                new_values = []
                for item in old_value:
                    if isinstance(item, ast.AST):
                        new_node = self.visit(item)
                        if new_node is None:
                            continue  # child silindi
                        elif isinstance(new_node, list):
                            new_values.extend(new_node)  # child → liste ile değiştirildi
                        else:
                            new_values.append(new_node)  # child → node ile değiştirildi
                    else:
                        new_values.append(item)
                setattr(node, field, new_values)
            elif isinstance(old_value, ast.AST):
                new_node = self.visit(old_value)
                if new_node is None:
                    setattr(node, field, None)  # child silindi
                else:
                    setattr(node, field, new_node)  # child değiştirildi
        return node

    def visit(self, node):
        """ Dispatcher mekanizması (transformer için override) """
        if node is None:
            return None
        method_name = "visit_" + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

# ===============================================================
# 🌀 NodeTransformer.generic_visit — Liste Alanlarının Mantığı
# ===============================================================
#
# AST içindeki bazı alanlar (fields) tekil bir node değil,
# birden fazla node içerebilir. Örnek:
#
#   Module.body → [Assign, Expr, FunctionDef, ...]
#   FunctionDef.body → [Assign, Return, ...]
#
# Bu tür alanlar "liste" olarak tutulur.
# ===============================================================

# ---------------------------------------------------------------
# ✅ Adım 1: Liste alanı tespit edilir
# ---------------------------------------------------------------
# generic_visit, node._fields üzerinde döner.
# Eğer o field bir "liste" ise → özel bir işleme girer.

# ---------------------------------------------------------------
# ✅ Adım 2: new_nodes adında boş bir liste hazırlanır
# ---------------------------------------------------------------
# Bu liste, ziyaret edilen her alt node’un
# "yeni sürümünü" toplayacaktır.

# ---------------------------------------------------------------
# ✅ Adım 3: Listedeki her node için visit() çağrılır
# ---------------------------------------------------------------
#   result = self.visit(child)
#
# 🔹 Eğer result `None` ise:
#   → bu node ağaçtan silinir
#   → continue ile geçilir
#   * bundan dolayı sonuç None ise ifade, Ast ağacından kaldırılır

# 🔹 Eğer result bir "liste" ise:
#   → nested list oluşmasın diye
#     new_nodes.extend(result) yapılır
#
# 🔹 Eğer result tek bir node ise:
#   → new_nodes.append(result) yapılır

# ---------------------------------------------------------------
# ✅ Adım 4: Alan güncellenir
# ---------------------------------------------------------------
# Döngü bittiğinde:
#   setattr(node, field, new_nodes)
#
# Yani orijinal alan (ör. body),
# artık sadece dönüşmüş node’ları içerir.
#
# Eğer bazıları None dönmüşse → onlar listeye eklenmez
# dolayısıyla AST’den "silinmiş" olur.

# ---------------------------------------------------------------
# ✅ Sonuç: Silme, değiştirme, çoğaltma
# ---------------------------------------------------------------
# Bu mekanizma sayesinde:
#   - return None → node listeden atılır
#   - return node → node değiştirilir
#   - return [node1, node2] → node çoğaltılır
#
# 🔍 Böylece NodeTransformer,
# AST’nin listeli alanlarında tam kontrol sağlar.
# ===============================================================

# 🔸 Bu davranış, Python AST sisteminin açıklanabilirliğini ve sürdürülebilirliğini artırır.
