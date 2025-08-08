# ================================================================================
# 📚 ModuleType Nesnesindeki Dunder (Double Underscore) Özellikler
# ================================================================================
# Bu tanım, Python'daki bir modül nesnesi (yani `ModuleType` örneği) üzerinde
# bulunan özel nitelikleri (dunder attributes) detaylı şekilde açıklar.

from types import ModuleType

# Basit bir modül nesnesi oluşturalım
my_mod = ModuleType("example_mod")

# ================================================================================

# __name__
# ------------------------------------------------------------------------------
# Modülün adı (string). Genellikle dosya adı veya yaratırken verdiğin isimdir.
# import edilen modüllerde __name__ modülün adıdır,
# doğrudan çalıştırılan script'te ise "__main__" olur.

print(my_mod.__name__)  # Çıktı: example_mod

# ================================================================================

# __doc__
# ------------------------------------------------------------------------------
# Modülün belge açıklamasıdır. Docstring olarak da bilinir.
# Eğer modül tanımlanırken açıklama verilirse burada tutulur.

my_mod.__doc__ = "This is a sample module used for demonstration."
print(my_mod.__doc__)  # Çıktı: This is a sample module used for demonstration.

# ================================================================================

# __dict__
# ------------------------------------------------------------------------------
# Modül içeriğini (fonksiyonlar, değişkenler, vb.) tutan özel bir sözlüktür.
# Bu sözlük sayesinde modülün içindeki her şeye dinamik olarak erişebilirsin.

my_mod.version = "1.0"
print(my_mod.__dict__["version"])  # Çıktı: 1.0
print(dir(my_mod))                 # __dict__ üzerinden oluşur

# ================================================================================

# __loader__
# ------------------------------------------------------------------------------
# Modülün nasıl yüklendiğini belirten özel bir nesnedir.
# import ile gelen modüllerde otomatik tanımlanır.
# Elle oluşturulan modüllerde genellikle None'dır.

print(my_mod.__loader__)  # Çıktı: None

# Bu özellik, import sisteminde özel yükleyiciler (loader) tanımlamak için kullanılır.

# ================================================================================

# __package__
# ------------------------------------------------------------------------------
# Modül bir paketin içindeyse, bu nitelik o paketin adını tutar.
# Ana modüllerde boş string veya None olur.
# import yapısı içinde yer alan alt modüllerde, ait olduğu paketin adıdır.

print(my_mod.__package__)  # Çıktı: None

# Örnek:
#   from mylib.submodule import x
#   x.__package__  --> "mylib"

# ================================================================================

# __spec__
# ------------------------------------------------------------------------------
# Modülün "specification" nesnesidir. Import işlemi sırasında
# nereden yüklendiğini ve nasıl çözümlendiğini içerir.

print(my_mod.__spec__)  # Çıktı: None

# Bu özellik yalnızca gerçek import edilen modüllerde doludur.
# Elle yaratılan modüllerde genelde None olur.

# Örnek bir import:
#   import math
#   print(math.__spec__)  # Çıktı: ModuleSpec(name='math', ...)

# ================================================================================

# __file__
# ------------------------------------------------------------------------------
# Modülün diskteki dosya yolunu gösterir.
# import edilen dosya modüllerinde vardır.
# Elle oluşturulan modüllerde veya built-in modüllerde olmayabilir.

try:
    print(my_mod.__file__)
except AttributeError:
    print("Bu modül dosyadan yüklenmediği için __file__ yok.")  # Bu olur

# Örnek:
#   import os
#   print(os.__file__)  → '/usr/lib/python3.11/os.py'

# ================================================================================
# 🔍 ÖZET TABLO

# | Özellik      | Açıklama                                   | Elle Modül? |
# |--------------|--------------------------------------------|-------------|
# | __name__     | Modülün adı                                | ✅          |
# | __doc__      | Açıklama (docstring)                       | ✅          |
# | __dict__     | İçerikler (fonksiyonlar, değişkenler...)   | ✅          |
# | __loader__   | Yükleyici                                  | ❌ (None)   |
# | __package__  | Bağlı olduğu paket adı                     | ❌ (None)   |
# | __spec__     | Import metadata (ModuleSpec objesi)        | ❌ (None)   |
# | __file__     | Dosya yolu                                 | ❌          |

# ================================================================================
# 💡 NOT:
# Python 3’te modül sistemi daha modüler hale getirilmiştir.
# importlib, loader, finder gibi yapılar bu dunder özelliklerin çalışmasında rol alır.
# ModuleType objesi bu yapıların temel parçasıdır.
# ================================================================================

