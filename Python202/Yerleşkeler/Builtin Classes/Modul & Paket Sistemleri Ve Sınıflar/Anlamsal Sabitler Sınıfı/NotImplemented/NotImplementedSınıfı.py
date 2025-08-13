# -*- coding: utf-8 -*-
# =============================================================================
#  PYTHON: NotImplemented — Sözel/Terorik Açıklama + Kullanım Alanları + Örnekler
# =============================================================================
#  "NotImplemented" Nedir?
# =============================================================================
# • NotImplemented, Python'da özel bir sabittir.
# • Türü: NotImplementedType
#       type(NotImplemented)  # <class 'NotImplementedType'>
# • Amacı: Özellikle operatör aşırı yükleme (dunder metotlar) sırasında,
#   "bu işlem bu tür için tanımlı değil, karşı tarafa dene" sinyali vermektir.
# • Hata değildir! Bir istisna fırlatmaz, sadece Python'a "bu işlemi ben yapamam"
#   der.
# • NotImplementedError ile karıştırma:
#       - NotImplemented  → özel bir değer/sinyal
#       - NotImplementedError → bir istisna türü
# =============================================================================


# =============================================================================
# 1) Kullanım Alanları
# =============================================================================
# 1.1 Operatör aşırı yükleme (aritmetik)
#     - __add__, __radd__, __eq__, __lt__ gibi metotlarda tür uyumsuzluğu varsa
#       NotImplemented döndürülür.
#     - Böylece Python diğer tarafın (karşı operandın) uygun metodu denemeye çalışır.
#
#     Örn:
#       class MyNum:
#           def __add__(self, other):
#               if isinstance(other, MyNum):
#                   return MyNum(self.value + other.value)
#               return NotImplemented
#
# 1.2 Karşılaştırma operatörleri
#     - __eq__, __lt__ vb. metotlarda tür farklıysa False döndürmek yerine
#       NotImplemented döndürmek daha doğru olur.
#       Böylece simetrik karşılaştırma korunur.
#
# 1.3 "Ben bu işlemi bilmiyorum" sinyali
#     - Kendi API'lerinizde de "bu yöntem desteklenmiyor" demek için kullanılabilir,
#       ancak genellikle operatör protokolünde anlamlıdır.
# =============================================================================


# =============================================================================
# 2) Özellikler
# =============================================================================
# • Tekil nesne: NotImplemented global olarak tek örnektir.
# • Doğruluk değeri: bool(NotImplemented) → True (ama bu amaçla kullanmayın)
# • Karşılaştırma: 'is' ile yapılır.
# • Çoğaltılamaz: copy.copy veya deepcopy yine aynı nesneyi döndürür.
# =============================================================================


# =============================================================================
# 3) Örnekler
# =============================================================================

if __name__ == "__main__":
    # Tür kontrolü
    print(type(NotImplemented))  # <class 'NotImplementedType'>
    print(NotImplemented is NotImplemented)  # True

    # 1.1 Operatör aşırı yükleme örneği
    class MyNum:
        def __init__(self, value):
            self.value = value

        def __add__(self, other):
            if isinstance(other, MyNum):
                return MyNum(self.value + other.value)
            return NotImplemented

        def __radd__(self, other):
            if isinstance(other, (int, float)):
                return MyNum(other + self.value)
            return NotImplemented

        def __repr__(self):
            return f"MyNum({self.value})"

    a = MyNum(10)
    b = MyNum(5)
    print(a + b)       # MyNum(15)
    print(3 + a)       # MyNum(13)
    try:
        print(a + "x") # Tür uyumsuz, TypeError oluşur
    except TypeError as e:
        print("Hata:", e)

    # 1.2 Karşılaştırma örneği
    class MyStr:
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            if isinstance(other, MyStr):
                return self.value == other.value
            return NotImplemented

        def deneme(self):pass

    s1 = MyStr("abc")
    s2 = MyStr("abc")
    print(s1 == s2)    # True
    print(s1 == "abc") # False (NotImplemented sayesinde)

