# ------------------------------------------------------------------------------
# ast.parse Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# ast.parse, Python kaynak kodunu (bir string olarak) alır ve onu soyut sözdizim
# ağacı (AST - Abstract Syntax Tree) yapısına dönüştürür.
#
# Kod analiz, transformasyon veya otomatik işlem yapılabilmesi için Python
# kodunun ağaç yapısında temsil edilmesi gerekir. Bu yapı, parse fonksiyonu ile elde edilir.
#
# Önemli: filename parametresi, AST içinde doğrudan kullanılmaz. Daha çok
# compile() aşamasında traceback'lerde görünecek olan dosya adını taşır.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.parse(
#     source: str,
#     filename: str = "<unknown>",
#     mode: str = "exec",
#     *,
#     type_comments: bool = False,
#     feature_version: int | tuple[int,int] | None = None
# ) -> ast.AST
#
# PARAMETRELER:
# - source (str):
#     AST’ye dönüştürülecek Python kodu
#
# - filename (str, default="<unknown>"):
#     Hata mesajlarında ve compile işleminde kullanılacak dosya ismi
#     Not: AST içinde aktif rolü yoktur
#
# - mode (str):
#     - "exec"  → birden fazla satırdan oluşan kod (modül)
#     - "eval"  → tek bir ifade (expression)
#     - "single" → interaktif prompt (REPL) gibi durumlar
#
# - type_comments (bool):
#     PEP 484 uyumlu tip yorumları (type comments) da AST’ye dahil edilsin mi?
#
# - feature_version (int, tuple veya None):
#     Hangi Python sürümünün sözdizimi kullanılacak? (örn: (3, 10))
#
# DÖNÜŞ:
# - Bir AST ağacı döner. Genellikle kök node ‘Module’ tipindedir.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ Kod analiz ve statik kontrol (linters, code quality araçları)
# ✅ AST transformasyonu (kod refactor, injection)
# ✅ Kod jenerasyonu ve compile ile çalıştırma
# ✅ IDE’lerde kod tamamlama / analiz sistemleri
# ✅ Eğitim, test, analiz, coverage araçları için kodu parçalamak
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# - filename sadece compile() işleminde traceback'te görünür;
#   parse edilen AST node'ları içinde tutulmaz
#
# - Eğer compile(tree, filename="...") denirse, traceback bu filename’i kullanır
#
# - AST node'ları lineno ve col_offset gibi konum bilgilerini içerir.
#
# - Elle oluşturulan AST node’ları bu bilgilere sahip değildir;
#   o yüzden fix_missing_locations kullanılması gerekir
#
# - mode seçimi çok önemlidir:
#     - exec: modül düzey kodlar için
#     - eval: tek bir ifade için
#     - single: REPL tarzı satırlar için
#
# - type_comments=True derseniz, PEP 484 type hints yorumları da AST’ye dahil edilir
#
# - parse() fonksiyonun Cpython'da tanımlıdır(parser modulu,PEG,AST işlemlerini kapsar) ast modülü de performans açısından;
#   dolayı doğrudan özel opcode'ları kullanarak cpython üzerinde işlem yapar bu durumda parse aşamasında koddaki biçim(parantez vb) unsurlar
#   cpython'un Grammer/ dizini altındaki yapılardaki işaretlerin tanım sırasına göre belirlenir( en yukardaki en düşük)
#   çalışma mantığı: yüksek önceliğe sahip olan sembollerde kullanılan parantezler gereksiz,
#   düşük seviye sembollerde kullanılan parantez,şemantik bağlamın korunması adına kalıcı olarak işaretlenir

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

import ast

# -------------------------------------------------------------------
# 📘 Örnek 1 - Basit parse işlemi
# -------------------------------------------------------------------
code = "a = 10\nprint(a)"
tree = ast.parse(code)

print(ast.dump(tree, indent=2, include_attributes=True))
# Bu AST, Module tipindedir. body içinde Assign ve Expr node'ları vardır.

# -------------------------------------------------------------------
# 📘 Örnek 2 - mode="eval" ile tek ifade parse etme
# -------------------------------------------------------------------
expr_tree = ast.parse("1 + 2 * 3", mode="eval")
print(ast.dump(expr_tree, indent=2, include_attributes=True))
# Root node 'Expression' tipindedir, body ise BinOp’tur

# -------------------------------------------------------------------
# 📘 Örnek 3 - filename etkisi (compile aşamasında)
# -------------------------------------------------------------------
tree = ast.parse("raise ValueError('oops')", filename="my_script.py")

# AST içinde filename bilgisi yok, ama compile'da kullanılır
code_obj = compile(tree, filename="my_script.py", mode="exec")

try:
    exec(code_obj)
except Exception:
    import traceback
    traceback.print_exc()
    # Çıktı:
    # Traceback (most recent call last):
    #   File "my_script.py", line 1, in <module>
    #   ValueError: oops

# -------------------------------------------------------------------
# Özet:
# - parse() → kodu AST yapısına çevirir
# - filename → compile zamanı etkilidir
# - AST dönüştürmek için ilk adımdır
# -------------------------------------------------------------------
