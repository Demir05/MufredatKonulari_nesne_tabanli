# ==========================================
# 🧠 How to Design Pythonic Custom Containers
# ==========================================

# 🚀 Bu belge, Python'da özel koleksiyon sınıfları (container types) tasarlarken
# profesyonelce dikkat edilmesi gereken yazılım ilkelerini içerir.

# -------------------------
# 1️⃣ ENUMERATE STRATEJİSİ
# -------------------------
# 🔹 Ne zaman kullanılır?
#   • Liste veya iterable üzerinde hem index'e hem de değere aynı anda ihtiyaç varsa

# 🔹 Neden önemlidir?
#   • Kodun hem okunabilirliğini hem de doğruluğunu artırır
#   • Örnek: (index, (key, value)) şeklinde erişim

# 🔹 Klasik kullanım:
#   for i, (k, v) in enumerate(my_list):


# -------------------------
# 2️⃣ INDEX GEÇERLİLİK KONTROLÜ
# -------------------------
# 🔹 Ne zaman yapılmalı?
#   • Kullanıcıdan gelen bir index ile çalışırken

# 🔹 Nasıl yapılır?
#   • `0 <= index < len(obj)` ➜ Pythonic ve güvenli yöntem
#   • Alternatif olarak: try/except kullanılarak IndexError yakalanabilir

# 🔹 Amaç:
#   • Sessiz hatalardan veya çökmeden kaçınmak
#   • discard-like davranış için → sadece kontrol et, hata verme


# -------------------------
# 3️⃣ GİRDİ TİPİ & YAPI DOĞRULAMA
# -------------------------
# 🔹 Hedef:
#   • Fonksiyona gelen argümanın beklenen yapı ve uzunlukta olup olmadığını kontrol etmek

# 🔹 Nasıl yapılır?
#   • `isinstance(x, tuple) and len(x) == 2` gibi yapılar kullanılarak
#   • Alternatif: `collections.abc` modülüyle daha soyut tip kontrolü

# 🔹 Avantaj:
#   • Yanlış veri ile sınıfın bozulması engellenir


# -------------------------
# 4️⃣ HATA YÖNETİMİ
# -------------------------
# 🔹 Hedef:
#   • Geliştiriciye/son kullanıcıya anlamlı geri bildirim sağlamak

# 🔹 Yöntem:
#   • `raise ValueError("...")` veya `TypeError`, `IndexError`, `KeyError`

# 🔹 İyi uygulama:
#   • Hataları sadece saptamak değil, anlatmak (neden oldu)


# -------------------------
# 5️⃣ PERFORMANS DÜŞÜNCESİ
# -------------------------
# 🔹 Amaç:
#   • O(n) yerine O(1) erişim — özellikle kontrol işlemlerinde

# 🔹 Strateji:
#   • `set` gibi yapıların lookup avantajını kullan
#   • `dict`, `set`, `frozenset` gibi yapılarda O(1) membership test mümkündür

# 🔹 Örnek:
#   if key in cache_set: ...


# -------------------------
# 6️⃣ API UYUMU: PROPERTY vs METHOD
# -------------------------
# 🔹 Property kullan:
#   • Eğer fonksiyon bir veri görünümüyse (hesaplama yapmıyorsa)
#   • `obj.keys` gibi doğal görünüm sun

# 🔹 Method kullan:
#   • Eğer işlem parametre alıyor ya da yan etki yapıyorsa

# 🔹 Bu ayrım, kullanıcıya sezgisel bir API sağlar


# -------------------------
# 7️⃣ STANDART API BENZERLİĞİ
# -------------------------
# 🔹 Sınıf metodlarının isimleri mümkünse Python built-in koleksiyonlarıyla örtüşmeli

# 🔹 Örnekler:
#   • `append()`, `pop()`, `clear()`, `update()`, `remove()`

# 🔹 Neden?
#   • Kullanıcı daha önce görmediği bir yapı ile çalışırken bile nasıl davranacağını tahmin edebilir

# 🔹 Not:
#   • Bu davranış, Python ekosistemine daha kolay entegre edilen nesneler üretir

