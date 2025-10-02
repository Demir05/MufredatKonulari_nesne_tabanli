# === [co_flags Bayrakları: CodeType Davranışları] ===
#
# Tanım:
# Python'da her derlenmiş fonksiyonun `__code__.co_flags` alanı, çalışma zamanındaki
# davranışlarını bit düzeyinde tanımlar. Her bayrak, fonksiyonun nasıl çalıştığını etkiler.
# Aşağıda en yaygın bayraklar sade ve semantik yorumlarla listelenmiştir.

# === [OPTIMIZED Bayrağı: Fast Locals Davranışı] ===
#
# Tanım:
# Python yorumlayıcısında bir CodeType nesnesi, `co_flags & 0x01` bayrağı aktifse
# "OPTIMIZED" modda çalışır. Bu, fonksiyonun yerel değişkenlere erişim için
# `frame.f_locals` yerine `fastlocals` adlı sabit boyutlu bir dizi kullandığı anlamına gelir.
#
# Amaç:
# - Yerel değişkenlere isimle arama (dict lookup) yerine indeksle erişim sağlamak
# - `LOAD_FAST`, `STORE_FAST` gibi hızlı opcode'larla performansı artırmak
# - `locals()` çağrısını snapshot haline getirmek (gerçek zamanlı değil)
#
# Etkiler:
# - `locals()['x'] = 42` gibi işlemler değişkeni etkilemez; sadece snapshot değişir
# - `locals()` çıktısı, `PyFrame_FastToLocals()` ile üretilir; değiştirilemez
# - `frame.f_locals` gerçek zamanlı değildir; `fastlocals` dizisiyle senkronize edilmez
#
# Ne zaman aktif değildir?
# - `exec`, `eval` gibi dinamik bağlamlarda derlenen kodlar
# - `class` gövdesi içindeki yürütülebilir bloklar
# - Elle oluşturulmuş `types.FunctionType` fonksiyonları (derleyici bağlam eksikse)
# - REPL ortamında bazı geçici tanımlar
#
# Semantik profiler için öneri:
# - `co_flags & 0x01 == False` ise `"UNOPTIMIZED"` etiketi eklenmeli
# - `locals()` çağrısı varsa ve `OPTIMIZED` yoksa → `"mutable_locals"` etiketiyle işaretlenmeli
# - `LOAD_NAME`, `STORE_NAME` opcode’ları varsa → optimize edilmemiş erişim semantiği tanımlanmalı
#
# Mimari not:
# Bu bayrak, introspection zincirinde `CodeType` davranışlarını semantik olarak sınıflandırmak için
# kritik bir parametredir. `OPTIMIZED` mod, kodun deterministik ve performans odaklı çalıştığını gösterir.

# Fonksiyon tanımı
code1 = compile("def f(): pass", "<string>", "exec")
func = eval(code1.co_consts[0])
print(func.__code__.co_flags)  # ✅ OPTIMIZED açık olabilir çünkü fonksiyon tanımı var

# Sınıf tanımı
code2 = compile("class A: pass", "<string>", "exec")
print(code2.co_flags)  # ❌ OPTIMIZED yok

# Modül kodu
code3 = compile("x = 1", "<string>", "exec")
print(code3.co_flags)  # ❌ Genellikle sadece NEWLOCALS (2)


# === [CO_NEWLOCALS: Yerel İsim Alanı Oluşturma] ===
#
# Tanım:
# Fonksiyon, kendi yerel isim alanını (`locals`) oluşturur. Bu, fonksiyonun çalıştığı frame içinde
# global isimlerle karışmadan, izole bir yerel sözlükle çalışmasını sağlar.
#
# Etki:
# - `locals()` çağrısı, sadece fonksiyon içindeki isimleri içerir.
# - Genellikle `def` ile tanımlanan fonksiyonlarda varsayılan olarak aktiftir.
# - `exec` gibi global bağlamda çalışan kodlarda bu bayrak devre dışı olabilir.
#
# Semantic profiler için:
# - `"isolated_namespace"` etiketiyle işaretlenebilir.
# - `frame.f_locals` içeriği sadece yerel isimleri içerdiğinde bu bayrak aktiftir.


# === [CO_VARARGS: Konumsal Argüman Toplayıcı (*args)] ===
#
# Tanım:
# Fonksiyon, tanımında `*args` içeriyorsa bu bayrak aktif olur. Konumsal olarak verilen fazla argümanlar
# bir liste halinde toplanır ve fonksiyon içinde `args` olarak erişilir.
#
# Etki:
# - `co_varnames` içinde `args` adlı bir parametre yer alır.
# - Bytecode'da `BUILD_LIST`, `UNPACK_SEQUENCE` gibi opcode'larla birlikte çalışabilir.
#
# Semantic profiler için:
# - `"variadic_positional"` etiketiyle işaretlenebilir.
# - Fonksiyonun çağrı esnekliği analiz edilirken bu bayrak dikkate alınmalıdır.

# === [CO_VARKEYWORDS: Anahtar Argüman Toplayıcı (**kwargs)] ===
#
# Tanım:
# Fonksiyon, tanımında `**kwargs` içeriyorsa bu bayrak aktif olur. Anahtar-değer şeklinde verilen fazla
# argümanlar bir sözlük halinde toplanır ve fonksiyon içinde `kwargs` olarak erişilir.
#
# Etki:
# - `co_varnames` içinde `kwargs` adlı bir parametre yer alır.
# - Bytecode'da `BUILD_MAP`, `CALL_FUNCTION_KW` gibi opcode'larla birlikte çalışabilir.
#
# Semantic profiler için:
# - `"variadic_keyword"` etiketiyle işaretlenebilir.
# - Fonksiyonun DSL uyumluluğu ve argüman esnekliği analizinde kritik rol oynar.

# === [CO_NESTED: İç Fonksiyon Davranışı] ===
#
# Tanım:
# Fonksiyon, başka bir fonksiyonun içinde tanımlanmışsa (nested function), bu bayrak aktif olur.
# Bu durumda closure bağlamı oluşabilir ve dış fonksiyonun değişkenlerine erişim sağlanabilir.
#
# Etki:
# - `co_freevars` dolu olabilir → dış bağlamdan gelen değişkenler.
# - `LOAD_DEREF`, `STORE_DEREF` gibi closure opcode'ları kullanılabilir.
#
# Semantic profiler için:
# - `"nested_scope"` etiketiyle işaretlenebilir.
# - Closure analizi ve bağlam çözümlemesi için bu bayrak kritik önemdedir.


# === [CO_NOFREE: Closure Bağlamı Yok] ===
#
# Tanım:
# Fonksiyonun closure bağlamı yoksa (yani dış değişkenlere referans içermiyorsa), bu bayrak aktif olur.
# `co_freevars` ve `co_cellvars` boş olur.
#
# Etki:
# - `LOAD_DEREF`, `STORE_DEREF` gibi closure opcode'ları kullanılmaz.
# - Fonksiyon tamamen kendi yerel isim alanında çalışır.
#
# Semantic profiler için:
# - `"no_closure"` etiketiyle işaretlenebilir.
# - Bağlam izolasyonu ve deterministik davranış analizinde bu bayrak önemlidir.

# === [CO_COROUTINE: Async Fonksiyon Davranışı] ===
#
# Tanım:
# Fonksiyon `async def` ile tanımlanmışsa bu bayrak aktif olur. Fonksiyon bir coroutine’dir ve
# `await` ile çalıştırılır.
#
# Etki:
# - `co_flags` içinde `CO_GENERATOR` olmadan `CO_COROUTINE` varsa → saf coroutine.
# - `GET_AWAITABLE`, `AWAIT` gibi async opcode'lar içerir.
#
# Semantic profiler için:
# - `"coroutine"` etiketiyle işaretlenebilir.
# - Zamanlayıcı uyumluluğu ve concurrency analizlerinde bu bayrak kritik rol oynar.

# === [CO_ASYNC_GENERATOR: Async + Yield Davranışı] ===
#
# Tanım:
# Fonksiyon hem `async` hem `yield` içeriyorsa bu bayrak aktif olur. Fonksiyon bir async generator’dır
# ve `async for` ile döngü içinde kullanılabilir.
#
# Etki:
# - Hem coroutine hem generator davranışı gösterir.
# - `YIELD_VALUE`, `AWAIT`, `GET_AWAITABLE` gibi opcode'lar birlikte bulunabilir.
#
# Semantic profiler için:
# - `"async_generator"` etiketiyle işaretlenebilir.
# - Akış kontrolü, concurrency ve bellek yönetimi analizlerinde bu bayrak özel olarak ele alınmalıdır.


# === [co_flags Bayrak Tablosu: Bit Mask Çözümleme] ===
#
# Tanım:
# `co_flags` alanı, Python'da derlenmiş bir `CodeType` nesnesinin çalışma zamanı davranışlarını
# bit mask olarak tanımlar. Her bayrak, belirli bir bit konumuna karşılık gelir.
# Aşağıdaki tablo, bayrakların sayısal değerlerini ve semantik anlamlarını gösterir.

# ┌──────────────┬────────────┬────────────────────────────────────────────┐
# │ Bayrak Adı   │ Değer (int)│ Açıklama                                   │
# ├──────────────┼────────────┼────────────────────────────────────────────┤
# │ CO_OPTIMIZED │     1      │ Yerel değişkenler fastlocals dizisinde     │
# │ CO_NEWLOCALS │     2      │ Fonksiyon kendi yerel isim alanını kurar   │
# │ CO_VARARGS   │     4      │ `*args` kullanımı                          │
# │ CO_VARKEYWORDS│    8      │ `**kwargs` kullanımı                       │
# │ CO_NESTED    │    16      │ Fonksiyon başka bir fonksiyon içinde       │
# │ CO_GENERATOR │    32      │ `yield` içerir → generator                 │
# │ CO_NOFREE    │    64      │ Closure bağlamı yok                        │
# │ CO_COROUTINE │   128      │ `async def` → coroutine                    │
# │ CO_ASYNC_GENERATOR│256    │ `async` + `yield` → async generator        │
# └──────────────┴────────────┴────────────────────────────────────────────┘

# Örnek: co_flags = 3
# → Binary: 0b00000011
# → Aktif bayraklar:
#    - CO_OPTIMIZED (1)
#    - CO_NEWLOCALS (2)
# → Semantik: Fonksiyon optimize edilmiş ve kendi yerel isim alanını kuruyor

# Örnek: co_flags = 67
# → 1 + 2 + 64 → OPTIMIZED + NEWLOCALS + NOFREE
# → Fonksiyon optimize edilmiş, izole çalışıyor ve closure kullanmıyor

# Not:
# Bayraklar bitwise OR ile birleşir → flags & bayrak_değeri ile kontrol edilir
# Semantic profiler içinde bu bayraklar `"execution_mode"` veya `"function_traits"` olarak etiketlenebilir
