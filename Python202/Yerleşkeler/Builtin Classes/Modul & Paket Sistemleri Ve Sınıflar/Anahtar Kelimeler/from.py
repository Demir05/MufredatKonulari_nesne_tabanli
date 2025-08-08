# ----------------------------------------
# 📌 FROM ... IMPORT ... NEDİR?
# ----------------------------------------

# from ... import ..., Python'da başka bir modül veya paketten
# spesifik isimleri (değişken, sınıf, fonksiyon vs.) doğrudan
# mevcut namespace'e **aktarır** (bind eder).

# Bu yapı import'tan farklı olarak, modülün tamamını değil
# sadece belirli üyeleri (attributes) yükler ve **doğrudan erişim sağlar.**

# ÖRNEK:
from math import sqrt

# Yukarıdaki ifade, 'math.sqrt' fonksiyonunu doğrudan 'sqrt' adıyla tanımlar:
# Artık sadece:
sqrt(25)
# demek yeterli olur, 'math.sqrt' demeye gerek kalmaz.

# Bu nedenle `from` yapısı **isim çözümlemeyi** kısaltır ama namespace'i genişletir.

# ----------------------------------------
# 📌 DÜŞÜK SEVİYEDE NE OLUYOR?
# ----------------------------------------

# from math import sqrt ifadesi, arka planda şu işlemlere eşdeğerdir:

import math          # 1️⃣ Önce modül içe aktarılır
sqrt = math.sqrt     # 2️⃣ Belirtilen öge mevcut namespace'e bind edilir

# Bu işlem, doğrudan erişim sağlar ancak modül ismini taşımaz (math.sqrt değil, sadece sqrt)

# ----------------------------------------
# 📌 DÜŞÜK SEVİYEDE __import__() İLE KULLANIMI
# ----------------------------------------

# from x import y işlemi, düşük seviyede __import__ fonksiyonu ile yönetilir.
# Ancak bu çağrıda, özel parametreler gerekir:

mod = __import__("math", globals(), locals(), ["sqrt"])
# math modülü yüklenir, ancak sadece "sqrt" erişimi açılır
sqrt = mod.sqrt

# ⚠️ DİKKAT: __import__ her zaman üst modülü döndürür! (from ... import ... için bile)
# Bu yüzden:
mod = __import__("os.path", fromlist=["join"])  # os modülü değil, os.path döner

# ----------------------------------------
# 📌 __import__() PARAMETRELERİ
# ----------------------------------------

# __import__(name, globals=None, locals=None, fromlist=(), level=0)

# name:        İçe aktarılacak modül adı (örn: 'os' ya da 'os.path')
# globals:     Global namespace – from işlemlerinin hangi bağlamda çözüleceğini belirtir
# locals:      Local namespace – genellikle globals ile aynı olur
# fromlist:    Hangi ögelerin çekileceğini belirtir (örn: ['sqrt'])
# level:       Göreceli mi mutlak mı import yapılacağını belirler
#              0 → Mutlak import (varsayılan)
#              1+ → Göreceli import (örneğin aynı paketten içe aktarma)

# ÖRNEK:
# from .utils import helper
__import__("utils", globals(), locals(), ["helper"], level=1)

# ----------------------------------------
# 📌 FROM ... IMPORT ... NE ZAMAN TERCİH EDİLİR?
# ----------------------------------------

# ✅ Belirli fonksiyonları veya sınıfları sık kullanıyorsan
# ✅ Daha kısa kod yazmak istiyorsan
# ✅ Özellikle namespace'e sadece gerekli şeyleri dahil etmek istiyorsan

# ❌ Ancak dikkat: Aynı isimde başka bir değişkeni ezebilir. Bu yüzden `import x` daha güvenlidir.

# ----------------------------------------
# 📌 __all__ ile Etkileşimi
# ----------------------------------------

# Bir modülde __all__ tanımlıysa:
# from mymod import * ifadesi __all__ listesindeki öğeleri yükler

# from mymod import x ise __all__'den bağımsız olarak doğrudan x aranır.


# ----------------------------------------
# 📌 globals, locals ve level Ne İşe Yarar?
# ----------------------------------------

# Bu 3 parametre, özellikle `__import__()` fonksiyonu kullanıldığında,
# **modülün nereye ve nasıl yükleneceğini** belirler.

# Yani sadece modülü yüklemek değil, **doğru bağlama (scope)** yüklemek için kullanılır.


# ----------------------------------------,
# 1️⃣ globals (Global Namespace)
# ----------------------------------------

# globals → Hangi bağlamın (modülün veya fonksiyonun) "global" isim alanı kullanılacak?
# Normalde, çağrıldığı yerin `globals()` çıktısı verilir.

# Bu, import edilen modülün global olarak nereye yazılacağını belirler.

example_globals = globals()

mod = __import__("math", example_globals)
# Burada, "math" modülü bu scope'un global'ine yazılır


# ----------------------------------------
# 2️⃣ locals (Local Namespace)
# ----------------------------------------

# locals → Fonksiyon gibi daha lokal bir scope varsa, buraya yazılır.
# Ancak genellikle globals ile aynıdır.

example_locals = locals()

mod = __import__("math", globals(), example_locals)
# math modülü yüklenir, erişim sağlanır ama varsayılan olarak sadece "globals" kullanılır

# locals çok nadiren kullanılır, çünkü çoğu zaman locals üzerinde doğrudan işlem yapmazsınız


# ----------------------------------------
# 3️⃣ level (Göreceli vs Mutlak Import)
# ----------------------------------------

# level → import işleminin **göreceli** mi yoksa **mutlak** mı olduğunu belirtir.

# level = 0 → Mutlak import (örn: import os, import mypackage.utils)
__import__("os", globals(), locals(), [], 0)

# level = 1+ → Göreceli import (bir üst modül, iki üst modül gibi)

# Örneğin:
# from .utils import helper     (level=1)
__import__("utils", globals(), locals(), ["helper"], level=1)

# from ..helpers.util import safe      (level=2)
__import__("helpers.util", globals(), locals(), ["safe"], level=2)

# 🧠 Bu, **aynı paketteki** modüller arasında dolaşırken oldukça faydalıdır.

# ----------------------------------------
# 📌 Özet:
# ----------------------------------------

# Parametre       | Görevi
# ----------------|-------------------------------
# globals         | Modülün yükleneceği global namespace
# locals          | Lokal isim çözümlemesi (çok nadir)
# fromlist        | import x ifadesinde hangi öğelerin çekileceği
# level           | Göreceli (.) mi, mutlak mı (import x)

