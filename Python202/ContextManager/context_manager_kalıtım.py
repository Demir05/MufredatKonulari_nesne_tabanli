# =============================================================================
# 📘 Context Manager Mirası: Teorik Tanım
# =============================================================================
# Python'da context manager, __enter__ ve __exit__ metodlarını tanımlayan sınıflardır.
# Bu sınıflar, with bloğu içinde kaynak yönetimi, hata kontrolü ve temizlik işlemleri sağlar.
#
# Miras alma (inheritance), bir context manager sınıfının davranışlarını başka bir sınıfa
# aktarmak için kullanılır. Alt sınıf (child class), üst sınıfın (base class) __enter__ ve
# __exit__ metodlarını devralabilir, isterse bunları override ederek kendi bağlamını tanımlayabilir.
#
# Miras sayesinde:
# - Ortak davranışlar tekrar yazılmadan kullanılabilir.
# - Alt sınıflar sadece ihtiyaç duydukları kısmı özelleştirir.
# - Kod daha modüler, test edilebilir ve genişletilebilir hale gelir.
#
# Context manager mirası, özellikle loglama, zamanlayıcı, dosya yönetimi, bağlantı kontrolü
# gibi sistemsel işlemlerde yaygın olarak kullanılır.

# =============================================================================
# 🧪 Örnek: Zamanlayıcı Context Manager, loglama davranışını miras alır
# =============================================================================

import time

class BaseContext:
    def __enter__(self):
        print("Bağlam başlatıldı.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Hata: {exc_type.__name__} → {exc_value}")
        else:
            print("Bağlam başarıyla kapatıldı.")
        return False  # Hatalar dışarı fırlatılır

class TimerContext(BaseContext):
    def __enter__(self):
        self.start = time.time()
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        self.duration = self.end - self.start
        print(f"Geçen süre: {self.duration:.4f} saniye")
        return super().__exit__(exc_type, exc_value, traceback)

# =============================================================================
# ✅ Kullanım
# =============================================================================

with TimerContext():
    print("İşlem başlıyor...")
    time.sleep(1.2)
    print("İşlem tamamlandı.")

# =============================================================================
# 🎯 Avantajlar
# =============================================================================
# - BaseContext sınıfı loglama ve hata yönetimini soyutlar.
# - TimerContext sadece zaman ölçümünü ekler, temel davranışı bozmadan genişletir.
# - super() ile üst sınıfın davranışı korunur.
# - Kod daha sade, modüler ve tekrar kullanılabilir hale gelir.
