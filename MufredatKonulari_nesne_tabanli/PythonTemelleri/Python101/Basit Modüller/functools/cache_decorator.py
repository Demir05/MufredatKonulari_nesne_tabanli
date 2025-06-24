from functools import cache

# @cache, Python 3.9+ sürümünde gelen bir decorator’dür.
# Amacı: Aynı argümanlarla çağrılan saf (pure) fonksiyonların çıktısını hafızada saklamak (memoization).
# Bu sayede tekrar aynı argümanlarla çağrıldığında hesaplama yapılmaz, doğrudan önbellekten (cache) sonuç döner.
# @lru_cache(maxsize=None) ile %100 aynıdır ama isim olarak daha sade ve "okunabilir" yapılmıştır.

# ❗ Pure (saf) fonksiyon nedir?
# - Girdi aynıysa çıktı daima aynıdır.
# - Yan etkisi (dosya yazmak, global değişken değiştirmek) yoktur.
# Örnek: fibonacci, matematiksel hesaplamalar, string manipülasyonları

# @cache sınırsız büyür. Yani:
# - Eski sonuçlar RAM’den silinmez.
# - Bu yüzden, bellek yönetimi yapmaz.
# - Büyük veri setlerinde veya çok fazla farklı argümanla çağrılan fonksiyonlarda dikkatli kullanılmalıdır.

# ➕ Avantajları:
# - Çok hızlıdır. Hash tabanlıdır.
# - Kurulumu, kullanımı aşırı basittir.
# - Küçük argüman alanı olan fonksiyonlarda oldukça etkilidir.

# ➖ Dezavantajları:
# - Bellek dostu değildir.
# - Sadece pure fonksiyonlarda işe yarar.
# - Kodu ilk bakışta daha karmaşık gösterebilir. Bu, bazı Python geliştiricileri tarafından sadelik (Zen of Python) ilkesine aykırı bulunabilir.

# ———————————————
# ÖRNEK:

@cache
def square(n):
    print(f"Hesaplanıyor: {n}")
    return n * n

print(square(10))  # hesaplanır
print(square(10))  # cache’den gelir
print(square(5))   # hesaplanır
print(square(5))   # cache’den gelir

# İlk çağrılar dışında, fonksiyon gövdesine girilmez. RAM’den sonuç döner.

# ———————————————
# İPUCU:
# @cache = @lru_cache(maxsize=None)
# Ama `@cache` daha okunur ve çağdaş görünür. Yeni projelerde tercih edilebilir.

# ———————————————
# ÖZET:
# @cache, basit, hızlı ama sınırsız büyüyen bir memoization tekniğidir.
# Python’un “sadelik güzeldir” ilkesine göre tartışmalı olabilir ama performans ve sadelikte pratik bir tercih sunar.
