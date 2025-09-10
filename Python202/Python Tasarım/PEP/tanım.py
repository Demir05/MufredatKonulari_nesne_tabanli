# 📌 NEDİR?
# PEP = Python Enhancement Proposal
# Türkçesi: Python Geliştirme Önerisi
# Python diline yeni özellik, davranış veya süreç eklemek isteyenlerin yazdığı resmi teklif belgesidir.
# Hem teknik hem topluluk kararlarını içerir.

# 🧠 NEDEN VAR?
# Python’un gelişimini rastgele değil, kontrollü ve tartışmalı bir şekilde yürütmek için.
# Herkesin önerisini ortak bir formatta sunabilmesini sağlar.
# Dilin evrimini belgelendirir ve karar alma sürecini şeffaflaştırır.

# 🎯 AMACI NE?
# Yeni dil özellikleri (örneğin: type hints, async/await gibi) önermek
# Standart kütüphane değişikliklerini açıklamak
# Topluluk süreçlerini (örneğin: sürüm döngüsü, çekirdek ekip yapısı) tanımlamak
# Python’un geleceğini planlamak ve tartışmak

# 📜 TARİHÇESİ
# İlk PEP: PEP 0 — PEP’lerin listesini tutar
# En bilinen erken PEP: PEP 8 — Kodlama standartları
# Guido van Rossum (Python’un yaratıcısı) uzun süre PEP’leri onaylayan kişiydi (BDFL)
# Artık PEP’ler PEP Editor’lar ve Steering Council tarafından yönetiliyor

# 🗂️ PEP KATEGORİLERİ
# 1. Standart PEP (Standard Track)
#    - Dil özellikleri, kütüphane değişiklikleri, implementasyon detayları
#    - Örnek: PEP 484 (type hints), PEP 572 (walrus operatörü)

# 2. Bilgilendirici PEP (Informational)
#    - Tavsiye niteliğinde, teknik olmayan rehberler
#    - Örnek: PEP 8 (kodlama stili), PEP 20 (Zen of Python)

# 3. Süreç PEP’i (Process)
#    - Python topluluğunun nasıl çalıştığını tanımlar
#    - Örnek: PEP 13 (Steering Council yapısı), PEP 8016 (yönetim modeli)

# 🔍 BONUS: PEP numaraları kronolojik değil, mantıksal dağılır.
# Örneğin PEP 302 → import sistemi için, PEP 420 → namespace paketler, PEP 451 → ModuleSpec yapısı

# ✅ SONUÇ
# PEP’ler Python’un gelişim yol haritasıdır.
# Kod yazarken karşılaştığın davranışların çoğu bir PEP’in sonucudur.
# Ezberlemek gerekmez — doğru anda doğru PEP’i tanımak yeterlidir.

# 📘 PEP ve Typing İlişkisi Tablosu (Yorum Satırı Formatında)
# ┌────────┬────────────────────────────┬─────────────────────────────┬────────────────────────────────────────────────────────────┐
# │ PEP No │ Konu                       │ Etki                        │ Açıklama                                                   │
# ├────────┼────────────────────────────┼─────────────────────────────┼────────────────────────────────────────────────────────────┤
# │ PEP 8  │ Kod stili                  │ Biçimsel tutarlılık         │ Okunabilirlik ve sürdürülebilirlik için stil rehberi       │
# │ PEP 257│ Docstring kuralları        │ Açıklanabilirlik            │ Fonksiyon, sınıf ve modül açıklamaları için standart       │
# │ PEP 20 │ Zen of Python              │ Felsefi rehberlik           │ Sadelik, açıklık, modülerlik gibi tasarım ilkeleri         │
# │ PEP 484│ Type Hinting               │ Statik tip sistemi          │ typing modülünün temeli, veri akışını açıkça tanımlar      │
# │ PEP 526│ Variable annotations       │ Değişken tipi belirtimi     │ `x: int = 5` gibi değişkenlere doğrudan tip ekleme         │
# │ PEP 585│ Yerleşik tipler            │ typing sadeleşmesi          │ `list[int]`, `dict[str, str]` gibi native kullanım          │
# │ PEP 586│ Literal types              │ Sabit değer sınırlaması     │ `Literal["aktif", "pasif"]` gibi sabit değerlerin kontrolü │
# │ PEP 604│ Union operatörü            │ Sözdizimsel sadeleşme       │ `Union[int, str]` yerine `int | str` kullanımı             │
# │ PEP 563│ Lazy annotations           │ Performans & döngüsel çözüm │ Tipler geç yüklenir, recursive yapılarda faydalı           │
# │ PEP 695│ Generic syntax             │ Generic tanım sadeleşmesi   │ `class Box[T]: ...` gibi yeni sözdizimi                    │
# └────────┴────────────────────────────┴─────────────────────────────┴────────────────────────────────────────────────────────────┘

# 🎯 Mimari Not:
# - PEP 8 + 257 + 20 → Kodun biçimi, açıklaması ve felsefesi
# - PEP 484 ve sonrası → Kodun veri akışı, tip güvenliği ve modül sınırları
# - typing modülü → Bu PEP’lerin pratiğe dökülmüş hali
# - safe_repr, traceback, log_formatter gibi mimari fonksiyonlarda hem okunabilirlik hem edge-case modellemesi sağlar
