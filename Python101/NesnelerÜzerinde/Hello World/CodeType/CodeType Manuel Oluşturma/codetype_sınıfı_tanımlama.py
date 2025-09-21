# 🧩 CodeType Manuel Üretimi
# ------------------------------------------------------------
# • types.CodeType(...) constructor'ı kullanılarak doğrudan CodeType nesnesi üretilebilir.
# • Ama bu pratik değildir çünkü çok fazla parametre ister (co_argcount, co_nlocals, co_code,
#   co_consts, co_names, co_varnames, co_filename, co_flags, vb.).
# • Bunları doğru doldurmak zordur ve hata yapmaya çok açıktır.
# • Yani "manuel üretim mümkündür ama zahmetlidir." ⚠️

# ------------------------------------------------------------
# 🛠️ Pratik Yol: compile()
# • Python’un compile() fonksiyonu string kodu derleyip CodeType nesnesine dönüştürür.
# • Örn: compile("x+1", "<string>", "eval") → bir CodeType nesnesi döner.
# • Böylece constructor parametrelerini tek tek doldurmaya gerek kalmaz.
# • compile() güvenli, kolay ve pratik bir yoldur. ✅

# ------------------------------------------------------------
# 📌 CodeType Örneği Ne Temsil Eder?
# • CodeType örneği = belirli bir Python kod parçasının DERLENMİŞ HALİ 📦
# • İçinde:
#   - Bytecode (co_code → ham opcode’lar)
#   - Sabitler (co_consts)
#   - Yerel değişkenler (co_varnames)
#   - Global isimler (co_names)
#   - Dosya ve satır bilgisi (co_filename, co_firstlineno)
# • Interpreter bu nesneyi alır ve içindeki co_code’u çalıştırır.
# • Biz de __code__ attribute’u sayesinde fonksiyonların CodeType’ına erişebiliriz.

# ------------------------------------------------------------
# ❓ Peki Neden Her Şeyde __code__ Yok?
# • Çünkü __code__ sadece yürütülebilir kod bloklarına atanır.
# • Örn:
#     def f(): return 1
#     f.__code__  # ✅ CodeType örneği
# • Ama "x = 2" gibi basit ifadeler ayrı bir code object üretmez,
#   bunlar modülün genel CodeType’ının parçasıdır.
#
# • ayrıca modül,çalıştırılmaz sadece bir namespace görevi görür bu nedenle modul nesnesinde;
# __code__ attribute'U bulunmaz
#
# ------------------------------------------------------------
# 🧪 Örnek: Module-level CodeType
# • compile() kullanarak modül seviyesindeki CodeType’ı görebiliriz:
#     code_obj = compile("x = 2", "<string>", "exec")
#     print(code_obj)        # <code object <module> ...>
#     print(code_obj.co_code)  # ham opcode
# • Bu gösteriyor ki en basit ifade bile aslında derlenmiş bir code object içinde saklanıyor.
# • Ama __code__ attribute'u sadece fonksiyon/lambda/class gibi ayrı scope yaratan nesnelere atanıyor.

# ------------------------------------------------------------
# 🎯 Özet
# • Manuel üretim → types.CodeType(...) ile mümkün ama çok karmaşık.
# • Pratik üretim → compile() ile kolayca yapılabilir.
# • CodeType örneği → derlenmiş kodun tüm bytecode ve metadata’sını temsil eder.
# • Fonksiyonlar → __code__ attribute ile kendi CodeType’ına erişebilir.
# • Basit ifadeler (x=2) → aslında module-level CodeType içindedir, ama kullanıcıya __code__ verilmez.
# • Python’un esnekliği: derlenmiş kod bile bir nesne (CodeType) olarak saklanır ve incelenebilir. 🔍


# 🧩 CodeType.__init__ — Python 3.11+ imzası (özet)
# -------------------------------------------------
# types.CodeType(
#     argcount: int,                # konumsel argüman sayısı
#     posonlyargcount: int,         # yalnız pos-arg sayısı (PEP 570)
#     kwonlyargcount: int,          # yalnız anahtar-sözcük arg sayısı
#     nlocals: int,                 # yerel değişken sayısı (co_nlocals)
#     stacksize: int,               # sanal makine yığın derinliği
#     flags: int,                   # co_flags (generator/coroutine/async vb. bit mask)
#     codestring: bytes,            # co_code → HAM BYTECODE (opcode baytları)
#     constants: tuple,             # co_consts → sabitler (None, sayılar, stringler, inner code objeleri…)
#     names: tuple[str, ...],       # co_names → global/attr isimleri havuzu
#     varnames: tuple[str, ...],    # co_varnames → yerel değişken adları
#     filename: str,                # co_filename → kaynak dosya adı
#     name: str,                    # co_name     → bu code objesinin adı
#     qualname: str,                # co_qualname → nitelikli ad (sınıf.içindeyse vs.)
#     firstlineno: int,             # co_firstlineno → kaynakta ilk satır
#     linetable: bytes,             # co_linetable → satır eşleme tablosu (3.11+)
#     exceptiontable: bytes,        # co_exceptiontable → istisna tablosu (3.11+)
#     freevars: tuple[str, ...],    # co_freevars → closure serbest değişken adları
#     cellvars: tuple[str, ...],    # co_cellvars → closure hücre değişken adları
# )
#
# 📝 Sürüm notu:
# • 3.10 ve öncesinde "linetable" yerine "lnotab" vardı ve "exceptiontable" yoktu.
# • 3.11+ (PEP 659 ve istisna tablosu) ile imza değişti. Bu nedenle ctor’u doğrudan
#   kullanmak sürüme sıkı bağımlılık yaratır.
#
# 🎯 Önemli çıkarım:
# • Elle CodeType üretmek "mümkün", ama "hata riski yüksek": codestring/linetable/exceptiontable
#   doğru üretilmeli. Bu yüzden pratikte iki sağlıklı yol var:
#   (A) code.replace(...)  (B) compile(...)
