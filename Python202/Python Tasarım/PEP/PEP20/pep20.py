# Güzel olan çirkinden daha iyidir.
# Estetik ve okunabilirlik önemlidir.

# Açık olan gizli olandan iyidir.
# Kodun ne yaptığı anlaşılır olmalı, sihirli davranışlardan kaçınılmalı.

# Basit olan karmaşıktan daha iyidir.
# Gereksiz soyutlamalardan kaçın.

# Karmaşık olan karmaşık olmayandan daha iyidir.
# Ama basitlik mümkünse tercih edilmeli.

# Düz olan girintili olandan daha iyidir.
# Kod yapısı sade olmalı, iç içe mantıklar azaltılmalı.

# Dağınık olan yoğun olandan daha iyidir.
# Kodun bölümleri net ayrılmalı, tek satıra sıkıştırılmamalı.

# Okunabilirlik önemlidir.
# Kod sadece çalışmak için değil, anlaşılmak için yazılır.

# Özel durumlar yeterince açıklanmadıkça kuralları bozmaz.
# İstisnalar olabilir ama açıkça belirtilmeli.

# Pratiklik saflığı yener.
# Teorik mükemmellik yerine işe yarayan çözümler tercih edilir.

# Hatalar sessizce geçilmemelidir.
# Hatalar fark edilmeli, gerekirse yükseltilmeli.

# Açıkça belirtilmedikçe sessizce geçilmemelidir.
# Hatalar göz ardı edilmemeli.

# Şimdi iyi bir fikir gibi görünse de, asla yapma.
# Aceleyle alınan kararlar uzun vadede sorun çıkarabilir.

# Namespace’ler harika bir fikirdir – bunu daha fazla kullanın!
# Modülerlik ve isim ayrımı Python’un güçlü yönüdür.

# 🧘 PEP 20 – The Zen of Python
# Python’un tasarım felsefesini 19 özlü ilkeyle tanımlar.
# Kodun sadece çalışması değil, sade, okunabilir ve sürdürülebilir olması hedeflenir.

# 1️⃣ Beautiful is better than ugly.
# Kod estetik olmalı, okunabilirliği yüksek olmalı.


def topla(x, y):
    return x + y  # Sade, net, estetik


# 2️⃣ Explicit is better than implicit.
# Ne yaptığı açık olmalı, sihirli davranışlardan kaçınılmalı.


def oku_dosya(yol: str) -> str:
    with open(yol, encoding="utf-8") as f:
        return f.read()


# 3️⃣ Simple is better than complex.
# Gereksiz soyutlamalardan kaçın.


def kare(x):
    return x * x  # Lambda veya class yerine sade fonksiyon


# 4️⃣ Complex is better than complicated.
# Karmaşıksa bile anlaşılır olmalı, girift olmamalı.


def normalize(liste):
    toplam = sum(liste)
    return [x / toplam for x in liste]  # Karmaşık ama sade


# 5️⃣ Flat is better than nested.
# İç içe yapıdan kaçınılmalı.


# ❌ Kötü
def hesapla(x):
    if x > 0:
        if x < 10:
            return x * 2


# ✅ İyi
def hesapla(x):
    if 0 < x < 10:
        return x * 2


# 6️⃣ Sparse is better than dense.
# Kod sıkışık olmamalı, boşluklar okunabilirliği artırır.


def selamla(isim):
    print(f"Merhaba, {isim}")


# 7️⃣ Readability counts.
# Kodun kendini anlatması gerekir.


def ortalama(liste):
    """Verilen sayı listesinin ortalamasını döndürür."""
    return sum(liste) / len(liste)


# 8️⃣ Special cases aren't special enough to break the rules.
# İstisnalar kuralları bozmak için yeterli sebep değildir.

# Örneğin: tek elemanlı tuple
tekli = (42,)  # Virgül zorunlu

# 9️⃣ Although practicality beats purity.
# Teorik mükemmellik yerine işe yarayan çözüm tercih edilir.


# ❌ Teorik olarak daha doğru ama karmaşık
# ✅ Pratik ve yeterli
def bol(x, y):
    return x / y if y else float("inf")


# 🔟 Errors should never pass silently.
# Hatalar fark edilmeli.

try:
    risky()
except Exception as e:
    print(f"Hata oluştu: {e}")

# 1️⃣1️⃣ Unless explicitly silenced.
# Hatalar bilinçli şekilde bastırılabilir.

try:
    risky()
except Exception:
    pass  # Bilinçli olarak sessiz geçildi

# 1️⃣2️⃣ In the face of ambiguity, refuse the temptation to guess.
# Belirsizlik varsa tahmin yürütme, açık ol.


def get_user(data):
    if "user" not in data:
        raise ValueError("Kullanıcı bilgisi eksik")
    return data["user"]


# 1️⃣3️⃣ There should be one-- and preferably only one --obvious way to do it.
# Bir işi yapmanın tek ve açık bir yolu olmalı.


def ters(liste):
    return list(reversed(liste))  # slice yerine daha açık


# 1️⃣4️⃣ Although that way may not be obvious at first unless you're Dutch.
# Guido van Rossum’a selam — bazen Python’un yolu sonradan anlaşılır.

# 1️⃣5️⃣ Now is better than never.
# Kod yazmaya başlamak, mükemmeli beklemekten iyidir.

# 1️⃣6️⃣ Although never is often better than *right* now.
# Ama aceleyle yazmak yerine düşünmek daha iyidir.

# 1️⃣7️⃣ If the implementation is hard to explain, it's a bad idea.
# Açıklaması zor olan kod, kötü fikirdir.


# ❌ Kötü
def x(a):
    return a**a % a + a // a * a - a


# ✅ İyi
def hesapla(a):
    """a'nın çeşitli işlemlerle dönüştürülmüş hali"""
    return (a**a % a) + (a // a * a) - a


# 1️⃣8️⃣ If the implementation is easy to explain, it may be a good idea.
# Açıklanabilir kod, iyi fikirdir.


def daire_alan(r):
    """Yarıçapı verilen dairenin alanını hesaplar."""
    return 3.14 * r * r


# 1️⃣9️⃣ Namespaces are one honking great idea -- let's do more of those!
# Modülerlik ve isim ayrımı Python’un temel gücüdür.

import math  # math.sqrt gibi açık namespace kullanımı
