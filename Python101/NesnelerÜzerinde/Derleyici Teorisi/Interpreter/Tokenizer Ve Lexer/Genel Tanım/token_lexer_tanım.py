# ============================================================
# 🔎 LEXER
# ============================================================
# 1) Genel Tanım:
#    - Lexer (Lexical Analyzer), kaynak kodu en küçük anlamlı birimlere (token’lara) ayıran araçtır.
#    - Amacı, parser’ın işini kolaylaştırmak için ham karakterleri sınıflandırmaktır.
#
# 2) İleri Tanımlar:
#    - Lexer, genellikle "finite state machine (FSM)" mantığıyla çalışır.
#      Karakterleri okur, durumlar arasında geçiş yapar, token sınırlarını belirler.
#    - Tokenizer ile farkı: Tokenizer yalnızca böler, Lexer hem böler hem de sınıflandırır.
#
# 3) Kullanım Alanları:
#    - Her derleyici ve yorumlayıcıda ilk aşama.
#    - Kaynak kod analizi, statik kod kontrolleri, güvenlik taramaları.
#    - Özel diller / DSL (Domain Specific Language) geliştirirken.
#
# 4) Ekstra Detaylar / Dikkat Edilecekler:
#    - Yorum satırları, boşluklar ve tab karakterleri genelde atılır.
#    - Python gibi dillerde girinti (INDENT / DEDENT) bile token’a dönüşebilir.
#    - String literal'ler, yorumlar ve çok karakterli operatörler özel işlenmelidir.
#
# 5) Örnek:
#    Kod:   x = 5 + 3
#    Lexer Çıktısı: [NAME("x"), OP("="), NUMBER("5"), OP("+"), NUMBER("3")]
# ============================================================


# ============================================================
# 🔎 TOKEN
# ============================================================
# 1) Genel Tanım:
#    - Token, kaynak kodun en küçük anlamlı birimidir.
#    - Tür (type) + değer (value) + konum bilgisi (line, column) içerir.
#
# 2) İleri Tanımlar:
#    - Token türleri genellikle: KEYWORD, IDENTIFIER, NUMBER, STRING, OPERATOR, DELIMITER, NEWLINE.
#    - Python tokenize modülü her token için "TokenInfo" nesnesi döndürür.
#
# 3) Kullanım Alanları:
#    - Parser’ın çalışması için gerekli girdiyi sağlar.
#    - Kod renklendirme (syntax highlighting).
#    - Statik analiz araçları (ör. pylint) token düzeyinde tarama yapabilir.
#
# 4) Ekstra Detaylar:
#    - Aynı sembol farklı bağlamlarda farklı token olabilir (örn. "=" atama iken "==" karşılaştırma).
#    - String literal içinde geçen semboller token’a ayrılmaz.
#
# 5) Örnek:
#    Kod: print("x=5")
#    Tokenler: [NAME("print"), OP("("), STRING("x=5"), OP(")")]
# ============================================================


# ============================================================
# 🔎 TOKENIZER
# ============================================================
# 1) Genel Tanım:
#    - Tokenizer, ham karakter akışını dilin tanımlı kurallarına göre parçalara böler.
#
# 2) İleri Tanımlar:
#    - Tokenizer genelde lexer’in bir alt parçası olarak çalışır.
#    - Ayrıştırma yapar ama sınıflandırmayı lexer tamamlar.
#
# 3) Kullanım Alanları:
#    - Dil işleme (compilers, interpreters).
#    - Veri işleme (ör. CSV, JSON parser'ları bile basit tokenizasyon yapar).
#
# 4) Ekstra Detaylar:
#    - Tokenizer yalnızca sınırları bulur, semantic anlam vermez.
#    - Örn: "123" sadece "sayı dizisi" olarak ayrılır, bunun "NUMBER token" olduğunu lexer karar verir.
#
# 5) Örnek:
#    Kod: abc123
#    Tokenizer Çıktısı: ["abc123"]
#    Lexer Çıktısı: [IDENTIFIER("abc123")]
# ============================================================


# ============================================================
# 🔎 REGEX İLE İLİŞKİ
# ============================================================
# 1) Genel Tanım:
#    - Lexer, karakter örüntülerini tanımlamak için regex benzeri kurallardan faydalanır.
#
# 2) İleri Tanımlar:
#    - Her token türü bir regex ile tarif edilebilir:
#        IDENTIFIER → [a-zA-Z_][a-zA-Z0-9_]*
#        NUMBER     → [0-9]+
#        STRING     → ".*?"
#
# 3) Kullanım Alanları:
#    - Lexer yazarken regex en hızlı çözüm.
#    - Token sınırlarını net şekilde tanımlamak için.
#
# 4) Ekstra Detaylar:
#    - Regex sadece deseni tanımlar, "bu desen IDENTIFIER’dır" yorumunu lexer yapar.
#    - Büyük dillerde lexer genelde regex yerine optimize edilmiş state machine kullanır.
#
# 5) Örnek:
#    Kod: var1 = 99
#    Regex ile eşleşmeler: [IDENTIFIER("var1"), OP("="), NUMBER("99")]
# ============================================================


# ============================================================
# 🔎 EBNF (Extended Backus–Naur Form) İLE İLİŞKİ
# ============================================================
# 1) Genel Tanım:
#    - EBNF, bir dilin gramerini tanımlamak için kullanılan formal bir notasyondur.
#
# 2) İleri Tanımlar:
#    - Lexer seviyesinde: hangi karakter örüntülerinin token oluşturacağını tarif eder.
#    - Parser seviyesinde: token’ların nasıl birleşip dil yapısını oluşturacağını tanımlar.
#
# 3) Kullanım Alanları:
#    - Programlama dillerinin resmi spesifikasyonları (örn. Python grammar).
#    - Parser jeneratörleri (ANTLR, yacc, bison).
#
# 4) Ekstra Detaylar:
#    - EBNF ile regex arasındaki fark: Regex → düşük seviye desenler, EBNF → dilin kuralları.
#    - EBNF, lexer ve parser arasındaki köprü gibidir.
#
# 5) Örnek:
#    EBNF kuralı:
#        assignment = identifier "=" expression ;
#        expression = number | expression "+" expression ;
#
#    Kod: x = 5 + 3
#    Tokenler: [NAME("x"), OP("="), NUMBER("5"), OP("+"), NUMBER("3")]
#    Parser → AST: Assign(Name("x"), BinOp(5, Add, 3))
# ============================================================
