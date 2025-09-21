# ✅ Python Çalışma Zamanı: Stack & Frame Katmanları

# 🔹 Python kodu çalıştığında her bir "çağrı" için bir frame (yığın katmanı) oluşturulur
# 🔹 Bu frame'ler çağrı yığını (call stack) üzerinde sıralanır
# 🔹 Frame, çalışmakta olan fonksiyonun bağlamını (context) tutar

# 🔻 Frame Türleri:

# 1️⃣ Main Frame
# - Script ilk çalıştığında oluşur
# - Global alanı temsil eder (modül düzeyindeki kodlar)
# - Programın giriş noktasıdır (`__main__`)
# - "globals()" gibi yapılar bu frame'e bağlıdır

# 2️⃣ Function Frame
# - Her fonksiyon çağrısında oluşturulur
# - İçinde:
#     • Yerel değişkenler (locals)
#     • Parametreler (args)
#     • Dönüş adresi (nereden çağrıldı)
#     • Üst frame referansı (parent)
#   gibi bilgiler saklanır
# - Fonksiyon bittiğinde bu frame, stack’ten çıkarılır

# 3️⃣ Generator / Coroutine Frame
# - `yield` veya `await` kullanan fonksiyonlar için oluşturulur
# - Duraklatılabilir, devam ettirilebilir
# - State (durum) bilgisi korunur, bu yüzden özel bir frame türüdür


import inspect

# 🔍 inspect.currentframe()
# - O anda çalışmakta olan frame nesnesini döner.
# - Genellikle introspection (öz gözlem) ve debugging için kullanılır.
frame = inspect.currentframe()

# 📌 frame.f_code
# - Bu frame'de çalıştırılan kod nesnesi (code object).
# - İçinde fonksiyon adı, dosya adı, ilk satır numarası gibi bilgiler bulunur.
# - Örn: frame.f_code.co_name → fonksiyon adı
print("Fonksiyon adı:", frame.f_code.co_name)

# ⚠️ İstisna:
# - Lambda fonksiyonlarda co_name → "<lambda>" olarak döner.
# - eval/exec gibi dinamik kodlarda anlamlı bir co_name olmayabilir.

# 📌 frame.f_locals
# - Bu frame içindeki yerel değişkenleri bir sözlük olarak döner.
# - Örn: {'x': 10, 'y': 'merhaba'}
print("Yerel değişkenler:", frame.f_locals)

# ⚠️ İstisna:
# - locals() ile birebir aynı değildir; bazı durumlarda gecikmeli güncellenebilir.
# - Özellikle generator/coroutine içinde state değişimi sırasında dikkatli kullanılmalı.

# 📌 frame.f_globals
# - Bu frame'in bağlı olduğu global alan (modül düzeyi değişkenler).
# - Genellikle main frame'de anlamlıdır.
print("Global değişkenler:", list(frame.f_globals.keys())[:5])  # ilk 5 global

# ⚠️ İstisna:
# - Eğer frame bir modül dışı ortamda oluşmuşsa (örneğin REPL, test runner), globals eksik veya farklı olabilir.

# 📌 frame.f_back
# - Bu frame'den önceki (çağıran) frame → bir nevi parent frame.
# - Call stack üzerinde geri gitmek için kullanılır.
print("Önceki frame:", frame.f_back.f_code.co_name if frame.f_back else "Yok")

# ⚠️ İstisna:
# - Zincirleme gezinirken sonsuz döngü riski olabilir → derinlik sınırı önerilir.
# - Bazı özel durumlarda (örneğin threading, async), f_back None olabilir.

# 📌 frame.f_lineno
# - Bu frame'de çalıştırılmakta olan satır numarası.
# - Dinamik olarak değişebilir (örneğin bir döngüde ilerlerken).
print("Satır numarası:", frame.f_lineno)

# ⚠️ İstisna:
# - Kod optimize edilmişse veya bytecode manipülasyonu varsa doğru satır numarası alınamayabilir.

# 📌 frame.f_lasti
# - Bytecode seviyesinde en son yürütülen opcode’un indeksidir.
# - Genellikle debugging veya bytecode analizinde kullanılır.
print("Son opcode indexi:", frame.f_lasti)

# ⚠️ İstisna:
# - Bu değer Python yorumlayıcısına özgüdür (CPython); diğer yorumlayıcılarda farklı davranabilir.
# - Yalnızca düşük seviyeli analizlerde anlamlıdır.

# 📌 frame.f_trace
# - Bu frame için atanmış özel trace fonksiyonu (profiling/debugging için).
# - sys.settrace() ile atanabilir.
print("Trace fonksiyonu:", frame.f_trace)

# ⚠️ İstisna:
# - Trace fonksiyonları performansı ciddi şekilde etkileyebilir.
# - Bazı ortamlar (örneğin Jupyter, IDE debugger) kendi trace fonksiyonlarını atayabilir → çakışma riski vardır.

# 🔁 Frame zinciriyle güvenli gezinme örneği:
depth = 0
while frame:
    print(f"{depth}. Frame: {frame.f_code.co_name} @ line {frame.f_lineno}")
    frame = frame.f_back
    depth += 1
    if depth > 20: break  # güvenlik sınırı

# ⚠️ Bellek yönetimi:
# - Frame nesneleri referans döngüsü oluşturabilir → GC tarafından temizlenmeyebilir.
# - Özellikle introspection araçlarında frame zinciri tutuluyorsa, manuel temizlik önerilir:
#   örn: del frame
