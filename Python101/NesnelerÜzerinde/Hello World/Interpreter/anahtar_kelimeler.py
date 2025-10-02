# ─────────────────────────────────────────────────────────────
# 🧠 PYTHON'DA KEYWORD (ANAHTAR KELİME) NEDİR?
# ─────────────────────────────────────────────────────────────

# Python'da "keyword" terimi, dilin sözdizimini tanımlayan rezerve edilmiş kelimeleri ifade eder.
# Örnekler: if, for, while, def, class, return, import, try, with, lambda, yield, etc.

# Bu kelimeler özel anlam taşır ve Python yorumlayıcısı tarafından tanınır.
# Bu yüzden değişken adı olarak kullanılamazlar:
# class = "math"  # ❌ SyntaxError: invalid syntax

# Keyword'ler dilin gramerini oluşturur — yani Python kodunun nasıl yazılacağını belirler.

# ─────────────────────────────────────────────────────────────
# ❌ KEYWORD'LER NEDEN NESNE DEĞİLDİR?
# ─────────────────────────────────────────────────────────────

# Python'da her şey nesne gibi görünse de, keyword'ler nesne değildir.
# Çünkü:
# - Bellekte bir nesne olarak temsil edilmezler
# - type(), id(), isinstance() gibi fonksiyonlarla sorgulanamazlar
# - __dict__ veya __annotations__ gibi attribute'ları yoktur
# - Kodun çalışması için değil, yorumlanması için vardır

# Örneğin:
# type("for") → <class 'str'>  # sadece string hali nesnedir
# Ama 'for' kelimesi, dilin sözdizimsel parçasıdır — bir token'dır, bir nesne değil.

# ─────────────────────────────────────────────────────────────
# 🔍 KEYWORD'LER NASIL ERİŞİLEBİLİR?
# ─────────────────────────────────────────────────────────────

# Python'da keyword'lere erişmek için 'keyword' adlı standart modül kullanılır:

import keyword

# keyword.kwlist → Python'daki tüm hard keyword'lerin listesi
# keyword.iskeyword("for") → True
# keyword.iskeyword("ozan") → False

# Bu modül, dilin rezerve edilmiş kelimelerini programatik olarak kontrol etmemizi sağlar.
# Özellikle kod üretimi, analiz, linting ve autocomplete gibi işlemlerde kullanılır.

# ─────────────────────────────────────────────────────────────
# 🧪 SOFT KEYWORD NEDİR?
# ─────────────────────────────────────────────────────────────

# Python 3.9 ile birlikte "soft keyword" kavramı tanıtıldı.
# Soft keyword'ler, belirli bağlamlarda keyword gibi davranan ama diğer yerlerde tanımlayıcı olarak kullanılabilen kelimelerdir.

# Örnek:
# match x:
#     case 1: ...

# Burada 'match' ve 'case' soft keyword olarak davranır.
# Ama şu da geçerlidir:
# match = "eşleşme"  # ✅ geçerli değişken adı

# Soft keyword'ler dilin esnekliğini artırmak için tanıtıldı.
# Böylece yeni dil özellikleri (örneğin pattern matching) eklenirken eski kodlarla çakışma yaşanmaz.

# ─────────────────────────────────────────────────────────────
# 🔧 SOFT KEYWORD'LER NASIL ERİŞİLİR?
# ─────────────────────────────────────────────────────────────

# keyword.softkwlist → Soft keyword'lerin listesi
# keyword.issoftkeyword("match") → True
# keyword.issoftkeyword("for") → False

# Bu yapı, dilin bağlam duyarlı hale gelmesini sağlar.
# Soft keyword'ler sadece belirli gramer kurallarında özel anlam taşır.

# ─────────────────────────────────────────────────────────────
# 🎯 ÖZET
# ─────────────────────────────────────────────────────────────

# ✅ Hard keyword → her yerde rezerve, değişken adı olarak kullanılamaz
# ✅ Soft keyword → sadece belirli bağlamlarda özel anlam taşır, diğer yerlerde kullanılabilir
# ❌ Keyword'ler nesne değildir → çünkü yorumlayıcı tarafından tokenize edilir, bellekte nesne olarak yer almaz
# 🔍 keyword modülü → hem hard hem soft keyword'leri programatik olarak kontrol etmemizi sağlar

# Python'un bu yapısı, dilin hem güçlü hem esnek olmasını sağlar.
# Yeni özellikler eklenirken eski kodlarla uyumluluk korunur.

# PEP 622 → Python’a pattern matching özelliğini ve soft keyword kavramını tanıttı.
# PEP 634 → match-case yapısının teknik tanımını ve gramer kurallarını belirledi.
# PEP 635 → pattern matching’in neden eklendiğini ve tasarım kararlarını açıkladı.
# PEP 636 → match-case kullanımını örneklerle anlattı, öğretici bir rehber sundu.
