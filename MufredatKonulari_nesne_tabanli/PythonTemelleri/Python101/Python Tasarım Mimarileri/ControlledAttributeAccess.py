# ======================================================
# 🧠 Controlled Attribute Access + Descriptor Protocol
# ======================================================

# 🎯 Amaç:
# - Attribute erişimini doğrudan değil, kontrollü şekilde yapmak.
# - Getter / Setter / Deleter metodlarıyla **özellik davranışlarını** belirlemek.

# ------------------------------------------------------
# 🔸 Bu tasarımın temel dayanağı: Descriptor Protocol
# ------------------------------------------------------
# - Eğer bir sınıf `__get__`, `__set__`, `__delete__` methodlarını tanımlıyorsa
#   bu sınıfa Python'da "descriptor" denir.
# - property sınıfı, descriptor protokolünü uygular.

# ------------------------------------------------------
# 🔸 Ne işe yarar?
# ------------------------------------------------------
# ✅ attribute'lara erişimi denetlemek
# ✅ veri validasyonu uygulamak
# ✅ sadece okunabilir/silinemez/yazılamaz özellikler oluşturmak
# ✅ modern, temiz API'ler tanımlamak

# ------------------------------------------------------
# 🔸 Kullanım Alanları:
# ------------------------------------------------------
# - ORM yapıları (Django model.field)
# - property kullanımı
# - özel cache’li özellik tanımlamaları
# - erişim loglama
# - API koruma/masking

# ======================================================
# ✅ ÖRNEK: CLASS → property + setter + deleter
# ======================================================

class Kisi:
    def __init__(self, ad):
        self._ad = ad

    @property
    def ad(self):
        # ✅ __get__ -> getter
        return self._ad

    @ad.setter
    def ad(self, yeni_deger):
        # ✅ __set__ -> setter
        if not isinstance(yeni_deger, str):
            raise ValueError("Ad bir string olmalıdır.")
        self._ad = yeni_deger

    @ad.deleter
    def ad(self):
        # ✅ __delete__ -> deleter
        print("Ad siliniyor...")
        del self._ad


# ======================================================
# 🔍 KULLANIM:
# ======================================================

k = Kisi("Ali")
print(k.ad)          # 🔹 __get__ çalışır → getter
k.ad = "Veli"        # 🔹 __set__ çalışır → setter
del k.ad             # 🔹 __delete__ çalışır → deleter

# ======================================================
# 🔀 ALTERNATİF: property olmadan benzer yapı mümkün mü?
# ======================================================

class Kisi2:
    def __init__(self, ad):
        self._ad = ad

    def get_ad(self):
        return self._ad

    def set_ad(self, deger):
        self._ad = deger

    ad = property(get_ad, set_ad)

# ⚠️ Ancak bu yapı .deleter desteklemez + zincirleme (getter().setter()) yapı kurulamaz
# Modern Python'da `@property` yapısı hem daha okunabilir hem daha güçlüdür.
