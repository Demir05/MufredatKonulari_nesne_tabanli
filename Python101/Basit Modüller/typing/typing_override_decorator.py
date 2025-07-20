# ---------------------------------------------
# 📌 1. `@override` Dekoratörü Nedir?
# ---------------------------------------------
# Python 3.12 ile `typing` modülüne eklenen `@override`, alt sınıfta,üst sınıftaki
# aynı isimdeki metodun bilerek override ettiğini belirtmek için kullanılır.
# Bu, sadece bir "niyet bildirimi"dir — Python çalışma zamanında hiçbir etkisi yoktur.

# ---------------------------------------------
# 🎯 2. Ne İşe Yarar?
# ---------------------------------------------
# - Kodun daha okunabilir olmasını sağlar
# - IDE ve statik analiz araçlarının override hatalarını yakalamasına olanak tanır
# - Büyük projelerde refactor sürecini güvenli hâle getirir

# ---------------------------------------------
# 🔍 3. Nasıl Çalışır? (Arka Plan)
# ---------------------------------------------
# `@override` dekoratörü aslında sadece method nesnesine bir attribute ekler:
#     __override__ = True
# Ancak `typing.override` olarak tanımlandığı için IDE’ler ve MyPy gibi araçlar
# bu dekoratörü özel olarak tanır ve override doğrulaması yapar.

# ---------------------------------------------
# 🚫 4. Neden Kendi `override()` Dekoratörün Çalışmaz?
# ---------------------------------------------
# Eğer sen kendi override fonksiyonunu şöyle tanımlarsan:
#     def override(func): func.__override__ = True; return func
# Bu runtime'da çalışır ama IDE bunu bilmez — çünkü sadece `typing.override` tanınır.

# ---------------------------------------------
# ✅ 5. Doğru Kullanım Örneği
# ---------------------------------------------
# from typing import override
#
# class Base:
#     def save(self): ...
#
# class Model(Base):
#     @override
#     def save(self):  # IDE artık bu methodu kontrol eder ✔️
#         ...

# ---------------------------------------------
# 🧠 6. Ne Zaman Kullanılmalı?
# ---------------------------------------------
# - Bir üst sınıftaki methodu ezmek istediğinde
# - Özellikle soyut sınıf veya interface tasarımı yaparken
# - Geniş kod tabanlarında methodların kontrolünü kaybetmek istemediğinde

# ---------------------------------------------
# 🧪 7. İpuçları ve Ekstra Bilgiler
# ---------------------------------------------
# - `@override` sadece statik analiz içindir (performansa etkisi sıfırdır)
# - Sadece methodlarda kullanılabilir
# - Python 3.12 ve üstünde çalışır
# - `__override__` attribute'u runtime'da okunabilir ama etkisi yoktur

# ---------------------------------------------
# 🔚 8. Özet
# ---------------------------------------------
# ✔️ `@override`, override niyetini açıkça belirtir
# ✔️ Kod kalitesini artırır, hataları önler
# ✔️ IDE'ler ve statik araçlar için çok değerli bir sinyaldir
# ❗️ Sadece `typing.override` kullanılmalı — kendi override fonksiyonun işe yaramaz

from typing import override

class Base:
    def __init__(self):
        self.name = "demir"
    @staticmethod
    def deneme():...

class Sub(Base):
    @override
    def __init__(self):
        self.name = "ozan"

    @staticmethod
    def deneme():...