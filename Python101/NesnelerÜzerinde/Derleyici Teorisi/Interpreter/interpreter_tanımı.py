# ┌────────────────────────────────────────────────────────────────────────────┐
# │ CPython Yorumlayıcısının Mimari Yapısı                                     │
# └────────────────────────────────────────────────────────────────────────────┘

# Python yorumlayıcısı dediğimiz şey, CPython’da birden fazla bileşenden oluşur.
# Bunlar sadece kodu çalıştırmakla kalmaz, aynı zamanda dilin tanımını, çalışma
# zamanını ve yürütme motorunu kapsar.

# ─────────────────────────────────────────────────────────────────────────────
# 1. Dil Tanımı (Grammar)
# ─────────────────────────────────────────────────────────────────────────────

# CPython, Python dilinin referans implementasyonudur. Yani dilin sözdizimi,
# anahtar kelimeleri ve yapısal kuralları burada tanımlanır.

# Dilin tanımı: Grammar/Grammar → EBNF formatında yazılmıştır
# Örnek: with_stmt: 'with' with_item (',' with_item)* ':' suite

# Bu dosya doğrudan kullanılmaz; pgen aracı ile DFA tablosuna çevrilir.
# DFA → Deterministic Finite Automaton → parser.c içinde yorumlanır

# Bu yapı sayesinde Python kodu önce token’lara ayrılır, sonra AST’ye çevrilir.

# ─────────────────────────────────────────────────────────────────────────────
# 2. Derleyici Katmanı (compile.c → CodeType)
# ─────────────────────────────────────────────────────────────────────────────

# Python kodu AST’ye çevrildikten sonra, CPython bunu derleyerek bir CodeType
# nesnesi üretir. Bu nesne, yürütülecek bytecode’u ve semantik bağlamı içerir.

# CodeType.co_code → bytecode dizisi
# CodeType.co_names, co_consts, co_varnames → semantik bağlam
# CodeType.co_flags → yürütme bayrakları
# CodeType.co_freevars, co_cellvars → closure bağlamı

# Derleme süreci: kaynak kod → AST → CodeType → co_code (bytecode)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Yorumlayıcının Çekirdeği (ceval.c → Eval Loop)
# ─────────────────────────────────────────────────────────────────────────────

# Yorumlayıcının çekirdeği, derlenmiş CodeType nesnesini opcode opcode yürütür.
# Bu döngü, CPython’un sıcak döngüsüdür → en fazla zaman burada harcanır.

# Fonksiyon: PyEval_EvalFrameEx() → Python/ceval.c içinde tanımlıdır
# Her opcode için switch-case yapısı vardır:
# Örnek: LOAD_FAST, CALL_FUNCTION, RETURN_VALUE

# Bu döngü, Python kodunun gerçek yürütme motorudur.

# ─────────────────────────────────────────────────────────────────────────────
# 4. Çalışma Zamanı Yapılandırması (initconfig.c → PyConfig)
# ─────────────────────────────────────────────────────────────────────────────

# CPython başlatıldığında, sistem ortamı ve komut satırı bayraklarıyla
# çalışma zamanı yapılandırması oluşturulur.

# Yapı: PyConfig → Include/cpython/initconfig.h
# Örnek alanlar: verbose, optimization_level, inspect, use_environment

# Bu yapı, yorumlayıcının hangi modda çalışacağını belirler:
# - REPL mi açılacak?
# - Dosya mı çalıştırılacak?
# - Modül mü çağrılacak?

# ─────────────────────────────────────────────────────────────────────────────
# 5. Standart Kütüphane ve Modüller
# ─────────────────────────────────────────────────────────────────────────────

# CPython dağıtımı sadece yorumlayıcı değil, aynı zamanda standart kütüphaneyi
# de içerir. Bunlar:
# - Lib/ → saf Python modülleri
# - Modules/ → C ile yazılmış modüller (örneğin math, ssl, gc)

# Bunlar yorumlayıcının davranışsal genişlemesini sağlar.

# ─────────────────────────────────────────────────────────────────────────────
# 6. Yorumlayıcı ≠ Sadece Eval Loop
# ─────────────────────────────────────────────────────────────────────────────

# “Yorumlayıcı” dediğimiz şey:
# - Grammar tanımı
# - Derleyici (compile.c)
# - Eval loop (ceval.c)
# - Çalışma zamanı yapılandırması (initconfig.c)
# - Standart kütüphane (Lib/, Modules/)

# “Yorumlayıcının çekirdeği” ise sadece eval loop’tur → sıcak döngü

# ─────────────────────────────────────────────────────────────────────────────
# 7. Derleme Süreci Yanıltıcı Anlatılır
# ─────────────────────────────────────────────────────────────────────────────

# Genellikle “Python kaynak kodu → bytecode” denir.
# Ama mimari olarak doğru ifade: kaynak kod → CodeType → co_code (bytecode)

# Bytecode, kendi başına bir varlık değil; CodeType nesnesinin içinde kapsanır.

# ─────────────────────────────────────────────────────────────────────────────
# 8. Real Python’un Katkısı
# ─────────────────────────────────────────────────────────────────────────────

# Real Python’daki rehber, CPython’un kaynak kod yapısını adım adım anlatır:
# - Grammar → AST → CodeType → Eval loop zinciri
# - Derleme süreci
# - Bellek yönetimi (PyArena, GC)
# - Tokenizasyon (tokenize.py vs tokenizer.c)

# Bu rehber, yorumlayıcının hem dil tanımını hem de çalışma motorunu
# somutlaştırmak için ideal bir kaynak.

# ─────────────────────────────────────────────────────────────────────────────
# 9. Performans Davranışı ve Isınma Süreci
# ─────────────────────────────────────────────────────────────────────────────

# CPython yorumlayıcısı, kaynak kodu çalıştırmadan önce derleyerek bytecode üretir.
# Bu bytecode, CodeType nesnesinin co_code alanında tutulur ve __pycache__(klasordür) altında
# .pyc dosyası olarak önbelleğe alınır.

# İlk çalıştırma:
# - Kaynak kod → AST → CodeType → co_code → yürütme
# - Derleme + yürütme birlikte gerçekleşir → daha yavaş

# İkinci ve sonraki çalıştırmalar:
# - __pycache__ içindeki .pyc dosyası doğrudan yüklenir
# - Derleme atlanır → sadece yürütme yapılır → daha hızlı

# Bu davranış, CPython’un “compile-once, execute-many” mimarisinden gelir.

# ─────────────────────────────────────────────────────────────────────────────
# 10. Sıcak Döngü ve Test Isınması
# ─────────────────────────────────────────────────────────────────────────────

# Eval loop (ceval.c → PyEval_EvalFrameEx), yorumlayıcının sıcak döngüsüdür.
# Python kodu çalışırken en fazla zaman burada harcanır.

# Test ve benchmark yaparken “ısınma” (warm-up) yapılmasının nedeni:
# - İlk çalıştırmada derleme, import, GC tetiklenmesi gibi ek maliyetler vardır
# - Kodun sıcak döngüye girmesi zaman alır
# - Özellikle closure, generator, decorator gibi yapılar ilk çağrıda yavaş olabilir

# Isınma süreci:
# - Kod birkaç kez çalıştırılır → opcode’lar cache’lenir
# - GC davranışı stabilize olur
# - Kodun sıcak yolları belirlenir → daha tutarlı ölçüm yapılabilir

# Bu nedenle performans testlerinde:
# - İlk birkaç çalıştırma göz ardı edilir
# - Sonraki çalıştırmaların ortalaması alınır

# ─────────────────────────────────────────────────────────────────────────────
# 11. JIT ve CPython 3.13 ile Gelen Potansiyel
# ─────────────────────────────────────────────────────────────────────────────

# CPython 3.13 ile deneysel JIT derleyici (PEP 744) eklendi.
# Varsayılan olarak kapalıdır çünkü:
# - Henüz stabil değil
# - LLVM bağımlılığı var
# - Platform uyumsuzluğu riski taşıyor

# JIT açıkken:
# - Sıcak döngüdeki opcode’lar makine koduna çevrilir
# - Eval loop atlanır → doğrudan CPU’ya uygun kod çalıştırılır
# - Özellikle döngü ve fonksiyon çağrılarında ciddi hız artışı sağlanabilir

# Ancak JIT’in ilk çalıştırma gecikmesi (warm-up cost) vardır.
# Bu nedenle küçük betikler için faydası sınırlı olabilir.

