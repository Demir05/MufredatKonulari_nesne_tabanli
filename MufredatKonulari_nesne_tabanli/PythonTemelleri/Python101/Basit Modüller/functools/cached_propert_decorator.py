# --------------------------------------------------------------------------------------
# 📌 functools.cached_property (Python 3.8+)
# --------------------------------------------------------------------------------------
# @cached_property, bir instance method’un sadece ilk çağrılışında hesaplanmasını ve
# sonucu instance’ın __dict__’ine kaydedip, sonraki erişimlerde yeniden hesaplanmadan
# direkt bu değerin dönmesini sağlar.
#
# Bu decorator bir descriptor’dür ve sınıf seviyesinde tanımlanır.
# En sık kullanımı:
#   - Hesaplanması pahalı, ama sabit kalan (immutable) değerleri
#     bir kez hesaplayıp cachelemek içindir.
#   - Property gibi çalışır, ama lazy + cache desteklidir.
#
# --------------------------------------------------------------------------------------
# 🔧 Kullanım Şekli:
# class MyClass:
#     @cached_property
#     def value(self):
#         print("hesaplandı")
#         return expensive_computation()
#
# obj = MyClass()
# obj.value  # ilk çağrıda hesaplanır
# obj.value  # sonraki çağrılarda cached değer kullanılır
# --------------------------------------------------------------------------------------
# ⚙️ Çalışma Mekanizması:
# 1. Sınıf tanımı okunurken cached_property(func) çağrılır.
# 2. Bu bir descriptor objesi döner (yani class attribute olarak kalır).
# 3. instance.value erişildiğinde __get__ çağrılır:
#     - Eğer value daha önce hesaplanmadıysa:
#         - func(self) çağrılır
#         - __dict__ içine {'value': sonuç} eklenir
#     - Eğer zaten hesaplandıysa:
#         - __dict__['value'] döndürülür
# 4. Böylece method her instance için sadece 1 kez hesaplanmış olur.
#
# --------------------------------------------------------------------------------------
# 🧠 @cached_property vs @property:
# - @property: her çağrıldığında methodu çalıştırır (hesaplama tekrarlanır)
# - @cached_property: sadece ilk seferde çalışır, sonra cache’den döner
#
# --------------------------------------------------------------------------------------
# ❗ Dikkat Edilmesi Gerekenler:
# - Değişken hesaplamaları için değil, sabit kalan sonuçlar için uygundur.
# - Instance mutable değilse (örn: __dict__ yoksa), çalışmaz.
#   Özellikle __slots__ kullanılıyorsa, __dict__ kaldırıldığı için:
#       -> AttributeError fırlatılır
#
#   Örnek:
#   class A:
#       __slots__ = ('x',)  # __dict__ yok!
#       @cached_property
#       def val(self):
#           return self.x * 2
#   -> AttributeError: 'A' object has no attribute '__dict__'
#
# - Eğer __slots__ kullanmak istiyorsan, şunu ekleyerek çalıştırabilirsin:
#       __slots__ = ('x', '__dict__')
#
# --------------------------------------------------------------------------------------
# ⚠️ @cached_property Cache Kullanımı:
# - Cache olarak __dict__ kullanır (yani ayrı bir bellek yapısı yoktur).
# - `lru_cache()` gibi bir otomatik sınırlandırma veya timeout sistemi yoktur.
# - Belleği çok kullanan objelerde, manuel olarak:
#       del obj.attr  # ile temizleme yapılabilir.
#
# --------------------------------------------------------------------------------------
# 👀 Kullanım Alanları:
# - Regex derleyip saklamak
# - API bağlantısı veya yapılandırma gibi “bir kez kurulan” yapılar
# - Lazy initialization (tembel başlatma) gerektiren property’ler
#
# --------------------------------------------------------------------------------------
# 🤓 Teknik Not:
# - __call__ tanımlı değildir; bu bir decorator function gibi kullanılmaz.
# - Sadece class property olarak (method üstü) kullanılabilir.
# - Bir instance için sadece bir kez hesaplama yapılır.
# - Sadece __get__ tanımlıdır, __set__ ve __delete__ tanımlı değildir.
#
# --------------------------------------------------------------------------------------
# 🎯 Örnek:
from functools import cached_property

class DataFetcher:
    def __init__(self, source):
        self.source = source

    @cached_property
    def data(self):
        print("📡 Veriler alınıyor...")
        return self.get_data()

    def get_data(self):
        return f"{self.source} -> veriler"

df = DataFetcher("server1")
print(df.data)  # ilk erişimde çalışır
print(df.data)  # cache'den alınır
# --------------------------------------------------------------------------------------
