# 📌 __annotations__ → Modül Düzeyinde Tip İpucu (Type Hint) Sözlüğü

# ───────────────────────────────────────────────
# 1️⃣ Tanım:
# Python'da `__annotations__`, bir modül (veya sınıf, fonksiyon) içinde
# tanımlanan değişkenlere ait tip ipuçlarının tutulduğu özel bir sözlüktür (dict).

# Bu sözlük, değişkenlerin yalnızca **type hint** (tür bildirimi) içerdiği
# durumlarda otomatik olarak oluşturulur.

# Eğer modülde hiç type hint kullanılmamışsa, `__annotations__` isimli bir
# değişken **oluşturulmaz.** Bu nedenle doğrudan erişim `NameError` hatası verir.

# ───────────────────────────────────────────────
# 2️⃣ Ne zaman oluşur?
# İlk kez bir modül düzeyinde değişken tip bildirimi yapıldığında:

# 🔽 Bu satırdan sonra __annotations__ oluşur
x: int = 10

# Artık şunu yazmak güvenlidir:
print(__annotations__)  # ➤ {'x': <class 'int'>}

# ───────────────────────────────────────────────
# 3️⃣ Varsayılan davranış:
# Eğer modülde **hiçbir değişken tiplenmemişse**, `__annotations__`
# adlı global isim **tanımlanmaz** ve erişim şu hatayı verir:

# NameError: name '__annotations__' is not defined

# 🔴 Örnek:
# print(__annotations__)   → Hata verir!

# ───────────────────────────────────────────────
# 4️⃣ Güvenli erişim:
# Bu nedenle `__annotations__`'a erişmek istiyorsan, her zaman:

annotations = globals().get("__annotations__", {})

# şeklinde kontrollü olarak erişmelisin.
# Böylece hata vermez, yoksa boş bir sözlük döner.

# ───────────────────────────────────────────────
# 5️⃣ Nerede işe yarar?
# - Modül içi tip kontrolü yapmak istediğinde
# - Dinamik tip analiz araçları geliştirmek istediğinde
# - IDE'lere, linter'lara destek vermek için
# - Sözleşmeye dayalı API'ler kurarken

# __annotations__ doğrudan kullanabileceğin, yorumlayıcının oluşturduğu
# faydalı bir metadata sözlüğüdür.

# ───────────────────────────────────────────────
# 6️⃣ Özet:
# - Otomatik oluşur (ilk type hint sonrası)
# - Varsayılan olarak yoktur
# - Doğrudan erişim → NameError
# - globals().get(...) ile güvenli kullanım ✅
