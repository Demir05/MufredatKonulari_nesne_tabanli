# ============================================================
# 🔎 REGEX TABANLI LEXER
# ============================================================
# 1) Genel Tanım:
#    - Token kuralları regex ifadeleriyle tanımlanır.
#    - Input string üzerinde bu regex’ler uygulanır, eşleşmelere göre token üretilir.
#
# 2) İleri Tanımlar:
#    - Lexer her token tipi için bir regex tanımlar:
#         NUMBER → "\d+"
#         IDENT  → "[a-zA-Z_][a-zA-Z0-9_]*"
#    - Kaynak kodda sırayla bu pattern’ler eşleşir, token listesi oluşturulur.
#
# 3) Kullanım Alanları:
#    - Küçük diller veya DSL (domain specific language).
#    - Eğitim amaçlı derleyici tasarımı.
#    - Prototipleme (hızlıca lexer yazmak için).
#
# 4) Ekstra Detaylar:
#    - Kolaydır ama performansı zayıftır (regex motoru ileri/geri bakış yapabilir).
#    - Büyük dillerde regex tabanlı lexer yetersiz kalır → yerine DFA/NFA tabanlı lexer kullanılır.
#
# 5) Örnek:
#    >>> TOKENS = [("NUMBER", r"\d+"), ("PLUS", r"\+"), ("IDENT", r"[a-zA-Z_]\w*")]
#    >>> "10 + x" → [('NUMBER', '10'), ('PLUS', '+'), ('IDENT', 'x')]
# ============================================================


# ============================================================
# 🔎 INDENT, DEDENT, NEWLINE (Girinti tabanlı dillerde özel tokenler)
# ============================================================
# 1) Genel Tanım:
#    - Çoğu dilde blok yapısı {} ile belirlenir, Python’da girinti ile.
#    - Bu yüzden lexer, girinti değişikliklerini özel token’lara dönüştürür:
#         INDENT  → girinti başladı
#         DEDENT  → girinti bitti
#         NEWLINE → satır sonu
#
# 2) İleri Tanımlar:
#    - Tokenizer girinti seviyesini bir stack üzerinde takip eder.
#    - Yeni bir satırda girinti artarsa INDENT token, azalırsa DEDENT token üretir.
#
# 3) Kullanım Alanları:
#    - Sadece Python gibi indentation-based dillerde.
#    - Parser’ın blok yapısını anlaması için zorunludur.
#
# 4) Ekstra Detaylar:
#    - Bu token’lar olmadan parser, hangi ifadelerin aynı blokta olduğunu bilemez.
#    - Diğer dillerde bu iş süslü parantez "{" "}" veya "begin-end" ile yapılır.
#
# 5) Örnek:
#    Kod:
#        if True:
#            x = 5
#    Tokenler:
#        NAME("if"), NAME("True"), OP(":"), NEWLINE,
#        INDENT, NAME("x"), OP("="), NUMBER("5"), NEWLINE, DEDENT
# ============================================================


# ============================================================
# 🔎 LEXER OPTİMİZASYONLARI (Regex vs DFA/NFA)
# ============================================================
# 1) Genel Tanım:
#    - Lexer implementasyonunda iki yaklaşım vardır:
#        a) Regex tabanlı lexer
#        b) State machine tabanlı lexer (DFA/NFA)
#
# 2) İleri Tanımlar:
#    - Regex tabanlı lexer:
#        • Token kuralları regex ile yazılır.
#        • Motor ileri/geri bakış yapabilir, maliyetlidir.
#    - DFA/NFA tabanlı lexer:
#        • Deterministic Finite Automaton (DFA) mantığıyla çalışır.
#        • Karakterleri tek geçişte işler, daha hızlıdır.
#
# 3) Kullanım Alanları:
#    - Regex tabanlı lexer → küçük diller, eğitim, prototip.
#    - DFA/NFA lexer → büyük diller (C, Python, Java).
#
# 4) Ekstra Detaylar:
#    - CPython’un tokenizer.c dosyası DFA tabanlıdır.
#    - DFA: Tek geçişte karar verir, bellek dostudur.
#    - Regex motoru: Çok geçişli olabilir, bellek kullanımı daha fazladır.
#
# 5) Örnek:
#    Regex tabanlı lexer:
#        "\d+" → "123" (NUMBER)
#    DFA tabanlı lexer:
#        Durumlar: START → DIGIT → NUMBER_ACCEPT
#        "123" → NUMBER token (tek geçişte)
# ============================================================