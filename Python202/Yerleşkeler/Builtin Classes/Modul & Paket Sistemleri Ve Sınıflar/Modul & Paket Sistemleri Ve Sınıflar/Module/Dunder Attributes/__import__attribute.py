# ⬛️ 1. __import__ nedir?
# Yerleşik (built-in) bir Python fonksiyonudur.
# Modülleri dinamik olarak (runtime'da) yüklemek için kullanılır.
# import deyiminin arka plandaki karşılığıdır ama çok daha esnektir.

# ⬛️ 2. Neden kullanılır?
# Modül adını string olarak belirtmek istenen dinamik durumlar için uygundur.
# Örnek: eklenti (plugin) sistemleri, reflektif yapılar, betik yükleyiciler.

# ⬛️ 3. Temel kullanım
# Basit bir import gibi davranır:
modul = __import__('math')  # import math

# ⬛️ 4. Parametreler
# __import__(name, globals=None, locals=None, fromlist=(), level=0)
# name: string olarak modül adı
# - bu ad,docstring olarak verilmeli ve verilen tüm isimler paket olmalı (modul.attribute verilemez)
# - eğer fromlist verilmemişse sadece ilk isim yüklenir bu durumda -> a.b.c durumunda sadece: a yüklenir
# globals, locals: hangi kapsamda (scope) yükleneceğini kontrol eder
# fromlist: modül içinden hangi alt öğelerin alınacağı
# level: 0 = mutlak, 1+ = göreli içe aktarma

# ------------------------------------------------
# 🚩 En çok karıştırılan parametre: fromlist
# ------------------------------------------------

# ✅ Amaç: Alt modül veya attribute’ların da yüklenmesini istemektir.
# Ancak: fromlist parametresi dönen sonucu DEĞİL, sadece neyin yükleneceğini etkiler.

# 🧪 ÖRNEK 1: Basit modül
mod1 = __import__('math')         # → math modülünü döner
mod2 = __import__('math', fromlist=['sqrt'])  # → yine math modülünü döner
# Ancak, bu durumda `sqrt` yüklenmiş olur, elle erişmeliyiz:
sqrt_fn = mod2.sqrt

# 🧪 ÖRNEK 2: Alt modül (os.path gibi)
mod3 = __import__('os.path')  # → SADECE os modülünü döner ❌
mod4 = __import__('os.path', fromlist=[''])  # → os.path modülünü döner ✔️

# NEDEN?
# - __import__('os.path') → import zinciri başlatır ama en üst modül `os`’u döndürür
# - __import__('os.path', fromlist=['']) → alt modülün de döndürülmesini sağlar

# ------------------------------------------------
# 🔁 En yaygın kullanım şekli:
mod = __import__('package.module', fromlist=['attr'])
attr = getattr(mod, 'attr')

# ------------------------------------------------
# 🧾 Genel Kural:
# - fromlist ne döneceğini DEĞİL, ne yükleneceğini belirler
# - Alt modül istiyorsan fromlist kullanmak zorundasın
# - Erişim her zaman elle yapılır (mod.attr gibi)

# ------------------------------------------------
# ⚠️ Yanlış Beklentiler:
# ❌ __import__('math', fromlist=['sqrt']) → sqrt döndürür zannetmek yanlıştır
# ✅ Her zaman modül döner, içindeki öğeleri sen çekersin

# ------------------------------------------------
# 🔁 Alternatif: importlib
# from importlib import import_module
# mod = import_module('os.path')  # doğrudan os.path döner

# ⬛️ 6. globals & locals
# Modülün nereye (hangi isim alanına) yazılacağını kontrol eder.
scope = {}
__import__('math', globals=scope)
print('math' in scope)  # True

# ⬛️ 7. level parametresi
# Göreli import işlemleri için kullanılır.
# Örn: 'from . import x' = level=1
# Bu, özellikle paket içi importlarda kritiktir.
# level, from . -> ifadesindeki nokta sayısını temsil eder
# kullanıldığı durumda mevcut modül doğrudan çağrılırsa ve __package__ set edilmediyse hata alınır

# 📦 Örnek:
# __import__('mod_b', globals(), locals(), [], 1)
# Şu anki paket içinde mod_b'yi bul ve yükle (relative import)

# ⬛️ 8. __import__ vs import
# import: okunabilirlik için ideal, sabit modül adlarında kullanılır
# __import__: dinamik, esnek, riskli — ama güçlüdür

# ⬛️ 9. __import__ vs importlib
# __import__: düşük seviye, doğrudan import mekanizmasını tetikler
# importlib: modern, güvenli, parçalanabilir yapı sunar

# ⬛️ 10. Güvenlik ve riskler
# User input ile birleştirilirse güvenlik açığı yaratabilir
# Kod okunabilirliğini azaltır, dikkatli ve kontrollü kullanılmalı

# ⬛️ 11. Ne zaman kullanılır?
# - runtime’da modül adını bilmiyorsan
# - eklenti sistemi geliştiriyorsan
# - test araçları ya da özel derleyiciler gibi meta-programlama yapıyorsan


# ️️⬛️ 12. Neden alternatifleri varken __import__ kullanılır ?
# - Çünkü __import__, geçiş fonksyiyonudur; interpreter'İn çekirdeğinde tanımlıdır,geriye dönüktür, düşük seviyedir ve hook'lanabilir tüm bunlar
#   onu hala import mekanizmasının temel kalbi yapar
# - Hook: "kendisini yeniden tanımlayabilme" anlamına gelir yani orjinal davranışına ek yeni davranışlar eklenebilir bu davranışlara örnek;
#   1) Debug
#   2) Log
#   3) Filtreleme yapılabilir.
#   hook'lanabilen nesnelere __import__'da dahildir ama kullanılması çok önerilmez çünkü
#   1) bazı 3.parti moduller,__import__ kullanmazlar, importlib kullanırlar bu durumda yazdığın hook,bypass edilir
#   2) bazı modullerde PEP uyumsuzluğu olabilir
#   3) Debug etmesi zorlaşabilir ve eğer yanlış bir işlem yapılmışsa ki buna level,fromlist dahil işlemin kendisi, global olduğu için tüm yapı değişir ve kaos olur


import sys
__package__ = "p.proje2"
sys.path.insert(0, r"C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\p\proje2")

__import__("a", globals(), level = 2) # burda bu modulun sanki p.projeler2 'nin altında varmış gibi gösterdik bu import sahteliciğine girer
# ileri seviye bir kullanım olsada doğrusu relative import değil(yani level kullanılmamalı) abs import kullanılmalı