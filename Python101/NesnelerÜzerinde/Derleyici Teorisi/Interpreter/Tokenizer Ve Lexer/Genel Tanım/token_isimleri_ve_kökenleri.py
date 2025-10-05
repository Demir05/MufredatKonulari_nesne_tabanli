# ============================================================
# 🔎 TOKEN İSİMLERİ VE KÖKENLERİ
# ============================================================
# 1) Genel Tanım:
#    - Python’daki token türleri (NAME, NUMBER, STRING, OP, INDENT, DEDENT, NEWLINE vb.)
#      CPython’un kaynak kodunda sabit (constant) olarak tanımlanır.
#    - Bu isimler daha sonra Python tarafında "token" modülüyle erişilebilir hale gelir.
#
# 2) İleri Tanımlar:
#    - CPython kaynak kodunda /Include/token.h dosyası vardır.
#      Burada her token’a bir sabit numara atanır:
#        #define NAME    1
#        #define NUMBER  2
#        #define STRING  3
#        ...
#    - Bu sabitler C tarafında kullanılır, Python tarafına yansıtılmak üzere token.py dosyası üretilir.
#    - token.py içinde hem sabitler hem de tok_name isimli bir dict bulunur.
#      Bu dict sayesinde sayı → isim eşlemesi yapılır.
#
# 3) Kullanım Alanları:
#    - Tokenizer (C ile yazılmış) token üretirken bu sabitleri kullanır.
#    - Token bilgisi Python tarafında TokenInfo nesnesine aktarılır.
#    - Kullanıcı, token modülü üzerinden bu isimleri görebilir.
#
# 4) Ekstra Detaylar / Dikkat Edilecekler:
#    - Token isimleri standarttır ve Python sürümleriyle birlikte güncellenebilir.
#      (örn. Python 3.9 ile birlikte "TYPE_COMMENT" token’i eklendi.)
#    - Token sayıları aslında sadece integer’dır, isimler okunabilirlik içindir.
#    - Tokenizer yalnızca bu sabitlere uygun değerler dönebilir.
#
# 5) Örnek:
#    >>> import token
#    >>> token.NAME
#    1
#    >>> token.NUMBER
#    2
#    >>> token.tok_name[1]
#    'NAME'
#    >>> token.tok_name[2]
#    'NUMBER'
# ============================================================


# ============================================================
# 🔎 CPYTHON DÜZEYİNDE TOKENIZER
# ============================================================
# 1) Genel Tanım:
#    - CPython’da tokenizer (tokenizer.c) kaynak kodu karakter karakter okur,
#      uygun token türünü belirler ve token.h’deki sabitlerle eşleştirir.
#
# 2) İleri Tanımlar:
#    - Örnek süreç:
#       Kod: "x = 5"
#       - "x" → NAME token (1)
#       - "=" → OP token (54)
#       - "5" → NUMBER token (2)
#    - Tokenizer, her bir token için:
#       • tür numarası (int)
#       • string değeri
#       • konum bilgisi (satır, sütun)
#      döner.
#
# 3) Kullanım Alanları:
#    - Parser’ın ihtiyaç duyduğu yapı taşlarını sağlar.
#    - Token akışını üretir, parser bu akış üzerinde gramer kurallarını uygular.
#    - Hata raporlama için satır/sütun bilgilerini taşır.
#
# 4) Ekstra Detaylar:
#    - Tokenizer aynı zamanda Python’un girinti kurallarını işler (INDENT, DEDENT).
#    - Yorum satırlarını atar, ama type comment gibi özel durumlarda onları token olarak üretir.
#    - Tokenizer’ın çıktısı olmadan parser çalışamaz.
#
# 5) Örnek:
#    Kod: "def foo(): return 1"
#    Token Akışı:
#       NAME("def")
#       NAME("foo")
#       OP("(")
#       OP(")")
#       OP(":")
#       NAME("return")
#       NUMBER("1")
#       NEWLINE
# ============================================================


# ============================================================
# 🔎 TOKENLERİN KAYNAK DOSYALARI
# ============================================================
# 1) Genel Tanım:
#    - CPython kaynak kodunda token’lar birkaç yerde tanımlıdır.
#
# 2) İleri Tanımlar:
#    - /Include/token.h → Token sabitleri (C tarafı tanımları)
#    - /Parser/token.c  → Tokenizer’ın implementasyonu (C kodu)
#    - /Lib/token.py    → Python tarafında token isimleri ve tok_name dict
#
# 3) Kullanım Alanları:
#    - C tarafı → derleyici çekirdeği
#    - Python tarafı → tokenize modülü, AST dönüşümleri, analiz araçları
#
# 4) Ekstra Detaylar:
#    - token.py dosyası CPython build sürecinde otomatik üretilir (token.h’den).
#    - Böylece C tarafı ve Python tarafı arasında tutarlılık sağlanır.
#
# 5) Örnek:
#    CPython kaynağına bakıldığında:
#       token.h:  NAME 1, NUMBER 2, STRING 3, ...
#       token.py: NAME=1, NUMBER=2, STRING=3, tok_name={1:"NAME",2:"NUMBER",3:"STRING",...}
# ============================================================
