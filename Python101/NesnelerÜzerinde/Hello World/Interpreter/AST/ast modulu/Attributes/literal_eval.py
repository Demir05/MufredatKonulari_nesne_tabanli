import ast

# ------------------------------------------------------------------------------
# ast.literal_eval Fonksiyonunun Tam Tanımı ve Kullanım Mantığı
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 1) TANIM
# ------------------------------------------------------------------------------
# `ast.literal_eval(node_or_string)` fonksiyonu, verilen bir AST ifade düğümünü
# (örneğin ast.Constant, ast.Tuple, ast.List, ast.Dict vs.) ya da literal yapıyı
# tanımlayan bir string’i değerlendirir ve karşılık gelen Python nesnesini döner.
#
# Önemli: Bu fonksiyon sadece **literal veya container literal yapılarını** işler:
# - string, bytes, sayılar (int, float, complex), boolean değerler, None, Ellipsis
# - tuple, list, dict, set (yani veri koleksiyonları)
#
# Bu fonksiyon, `eval()` gibi genel Python ifadelerini çalıştırmaz; yani operatörler,
# fonksiyon çağrıları, değişken isimleri, indexing gibi yapıları kabul etmez.
# Bu yönüyle görece “güvenli” kabul edilir.
# (Python belgelerinde literal_eval, “Saf biçimde literal yapıların değerlendirilmesi” olarak geçer) :contentReference[oaicite:0]{index=0}
#
# Ancak unutma: “güvenli” demek tamamen risksiz demek değildir; çok derin veya büyük literaller
# girildiğinde bellek ya da yığın (stack) sınırlarına takılabilirsin. :contentReference[oaicite:1]{index=1}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 2) SÖZDİZİMİ
# ------------------------------------------------------------------------------
# ast.literal_eval(node_or_string) -> object
#
# PARAMETRELER:
# - node_or_string: ast.AST veya str
#     Eğer `str` ise, bu string literal yapıyı temsil eden bir Python kodu olmalıdır,
#     örneğin `"[1, 2, {'a': 3}]"`.
#     Eğer `AST` ise, literal yapıyı temsil eden AST düğümüdür (örneğin ast.Constant, ast.Tuple, vs.)
#
# DÖNÜŞ:
# - Literal değerlere dönüştürülmüş Python objesi (örneğin list, dict, int, vs.)
# - Eğer yapı geçerli literal değilse, ValueError, TypeError, SyntaxError gibi hata fırlatabilir :contentReference[oaicite:2]{index=2}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 3) KULLANIM ALANLARI
# ------------------------------------------------------------------------------
# ✅ Dışarıdan gelen string formatta literal veri (örn. yapılandırma, JSON benzeri ama Python literal) okumak
# ✅ Güvenli veri değerlendirme (kötü niyetli kod çalıştırmaktan kaçınmak)
# ✅ AST bazlı kod araçlarında, literal AST düğümlerinden gerçek Python değerini elde etmek
# ✅ Konfigürasyon verilerini Python literal notasyonla saklayıp yüklemek
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 4) EKSTRA / DİKKAT EDİLMESİ GEREKENLER
# ------------------------------------------------------------------------------
# ❓ Neden bunu özel bir fonksiyon olarak koydular? Neden `eval()` ya da `walk` ile çözemediler?
#
# - `eval()` çok genel bir çözüm: tüm Python ifadelerini çalıştırabilir, bu da güvenlik riski yaratır.
#   `literal_eval` yalnızca belirli, güvenli literal yapılarını değerlendirmeye izin verir — bu yüzden ayrıdır. :contentReference[oaicite:3]{index=3}
#
# - `walk` bir dolaşma aracıdır, yani AST üzerinde gezinmek içindir; değer “değerlendirme” yapmaz.
#   `walk` ile tüm literal AST node’larını bulabilirsin, ama onları Python objesine dönüştürmez.
#
# - `literal_eval`, AST ya da string içindeki literal yapıyı **doğrudan dönüştürür**, kod yürütmez; bu yüzden hem amaca yönelik hem daha güvenlidir.
#
# - `literal_eval` girdiyi AST’ye parse eder (eğer string verildiyse) ve sonra _sadece_ literal yapıları mümkünse dönüştürür; aksi halde hata verir.
#
# - Python belgeleri uyarır: `literal_eval` “safe” olarak dokümante edilmiştir, ama tamamen risksiz değildir — özellikle derin girdilerle bellek ya da yığın sınırları zorlanabilir. :contentReference[oaicite:4]{index=4}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# 5) ÖRNEKLER
# ------------------------------------------------------------------------------

# Örnek 1: String literal ifadeyi değerlendir
s = "[1, 2, {'a': 5, 'b': [3, 4]}]"
obj = ast.literal_eval(s)
print(obj, type(obj))
# çıktı: [1, 2, {'a': 5, 'b': [3, 4]}] <class 'list'>

# Örnek 2: AST düğümünden literal değer almak
node = ast.parse("({'x': 10, 'y': 20})", mode="eval").body
# burada node bir ast.Tuple veya ast.Dict / ast.Constant vs olabilir
val = ast.literal_eval(node)
print(val, type(val))
# çıktı: {'x': 10, 'y': 20} <class 'dict'>

# Örnek 3: Hatalı ifade → hata fırlatır
try:
    ast.literal_eval("1 + 2")  # bu bir işlem dir, literal değil
except Exception as e:
    print("Hata:", type(e), e)

# Örnek 4: Güvenlik avantajı (eval ile karşılaştırma)
mal = "__import__('os').system('rm -rf /')"
try:
    ast.literal_eval(mal)
except Exception as e:
    print("literal_eval engelledi:", type(e), e)

# eval(mal) yaparsan kod çalışır (riskli) — bu yüzden literal_eval tercih edilir :contentReference[oaicite:5]{index=5}

# --------------------------------------------------------------------------
# Bu yorumlu kod parçası, ast.literal_eval’in amacını, sınırlarını, avantajlarını
# ve kullanım senaryolarını net bir şekilde anlatır.
# --------------------------------------------------------------------------
