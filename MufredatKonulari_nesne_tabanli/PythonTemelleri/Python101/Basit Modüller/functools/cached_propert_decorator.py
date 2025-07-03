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

# ✅ Neden `cached_property`'de `typed` gibi bir parametreye gerek yok?

# 1. `lru_cache` gibi dekoratörler bir fonksiyonu her çağrıda çalıştırır.
#    - Bu yüzden, aynı argümanların farklı tiplerde verilmesi (1 vs 1.0) cache anahtarını etkileyebilir.
#    - Bu durumlarda `typed=True` ile argüman tiplerini dikkate alabiliriz.

# 2. `cached_property` ise bir method'dur, argüman almaz, sadece `self`'i alır.
#    - Dolayısıyla, burada yapılan cacheleme işleminde `self`'in hangi attribute üzerinden işlem yapıldığı önemlidir.
#    - Cache anahtarı olarak fonksiyonun adı (property adı) kullanılır ve sonuç instance.__dict__[name] içine yazılır.

# 3. Örneğin:
#     class A:
#         @cached_property
#         def result(self):  # sadece self'e bağlı
#             return expensive_computation(self.data)

#     a = A()
#     a.result  # burada argüman yok, dolayısıyla hash veya typed kontrolü yoktur.

# 4. Bu sebeple:
#     - cached_property, her instance için **tek bir cacheleme** yapar.
#     - Aynı metoda farklı argümanlar verilme durumu **zaten mümkün değildir**.
#     - Dolayısıyla `typed` gibi bir parametre burada anlamsız olur.

# ❗ Ve evet: descriptor ismi (attribute adı) geçerli bir Python identifier olmalıdır,
#    çünkü sınıf tanımında bir `class attribute` olarak tanımlanır, örneğin: `value = cached_property(...)`
#    Bu da `__set_name__` metodunda name olarak gelir ve instance.__dict__[name] olarak kullanılır.


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
import functools
from functools import cached_property, wraps
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
print(df.__dict__)
print(df.data)  # ilk erişimde çalışır
print(df.data)  # cache'den alınır
print(df.__dict__) # 'data': 'server1 -> veriler'}
# --------------------------------------------------------------------------------------


class MyCachedProperty:

    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self.intance_attribute_name = name

    def __get__(self, instance, owner):

        instance.__dict__[self.intance_attribute_name]= self.func(instance)
        return instance.__dict__[self.intance_attribute_name]

class A:

    def __init__(self, data):
        self.data = data

    @MyCachedProperty
    def deneme(self):
        return f"{self.data} -> TAMAM"


a = A("dcvbm")
print(a.__dict__) # {'data': 'dcvbm'}
print(a.deneme) # dcvbm -> TAMAM
print(a.__dict__) # {'data': 'dcvbm', 'deneme': 'dcvbm -> TAMAM'}

del a.deneme # cached_property'de temizlik böyle yapılır
print(a.__dict__) # {'data': 'dcvbm'}


