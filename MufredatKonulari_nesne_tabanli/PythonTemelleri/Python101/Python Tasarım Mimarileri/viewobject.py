# ------------------------------------------------------------------------------
# 🔍 KONU: "View Object" Tasarımı – Hashlist'e Pythonic Erişim Sağlamak
# ------------------------------------------------------------------------------

# 📌 AMAÇ:
# Python'daki `dict.keys()`, `dict.values()`, `dict.items()` gibi fonksiyonlar
# doğrudan liste dönmezler. Bunun yerine, bellekteki verilere 'canlı pencere' açan
# hafif, tembel (lazy) ve güncel kalan "view object" ler dönerler.
# Biz de `Hashlist` isimli özel yapımıza benzer bir pencere sistemini
# kendi sınıflarımızla kurmak istiyoruz.

# 📦 Yapılacak Şey:
# Her biri sadece özel bir görevi olan 3 view sınıfı tanımlıyoruz:
# - `Hashkeysview`: sadece anahtarları döndürür
# - `Hashvaluesview`: sadece değerleri döndürür
# - `Hashitemsview`: (anahtar, değer) çiftlerini döndürür

# Bu sınıflar, `__iter__()` tanımlayarak iterable hale getirilirler.
# Böylece for döngülerinde ya da list(), tuple(), set() gibi yapılarda rahatça kullanılırlar.

# ✅ Bu yapı sayesinde:
# - Bellekteki verinin kopyasını almadan erişim sağlanır
# - Ana veri (`self._place`) değişirse, view de otomatik güncel kalır
# - dict-vari API sağlanmış olur
# ------------------------------------------------------------------------------

class Hashkeysview:
    def __init__(self, hashs):
        # 🔹 Ana veri yapısına referans tutuyoruz (kopya değil!)
        self._place = hashs

    def __iter__(self):
        # 🔁 Anahtarlar üzerinde gezinmek için generator döndürüyoruz
        return (key for key, _ in self._place)


class Hashvaluesview:
    def __init__(self, hashs):
        # 🔹 Aynı şekilde değerleri görmek için pencere açıyoruz
        self._place = hashs

    def __iter__(self):
        # 🔁 Sadece değerler
        return (value for _, value in self._place)


class Hashitemsview:
    def __init__(self, hashs):
        # 🔹 Ana (key, value) çiftleri
        self._place = hashs

    def __iter__(self):
        # 🔁 Tüm (anahtar, değer) çiftlerini döndür
        return (items for items in self._place)
