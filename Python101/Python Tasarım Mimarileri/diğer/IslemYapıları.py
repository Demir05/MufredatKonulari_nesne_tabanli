# ===========================================
# 📘 PYTHON'DA İŞLEM TÜRLERİ VE SÖZDİZİMİ YAPILARI
# ===========================================


# 🔹 EXPRESSION (İfade)
# -------------------------------------------
# Bir değeri hesaplayan ve mutlaka bir değer döndüren yapılardır.
# Expression → değerlendirilebilir (evaluatable) ifadelerdir.
# Genellikle fonksiyon çağrısı, matematiksel işlem, değişken, mantıksal ifade gibi yapılar expression'dır.

# ➕ Expression Özellikleri:
# - Bir değer döndürmek zorundadır
# - Eval gibi fonksiyonlara geçebilir
# - Tek satırda bir ifadeden oluşur

# 🧪 Örnekler:

print(sum([1, 2]))              # Fonksiyon çağrısı (matematiksel expression)
degisken = "aslı"               # Değişken referansı da bir expression'dır
sonuc = 10 < 20 and "değer"     # Mantıksal işlem → expression

print(sonuc)                    # çıktı: "değer"
print(10 > 20)                  # çıktı: False (bool türü de expression sayılır)

# in operatorü de expression içinde kullanılabilir:
listem = list(range(5))
2 in listem and print(True)     # True olduğu için print çalışır


# 🔹 STATEMENT (İşlem Bildirimi)
# -------------------------------------------
# Python'da doğrudan bir işlem gerçekleştiren, ancak bir değer döndürmeyen kod satırlarıdır.
# Expression içerebilir ama statement yapısı genel bir işlemi temsil eder.
# Birden fazla ifade barındırabilir.

# ➕ Statement Özellikleri:
# - Değer döndürmek zorunda değildir
# - Kontrol yapıları, tanımlar ve atamalar örnektir
# - Python’da her satır genellikle bir statement’tır

# 🧪 Örnekler:

deger1 = "ali"                  # Atama işlemi (statement)
a, b = 10, 20                   # Çoklu atama (statement)
for _ in range(5): a = 5        # Döngü ve içindeki atama (statement)
if a == 5: print("ok")          # Koşul yapısı (statement)
import re                       # Modül içeri aktarma (statement)


# 🔹 SÖZDİZİMİ AYRAÇLARI
# ===========================================

# ✅ VIRGÜL ( , )
# Değerleri, argümanları veya parametreleri ayırmak için kullanılır.
# Expression'lar arasında ayrım yapmaya yarar.

# ➕ Kullanım Alanları:
# - tuple, list, set, dict tanımı
# - fonksiyon çağrısı ve tanımı
# - unpacking, çoklu atama
# - mantıksal ifadeler arasında ayrım

t = 1, 2, 3                     # Tuple tanımı
sozluk = {"isim": "demir", "yas": 20}
v, *v_ = [1, 2, 3, 4]
print("ad {}, yaş {}".format("demir", 20))
10 > 2 and print("evet"), print("ifade bitti")


# ✅ NOKTALI VİRGÜL ( ; )
# Bağımsız statement’ları tek satırda ayırmak için kullanılır.
# Kod okunabilirliği açısından genellikle önerilmez, daha çok terminal ortamında veya REPL kullanımında tercih edilir.

# ➕ Kullanım Alanları:
# - Aynı satırda birden fazla işlem tanımlamak
# - Kısa betiklerde işlem zinciri yapmak

import time; start = time.time(); print("Başladı")
a = 10; b = 20
if a == 10: print("a 10"); del a

# ❗ Uyarı: Noktalı virgül, kodun okunabilirliğini düşürür.
# Python’un tasarım felsefesi → “Bir satır, bir işlem”


# 🧠 Özet:

# Expression → değer döndüren her şey
# Statement → bir işlem veya tanım gerçekleştiren kod parçaları
# Virgül → ifadeler/parametreler arasında ayraç
# Noktalı virgül → bağımsız işlem bloklarını tek satırda yazmak için

