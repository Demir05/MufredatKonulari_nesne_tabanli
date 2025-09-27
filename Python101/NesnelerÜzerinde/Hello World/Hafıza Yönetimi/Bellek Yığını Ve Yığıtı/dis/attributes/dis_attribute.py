# 🧩 dis.dis(obj, *, file=None, depth=None)
# ------------------------------------------------------------
# Python’un disassembler modülündeki en temel fonksiyondur.
# Verilen bir nesnenin (fonksiyon, sınıf, modül, lambda, coroutine, generator, code object)
# CPython yorumlayıcısı tarafından nasıl çalıştırıldığını gösteren **bytecode çıktısını** üretir.

# 🔍 Fonksiyonun Amacı:
# - Python kodunun görünmeyen alt katmanını açığa çıkarmak
# - Kodun nasıl derlendiğini ve yorumlandığını satır satır analiz etmek
# - Performans, optimizasyon ve hata ayıklama süreçlerinde derin içgörü sağlamak

# ⚙️ Parametreler:
# - obj     : Disassemble edilecek nesne. Fonksiyon, yöntem, sınıf, modül, lambda, coroutine, generator, code object olabilir.
# - file    : Çıktının yazılacağı dosya nesnesi (varsayılan: sys.stdout). Terminal dışına yönlendirme için kullanılır.
# - depth   : İç içe tanımlanmış fonksiyonlar, lambdalar veya kapsanan code object’ler için kaç seviye derinliğe kadar analiz yapılacağı.

# 📤 Çıktı Formatı:
# - Satır numarası (kaynak koddaki)
# - Bytecode offset (komutun konumu)
# - Opcode adı (örneğin LOAD_FAST, CALL, RETURN_VALUE)
# - Argüman değeri (varsa)
# - Hedef adres (atlama komutlarında)
# - Exception table (Python 3.11+ için hata yakalama blokları)
#<satır numarası>   <bytecode offset>   <opcode adı>   <arg> (<argval>)

# 🛠️ Kullanım Alanları:
# - 🔎 Kod analizi: Karmaşık yapıları (closure, async, generator) çözümlemek
# - 🧪 Performans ve optimizasyon: Gereksiz opcode’ları tespit etmek, verimli derlemeyi incelemek
# - 🐞 Debugging: Hatalı davranışların nedenini bytecode düzeyinde anlamak
# - 🧬 Meta-programlama: Derleyici mantığını taklit etmek, DSL sistemleri kurmak
# - 🎓 Eğitim: Python’un yorumlayıcı mantığını öğretmek

# 🖨️ Tipik Kullanım:
# import dis
# def example(x): return x + 1
# dis.dis(example)

# 🎯 Özet:
# dis.dis(), Python’un görünmeyen “makine dili”ni açığa çıkarır.
# Kodun ne yaptığı değil, nasıl yaptığı da artık senin kontrolünde olur.


# 🧠 OpCode (Operation Code), Python yorumlayıcısının çalıştırdığı en düşük seviyeli komutlardır.
# Python kodu önce derlenir → bir ara dil olan bytecode’a çevrilir → bu bytecode, opcode’lardan oluşur.
# CPython yorumlayıcısı bu opcode’ları bir sanal makine gibi satır satır yürütür.
# Her opcode, belirli bir işlemi temsil eder: veri yükleme, fonksiyon çağırma, döngü yürütme, vs.
# Python 3.6+ ile birlikte bytecode artık "wordcode" formatındadır: her opcode sabit uzunluktadır.


# 🔹 LOAD_CONST
# Sabit bir değeri (örneğin 42, "merhaba", None) stack’e yükler.
# Kullanım: x = 42 → önce 42 sabiti yüklenir.

# 🔹 LOAD_FAST
# Yerel bir değişkeni stack’e yükler.
# Kullanım: return x → x değişkeni yüklenir.

# 🔹 STORE_FAST
# Stack’teki değeri yerel bir değişkene atar.
# Kullanım: x = 5 → 5 değeri stack’ten alınır ve x’e atanır.

# 🔹 LOAD_GLOBAL
# Global bir ismi stack’e yükler (örneğin print, len).
# Kullanım: print("selam") → print fonksiyonu yüklenir.

# 🔹 CALL / CALL_FUNCTION
# Stack’teki argümanlarla fonksiyon çağırır.
# Kullanım: len("abc") → len fonksiyonu çağrılır.

# 🔹 RETURN_VALUE / RETURN_CONST
# Fonksiyondan dönüş yapılır.
# Kullanım: return x → x stack’ten alınır ve döndürülür.

# 🔹 POP_TOP
# Stack’in en üstündeki değeri atar.
# Kullanım: 3 + 4 → sonuç kullanılmazsa atılır.

# 🔹 COMPARE_OP
# İki değeri karşılaştırır (==, <, >, vs.)
# Kullanım: x == 5 → karşılaştırma yapılır.

# 🔹 GET_ITER
# Bir iterable nesne üzerinden iterator başlatır.
# Kullanım: for i in range(3) → range objesi iterator’a çevrilir.

# 🔹 FOR_ITER
# Iterator’dan bir sonraki değeri alır, döngü adımını yürütür.
# Kullanım: for döngüsü içinde her adımda çalışır.

# 🔹 JUMP_FORWARD / JUMP_BACKWARD
# Bytecode içinde ileri veya geri atlama yapar.
# Kullanım: döngü, if, try gibi kontrol yapılarında kullanılır.

# 🔹 BUILD_LIST
# Yeni bir liste oluşturur.
# Kullanım: [i for i in range(10)] → boş liste başlatılır.

# 🔹 LIST_APPEND
# Stack’teki değeri listeye ekler.
# Kullanım: comprehension içinde her adımda çağrılır.

# 🔹 UNPACK_SEQUENCE
# Tuple veya listeyi parçalayıp değişkenlere dağıtır.
# Kullanım: a, b = (1, 2) → a ve b’ye ayrı ayrı atanır.

# 🔹 RESUME (Python 3.11+)
# Kod bloğunu başlatır veya devam ettirir.
# Kullanım: fonksiyon, generator, async gibi yapılarda başlangıç komutu.

# 🔹 SWAP
# Stack’teki iki değerin yerini değiştirir.
# Kullanım: bazı içsel dönüşümlerde kullanılır.

# 🔹 STORE_FAST_LOAD_FAST (optimize edilmiş birleşik komut)
# Aynı anda hem değişkeni atar hem yükler.
# Kullanım: comprehension gibi yoğun döngülerde performans için.

# 🔹 RERAISE
# Exception’ı yeniden fırlatır.
# Kullanım: try-except bloklarında hata zincirini korumak için.

# 🔹 END_FOR
# for döngüsünün sonlandığını belirtir.
# Kullanım: döngü tamamlandığında çağrılır.
