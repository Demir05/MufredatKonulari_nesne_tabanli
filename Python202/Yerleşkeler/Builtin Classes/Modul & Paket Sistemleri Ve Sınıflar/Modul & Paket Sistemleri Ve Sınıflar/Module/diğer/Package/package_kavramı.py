# ================================================================================
# 📦 PAKET KAVRAMI VE __package__ – DETAYLI YORUMLU AÇIKLAMA
# ================================================================================

# Python'da "paket", iç içe klasör yapısı kullanılarak oluşturulan bir modül koleksiyonudur.
# Paketler, daha büyük projelerde kodu organize etmek, modülerleştirmek ve yeniden kullanılabilir
# hale getirmek için kullanılır.

# ================================================================================
# 1️⃣ TANIM – PAKET NEDİR?
# ------------------------------------------------------------------------------

# Basitçe:
#   📁 bir klasör
#   +
#   📄 içinde __init__.py dosyası varsa
#   =
#   📦 o klasör bir "paket" olur

# Örnek klasör yapısı:
#   myproject/
#     __init__.py         ← bu dosya varsa "myproject" artık bir paket
#     utils/
#         __init__.py     ← bu da bir alt paket
#         mathtools.py    ← bu bir modül (dosya)

# Yukarıdaki yapıda:
#   - `myproject` bir ana pakettir
#   - `myproject.utils` bir alt pakettir
#   - `myproject.utils.mathtools` bir modüldür

# ================================================================================
# 2️⃣ __package__ NEYİ GÖSTERİR?
# ------------------------------------------------------------------------------

# __package__, bir modülün (veya alt modülün) **ait olduğu paket zincirini** belirtir.
# Bu, Python'un import sistemi için çok önemlidir çünkü relative importlar bu bilgiye göre yapılır.

# Örnek:
# Eğer dosya `myproject/utils/mathtools.py` içindeyse, `__package__` şöyle olur:
#     __package__ == "myproject.utils"

# Bu sayede, aynı paket içindeki diğer modülleri şöyle import edebilirsin:
#     from .othermodule import something

# Eğer modül doğrudan çalıştırılıyorsa:
#     __package__ == None  veya boş string olur

# ================================================================================
# 3️⃣ ÖRNEK: MODÜL VE __package__ DEĞERİ
# ------------------------------------------------------------------------------

# Örnek dosya: myproject/utils/strings.py
# İçeriği:
#   print(__name__)      → myproject.utils.strings
#   print(__package__)   → myproject.utils

# Örnek dosya: ana.py
# İçeriği:
#   import myproject.utils.strings

# Bu durumda strings.py'nin __package__'ı "myproject.utils" olur.

# ================================================================================
# 4️⃣ __package__ NEREDE KULLANILIR?
# ------------------------------------------------------------------------------

# 1. Relative importlar yapılırken Python hangi pakette olduğunu anlamak için kullanır.
# 2. Bazı loader sistemleri (importlib gibi) modülün bulunduğu bağlamı tanımlamak için kullanır.
# 3. Derin modüllerde yukarı çıkmadan import yapabilmek için gereklidir.

# ================================================================================
# 5️⃣ Elle Oluşturulmuş Modüllerde __package__
# ------------------------------------------------------------------------------

# from types import ModuleType
# m = ModuleType("modul")

# print(m.__package__)  → None
# Çünkü bu modül dosya sistemine bağlı olmadığı için paketi bilinmez.

# Ama elle ayarlanabilir:
# m.__package__ = "myproject.utils"

# Bu sayede relative import gibi sistemler elle simüle edilebilir.

# ================================================================================
# ✅ ÖZET

# - Paket, içindeki __init__.py ile tanımlanmış klasördür
# - __package__ bir modülün hangi pakete ait olduğunu belirtir
# - Relative importlar bu bilgiye göre çözülür
# - Elle oluşturulan modüllerde boş olur ama elle verilebilir
# - import sisteminde konum belirleyici anahtar değişkendir

# ================================================================================


