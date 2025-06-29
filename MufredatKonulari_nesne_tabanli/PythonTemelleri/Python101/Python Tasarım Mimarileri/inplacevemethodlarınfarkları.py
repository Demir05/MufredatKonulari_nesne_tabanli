# ------------------------------------------------------------------------------
# 🔍 Python'da In-Place Operatörler (`+=`, `*=`, `|=`) vs. Metot Çağrıları (`.extend()`, `.update()`)
# ------------------------------------------------------------------------------

# 🎯 TEMEL AMAÇ:
# Bu iki yaklaşım genellikle benzer işler yapar gibi görünür:
#     a += [1, 2, 3]
#     a.extend([1, 2, 3])
# Ancak arka planda hem davranışları hem de performansları farklıdır.

# ------------------------------------------------------------------------------
# ⚙️ 1. In-Place Operatörler (`+=`, `*=`, `|=`, ...)
# ------------------------------------------------------------------------------

# 🔁 "In-place" kelimesi, hedef nesne üzerinde doğrudan değişiklik yapılacağı anlamına gelir
# Bu operatörler aslında şuna dönüşür:
#     a += b  →  a = a.__iadd__(b)
#     x *= y  →  x = x.__imul__(y)

# Eğer nesne `__iadd__` gibi methodları override etmemişse:
# Python geri plana düşer:
#     a += b  →  a = a.__add__(b)  # Yeni nesne üretilebilir ❗

# 📌 Bu durumda, mutable nesneler (`list`, `set`, `dict` gibi) çoğu zaman
# `__iadd__` gibi methodları override ederek kendi içeriklerini yerinde günceller.

# ❗ Ancak bu davranışın **garantisi yoktur**, nesneye göre değişebilir.
# Bu yüzden `+=` gibi operatörler her zaman predictable değildir.

# ------------------------------------------------------------------------------
# 🛠️ 2. Yöntem Çağrıları (Method Calls) — `.extend()`, `.update()`, `.add()`
# ------------------------------------------------------------------------------

# ✅ Bu çağrılar genellikle doğrudan C'de tanımlanmış methodlara gider:
#     a.extend(b)  →  PyList_Extend()
#     s.update(t)  →  PySet_Update()

# Bu sayede:
# - Daha hızlıdırlar
# - Kararlı ve deterministik çalışırlar
# - Geriye değer dönmez, doğrudan nesne üzerinde işlem yapar

# ------------------------------------------------------------------------------
# 🧪 3. PERFORMANS ÖRNEĞİ: `.extend()` vs `+=`
# ------------------------------------------------------------------------------

import time

a = list(range(100_000))
b = list(range(100_000))

start = time.time()
a += b
print("+= :", time.time() - start)

a = list(range(100_000))
b = list(range(100_000))

start = time.time()
a.extend(b)
print(".extend():", time.time() - start)

# ÖRNEK ÇIKTI:
#     += : 0.0045s
#     .extend(): 0.0030s
# 🚀 Sonuç: `.extend()` çoğu durumda daha hızlıdır
# Nedeni: doğrudan C optimizasyonu ile çalışır

# ------------------------------------------------------------------------------
# 📚 4. GENELLEME — Hangisi Ne Zaman Kullanılmalı?
# ------------------------------------------------------------------------------

# ✅ `.extend()`, `.update()`, `.add()` → Performans önemliyse, belirsizlik istenmiyorsa
# ✅ `+=`, `*=`, `|=` → Küçük işlemlerde okunabilirlik için

# ❌ In-place operatörler immutable nesnelerde (örneğin `tuple`, `int`) yeni nesne döner
#    Yani:
#        t = (1, 2)
#        t += (3,)  # Bu aslında: t = t + (3,)  → Yeni tuple oluşur ❗

# ------------------------------------------------------------------------------
# ✅ SONUÇ
# ------------------------------------------------------------------------------

# 🧠 Metotlar: Daha net, hızlı, güvenli
# 🤹 Operatörler: Daha kısa, okunabilir ama kontrolü sınırlı
# 📦 Büyük veriler ve özel veri yapılarında: metot kullanımı daha Pythonic ve ölçeklenebilirdir
