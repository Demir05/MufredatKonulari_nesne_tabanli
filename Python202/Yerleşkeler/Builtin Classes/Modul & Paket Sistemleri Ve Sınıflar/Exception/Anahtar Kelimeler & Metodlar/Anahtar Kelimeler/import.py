# ----------------------------------------------
# 🔍 PYTHON'DA `import` ANAHTAR KELİMESİ
# ----------------------------------------------

# `import`, başka bir modül veya paketin içeriğini kullanılabilir hale getirir.
# Bu işlem sırasında Python şunları yapar:

# 1️⃣ 📂 sys.modules kontrol edilir → daha önce yüklenmiş mi?
# 2️⃣ 📁 sys.path üzerinden dosya veya paket aranır
# 3️⃣ 📜 .py dosyası (veya .pyc) yüklenir ve çalıştırılır
# 4️⃣ 🧠 Yeni bir **frame** oluşturulur (Stack + Heap)
#     🔹 Stack: Kodun çalıştığı çağrı sırası
#     🔹 Heap: Global değişkenler, objeler vs.
# 5️⃣ 💼 Modülün içeriği, kendi **scope**'unda (namespace) tanımlanır
# 6️⃣ 🔗 Çağıran modülün namespace’ine `modül_adı` değişkeni eklenir

# ----------------------------------------------
# 🔹 NEDEN `modül.üye` ŞEKLİNDE ERİŞİLİR?
# ----------------------------------------------

# Çünkü:
# - `import math` dediğimizde, sadece `math` isminde bir referans tanımlanır.
# - `math.pi` kullanımı bu modül nesnesinin içinden erişimdir.
# - Bu, küresel namespace'in kirlenmesini önler ✅

import math
print(math.sqrt(16))  # Evet! 'sqrt' doğrudan değil, math üzerinden erişilir.

# ----------------------------------------------
# 🧠 SCOPE ve FRAME AÇIKLAMASI
# ----------------------------------------------

# 📦 Her modül yüklendiğinde:
# - Kendine özel bir **global scope** oluşturur
# - Bu scope, `modül.__dict__` ile temsil edilir
# - Yani her modülün kendi isim alanı vardır. Başka modülleri etkilemez.

# 🔁 import edilen modülün frame’i sadece bir defa çalışır
#    (sys.modules içinde tutulduğu için tekrar çağrıldığında yeniden çalışmaz)

# ----------------------------------------------
# 💡 `__import__()` Fonksiyonu (LOW LEVEL)
# ----------------------------------------------

# 🔧 Python, aslında `import` anahtar kelimesini kullanırken
#    perde arkasında `__import__()` fonksiyonunu çağırır.

# 🧾 Söz Dizimi:
# __import__(name, globals=None, locals=None, fromlist=(), level=0)

# - name: modül adı (örn: 'math')
# - globals/locals: bağlam (genellikle otomatik verilir)
# - fromlist: 'from x import y' için y kısmı
# - level: 0 → mutlak, 1+ → göreli import

# 🔍 Kullanım Amacı:
# - Dinamik modül yüklemek
# - `eval`, `exec` içinde modül çağırmak
# - Plugin sistemlerinde ya da modül adını string olarak alan yapılarda

# Örnek:
modul = __import__('math')
print(modul.sqrt(25))  # math modülü üzerinden çalışır

# ----------------------------------------------
# 🔁 from <modül> import <isim> FARKI
# ----------------------------------------------

# Bu yapı sadece istenen üyeyi doğrudan scope'a getirir
# ✅ from math import sqrt → artık doğrudan sqrt() yazabiliriz

# Ancak: bu, `import math` gibi namespace kontrolü sağlamaz!

# __import__() fonksiyonu her zaman bir modül nesnesi döner.
# Bu, import ifadesinin düşük seviyeli karşılığıdır ve modülün kendisini geri verir.
# Dönen değer hiçbir zaman bir sınıf, fonksiyon ya da attribute değildir.

# fromlist parametresi, __import__'a hangi alt öğelerin (attribute/modül vs.) yüklenmesi gerektiğini bildirir.
# Ancak bu öğeler doğrudan döndürülmez — sadece ilgili modülün namespace'ine dahil edilmesi sağlanır.

# Örnek:
# mod = __import__("importlib.machinery", fromlist=["ModuleSpec"])
# Burada mod, importlib.machinery modülüdür.
# fromlist=["ModuleSpec"] sadece, mod.ModuleSpec ifadesinin çalışabilir olmasını sağlar.
# Ama mod'un kendisi ModuleSpec sınıfı değildir, hâlâ bir modüldür.

# Yani fromlist ifadesi gereksiz değildir — aksine, modül içinde hangi ögenin erişilebilir olacağını kontrol eder.
# Ancak beklenti hatalı olmamalıdır: fromlist, doğrudan o ögeyi döndürmez.