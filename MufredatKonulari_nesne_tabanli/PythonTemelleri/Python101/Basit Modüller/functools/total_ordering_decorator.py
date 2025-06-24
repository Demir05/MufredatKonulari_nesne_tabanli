# -------------------------------------------------------------------------------------
# @functools.total_ordering Decorator'ü
# -------------------------------------------------------------------------------------
# Tanım:
# Bu decorator, bir sınıfın __eq__() ve bir tane karşılaştırma metodu (__lt__, __le__, __gt__, __ge__)
# tanımlaması durumunda diğer karşılaştırma metodlarını otomatik olarak üretir.
#
# Yani, gereksiz kod tekrarını azaltır ve sınıfına tam karşılaştırma (total ordering) yeteneği kazandırır.
#
# Kullanım Amacı:
# - Eğer bir objenin sıralanabilir, eşitlik kontrolü yapılabilir, karşılaştırılabilir olması gerekiyorsa,
#   sadece 2 metot yazarak 6 metodu elde etmiş olursun.
#
# Nerelerde Kullanılır:
# - Sıralanması gereken özel sınıflar (örneğin: Varlık, Skor, Tarih, Versiyon, Koordinat, Öğrenci, Ürün)
# - sorted(), max(), min(), bisect gibi karşılaştırma yapan fonksiyonlarla uyumlu hale getirmek için
#
# Gereksinim:
# - __eq__() zorunludur (eşitlik kontrolü için)
# - Diğerlerinden yalnızca biri yeterlidir: __lt__, __le__, __gt__, __ge__
#
# UYARILAR:
# - __eq__ tanımlı değilse, decorator çalışmaz ❌
# - Eğer karşılaştırma metodlarından birini eksik bırakırsan, TypeError alırsın.
# - Otomatik türetilen metotların performansı manuel yazılanlardan biraz daha yavaş olabilir.
#
# Farkı:
# - Bu bir runtime çözümüdür, sadece sınıfın method dictionary’sine dinamik olarak yeni metotlar ekler.
# - Birçok framework bu decorator'ü kullanır çünkü DRY (Don't Repeat Yourself) felsefesine uygundur.
#
# Kısıtlama:
# - Sadece yeni-style classes (Python 3.x) ile kullanılmalıdır. (Tüm modern Python'lar zaten bu şekilde)

# -------------------------------------------------------------------------------------
# ÖRNEK:
# Bir "Student" sınıfı düşünelim, sadece notlarına göre karşılaştırmak istiyoruz.
# __eq__ ve __lt__ tanımlayarak tüm diğer karşılaştırmaları elde edebiliriz.
# -------------------------------------------------------------------------------------

from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade == other.grade

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade < other.grade

# -------------------------------------------------------------------------------------
# Şimdi aşağıdaki metotlar OTOMATİK olarak oluşturulur:
# __le__, __gt__, __ge__
#
# Örneğin:
# s1 <= s2 çağrıldığında -> s1 < s2 or s1 == s2
# s1 >= s2 çağrıldığında -> not s1 < s2
# s1 > s2 çağrıldığında  -> not (s1 < s2 or s1 == s2)
# -------------------------------------------------------------------------------------

# Kullanım
s1 = Student("Ali", 85)
s2 = Student("Ayşe", 92)

print(s1 < s2)   # True  (__lt__)
print(s1 <= s2)  # True  (automatically derived)
print(s1 == s2)  # False (__eq__)
print(s1 != s2)  # True  (inverse of __eq__)
print(s1 > s2)   # False (automatically derived)
print(s1 >= s2)  # False (automatically derived)

# -------------------------------------------------------------------------------------
# Bu sayede sadece 2 method tanımlayarak 6 karşılaştırma davranışı kazandırmış olduk!
# Bu hem kodu sadeleştirir hem de tekrarları ortadan kaldırır.
# -------------------------------------------------------------------------------------
