    # ============================================================
# 🧠 FUNCTIONAL CHAINING + IMMUTABILITY → Python Tasarımı
# ============================================================

# 🔹 Amaç:
#     Her method çağrısında objeyi doğrudan değiştirmek yerine,
#     onun yeni bir versiyonunu üretip geri döndürmek.

# 🔹 Bu iki prensip şunları sağlar:
#     ✅ Nesneler değişmezdir (Immutability)
#     ✅ Fonksiyonlar birbirine zincirlenebilir (Functional Chaining)

# 🔹 Böylece:
#     - Kodun okunabilirliği artar
#     - Yan etkisiz işlemler yapılır
#     - Her adımda önceki state bozulmadan ilerlenir
#     - Sınıflar "builder-pattern" tarzında API kazanır

# 🔹 Kullanım yerleri:
#     - config yapıları
#     - HTTP sorguları
#     - ORM filtreleri
#     - ML Pipeline adımları
#     - veri işleme zincirleri (pandas, numpy, torch vs.)

# ============================================================
# ✅ ÖRNEK: Zincirlenebilir ve Değiştirilemez Config Sınıfı
# ============================================================

class Config:
    def __init__(self, **opts):
        # Ayarları dict içinde tut
        self._options = opts

    def with_option(self, key, value):
        # Yeni yapılandırma sözlüğü oluştur (mevcut state bozulmasın)
        new_opts = self._options.copy()
        new_opts[key] = value

        # Yeni bir Config nesnesi döndür (immutability)
        return Config(**new_opts)

    def __str__(self):
        return str(self._options)

# ============================================================
# 🧪 ÖRNEK KULLANIM VE AÇIKLAMALAR
# ============================================================

cfg1 = Config().with_option("debug", True)
cfg2 = cfg1.with_option("timeout", 30)

print(cfg1)  # 🔹 {'debug': True}
print(cfg2)  # 🔹 {'debug': True, 'timeout': 30}

# 💡 Açıklama:
# - `cfg1` ilk oluşturulan yapı → sadece "debug" içeriyor
# - `cfg2`, `cfg1`'den türeyen yapı → üstüne "timeout" eklendi
# - Hiçbiri diğerini ezmedi ❗ (immutability)
# - Zincirleme yapılarak okunabilir API tasarlandı (chaining)

# ------------------------------------------------------------
# 🔁 Zincirleme kullanım örneği:
cfg = Config().with_option("lang", "TR").with_option("env", "prod").with_option("debug", True)
print(cfg)
# 🔹 {'lang': 'TR', 'env': 'prod', 'debug': True}