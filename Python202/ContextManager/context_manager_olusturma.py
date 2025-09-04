# ----------------------------------------------------------------------------------
# 🧱 1. AMAÇ NEDİR? — CONTEXT MANAGER NEDEN TANIMLIYORUZ?
#
# Bir context manager (bağlam yöneticisi), belirli bir kaynağı veya işlemi
# "giriş-çıkış" mantığıyla kontrol altına almak için kullanılır.
#
# Örneğin:
# - Dosya açmak ve işlem sonunda kapatmak
# - Zaman ölçümü yapmak
# - Hataları loglamak
# - Bir işlemi geçici olarak yapmak, sonra eski haline dönmek
#
# Biz de şimdi bu yapıyı sınıf bazlı bir context manager yazarak sıfırdan tanımlayacağız.
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# 🧰 2. GEREKLİ YAPI: BİR SINIF OLUŞTURMALIYIZ
#
# `with` ifadesi, sadece "context manager" protokolünü uygulayan nesneleri kabul eder.
#
# Bu nedenle bir context manager tanımlamak istiyorsak, özel bir sınıf yazmalıyız.
# Bu sınıf, iki temel DUNDER (double underscore) metoda sahip olmalıdır:
#
#     1. __enter__(self)
#     2. __exit__(self, exc_type, exc_val, exc_tb)
#
# Bu metotlar, Python’un "context management protocol" adını verdiği özel kurallar bütününü temsil eder.
# ----------------------------------------------------------------------------------

class BasitContext:

    # ------------------------------------------------------------------------------
    # 🔑 __enter__ METODU
    #
    # - Bu metod, `with` bloğuna girildiğinde otomatik olarak çağrılır.
    # - Genellikle kullanılacak kaynağı başlatır, hazırlar.
    # - İstenirse `as` anahtar kelimesine atanacak nesneyi döndürebilir.
    #
    # Python: with BasitContext() as x: → x = self.__enter__()
    # ------------------------------------------------------------------------------
    def __enter__(self):
        print("⏳ __enter__ çağrıldı: Kaynak hazırlanıyor...")
        return self  # `as` ile kullanılacak nesne


    # ------------------------------------------------------------------------------
    # 🧹 __exit__ METODU
    #
    # - Bu metod, `with` bloğundan çıkıldığında otomatik olarak çağrılır.
    # - `__enter__` tarafından açılan kaynaklar burada kapatılır veya temizlenir.
    # - Hata (exception) oluşsa bile __exit__ kesinlikle çalıştırılır.
    #
    # Parametreler:
    # - exc_type : Oluşan hatanın tipi (örnek: ValueError)
    # - exc_val  : Hata mesajı ya da örneği (örnek: ValueError("hata oldu"))
    # - traceback: Hatanın oluştuğu yerin izleri
    #
    # Eğer bu metod "True" dönerse, Python hatayı yutmuş sayar (propagate etmez).
    # ------------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("✅ __exit__ çağrıldı: Kaynak kapatılıyor...")

        if exc_type:
            print(f"⚠️ Hata oluştu: {exc_type.__name__}: {exc_val}")
        else:
            print("🚀 with bloğu başarıyla tamamlandı.")

        # True dönersek hata bastırılır, False dönersek Python hatayı normal şekilde fırlatır
        return False



# ----------------------------------------------------------------------------------
# 🧪 3. KULLANIM: `with` İFADESİYLE BU SINIFI KULLANMAK
#
# `with BasitContext()` ifadesi çalıştığında:
#
# 1. __enter__ metodu çağrılır
# 2. with bloğunun içi çalıştırılır
# 3. __exit__ metodu çağrılır
#
# Böylece hem kaynak açma/temizleme işlemleri otomatikleşmiş olur
# hem de kodumuz sade, okunabilir ve hata güvenli olur.
# ----------------------------------------------------------------------------------

with BasitContext() as ctx:
    print("🧪 with bloğu içindeyiz: kaynak aktif")
    # Burada bir hata oluşsa bile __exit__ kesinlikle çalışacaktır.
    # raise ValueError("Test hatası")  # denemek istersen bunu açabilirsin

print("🌍 with bloğu dışında: kaynak kapatıldı")

# ----------------------------------------------------------------------------------
# 🧩 `with` İFADESİNİN ARKA PLANDA NASIL ÇALIŞTIĞI - AÇILIM
#
# Bu açıklamalar, şu yapı üzerinden yapılmıştır:
#
#   with BasitContext() as x:
#       ... with bloğu ...
#
# Bu ifade Python tarafından aşağıdaki adımlar hâlinde yorumlanır:
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# ✅ 1. SINIF ÖRNEĞİ OLUŞTURULUR
#
# İlk adımda, with ifadesine verilen sınıf çağrılır.
# Bu aslında normal bir sınıf oluşturma işlemidir.
#
# BasitContext() → bir nesne (örnek) oluşturur
# Bu nesne geçici olarak bir değişkene atanır. Örnek: obj = BasitContext()
# ----------------------------------------------------------------------------------
obj = BasitContext()  # with bloğundaki nesne örneği oluşturuluyor

# ----------------------------------------------------------------------------------
# 🔓 2. __enter__() METODU ÇAĞRILIR
#
# Python, context manager protokolü gereği `obj.__enter__()` metodunu çağırır.
# Bu metod genellikle kaynağı hazırlar.
# Bu metodun döndürdüğü değer, "as" anahtar kelimesinden sonraki değişkene atanır.
#
# Örneğin:
#   with BasitContext() as x:  →  x = obj.__enter__()
# ----------------------------------------------------------------------------------
x = obj.__enter__()  # genelde self döner, ama her şey olabilir

# ----------------------------------------------------------------------------------
# 🔁 3. with BLOĞU ÇALIŞTIRILIR
#
# Artık kaynak hazırlanmıştır.
# Python, `with` bloğunun içindeki kodları sırasıyla çalıştırır.
# Bu blokta hata olup olmaması önemli değildir, __exit__ mutlaka çağrılacaktır.
# ----------------------------------------------------------------------------------
try:
    # ← işte burası with bloğunun içi
    # Python burada kullanıcı kodunu çalıştırır
    ...

# ----------------------------------------------------------------------------------
# 🧹 4. __exit__() METODU ÇAĞRILIR (HER DURUMDA)
#
# Python, with bloğundan çıkıldığında otomatik olarak `__exit__()` metodunu çağırır.
# Bu metodun görevi kaynakları kapatmak, temizlik yapmak ve gerekiyorsa hataları bastırmaktır.
#
# Eğer with bloğunda bir hata oluşmuşsa, bu hatanın detayları `__exit__` metoduna verilir:
#   - exc_type  → hata tipi
#   - exc_value → hata mesajı
#   - traceback → hata yığını
#
# Bu metod "True" dönerse, Python hatayı bastırır.
# "False" dönerse, hata dışarıya fırlatılır.
# ----------------------------------------------------------------------------------
finally:
    obj.__exit__(exc_type, exc_value, traceback)
