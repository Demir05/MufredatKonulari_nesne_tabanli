# ─────────────────────────────────────────────────────────────
# 📌 PYTHON'DA SCOPE (KAPSAM) KAVRAMI

# Scope, bir ismin (değişken, fonksiyon, sınıf vs.) hangi bağlamda tanınacağını belirleyen
# mantıksal bir bellek alanıdır. Bu alan fiziksel değildir; yani heap veya stack gibi değildir.
# Python yorumlayıcısı, bir ismi gördüğünde onu hangi bağlamda arayacağını scope sayesinde bilir.

# Scope, programın çökmesini engelleyen ve isimlerin çakışmasını (shadowing) önleyen bir sistemdir.
# Bu nedenle scope olmadan program çalışamaz; çünkü isim çözümleme (name resolution) yapılamaz.

# Python'da 4 temel scope vardır. Yorumlayıcı bir isimle karşılaştığında şu sırayla arama yapar:
# 1️⃣ Local       → Şu anki fonksiyonun içindeki isimler
# 2️⃣ Enclosing   → İç içe fonksiyon varsa, dış fonksiyonun local scope'u
# 3️⃣ Global      → Modül düzeyindeki isimler
# 4️⃣ Built-in    → Python'un kendi tanımlı isimleri (len, print, Exception vs.)

# Bu arama zinciri LEGB olarak adlandırılır ve yukarıdan aşağıya doğru çalışır.
# İlk eşleşme bulunduğunda arama durur.

# Lookup işlemi teorik olarak O(1) olsa da, çok fazla bağlam varsa (nested fonksiyonlar, modül içi import zincirleri)
# sıcak kodda (hot path) performansı negatif etkileyebilir.
# Bu yüzden "yerelleştirme" yapılır: global bir ismi local'e çekmek (örneğin x = global_x) → daha hızlı erişim sağlar.

# Scope ve Frame farklı yapılardır ama senkronize çalışırlar.
# Örneğin:
# - Main frame (dosya düzeyinde) → global scope'a bağlıdır
# - Fonksiyon çağrısı → local frame oluşturur → local scope'a bağlanır

# Her frame'in f_locals ve f_globals sözlükleri vardır → bunlar scope'u temsil eder.

# Eğer bir isim LEGB zincirinde bulunamazsa → Python NameError fırlatır.
# Örnek: print(x)  # x tanımlı değilse → NameError

# Eğer local frame'de iken global olan immutable bir veriye atama yapılırsa → UnboundLocalError oluşur.
# Bu hata, ismin tanındığını ama mevcut scope'da bulunamadığını gösterir.
# Örnek:
# x = 10
# def f():
#     print(x)      # hata: x local'de tanımlanacak ama önce erişiliyor
#     x = x + 1     # çözüm: global x

# Bu hata, aslında işlemin sağlıksız olduğunu ve ileride veri sızıntısı gibi sorunlara yol açabileceğini
# dolaylı olarak bildirir. Bu yüzden global anahtar kelimesiyle ismin kapsamı açıkça belirtilmelidir.

# Python'da mevcut scope'daki isimlere erişmek için iki özel fonksiyon vardır:
# 🔸 globals() → global scope'daki isimleri ve değerleri canlı olarak döner
# 🔸 locals()  → local scope'daki isimleri döner ama canlı değildir; geçmiş görüntüdür

# locals() ile yapılan değişiklikler genellikle program akışını etkilemez.
# Main frame'de çağrılırsa → locals() ve globals() aynı sonucu verir çünkü kapsam globaldir.

# Scope, Python'un isim çözümleme sisteminin temelidir.
# Doğru kullanıldığında hem performans hem güvenlik hem de kod okunabilirliği açısından büyük avantaj sağlar.
