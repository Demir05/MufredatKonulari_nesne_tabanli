# ============================================================
# 📌 raise ... from ...  — DETAYLI TANIM
# ============================================================

# ------------------------------------------------------------
# 1️⃣ raise from NEDİR?
# ------------------------------------------------------------
# - "Bu yeni hatanın asıl sebebi başka bir hatadır" demek için kullanılır.       # root cause bağlama
# - Teknik olarak, yeni hatanın __cause__ attribute’unu eski hata nesnesine set eder. # zincirleme hata bilgisi
# - Python traceback çıktısında:
#       The above exception was the direct cause of the following exception:
#   şeklinde ek bilgi görürsün.                                                  # okunabilir zincir

# ------------------------------------------------------------
# 2️⃣ NEDEN ÖNEMLİ?
# ------------------------------------------------------------
# - Hata zincirini açıkça gösterir → debug kolaylaşır.                           # hatanın kaynağı korunur
# - Farklı katmanlarda hata tipini değiştirebilirsin ama sebebi saklarsın.       # tip çevirme + sebep saklama
# - Örn: altta gelen ValueError'ı üst katmanda RuntimeError’a çevirip atabilirsin.

# ------------------------------------------------------------
# 3️⃣ NASIL KULLANILIR?
# ------------------------------------------------------------
# raise YeniHataTipi("mesaj") from EskiHataNesnesi
# - YeniHataTipi: üst katmanın anlayacağı tip (ör. domain error)
# - EskiHataNesnesi: try/except ile yakalanmış orijinal hata

# ÖRNEK:
try:
    int("abc")                                     # burada ValueError oluşur
except ValueError as e:                            # e = orijinal hata
    raise RuntimeError("number parse failed") from e  # e, __cause__ olarak atanır

# ÇIKTI (özet):
# ValueError: invalid literal for int() with base 10: 'abc'
#
# The above exception was the direct cause of the following exception:
#
# RuntimeError: number parse failed

# ------------------------------------------------------------
# 4️⃣ raise from ve __context__ FARKI
# ------------------------------------------------------------
# - raise from kullanmazsan, Python otomatik olarak __context__ ile zincir kurar.
# - Ancak bu durumda "During handling of the above exception..." mesajı çıkar.
# - raise from kullanırsan, zincir "direct cause" olarak görünür (daha net anlam).
#
# Örnek:
# try:
#     int("abc")
# except ValueError:
#     raise RuntimeError("hata")        # __context__ zinciri
#
# try:
#     int("abc")
# except ValueError as e:
#     raise RuntimeError("hata") from e # __cause__ zinciri

# ------------------------------------------------------------
# 5️⃣ __suppress_context__ ile İLGİSİ
# ------------------------------------------------------------
# - raise from None dersen, Python __context__’i bastırır, zincir gösterilmez.
# - Bu, özellikle alttaki hatayı göstermek istemediğinde kullanılır.
#
# Örnek:
# try:
#     int("abc")
# except ValueError:
#     raise RuntimeError("gizli sebep") from None  # sadece üst hata görünür

# ============================================================
# 📌 1) raise from None — zinciri gizlemek
# ============================================================
# Amaç: Kullanıcıya sade hata mesajı vermek, alttaki teknik sebebi gizlemek.
# Kullanım alanı: Güvenlik (hassas iç bilgi sızdırmamak) veya kullanıcı dostu mesaj.

def get_config_value(key: str):
    config = {"host": "localhost"}
    try:
        return config[key]   # KeyError olabilir
    except KeyError:
        # Kullanıcıya "key bulunamadı" demek istiyoruz, teknik traceback istemiyoruz.
        raise ValueError(f"Config key not found: {key}") from None

# get_config_value("port")
# ÇIKTI: ValueError: Config key not found: port
#        (Altta KeyError traceback'i görünmez)

# ============================================================
# 📌 2) raise from ile loglama best practice
# ============================================================
# Amaç: Kullanıcıya sade bir üst hata göstermek ama loglarda alt hatayı da saklamak.
# Kullanım alanı: Production ortamında hem debug hem kullanıcı deneyimi.

import logging
logging.basicConfig(level=logging.ERROR)

def load_number_from_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return int(f.read().strip())   # FileNotFoundError veya ValueError olabilir
    except (OSError, ValueError) as cause:
        # Önce logla (alt hatanın detaylarını sakla)
        logging.exception("load_number_from_file failed")
        # Sonra kullanıcıya anlamlı hata ver
        raise RuntimeError("Unable to load number from file") from cause

# load_number_from_file("missing.txt")
# LOG: ERROR:load_number_from_file failed
#      Traceback (most recent call last):
#        ...
#        FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
#
#      The above exception was the direct cause of the following exception:
#      RuntimeError: Unable to load number from file
