# ----------------------------------------------
# 📦 Python'da Göreceli (Relative) Import Nedir?
# ----------------------------------------------

# Göreceli import, bir modülün **aynı paket içindeki** diğer modülleri
# veya alt modülleri içeri aktarmasını sağlar.
# Bu, proje içi modüller arasında bağlantı kurarken önemlidir.

# ----------------------------------------------
# 📌 Göreceli Semboller: `.` ve `..` Ne Demek?
# ----------------------------------------------

# `.`  : Bulunduğun modülün **bulunduğu klasör**
# `..` : Bulunduğun klasörün **bir üstü**
# `...`: İki üst klasör (vb.)

# 💡 Bu yapı, modülün dosya sistemindeki konumuna göre çözülür.
# Dolayısıyla bağımsız script'lerde değil, **paket içi modüllerde** işe yarar.

# ----------------------------------------------
# 📁 Örnek Proje Yapısı:
#
# myproject/
# ├── main.py
# └── package/
#     ├── __init__.py
#     ├── module_a.py
#     └── utils/
#         ├── __init__.py
#         └── helper.py
# ----------------------------------------------


# Eğer helper.py içindeysen:

# 👉 from . import helper
# Bu, aynı klasördeki başka bir modülü import eder
# (Yani utils/helper.py → utils/__init__.py gibi)

# 👉 from .. import module_a
# utils/helper.py → package/module_a.py'yi içeri aktarır

# 👉 from ..module_a import foo
# module_a.py içindeki `foo` fonksiyonunu import eder


# ----------------------------------------------
# 🧠 NOT:
# ----------------------------------------------
# Relative import sadece **modül bir paket içinde çalıştırıldığında**
# veya `python -m package.module` komutuyla başlatıldığında çalışır.
# Aksi takdirde "attempted relative import with no known parent package" hatası alırsın.

# Örneğin:
# ✅ python -m package.module_a    ✔️
# ❌ python package/module_a.py    ❌


# ----------------------------------------------
# 🔎 Mutlak vs Göreceli Import
# ----------------------------------------------

# 🧱 Mutlak Import:
import package.module_a
# Her zaman `sys.path`’e göre çözülür (en üstten başlar)

# 📐 Göreceli Import:
from ..module_a import foo
# Mevcut modülün konumuna göre yukarı çıkar, oradan başlar

# ----------------------------------------------
# 📌 __import__() ile Göreceli Import:
# ----------------------------------------------
__import__("module_a", globals(), locals(), [], 1)
# 1 → bir üst klasörde module_a'yı ara
# 2 → iki üst klasörde ara
# 0 → mutlak olarak ara (varsayılan)

