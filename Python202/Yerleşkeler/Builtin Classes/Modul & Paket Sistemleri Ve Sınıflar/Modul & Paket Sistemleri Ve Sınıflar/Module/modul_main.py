# -----------------------------------------
# 🧠 __main__ Nedir? Neden Özel Bir Ad?
# -----------------------------------------
# Python’da her çalıştırılan dosya, otomatik olarak '__main__' adlı özel bir modül olarak adlandırılır.
# Bu sayede, bir dosya doğrudan mı çalıştırıldı yoksa başka bir dosya tarafından mı import edildi, kolayca anlaşılır.

# Örnek:
# $ python script.py  ->  __name__ == "__main__"
# Ancak başka bir modül tarafından import edilirse:  __name__ == "script"

# -----------------------------------------
# 🎯 import __main__ Ne İşe Yarar?
# -----------------------------------------
# 1. Kendi modülüne (çalışan script'e) dışarıdan bir modülmüş gibi erişmeni sağlar
# 2. Global namespace üzerinde doğrudan kontrol sağlar (örneğin __doc__, __file__, custom attribute'lar)
# 3. Yürütülen script'in çalışma konumu, dosya ismi gibi bilgilere erişilir
# 4. Runtime'da kendi kendini değiştirme / güncelleme imkanı verir

# -----------------------------------------
# 🔍 import __main__ Alternatiflerine Göre Avantajlıdır:
# -----------------------------------------
# - globals() daha kısıtlıdır, sadece fonksiyon dışındaysan işe yarar
# - sys.modules['__main__'] uzun ve dolaylıdır
# - __main__ modülünü doğrudan import etmek hem kısa hem anlaşılırdır

# -----------------------------------------
# 🔧 Örnek Kullanım:
# -----------------------------------------
import __main__

# __main__ modülünün adı
print(__main__.__name__)     # "__main__"

# Dosya yolu (bazı REPL ortamlarda olmayabilir)
print(getattr(__main__, '__file__', 'REPL'))

# Çalışan script'in docstring'ini atayalım
__main__.__doc__ = "Bu script, __main__ kullanımı örneğidir."

# Script globaline runtime'da değer enjekte etmek
__main__.config = {'mode': 'debug', 'version': '1.0'}

# Tanımlanan değer artık başka yerden erişilebilir
print(__main__.config['mode'])   # "debug"

# -----------------------------------------
# 📜 Teknik Bilgi: __main__ bir ModuleType örneğidir
# -----------------------------------------
# Tüm modüller gibi, import edilen __main__ da types.ModuleType sınıfındandır.
# Bu sayede, hasattr/getattr/setattr gibi dinamik işlemler mümkün hale gelir.

# -----------------------------------------
# 🧩 Kullanım Alanları:
# -----------------------------------------
# - Dynamic docstring veya global değerler belirlemek
# - Unit test sırasında davranışı özelleştirmek
# - CLI (command-line) scriptlerde modülün yürütme durumuna göre işlem yapmak


# 📌 MODÜL: __main__ ve globals() farkları

import __main__  # 🔍 __main__ modülünü import ederiz, bu özel bir modüldür
import types     # ModuleType gibi yapıları görmek için

# ✅ __main__ modülü nedir?
# -------------------------
# Python'da bir dosya doğrudan çalıştırıldığında (__name__ == "__main__"),
# bu dosyanın global değişkenleri, fonksiyonları ve sınıfları '__main__' adlı özel bir modülde toplanır.
# Yani __main__ modülü, çalıştırılan ana programın ortamını temsil eder.

assert isinstance(__main__, types.ModuleType)  # ✔️ Gerçekten bir ModuleType nesnesidir

# ✅ globals() nedir?
# -------------------
# globals(), içinde bulunduğunuz modülün global isim-nesne eşleşmelerini içeren bir sözlüktür.
# Bu fonksiyon her zaman aktif namespace'e ait sözlüğü döndürür.
globals_dict = globals()

# 🎯 FARK 1: Tip Farkı
print(type(__main__))         # <class 'module'> ➜ modül nesnesi
print(type(globals_dict))     # <class 'dict'>   ➜ yalnızca isim-nesne eşleşmesi

# 🎯 FARK 2: Metadata Farkı
# __main__ modülü, modüle ait metadata'ları içerir: __file__, __package__, __doc__, __name__, __loader__, __spec__ vs.
print(__main__.__name__)      # '__main__'
print(__main__.__doc__)       # None (ya da dosya başında varsa docstring)

# globals() ise sadece tanımlı değişkenleri içerir.
# Metadata genelde bu sözlükte olmaz:
print('__name__' in globals_dict)  # ✅ True
print('__doc__' in globals_dict)   # ✅ True veya False
print('__spec__' in globals_dict)  # ❌ Genellikle False olabilir

# 🎯 FARK 3: Dinamik Erişim
# __main__ modülü üzerinden direkt nesne erişimi mümkündür:
print(getattr(__main__, '__name__'))  # '__main__'
# globals() ise sadece dict üzerinden erişim sunar:
print(globals_dict.get('__name__'))  # '__main__'

# 🎯 FARK 4: Yazma Davranışı
# Her iki yapı da yazılabilir, ancak globals() üzerinden yazmak doğrudan namespace’e işler
globals_dict['x'] = 123
print(__main__.x)  # ✅ 123

__main__.y = 456
print(globals_dict['y'])  # ✅ 456

# Bu gösterir ki globals() ve __main__ birbirine bağlıdır, ancak:
# globals() sadece değişkenleri içerirken
# __main__ aynı zamanda modül metadata'sını da barındırır.

# 💡 Örnek: __main__ metadata’sı
for attr in dir(__main__):
    if attr.startswith("__") and not attr.endswith("__"):
        print(attr, ":", getattr(__main__, attr))  # Core meta-attributeları göster

# 🧠 ÖZET:
# -----------------------------------------------------------------------------
# - `globals()` sadece isim-değer sözlüğüdür, modül hakkında bilgi taşımaz.
# - `__main__` ise hem bu sözlüğü içerir hem de modüle dair metadata’yı barındırır.
# - Interaktif shell’lerde veya yeniden çalıştırmalarda bazı metadata’lar `globals()`’ta eksik olabilir.
# - Bu yüzden introspection, meta-programlama gibi işler için `import __main__` tercih edilir.


# ----------------------------------------------
# 🔍 __main__ MODÜLÜ VE ERİŞİM BİÇİMLERİ
# ----------------------------------------------

# Python'da bir dosya doğrudan çalıştırıldığında
# yorumlayıcı, bu dosya için "__main__" adlı özel bir modül oluşturur

# Bu modül bellekte bir ModuleType nesnesidir, ama otomatik olarak
# global namespace'e "kendisi" olarak eklenmez!

# __main__ modülüne erişmek için 2 yol vardır:

# 1️⃣ Doğrudan import
import __main__  # sys.modules['__main__'] üzerinden yüklenir

print(__main__.__name__)   # -> "__main__"
print(__main__.__dict__)   # -> modülün tüm üyeleri (namespace)

# 2️⃣ sys.modules üzerinden erişim
import sys

main_module = sys.modules['__main__']
print(main_module is __main__)  # -> True (aynı nesne)

# ----------------------------------------------
# 📌 globals() nedir ve __main__ ile farkı?
# ----------------------------------------------

# globals(), aktif modülün global namespace sözlüğüdür
print("__name__ in globals:", '__name__' in globals())  # -> True
print("globals()['__name__']:", globals()['__name__'])  # -> "__main__" ise ana dosya

# Ancak dikkat: __main__ modülüne ait olan ama globals() sözlüğünde olmayan şeyler olabilir
# Çünkü globals() sadece bu dosyanın "içinde tanımlanan" adlara erişir

# ----------------------------------------------
# 🤔 Peki neden __main__ globalde yok?
# ----------------------------------------------

# Python yorumlayıcısı, modülün adı '__main__' olsa bile,
# bu ismi doğrudan global namespace'e koymaz
# Bu modül sys.modules içinde tutulur ve erişilmek istenirse import edilmelidir

# Eğer şöyle yazarsan:
# print(__main__)
# HATA: NameError: name '__main__' is not defined

# Bu yüzden:
# ✅ `import __main__` veya ✅ `sys.modules['__main__']`
# ile erişmek gerekir

# ----------------------------------------------
# 🎯 Özet
# ----------------------------------------------

# - __main__ → doğrudan erişilemez, import edilmeli
# - globals() → sadece aktif modülün sözlüğü
# - sys.modules → tüm modül nesnelerinin kayıtlı olduğu yer
# - __main__ modülü, çalışma zamanında oluşur ve yorumlayıcının giriş noktasıdır

# 💡 Bu bilgi, introspection, modül enjeksiyonu, REPL, test frameworkleri gibi
# ileri seviye konularda oldukça önemlidir.
