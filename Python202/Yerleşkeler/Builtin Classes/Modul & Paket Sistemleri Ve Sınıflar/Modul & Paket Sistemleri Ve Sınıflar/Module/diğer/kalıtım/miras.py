
# -----------------------------------------------------------------------------
# 🔍 PYTHON'DA ModuleType SINIFI – DETAYLI AÇIKLAMA ve UYGULAMA
# -----------------------------------------------------------------------------

# --------------------------------------------------------------------
# 📘 1. TEMEL TANIM:
# --------------------------------------------------------------------
# - Python'da her modül (örn. import edilen .py dosyası), aslında `types.ModuleType` sınıfının bir örneğidir.
# - Bu sınıf, `types` modülünün içinde tanımlanmıştır.
# - Dolayısıyla her `.py` dosyası belleğe yüklendiğinde, onun için bir `ModuleType` nesnesi oluşur.

# --------------------------------------------------------------------
# 🧱 2. ModuleType NASIL BİR NESNE OLUŞTURUR?
# --------------------------------------------------------------------
# - __name__: Modülün adı
# - __doc__: Modülün dokümantasyonu (modül seviyesindeki docstring)
# - __dict__: Modülün namespace sözlüğü
# - (Daha sonra atananlar): __file__, __package__, __loader__, __spec__

# ⚠️ Bunların çoğu, `importlib` sistemi tarafından yükleme sırasında `setattr` ile atanır.

# --------------------------------------------------------------------
# 🔧 3. ModuleType NASIL KULLANILIR?
# --------------------------------------------------------------------
# - Yeni modüller yaratmak (örneğin dinamik olarak)
# - Modül davranışlarını özelleştirmek (örneğin lazy import, özel __getattr__)
# - import mekanizmasını değiştiren özel sistemlerde

# --------------------------------------
# 🧩 Ama Önemli Bir Fark:
# --------------------------------------
# ➤ Normal `import` ile gelen modüller → CPython tarafından C diliyle optimize edilmiş özel yapılardır.
#     - Bu yüzden bu modüllerde `__getattribute__` çalışmaz.
#     - Yalnızca PEP 562 sonrası `__getattr__` desteklenir (modül düzeyinde).
#
# ➤ Ama biz `ModuleType`'dan türeyerek bir **custom sınıf** oluşturduğumuzda:
#     - Artık bu nesne Python sınıfı gibi davranır.
#     - `__getattribute__`, `__getattr__`, `__dir__` gibi tüm özel metodlar çağrılabilir.
#     - Bu yüzden davranışı tamamen kontrol edebiliriz.

# --------------------------------------
# 🎯 Kullanım Alanları:
# --------------------------------------
# ✅ Lazy import (tembel modül yükleme)
# ✅ Bazı attribute’ları dinamik veya koşullu sağlama
# ✅ Modül davranışını loglama / izleme (debug için)
# ✅ `__dir__` ile IDE/autocomplete görünürlüğünü artırmak
# ✅ Versiyon uyumluluğu için backward-compat özellikleri eklemek
# ✅ Gelişmiş API yapıları sağlamak (Flask, Django tarzı modüler sistemler)

# --------------------------------------
# 🌍 Gerçek Dünya Senaryoları:
# --------------------------------------
# 📌 NumPy gibi büyük modüller → bazı alt modülleri sadece ihtiyaç anında yükler
# 📌 Flask ve Django → modül düzeyinde API'leri `__getattr__` ile dinamik sunar
# 📌 Google iç sistemleri → sandbox edilmiş modülleri `ModuleType` mirasıyla sınırlar
# 📌 TensorFlow gibi dev framework'ler → yalnızca kullanılan modülleri belleğe alır

# --------------------------------------------------------------------
# 🧠 4. ModuleType'dan KALITIM ALMA
# --------------------------------------------------------------------
# ✅ ModuleType'dan kalıtım almak, modül gibi davranan özel nesneler üretmeyi sağlar.
# ✅ Bu sayede modüllerde tembel yükleme, özel hata kontrolü, attribute saklama gibi özellikler eklenebilir.

# --------------------------------------------------------------------
# 🧪 5. KODSAL TEMSİL – ModuleType'ın __init__ METODU
# --------------------------------------------------------------------

class ModuleType:
    def __init__(self, name: str, doc: str | None = None) -> None:
        self.__name__ = name         # Modül adı
        self.__doc__ = doc           # Modül dokümantasyonu
        # __dict__ varsayılan olarak sağlanır
        # Diğer özellikler (örneğin __file__) daha sonra atanır


# --------------------------------------------------------------------
# 🧪 6. ÖRNEK: ModuleType’dan MİRAS ALAN ve ALMAYAN SINIFLAR
# --------------------------------------------------------------------

import types
import sys

# ✅ DOĞRU KULLANIM – Miras alan, uyumlu özel modül sınıfı
class MyLazyModule(types.ModuleType):
    def __init__(self, name):
        super().__init__(name)
        self._lazy_cache = {}

    def __getattr__(self, name):
        if name == "np":
            print("Lazy importing numpy...")
            import numpy as np
            self._lazy_cache[name] = np
            return np
        raise AttributeError(f"{name} bulunamadı")

    def __dir__(self):
        return super().__dir__() + ["np"]


# ❌ HATALI veya RİSKLİ KULLANIM – Miras almıyor, temel özellikleri elle tanımlıyor
class BrokenModule:
    def __init__(self, name):
        self.__name__ = name
        self.__doc__ = "Manual doc"
        self.__dict__ = {}  # elle müdahale
        self.some_attr = 123

# ⚠️ Bu sınıf bir modül gibi davranmaz. import mekanizması bunu tanımaz.
# sys.modules["mod"] = BrokenModule() dersen sistemin birçok kısmı bozulabilir.


# ✅ ALTERNATİF – Miras almadan, ama dikkatlice oluşturulmuş (çok nadir gerekebilir)
class ManualCompatibleModule:
    def __init__(self, name):
        self.__name__ = name
        self.__doc__ = "Modül gibi davranmaya çalışıyor"
        self.__dict__ = {"hello": "world"}

    def __getattr__(self, name):
        return self.__dict__.get(name, f"{name} bulunamadı")


# --------------------------------------------------------------------
# 🧪 7. sys.modules İLE KULLANIM
# --------------------------------------------------------------------

# Bu modül dosyasının kendi sınıfını değiştirelim
sys.modules[__name__].__class__ = MyLazyModule

# Artık bu modül üstünden np kullanılınca numpy sadece o zaman içe aktarılır:
# Örn: mymodule.np.array([...])
