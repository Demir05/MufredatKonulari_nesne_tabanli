# ==========================================================
# 📘 TEMEL TASARIM PRENSİPLERİ — DECORATOR & CLASS STRUCTURE
# ==========================================================

# 🔹 1. SINIF DIŞINDAKİ LOJİĞİN YERİ:
# -----------------------------------
# "Bir sınıfın içinde sadece o sınıfın yapısını ve davranışlarını tanımlayan kod olmalı."
# 
# ⛔ YANLIŞ: Sınıf gövdesi içinde for döngüleriyle veri işleme, metot silme, dictionary manipülasyonu
# ✅ DOĞRU: Bu işlemleri sınıf dışına almak, hem okunabilirlik hem de sorumluluk ayrımı açısından daha doğrudur.
#
# ➕ Faydaları:
# - Sınıf tanımı sade kalır
# - Hatalar daha kolay izlenir
# - Sorunlar separation of concerns ilkesine göre ayrılır
#
# 💡 Unutma: class blokları `locals()` ortamında çalışır, dışarıdan değişken erişimi sınırlıdır

# 🔹 2. DECORATOR NESNELERİ — ÇAĞRILABİLİRLİK FARKINDALIĞI
# ---------------------------------------------------------
# Python'da bir decorator:
#   @mydecorator
# ...şu hale gelir:
#   MyClass = mydecorator(MyClass)
#
# Bu şu anlama gelir:*

# ✅ Decorator aslında sadece bir çağrılabilir fonksiyondur
# ✅ Fonksiyon gibi de çağrılabilir: mydecorator(MyClass)
# ✅ Bu yüzden:
#   - Sınıf / fonksiyon süsleme dışında
#   - Genişletilebilir bir API gibi kullanılabilir
#
# 🌀 Örnek:
#   class my_decorator:
#       def register(...): ...
#       def __call__(...): ...
#
# Bu yapılar hem süsleme (syntactic sugar) sağlar, hem de gerektiğinde açık fonksiyonel kullanımı mümkün kılar

# 🔹 3. ENTEGRE YAPI: DESCRIPTOR + DECORATOR + DISPATCH
# ------------------------------------------------------
# Çok yönlü decorator'ler oluşturmak için:
# - __get__ (descriptor) → attribute gibi erişim
# - __call__ (decorator/fonksiyon) → callable gibi kullanım
# - .register() gibi özel metodlar → dispatch kontrolü
#
# ✅ Bu hibrit yapı Python'da güçlü bir API deneyimi sunar
# ✅ Kütüphane yazarken veya DSL (domain-specific language) inşa ederken büyük avantaj sağlar

# ==========================================================
