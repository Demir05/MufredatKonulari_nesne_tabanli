# ===============================================================
# 🧠 CLOSURE HATASINI ÖNLEMEK İÇİN DEFAULT PARAMETRE KULLANIMI
# ===============================================================
#
# 🔹 Python'da döngü içinde fonksiyon (özellikle lambda) tanımlarken,
#     döngü değişkenleri closure ile referans olarak bağlanır.
#
# 🔸 Bu şu demektir:
#     Tüm fonksiyonlar aynı değişkeni paylaşır ve döngünün SON değerine göre davranır!
#
# 🎯 ÖRNEK (closure bug'ı tetikler):
# funcs = []
# for op in ("a", "b", "c"):
#     funcs.append(lambda: print(op))   # ❌ hepsi "c" yazdırır
#
# ---------------------------------------------------------------
# ✅ ÇÖZÜM: Default parametre ile closure'dan kaçmak
# ---------------------------------------------------------------
#
# lambda self, item, _name=name: pows[_name](self, target, item)
#
# 🔸 Burada `_name=name` kısmı sayesinde:
#     - `lambda` fonksiyonuna `_name` isminde YENİ bir local parametre tanımlanır
#     - Bu parametre, döngüdeki `name`'in DEĞERİ ile sabitlenir
#     - Artık closure değil, local sabit olarak davranır
#
# 🔐 Böylece:
# ➤ Her `lambda`, kendi `_name` parametresi ile çalışır
# ➤ Döngüdeki değişimlerden etkilenmez
#
# ---------------------------------------------------------------
# 📌 SONUÇ:
# ---------------------------------------------------------------
# 🔹 Döngüde fonksiyon/lambda tanımlıyorsan,
# 🔹 Ve o fonksiyonda döngü değişkeni kullanıyorsan,
# 🔸 mutlaka: `_var=var` yapısıyla default argüman kullan!
#
# Bu Python’da closure-safe kod yazmanın en net ve önerilen yoludur ✅
# ===============================================================


b = []

for a in ["d","e","f","g","h","i","j"]: # a = j -> global
    def f():
        return a
    b.append(f)

