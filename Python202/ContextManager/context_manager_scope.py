# =============================================================================
# 📘 with Bloğu: Frame ve Scope Davranışı
# =============================================================================
# Python'da with bloğu, context manager protokolünü tetikleyen bir kontrol yapısıdır.
# Ancak with bloğu kendi başına yeni bir frame (çağrı çerçevesi) oluşturmaz.
# Frame sadece fonksiyon, jeneratör, sınıf gibi yapılarla oluşur.
#
# with bloğu içindeki değişkenler, bulunduğu yerin scope'una göre tanımlanır:
# - Eğer with bloğu bir fonksiyon içindeyse → isimler local scope'ta tanımlanır.
# - Eğer with bloğu modül seviyesindeyse → isimler global scope'ta tanımlanır.
#
# with bloğu içindeki işlemler, context manager'ın __enter__ ve __exit__ metodları
# arasında çalışır ama bu işlemler için ayrı bir execution frame yaratılmaz.

# =============================================================================
# 🧪 Örnek: Global Scope'ta with Bloğu
# =============================================================================

class Demo:
    def __enter__(self):
        print("⏳ __enter__")
        return "demir"

    def __exit__(self, exc_type, exc_val, tb):
        print("✅ __exit__")

with Demo() as x:
    print(x)  # x burada global scope'ta tanımlanır

# =============================================================================
# 🧪 Örnek: Fonksiyon İçinde with Bloğu
# =============================================================================

def run():
    with Demo() as y:
        print(y)  # y burada run() fonksiyonunun local scope'undadır

run()

# =============================================================================
# ✅ Özet Avantajlar ve Davranışlar
# =============================================================================
# ✔ with bloğu ayrı bir frame oluşturmaz → performans açısından hafiftir.
# ✔ İsimler bulunduğu bağlama göre tanımlanır → global veya local olabilir.
# ✔ __enter__ ve __exit__ metodları çağrılır → kaynak yönetimi garanti edilir.
# ✔ Kodun semantiği sadeleşir → try/finally ihtiyacını ortadan kaldırır.

# =============================================================================
# 🎯 Sonuç
# =============================================================================
# with bloğu, context manager protokolünü çalıştıran ama ayrı bir çağrı çerçevesi
# oluşturmayan bir yapıdır. İsimlerin scope'u bulunduğu bağlama göre belirlenir.
# Bu yapı, kaynak yönetimini sade ve güvenli şekilde gerçekleştirmek için idealdir.
