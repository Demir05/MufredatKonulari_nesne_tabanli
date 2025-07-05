# 🔄 DATA MUTATION — Python'da Değiştirilebilir Veri Yapıları ve Tasarım İlkeleri

# ------------------------------------------
# 📌 1. TANIM — DATA MUTATION NEDİR?
# ------------------------------------------
# Data mutation, bir nesnenin içeriğinin doğrudan değiştirilmesidir.
# Yani yeni bir nesne üretmeden, mevcut nesnenin "içini" değiştiririz.

# Örnek:
a = [1, 2, 3]
a.append(4)  # ❗ Bu bir mutation'dır → a artık [1, 2, 3, 4]

# ------------------------------------------
# 📌 2. MUTABLE YAPILAR — NEDEN VAR?
# ------------------------------------------
# Python'da mutable (değiştirilebilir) veri tipleri şunlardır:
# list, dict, set, bytearray, class instance (varsayılan olarak)

# Amaç:
# - In-place işlem yaparak bellek kullanımını azaltmak
# - Performansı artırmak
# - Değiştirilebilir state yönetimi (cache, oyunlar, makineler)

# ------------------------------------------
# 📌 3. TEHLİKELERİ
# ------------------------------------------
# - 🔁 Side effects: Bir yerde yapılan değişiklik, başka yerleri etkileyebilir
# - 🔍 Debug zorlaşır: Hangi fonksiyon neyi ne zaman değiştirdi izlenemez hale gelir
# - ⚠️ Predictability bozulur: Aynı fonksiyon farklı zamanlarda farklı sonuç dönebilir

# Örnek:
x = [1, 2]
y = x
y.append(3)
print(x)  # [1, 2, 3] ❗ x de değişti çünkü y sadece referans

# ------------------------------------------
# 📌 4. NASIL DOĞRU KULLANILIR?
# ------------------------------------------
# ✅ Eğer mutable bir class kullanıyorsan:
# - mutation açık ve belgelenmiş olmalı
# - mümkünse sadece `__iadd__`, `__setitem__` gibi özel amaçlı yapılarda kullanılmalı
# - public API'de kullanıyorsan "değiştirilebilir nesne" olduğunu net belirt

# Alternatif:
# - Immutable yapı tercih et
# - Mutation yerine yeni nesne üret

# Immutable örnek:
z = (1, 2, 3)
z_new = z + (4,)  # 🔒 mutation yok, yeni tuple

# ------------------------------------------
# 📌 5. SENİN PROJENDE (CLASS TOOLS) NE OLUYOR?
# ------------------------------------------
# Bu projede:
# - left/inplace/right operator sistemleri var
# - `inplace` modunda bilinçli mutation yapılıyor (örneğin: setattr)
# - Eğer mutable yapı ise `self` döndürülüyor
# - Eğer immutable yapı ise yeni nesne üretiliyor

# Bu, Python'da en doğru in-place operator davranış biçimidir ✔️

# ------------------------------------------
# ✅ SONUÇ
# ------------------------------------------
# Mutation doğru kullanıldığında faydalıdır.
# Ama iyi belgelenmeli, kontrol altında olmalı ve amacı net olmalı.
# Bu projedeki yapı, mutation'ı bilinçli ve güvenli kullanan ileri seviye bir mimari örneğidir.
