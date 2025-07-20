# ====================================================
# 🔍 PYTHON'DA ABSTRACT CLASS ve METHOD REHBERİ
# ====================================================

# ✅ 1. Abstract nedir?
# ---------------------
#    Soyut sınıflar, doğrudan örneklenemeyen ama alt sınıflar için ortak bir yapı sunan sınıflardır.
#    Amaç: Alt sınıfların bazı methodları kesinlikle override etmesini zorunlu kılmak.

# ✅ 2. Hangi bileşenler olmalı?
# -----------------------------
#    ✅ Bir ana abstract sınıf (genelde ABC'den türetilir)
#    ✅ En az bir soyut method (yani override edilmesi ZORUNLU method)
#    ✅ Alt sınıf, soyut methodları override etmezse hata fırlatılmalı
#    ✅ Gerekiyorsa soyut sınıfın örneklenmesi engellenmeli (__new__ ile)

# ✅ 3. Abstract method nasıl tanımlanır?
# ---------------------------------------
#    🔹 Ya `abc` modülündeki @abstractmethod decorator'ü kullanılır
#    🔹 Ya da kendi decorator'ünle `func.__is_abstract__ = True` gibi işaretleme yapılır

# ✅ 4. Alt sınıflar nasıl kontrol edilir?
# ---------------------------------------
#    🔹 __init_subclass__ kullanılarak sınıf tanım anında override kontrolü yapılabilir
#    🔹 __new__ kullanılarak örneklenme anında ekstra güvenlik eklenebilir

# ✅ 5. Neden kontrol edilmeli?
# -----------------------------
#    ❗ Alt sınıf soyut methodları override etmezse, soyut sınıfın davranışı eksik kalır
#    ❗ Bu da ileride `AttributeError`, `NotImplementedError` gibi beklenmeyen hatalara yol açar

# ✅ 6. İyi bir soyut sınıf tasarımı şunları içerir:
# --------------------------------------------------
#    🔸 Soyut methodlar açıkça tanımlanmalı
#    🔸 override edilmeyen methodlar kullanıcıyı uyarmalı
#    🔸 Gerekiyorsa örnekleme kısıtlanmalı
#    🔸 Belgelendirme yapılmalı (hangi method zorunlu, neden, ne zaman kullanılmalı)

# ✅ 7. `abc` kullanımı mı, manuel mi?
# -----------------------------------
#    🔸 Küçük projelerde kendi decorator + __init_subclass__ ile kontrol etmek yeterlidir
#    🔸 Geniş projelerde `abc.ABCMeta` ve `@abstractmethod` ile standart yapı tercih edilir

# ✅ 8. Ekstra Tavsiyeler
# ------------------------
#    🔹 Method override kontrolü yaparken MRO zincirini gezmeyi unutma
#    🔹 Fonksiyonlara işaretleme yaparken `__is_abstract__` gibi özelleştirilmiş flag'ler kullanabilirsin
#    🔹 `Main.abstract_classes` gibi bir takip sistemi kurarak hangi sınıfın soyut olduğunu anlamak kolaylaşır

# ====================================================
# 🚀 Kendi soyut sistemini yazmak, metaclass'lara giriş kapısıdır!
# ====================================================
