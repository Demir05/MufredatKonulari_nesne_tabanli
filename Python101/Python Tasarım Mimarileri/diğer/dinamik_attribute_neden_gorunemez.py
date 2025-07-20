# 📌 IDE'ler Neden Dinamik Olarak Eklenen Attribute'ları Göstermez?

# Python'da setattr() gibi fonksiyonlarla çalışma zamanında (runtime) bir nesneye yeni attribute eklenebilir.
# Ancak bu tür attribute'lar, IDE (PyCharm, VSCode, vb.) tarafından otomatik tamamlama (autocomplete) listesine dahil edilmez.
# Bunun temel sebebi IDE'lerin çalışma şeklidir:

# 1️⃣ IDE'ler "statik analiz" yapar:
#    - Yani kodu çalıştırmadan analiz ederler.
#    - `setattr(obj, "x", 10)` gibi dinamik işlemler ancak kod çalışırken anlam kazanır.
#    - Bu nedenle IDE, böyle attribute'ları önceden "tahmin edemez".

# 2️⃣ IDE, class içindeki açık tanımları (attribute, type hint, docstring) okur:
#    - Örnek: `class A: x: int` veya `class A: x = 0`
#    - Bu şekilde tanımlanmış attribute'lar autocomplete içinde görünür.

# 3️⃣ __dir__() metodunu override etmek işe yaramaz:
#    - Çünkü IDE `dir()` fonksiyonunu çağırmaz, sadece statik yapıyı tarar.
#    - `def __dir__(self): return ["foo"]` gibi tanımlar sadece kod çalıştığında `dir(obj)` çıktısını etkiler.

# ✅ Çözüm:
#    - IDE'nin görmesini istediğin attribute'ları class içinde açıkça tanımla.
#    - Örneğin: `x: int = 0` veya sadece `x: int` gibi tip ipucu ver.

# 🔁 Özet:
#    - IDE = statik zihinli
#    - Python = dinamik davranışlı
#    - Aradaki farktan dolayı, runtime attribute'lar autocomplete'e yansımaz
