# 📘 PEP 8: Python Kodlama Standartları
# Python topluluğunun kabul ettiği stil rehberidir.
# Amaç: Kodun okunabilirliğini, sürdürülebilirliğini ve ekip uyumunu artırmak.

# 1️⃣ Girintileme (Indentation)
# Her blok 4 boşlukla girintilenmeli. Tab yerine boşluk kullanılmalı.

def selamla():
    print("Merhaba")
    if True:
        print("Dünya")


# 2️⃣ Satır Uzunluğu
# Satırlar 79 karakteri geçmemeli. Uzunsa parantez içinde bölünmeli.

uzun_mesaj = (
        "Bu satır çok uzun olduğu için parantez içinde bölünüyor "
        "ve okunabilirliği artırıyor."
)


# 3️⃣ Fonksiyon ve Değişken İsimleri
# Fonksiyon ve değişken isimleri snake_case ile yazılmalı.

def hesapla_toplam(sayi_1, sayi_2):
    toplam = sayi_1 + sayi_2
    return toplam


# 4️⃣ Sınıf İsimleri
# Sınıf isimleri PascalCase ile yazılmalı.

class DosyaYukleyici:
    def yukle(self):
        print("Dosya yüklendi.")


# 5️⃣ Boşluk Kullanımı
# Operatörlerin etrafında birer boşluk olmalı.

x = 5
y = 10
z = x + y


# 6️⃣ Fonksiyon Parametrelerinde Boşluk
# Parantez içinde ve parametreler arasında boşluk bırakılmamalı.

def topla(x, y):
    return x + y


# 7️⃣ Import Sırası ve Gruplama
# Standart → 3. parti → yerel modüller şeklinde sıralanmalı.

import os
import sys

import numpy as np

import benim_modulum  # yerel modül örneği


# 8️⃣ Satır Aralıkları
# Fonksiyonlar arasında 1 boşluk, sınıflar arasında 2 boşluk bırakılmalı.

def birinci_fonksiyon():
    pass


def ikinci_fonksiyon():
    pass


class BirinciSinif:
    pass


class IkinciSinif:
    pass


# 9️⃣ Tip İpuçları (Type Hints)
# Fonksiyonların parametre ve dönüş tipleri açıkça belirtilmeli.

def carp(x: int, y: int) -> int:
    return x * y


# 🔟 None ile Karşılaştırma
# None ile karşılaştırma yapılırken 'is' kullanılmalı.

deger = None
if deger is None:
    print("Değer yok")

# 1️⃣1️⃣ Boolean ile Karşılaştırma
# True/False ile karşılaştırma yapılırken doğrudan kullanılır.

aktif = True
if aktif:
    print("Aktif")

# 1️⃣2️⃣ Tek Satırda Birden Fazla İşlemden Kaçın
# Kodun okunabilirliğini azaltır, ayrı satırlara bölünmeli.

if x > 0:
    print("Pozitif")

# 1️⃣3️⃣ Veri Yapılarında Boşluk Kullanımı
# Virgülden sonra boşluk, parantez içinde boşluk olmamalı.

liste = [1, 2, 3]
sozluk = {"ad": "Demir", "yas": 30}
kume = {1, 2, 3}


# 1️⃣4️⃣ Açıklayıcı Yorumlar
# Kodun ne yaptığını sade şekilde anlatmalı, gereksiz yorumdan kaçınılmalı.

def faktoriyel(n: int) -> int:
    # Rekürsif olarak faktöriyel hesaplar
    if n == 0:
        return 1
    return n * faktoriyel(n - 1)


# 1️⃣5️⃣ Boş Satır Kullanımı
# Modül seviyesinde 2 boş satır, sınıf içinde 1 boş satır önerilir.

class Kullanici:
    def __init__(self, ad: str):
        self.ad = ad

    def selamla(self):
        print(f"Merhaba {self.ad}")


# Modülün en üstünde tanımlanan global değişkenler, sabitler, fonksiyonlar arasında 2 boşluk bırakılır

PI = 3.14


def alan(r):
    return PI * r * r

# ✅ Bu dosya PEP 8’e uygun yazılmıştır.
# Kodun okunabilirliği, sürdürülebilirliği ve ekip uyumu için bu kurallar temel teşkil eder.
