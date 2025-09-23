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


# =============================================================================
# 🧩 CodeType Constructor — Python 3.11+ (Yorumlu Referans Bloğu)
# =============================================================================
# Bu yapı, bir Python fonksiyonunun çalışma zamanındaki davranışını tanımlayan
# düşük seviyeli `CodeType` nesnesini üretmek için kullanılır.
# Genellikle `func.__code__` üzerinden erişilir; introspection, debugger,
# profiler, metaprogramlama ve kod manipülasyonu gibi alanlarda kritik rol oynar.
# -----------------------------------------------------------------------------

from types import CodeType


CodeType(
    argcount,               # co_argcount
    # Fonksiyonun konumsel (positional) argüman sayısı.
    # inspect.signature ile eşleşir. Parametrelerin sıralı çözümlemesinde kullanılır.

    posonlyargcount,        # co_posonlyargcount
    # Sadece konumla verilebilen argüman sayısı (PEP 570).
    # `def f(x, /)` gibi tanımlarda kullanılır. `bind()` sırasında hata ayıklamada önemlidir.

    kwonlyargcount,         # co_kwonlyargcount
    # Sadece anahtar sözcükle verilebilen argüman sayısı.
    # `def f(*, x)` gibi tanımlarda kullanılır. Signature binding sırasında ayrıştırılır.

    nlocals,                # co_nlocals
    # Yerel değişken sayısı (parametreler + lokal tanımlar).
    # Bytecode'da `LOAD_FAST`, `STORE_FAST` gibi opcode'larla erişilir.

    stacksize,              # co_stacksize
    # Python sanal makinesinin bu kodu çalıştırırken ihtiyaç duyduğu yığın derinliği.
    # Bytecode optimizasyonu ve `eval_frame` sırasında kritik.

    flags,                  # co_flags
    # Fonksiyon tipi bayrakları (bit mask).
    # Örnek: generator (0x20), coroutine (0x80), async generator (0x100).
    # `inspect.isgeneratorfunction`, `iscoroutinefunction` gibi kontrollerde kullanılır.

    codestring,             # co_code
    # Ham bytecode (bytes tipinde).
    # `dis.dis(code)` ile okunabilir. Opcode dizisi içerir.
    # Kodun gerçek davranışını belirler.

    constants,              # co_consts
    # Sabitler havuzu (None, sayılar, stringler, inner code objeleri vs.).
    # Bytecode'da `LOAD_CONST` ile erişilir. `return 42` → `co_consts = (None, 42)`.

    names,                  # co_names
    # Global namespace’ten erişilen isimler.
    # `LOAD_GLOBAL`, `STORE_NAME`, `IMPORT_NAME` gibi opcode'lar bu tuple'dan string alır.
    # Örnek: `print`, `len`, `math`, `open`,'dosya düzeyinde tanımlı attr'ler' gibi isimler burada tutulur.

    varnames,               # co_varnames
    # Yerel değişken isimleri (parametreler dahil).
    # `LOAD_FAST`, `STORE_FAST` gibi opcode'lar bu tuple'dan isim alır.
    # Closure dışı lokal çözümleme için kullanılır.

    filename,               # co_filename
    # Kaynak dosya adı.
    # Traceback, debugger, profiler çıktılarında görünür. `__file__` ile eşleşebilir.

    name,                   # co_name
    # Fonksiyonun adı (etiket).
    # `repr(func)`, `traceback`, `dis` çıktılarında görünür.
    # `def greet():` → `co_name = "greet"`, lambda için `"<lambda>"`.

    qualname,               # co_qualname
    # Nitelikli ad (sınıf.içindeyse Class.method gibi).
    # `__qualname__` ile eşleşir. Nested fonksiyonlarda tam yol gösterimi sağlar.

    firstlineno,            # co_firstlineno
    # Fonksiyonun kaynakta başladığı satır numarası.
    # Traceback ve `dis` çıktılarında satır eşlemesi için kullanılır.

    linetable,              # co_linetable
    # Satır eşleme tablosu (bytes).
    # Python 3.11 ile `co_lnotab` yerine geldi. Bytecode → kaynak satır eşlemesi sağlar.

    exceptiontable,         # co_exceptiontable
    # İstisna yakalama tablosu.
    # `try/except/finally` bloklarının bytecode'daki konumlarını ve handler'larını tanımlar.

    freevars,               # co_freevars
    # Closure’dan gelen serbest değişken isimleri.
    # `LOAD_DEREF` ile erişilir. `outer → inner` geçişte kullanılır.
    # `def outer(): x=1; def inner(): return x` → `inner.co_freevars = ('x',)`

    cellvars                # co_cellvars
    # Closure’a dışarıdan aktarılan hücre değişkenleri.
    # `outer` fonksiyonda tanımlanıp `inner` tarafından kullanılan değişkenler.
    # `co_cellvars` + `co_freevars` birlikte closure bağlamını tanımlar.
)

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

# 🧩 CodeType.replace() Metodu
# =============================================================================
# CodeType nesneleri IMMUTABLE’dır (değiştirilemez). Yani bir kere üretildiğinde
# içindeki co_code, co_consts, co_names vs. alanlarını doğrudan değiştiremezsin.
#
# • __init__ kullanılmaz çünkü CodeType bir "built-in type" (C seviyesinde).
# • Oluşturulurken __new__ üzerinden tahsis edilir (immutable yapılar hep böyledir).
#
# Tam da bu yüzden .replace() metodu vardır:
# -----------------------------------------------------------------------------
# 📌 Amaç:
#   - Mevcut bir CodeType nesnesinden yola çıkarak,
#   - bazı alanları değiştirmek,
#   - ama geri kalanını aynı tutmak,
#   - ve sonuçta YENİ bir CodeType nesnesi döndürmek.
#
# 📌 İmza (3.11+ için özet):
#   CodeType.replace(
#       self,
#       *,
#       co_argcount: int | None = None,
#       co_posonlyargcount: int | None = None,
#       co_kwonlyargcount: int | None = None,
#       co_nlocals: int | None = None,
#       co_stacksize: int | None = None,
#       co_flags: int | None = None,
#       co_code: bytes | None = None,
#       co_consts: tuple | None = None,
#       co_names: tuple[str, ...] | None = None,
#       co_varnames: tuple[str, ...] | None = None,
#       co_filename: str | None = None,
#       co_name: str | None = None,
#       co_qualname: str | None = None,
#       co_firstlineno: int | None = None,
#       co_linetable: bytes | None = None,
#       co_exceptiontable: bytes | None = None,
#       co_freevars: tuple[str, ...] | None = None,
#       co_cellvars: tuple[str, ...] | None = None,
#   ) -> CodeType
#
# 📌 Çalışma Mantığı:
#   - Eğer bir argüman verirsen, o alan yeni CodeType nesnesinde güncellenir.
#   - Vermediğin argümanlar → eski nesnedeki değerleriyle kalır.
#   - Yani "copy with modification" yaklaşımıdır. (dataclass.replace gibi düşünebilirsin.)
#
# 📌 Avantajı:
#   - Uzun ve sürüm bağımlı types.CodeType(...) ctor’una dokunmadan
#     güvenle sadece ihtiyacın olan alanı değiştirebilirsin.
#
# -----------------------------------------------------------------------------
# 🧪 Örnek:
# def foo(x): return x+1
# orig = foo.__code__
#
# # Sadece co_name’i değiştiriyoruz
# new_code = orig.replace(co_name="bar")
#
# # Yeni bir fonksiyona sarabiliriz
# import types
# bar = types.FunctionType(new_code, globals())
# print(bar(5))  # 6
#
# -----------------------------------------------------------------------------
# 🎯 Özet:
# • CodeType immutable → __init__ kullanılmaz, __new__ ile tahsis edilir.
# • replace() → "eski nesne + verilen değişiklikler = yeni CodeType nesnesi"
# • Böylece güvenli, sürüm-dostu, hatasız özelleştirme yapılabilir.
