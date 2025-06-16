# -----------------------------------------------------------------------
# @classmethod Decorator'ü
# -----------------------------------------------------------------------

# @classmethod, sınıfın kendisini (class) parametre olarak alan özel bir metod türüdür.
# Bu metodlar, sınıf düzeyinde çalışır ve sınıfla ilgili işlemleri gerçekleştirmek için kullanılır.
# İlk parametresi geleneksel olarak "cls" olarak adlandırılır.

# -----------------------------------------------------------------------
# Neden Var? Amacı Nedir?
# -----------------------------------------------------------------------

# 1. Sınıf düzeyinde işlem yapmayı sağlar. Örnekten değil, doğrudan sınıfın kendisiyle ilgilidir.
# 2. Sınıfla ilgili konfigürasyon, durum ya da nesne yaratımı gibi işlemlerde kullanılır.
# 3. Alt sınıflar tarafından miras alındığında, cls parametresi sayesinde alt sınıfın kendisi ile çalışır.
#    Bu sayede "factory" gibi yapılar kurulabilir → esneklik ve yeniden kullanılabilirlik sağlar.
# 4. daha fazla kontrol sağlar şöyle düşün:
#   sınıftan bir örnek oluşturmayı bir fonksiyonla sağlıyorsun burda __init__() kullanmaktan daha fazla esnekliğe sahipsin çünkü ekstra bir katman oluşur bu katmanda;
#   input doğrulama, loglama, ön işlem/temizlik, varsayılanlar, hata yönetimi yapabilirsin 

# -----------------------------------------------------------------------
# Sözdizimi:

# class SınıfAdı:
#     @classmethod
#     def fonksiyon_adı(cls, ...):
#         ...
   # Bu bir sınıf metodudur, bu yüzden ilk parametresi "cls" olur
    # → "cls", metoda hangi sınıf üzerinden ulaşıldıysa **o sınıfı** temsil eder.
    # → tıpkı instance method'lardaki "self" gibi, ama "sınıf" için.
    # cls → örneğin Hayvan, Kedi, Kopek olabilir
        # bu sayede alt sınıf kendi "isim" değerini değiştirebilir

# Çağrılma:
# SınıfAdı.fonksiyon_adı(...)
# veya
# örnek.fonksiyon_adı(...)  → burada da cls, örneğin ait olduğu sınıfı temsil eder

# -----------------------------------------------------------------------
# Örnek:

class Araba:
    marka = "Renault"

    def __init__(self, model):
        self.model = model

    @classmethod
    def marka_degistir(cls, yeni_marka):
        cls.marka = yeni_marka

# Hem sınıf üzerinden hem örnek üzerinden çağrılabilir
Araba.marka_degistir("Toyota")
print(Araba.marka)  # → Toyota

a = Araba("Corolla")
a.marka_degistir("Honda")
print(Araba.marka)  # → Honda  (sınıfın tüm örnekleri etkilenir)

# -----------------------------------------------------------------------
# Teknik Detaylar:

# Sınıf tanımında:
# Araba.__dict__['marka_degistir'] → classmethod objesi
# Çağırıldığında:
# Araba.__dict__['marka_degistir'].__get__(None, Araba) → bound method döner
# Bu method, Araba sınıfını (cls) ilk argüman olarak alır.

# -----------------------------------------------------------------------
# @classmethod vs @staticmethod

# Ortak noktaları:
# - İkisi de örnek (self) almaz
# - Sınıfın kendisiyle ilgili fonksiyonları sınıf içinde tanımlamak için kullanılır

# Farkları:
# - @staticmethod: Ne sınıf ne de örnek bilgisi alır → bağımsız çalışır
# - @classmethod: Sınıf bilgisini (cls) alır → sınıf düzeyinde işlem yapar
# - @classmethod, genellikle factory method’lar ve sınıfı etkileyen işlemler için uygundur

# -----------------------------------------------------------------------
# Ne Zaman Kullanılır?

# - Sınıfa özel ayarlar/değişkenler üzerinde işlem yapılacaksa
# - Alt sınıflarda dinamik olarak işlem yapılması gerekiyorsa
# - Yeni nesne yaratımı için alternatif factory method oluşturulacaksa

# -----------------------------------------------------------------------
# Örnek: Factory Method

class Kitap:
    def __init__(self, isim, sayfa):
        self.isim = isim
        self.sayfa = sayfa

    @classmethod
    def dosyadan_olustur(cls, veri: str):
        isim, sayfa = veri.split(",")
        return cls(isim, int(sayfa))

k = Kitap.dosyadan_olustur("Python101,350")
print(k.isim, k.sayfa)  # → Python101 350


class Hayvan:
    isim = "Tanımsız"

    # Bu bir sınıf metodudur, bu yüzden ilk parametresi "cls" olur
    # → "cls", metoda hangi sınıf üzerinden ulaşıldıysa **o sınıfı** temsil eder.
    # → tıpkı instance method'lardaki "self" gibi, ama "sınıf" için.
    @classmethod
    def isim_ayarla(cls, isim):
        # cls → örneğin Hayvan, Kedi, Kopek olabilir
        # bu sayede alt sınıf kendi "isim" değerini değiştirebilir
        cls.isim = isim

# Alt sınıflar
class Kedi(Hayvan): pass
class Kopek(Hayvan): pass

# cls = Kedi → Kedi sınıfının "isim" attribute'u değişir
Kedi.isim_ayarla("Tekir")

# cls = Kopek → Kopek sınıfının "isim" attribute'u değişir
Kopek.isim_ayarla("Karabaş")

# Şimdi bakalım hangi sınıf ne olmuş:
print(Kedi.isim)     # Tekir
print(Kopek.isim)    # Karabaş
print(Hayvan.isim)   # Tanımsız (değişmedi!)