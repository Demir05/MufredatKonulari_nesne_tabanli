# ============================================================
# 🧠 PYTHON'DA __qualname__ NEDİR? — DETAYLI AÇIKLAMA
# ============================================================

# ✅ __qualname__ (qualified name), bir nesnenin "nitelikli ismini" verir.
# - Bu isim, sadece sınıf adı değil, ait olduğu sınıfları ve yapıları da içerir
# - Özellikle iç içe tanımlanmış sınıflar veya fonksiyonlarda kullanılır

# 🔍 Neden önemli?
# -----------------
# - Debug ve log işlemlerinde daha doğru yer belirleme sağlar
# - IDE ve hata ayıklayıcılar (__qualname__) sayesinde iç içe yapıları ayırt eder
# - Dinamik import veya introspection işlemlerinde tercih edilir


# ============================================================
# 🧪 TEMEL ÖRNEK
# ============================================================

class Outer:
    class Inner:
        def method(self): pass

print(Outer.Inner.__name__)      # "Inner"
print(Outer.Inner.__qualname__)  # "Outer.Inner"

# ✅ __name__ sadece sınıfın adını verir
# ✅ __qualname__ ise nerede tanımlandığını da içerir
# 🔧 __module__ → Dosya/Başlangıç noktası (nerede TANIMLANDI)
# 🔧 __qualname__ → Yapı içinde NEREDE yer alıyor


# ============================================================
# 🧪 GERÇEK HAYATTA KULLANIM: LOGGING SİSTEMİ
# ============================================================

import logging

def dynamic_logger(obj: object) -> logging.Logger:
    """
    Nesnenin bulunduğu yapı ve sınıfa göre dinamik logger oluşturur
    """
    name = f"{obj.__class__.__module__}.{obj.__class__.__qualname__}"
    return logging.getLogger(name)

# Kullanım
class MyService:
    def __init__(self):
        self.logger = dynamic_logger(self)

    def process(self):
        self.logger.info("İşlem başlatıldı.")

# 📦 logger adı şu olur: "__main__.MyService" → hem modül hem sınıf bilgisi içerir

