# ============================================================
# 🧠 NESTED CLASS (İÇ İÇE SINIF) — TEORİK TEMELLER
# ============================================================

# ✅ Nested Class nedir?
# ------------------------------------------------------------
# - Python'da bir sınıfın içinde başka bir sınıf tanımlanmasına "nested class" denir.
# - Bu yapı, dış sınıfın scope'u içinde bir iç sınıf tanımıdır.
# - Ancak iç sınıf, **dış sınıfla özel bir bağa sahip değildir**.
#   Yani self, dış sınıfa bağlı bir context taşımaz (closure gibi davranmaz).
#
# - Yine de __qualname__ sayesinde, iç sınıfın tanım zinciri (qualified name) dış sınıfla bağlantılı olur.

# 🔍 Temel Örnek:
class Outer:
    class Inner:
        pass

# - Burada Inner sınıfı Outer.Inner şeklinde çağrılır.
# - Ancak Inner sınıfı bağımsızdır. Outer ile state veya context paylaşmaz.


# ✅ Nested Class pythonic mi? Gerçek hayatta sık kullanılır mı?
# --------------------------------------------------------------
# - KOD GÖRSELLİĞİ açısından kafa karıştırıcı olabilir.
# - Özellikle dış sınıfın init metodunda, iç sınıfın dinamik olarak kullanılmaması önerilir.
# - Python'da nested class genellikle:
#    • Sabit iç türleri gruplamak
#    • Enum, config, validator gibi sistemlerde kullanılır
#    • DSL (domain-specific language) mimarilerde

# ❗️Ancak birçok durumda, iç içe sınıflar yerine bağımsız sınıflar tanımlamak daha okunabilirdir.
#    - Çünkü nested class'lar hem kod derinliğini artırır, hem de test, import, analiz işlemlerini zorlaştırır.

# ✅ __qualname__ etkisi:
# --------------------------------------------------------------
# - __qualname__ (qualified name), sınıfın tam yolunu gösterir.
# - Nested class'larda, __qualname__ iç içe tanımlamayı net şekilde yansıtır.

print(Outer.Inner.__qualname__)  # 👉 'Outer.Inner'


# ✅ Nested Class'ın Dezavantajları:
# --------------------------------------------------------------
# - Sınıf çözümleme (type hint, docstring, debugger, inspect) gibi işlemleri zorlaştırır.
# - IDE desteği düşer (otomatik tamamlama, class browser).
# - Sınıflar test edilirken iç sınıfa doğrudan erişim karmaşıklaşır.
# - Bazı third-party framework'ler (örneğin Django) iç içe sınıf yapısını desteklemez veya hatalı işler.
# - Pickle, dill gibi modüllerle serialize edilebilirlik bozulabilir.
# - __module__ attribute'ü dış sınıfa değil, tanımlandığı dosyaya aittir. (yanıltıcı olabilir!)

# 🔧 Not:
# - Sadece sınıfın görünümde iç içe olması, onun runtime'da yapışık olduğu anlamına gelmez.
# - İki sınıf bağımsız olarak __dict__, __slots__, __mro__, vs. zincirini korur.


# ✅ Özet:
# --------------------------------------------------------------
# - Nested Class: Sınıfın içinde sınıf. Python destekler, ama çok önerilmez.
# - Teknik olarak legal ve bazı niş kullanım alanları var.
# - Genelde namespace derinliğini artırır, okunabilirliği düşürür.
# - IDE, framework, inspect gibi araçlarla kullanımı zordur.
# - Tercihen dışarıda tanımlı sınıfların import edilerek kullanılmasını öneririz.

