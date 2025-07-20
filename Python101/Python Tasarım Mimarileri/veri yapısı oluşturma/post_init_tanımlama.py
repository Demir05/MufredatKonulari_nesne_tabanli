# 🔖 KONU: __post_init__() — Yardımcı Başlatıcı Fonksiyon
#
# 📘 TANIM:
# __post_init__(), Python'da genellikle sınıfın __init__ metodundan sonra çağrılan özel bir yardımcı fonksiyondur.
# Amacı, nesne oluşturulduktan sonra yapılması gereken ek işlemleri, düzenlemeleri, kontrolleri ayrı bir yere taşımaktır.
# Bu yöntem, özellikle sınıfın başlatma (initialization) işlemleri karmaşıklaşmaya başladığında tercih edilir.
#
# 🧠 NEDEN KULLANILIR?
# - __init__ metodunu sade ve okunabilir tutmak
# - Veri doğrulama, dönüştürme, hesaplama gibi iş mantığını ayırmak
# - Kodun daha modüler, test edilebilir ve anlaşılır olması
#
# ✅ NE ZAMAN TERCİH EDİLMELİ?
# - Sınıfın başlatma süreci birkaç adımdan oluşuyorsa (örneğin: validasyon + transformasyon)
# - __init__ içinde çok fazla işlem yapılıyorsa
# - Kod okunabilirliğini artırmak istiyorsan
# - dataclass kullanıyorsan (otomatik çağrılır)
#
# 🚫 NE ZAMAN TERCİH EDİLMEMELİ?
# - Sınıf sadece veri taşıyorsa (örneğin 1-2 attribute'luk basit sınıflar)
# - Başlatma işlemi çok basitse
# - Performans kritik yerlerde gereksiz soyutlama yapmak istemiyorsan

# 🎯 ÖRNEK:

class Kullanici:
    def __init__(self, isim, email):
        self.isim = isim
        self.email = email
        self.__post_init__()  # 👈 Tüm ek işlemler, init sonrası burada yapılır

    def __post_init__(self):
        # 🔧 E-posta doğrulama işlemi
        self.validate_email()

        # 🔧 İsim düzenleme
        self.isim = self.isim.capitalize()

        # 🔧 Domain bilgisi çıkarımı
        self.domain = self.email.split("@")[1]

    def validate_email(self):
        if "@" not in self.email:
            raise ValueError("Geçersiz email adresi")

# 🧪 Kullanım:
k = Kullanici("ahmet", "ahmet@example.com")
print(k.isim)    # Ahmet
print(k.domain)  # example.com


