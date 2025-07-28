# ============================================================
# 🔍 PYTHON'DA `__weakref__`, `__slots__` ve `weakref` REHBERİ
# ============================================================

# ✅ `__weakref__` NEDİR?
# -----------------------
# `__weakref__`, bir sınıf örneğinin zayıf referans (weak reference) desteği olup olmadığını belirler.
# Python nesnelerinin, zayıf referansla takip edilebilmesi için bu özelliğe sahip olması gerekir.
# Normal sınıflar (yani `__slots__` tanımlamayanlar) bu attribute'a zaten sahiptir.

# 🧠 Peki `weakref` ne işe yarar?
# -------------------------------
# - Zayıf referanslar, nesneleri RAM'de tutmadan referanslamanı sağlar.
# - Garbage Collector (çöp toplayıcı), eğer sadece weakref varsa nesneyi toplayabilir.
# - Bu sayede büyük nesneleri geçici izleme, önbellekleme (cache), referans döngülerini kırma gibi işlerde kullanılır.

# 🧪 Örnek kullanım:
# -------------------
# import weakref
# class Person:
#     pass
# p = Person()
# r = weakref.ref(p)
# print(r())  ➜ p nesnesine ulaşır

# ✅ `__slots__` ve `__weakref__` ilişkisi
# ---------------------------------------
# - Eğer sınıfta `__slots__` tanımlarsan, Python artık `__dict__` ve `__weakref__` gibi dinamik yapıları otomatik eklemez.
# - Bu durumda `weakref.ref(obj)` çalışmaz!
# - Çözüm: `__weakref__` slot'unu elle eklemek.

# 🛑 Aksi halde:
# TypeError: cannot create weak reference to 'MyClass' object

# ✅ Doğru kullanım:
class Person:
    __slots__ = ('name', '__weakref__')  # weakref için açıkça belirtilmeli

    def __init__(self, name):
        self.name = name

import weakref
p = Person("Ada")
ref = weakref.ref(p)
print(ref())  # ✅ Çalışır

# ✅ Nerelerde Kullanılır?
# -------------------------
# 1. 🔁 Cache sistemlerinde: Büyük nesneleri weakref ile tut, ihtiyaç kalmayınca sistem silsin.
# 2. 🔄 Referans döngüsü oluşturmamak için.
# 3. 🧹 Hafif gözlem mekanizmaları (observer pattern, callback yapıları)
# 4. 🔄 Karmaşık veri yapılarında bellek sızıntısını önlemek

# ⚠️ Ne zaman Gerekmez?
# ----------------------
# - Basit uygulamalarda çoğunlukla ihtiyaç duyulmaz.
# - Bellek yönetimini Python'un Garbage Collector'ına bırakmak yeterlidir.

# ✅ Sonuç
# --------
# - `__weakref__` = Nesnene weakref.ref uygulamak için gerekli altyapıdır.
# - `__slots__` = Bu yapıyı devre dışı bırakabilir.
# - `__slots__` kullandığında `__weakref__` eklemeyi **unutma**, yoksa `weakref` çalışmaz!
# - `weakref` = Performans, bellek, geçici izleme, önbellekleme gibi gelişmiş sistemlerde çok güçlüdür.

# ============================================================
# 💡 UZMAN NOTU:
# ============================================================
# Zayıf referanslar büyük sistemlerde “hayalet takip” gibi çalışır — nesne varsa göster, yoksa sön.
# Bu sayede belleği koruyarak daha sürdürülebilir yazılım geliştirmeyi sağlar.
