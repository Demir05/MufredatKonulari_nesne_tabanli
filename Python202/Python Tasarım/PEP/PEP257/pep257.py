# 📘 PEP 257: Docstring Conventions
# Python'da modül, sınıf, fonksiyon ve metodların içine yazılan açıklama metinlerinin (docstring)
# nasıl biçimlendirilmesi gerektiğini tanımlar.
# Amaç: Kodun ne yaptığını açıkça anlatmak, okunabilirliği ve sürdürülebilirliği artırmak.

# 🧠 Docstring nedir?
# Tanımın hemen altında yer alan string literal'dir.
# Python'da __doc__ attribute olarak erişilebilir.

def topla(x, y):
    """İki sayıyı toplar."""
    return x + y


print(topla.__doc__)  # "İki sayıyı toplar."

# 1️⃣ Docstring her zaman üçlü çift tırnak (""" """) ile yazılmalı.
# Tek satırlık bile olsa üçlü tırnak kullanılır — genişletilebilirlik sağlar.

def selamla():
    """Kullanıcıyı selamlar."""
    print("Merhaba")

# 2️⃣ Tek satırlık docstring'lerde açılış ve kapanış aynı satırda olmalı.

def kare(x):
    """Verilen sayının karesini döndürür."""
    return x * x

# 3️⃣ Çok satırlı docstring'lerde açıklama bir paragraf gibi yazılır.
# Açıklama satırından sonra bir boşluk bırakılır, kapanış ayrı satıra gelir.

def carp(x, y):
    """
    İki sayıyı çarpar.

    Parametreler:
    x -- birinci sayı
    y -- ikinci sayı
    """
    return x * y

# 4️⃣ Modüller, sınıflar ve fonksiyonlar docstring içermelidir.
# Public API'ye ait her yapı belgelenmelidir.

class DosyaYukleyici:
    """
    Dosya yükleme işlemlerini yöneten sınıf.
    """

    def yukle(self, yol: str) -> None:
        """Verilen yoldan dosyayı yükler."""
        print(f"{yol} yüklendi.")

# 5️⃣ Sınıf docstring'i ile ilk metod arasında bir boşluk bırakılmalı.

# 6️⃣ Docstring içinde backslash (\) varsa raw string (r"""...""") kullanılabilir.

def yol_goster():
    r"""C:\kullanici\belgeler yolunu döndürür."""
    return r"C:\kullanici\belgeler"

# 7️⃣ Docstring, kodun ne yaptığına odaklanmalı — nasıl yaptığına değil.

def ortalama(liste):
    """Verilen sayı listesinin ortalamasını döndürür."""
    return sum(liste) / len(liste)

# 8️⃣ Docstring içinde örnek kullanım, parametre açıklamaları, dönüş tipi gibi bilgiler verilebilir.

def bol(x: int, y: int) -> float:
    """
    İki sayıyı böler.

    Args:
        x (int): Pay
        y (int): Payda

    Returns:
        float: Bölüm sonucu
    """
    return x / y

# 📘 PEP 257'e göre public API'ye ait her yapı docstring içermelidir.
# Public API: dışarıdan erişilmesi ve kullanılması amaçlanan fonksiyon, sınıf, modül gibi yapılardır.

# 🧠 Ancak bir public fonksiyonun içinde tanımlanan nested (iç içe) fonksiyonlar,
# doğrudan dış dünyaya açık olmadıkları için public API sayılmazlar.

# 🔍 Bu durumda PEP 257 açısından docstring zorunlu değildir.
# Ama kodun okunabilirliği için yorum satırı veya docstring ile açıklanması önerilir.

def islem_yap(x, y):
    """Verilen iki sayıyla işlem yapar."""

    def topla(a, b):
        # Dahili kullanım: iki sayıyı toplar
        return a + b

    return topla(x, y)

# ✅ Nested fonksiyon karmaşık bir işlem yapıyorsa, docstring ile açıklanabilir.

def hesapla(x, y):
    """Verilen iki sayıyı normalize edip toplar."""

    def normalize(z):
        """Veriyi 0-1 aralığına çeker."""
        return z / 100

    return normalize(x) + normalize(y)

# 🧩 Nested fonksiyonlar dışarıdan erişilemez, bu yüzden public API değildir.
# Ama mantıksal olarak önemliyse, docstring ile belgelenmesi iyi bir pratiktir.

# 🎯 Sonuç:
# - Public fonksiyon → docstring zorunlu
# - Nested fonksiyon → docstring opsiyonel ama önerilir
# - Kodun mimarisi karmaşıksa → açıklayıcı docstring yazmak sürdürülebilirliği artırır



# ✅ Sonuç:
# PEP 257, kodun ne yaptığını açıkça anlatan, tutarlı ve sade docstring'ler yazmamızı sağlar.
# PEP 8 ile birlikte kullanıldığında hem biçim hem içerik açısından güçlü bir kod yapısı elde edilir.
