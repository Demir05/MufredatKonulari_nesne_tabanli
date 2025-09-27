# =================================================================
# ✅ PYTHON ÇALIŞMA ZAMANI: STACK & FRAME KATMANLARI
# =================================================================

# 🔍 Her Python kodu çalıştırıldığında, CPython yorumlayıcısı (interpreter)
#     bir *execution frame* (çalışma çerçevesi) oluşturur.

# 🔸 Bu frame yapısı:
#     ➤ Fonksiyonun parametrelerini
#     ➤ Yerel değişkenleri
#     ➤ Global referansları
#     ➤ Üst çağıran frame’i (f_back)
#     ➤ Ve yürütme konumunu (line no, opcode, trace...)
#     içerir.

# 🧱 Frame, çalışan fonksiyonun "çalışma bağlamını" (execution context) temsil eder.

# 🔄 Tüm bu frame'ler, bir çağrı yığını (call stack) üzerinde zincir halinde sıralanır.

# -----------------------------------------------------------------
# 🔍 Peki bu frame'lere nasıl erişiyoruz?
# -----------------------------------------------------------------

# 🔧 `inspect` modülü üzerinden → inspect.currentframe() çağrısı ile
#     o anda çalışan en içteki frame’e ulaşabiliriz.

import inspect
frame = inspect.currentframe()  # 👈 Aktif çalışmakta olan kod bloğunun frame’i

# 🔹 Bu frame aslında CPython’da bir `PyFrameObject` türüdür.
# 🔹 Python'da bu yapıların erişimi sadece sınırlı yollarla mümkündür.

# 📌 CPython, frame yapısını doğrudan dışa açmaz.
#     ➤ inspect.currentframe() bir "gizli geçit" gibi davranır
#     ➤ Alternatif yollar da var, birazdan geleceğiz.

# -----------------------------------------------------------------
# 🔁 FRAME TÜRLERİ (Stack Katmanları)
# -----------------------------------------------------------------

# 1️⃣ Main Frame:
#     - Script çalıştığında otomatik oluşur
#     - `__main__` seviyesindeki global kodları temsil eder
#     - globals(), __name__ vs. bu frame’e bağlıdır

# 2️⃣ Function Frame:
#     - Her fonksiyon çağrıldığında yeni bir frame oluşturulur
#     - Parametreler, locals, üst frame referansı bu yapıdadır

# 3️⃣ Generator/Coroutine Frame:
#     - yield / await içeren yapılar için oluşturulan özel frame’lerdir
#     - Devam ettirilebilir (resumable) oldukları için durum bilgisi içerirler

# -----------------------------------------------------------------
# 🔬 Frame İçeriği — Örnek İnceleme
# -----------------------------------------------------------------

print("Fonksiyon adı:", frame.f_code.co_name)             # Çalışan fonksiyon adı
print("Yerel değişkenler:", frame.f_locals)               # Locals sözlüğü
print("Global değişkenler:", list(frame.f_globals)[:5])   # İlk 5 global isim
print("Önceki frame:", frame.f_back.f_code.co_name if frame.f_back else "Yok")
print("Satır numarası:", frame.f_lineno)
print("Son opcode indexi:", frame.f_lasti)
print("Trace fonksiyonu:", frame.f_trace)

# -----------------------------------------------------------------
# 🔁 Frame Zinciri Gezinme — Derinlik Kontrollü
# -----------------------------------------------------------------

depth = 0
while frame:
    print(f"{depth}. Frame: {frame.f_code.co_name} @ line {frame.f_lineno}")
    frame = frame.f_back
    depth += 1
    if depth > 20: break  # Sonsuz döngü engeli

# -----------------------------------------------------------------
# 🧠 MEMORY & GC — Frame Nesneleri Hafızada Kalıcı Olabilir
# -----------------------------------------------------------------

# 🔥 inspect.currentframe() gibi introspection işlemleri,
#     Python’un normalden farklı davranmasına yol açabilir.

# ❗ Frame zinciri kendini referanslayabilir → döngü oluşur
#     ➤ Bu durumda GC (Garbage Collector) frame'leri temizleyemeyebilir
#     ➤ Manuel olarak `del frame` ile temizlemek gerekebilir

# -----------------------------------------------------------------
# ⚠️ GECİKME SORUNU:
# - f_locals her zaman güncel olmayabilir
# - Özellikle generator ve async fonksiyonlarda state değişimi sırasında dikkatli olunmalıdır

# -----------------------------------------------------------------
# ❓ INSPECT MODÜLÜ ŞART MI?
# -----------------------------------------------------------------

# 🔎 Soru: `inspect` tek yol mu? Frame’e onsuz ulaşabilir miyiz?

# 🧠 Cevap: `inspect` sadece bir arayüzdür.
#     Asıl erişim `sys._getframe()` fonksiyonu üzerinden gerçekleşir. (CPython'a özel)

# ✅ Yani `inspect.currentframe()` aslında şu şekilde tanımlanır:
#     inspect.currentframe = lambda: sys._getframe(0)

import sys
f = sys._getframe(0)   # 👈 Bu da aynı frame’e ulaşır
print("Sys üzerinden frame:", f.f_code.co_name)

# ⚠️ Not:
#     sys._getframe() CPython’a özgüdür → diğer Python yorumlayıcılarda çalışmayabilir
#     Özellikle Jython, IronPython, PyPy gibi alternatiflerde desteklenmeyebilir.

# -----------------------------------------------------------------
# 🎯 CO_TYPE (code object) ÜZERİNDEN FRAME BİLGİSİNE ULAŞAMAYIZ
# -----------------------------------------------------------------

# ❌ CodeType nesneleri (f_code) içinde frame yoktur!
#     ➤ Bunlar sadece fonksiyonun "ham derlenmiş" halidir
#     ➤ Değişkenler, yürütme konumu, f_back gibi bilgiler burada bulunmaz

# ✅ Frame ise "çalışma anı nesnesi"dir — yani runtime oluşur
#     ➤ Sadece çalıştırılan kod sırasında erişilebilir
#     ➤ Derlenmiş (bytecode) nesnede frame bilgisi **yoktur**

# 🔍 f_code sadece şunları içerir:
#     • co_name → fonksiyon adı
#     • co_filename → kaynak dosya
#     • co_firstlineno → başlangıç satırı
#     • co_varnames → argüman ve lokal isimler
#     • co_consts → sabitler
#     ➤ Ama yürütme durumu (line, stack, back...) içermez ❗

# -----------------------------------------------------------------
# ✅ SONUÇ:
# -----------------------------------------------------------------

# ✅ Python çalışma zamanı, her fonksiyon ve context için bir frame oluşturur
# ✅ Bu frame'ler zincir halinde call stack’te tutulur
# ✅ inspect veya sys._getframe() ile bu yapılara erişebiliriz
# ✅ Frame, derlenmiş kod nesnesinden (code object) farklıdır:
#     ➤ code → statik (ne yapılacak)
#     ➤ frame → dinamik (ne zaman, nerede, kimle)

# 🔐 Gelişmiş introspection / debugging / tracing işlemleri için frame yapıları kritik önemdedir

# 💡 Performans ve temizlik açısından dikkatli kullanılmalı
#     Özellikle introspection sonrası `del frame` ile manuel bellek yönetimi yapılmalıdır

# 🔥 İleri seviye Python geliştiricileri için bu bilgiler:
#     ➤ Profiling
#     ➤ Debugging araçları
#     ➤ Özel traceback ve log sistemleri
#     gibi alanlarda büyük avantaj sağlar
