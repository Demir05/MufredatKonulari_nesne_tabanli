import dis

# 🧩 dis.Bytecode Sınıfı Nedir?
# ------------------------------------------------------------
# 🧠 dis.Bytecode Nedir?
# ------------------------------------------------------------
# • dis modülündeki "Bytecode" sınıfı; fonksiyon, code object veya kaynak kod dizesini
#   (compile edilmiş) alıp, bunların ürettiği Python bytecode’unu okunabilir bir biçimde
#   sunar.
# • "Gerçek çalışan" nesne değildir; çalıştırılan şey aslında types.CodeType’tır.
#   Bytecode, CodeType’ı "insan dostu" şekilde dolaşmana yardım eden BİR SARICI (wrapper) gibidir. 🎁
# • Bytecode nesnesi "iterable"dır: üzerinde dolaştığında her adımda bir Instruction döner.


# 🔁 "Her adım" ne demek?
# Bytecode, Python yorumlayıcısının çalıştırdığı talimatlar dizisidir.
# Bu dizideki her talimat bir opcode’dur → LOAD_FAST, RETURN_VALUE, vs.
# İşte bu opcode’ların her biri bir Instruction nesnesi olarak temsil edilir.

# ------------------------------------------------------------
# 🧪 Örnek Fonksiyon
def örnek(x):
    return x + 1

# ------------------------------------------------------------
# 🔍 Bytecode nesnesi oluşturuluyor
bc = dis.Bytecode(örnek)


# ------------------------------------------------------------
# 🔁 Bytecode Nesnesi Üzerinde Dolaşmak
# Her adımda bir Instruction nesnesi döner
for instr in bc:
    print(f"{instr.offset:<3} {instr.opname:<20} {instr.argrepr}")

# ------------------------------------------------------------
# 🛠️ dis.Bytecode Nerelerde Kullanılır?
# - Fonksiyonların nasıl çalıştığını analiz etmek
# - Performans optimizasyonu yapmak
# - Derleyici davranışını anlamak
# - Eğitim ve öğretim amaçlı bytecode çözümlemesi
# - Meta-programlama ve kod üretimi sistemlerinde


# 🧩 dis.Bytecode Instance Attribute'ları
# ============================================================


# 🧩 Bytecode.dis() Metodu
# ------------------------------------------------------------
# • dis.Bytecode sınıfına ait bir instance metodudur.
# • Amaç: ilgili Bytecode nesnesinin opcode’larını (Instruction’ları) ekrana basmak.
# • İçeride yaptığı iş: get_instructions() kullanarak Instruction listesi çıkarır,
#   ardından bu listeyi .show_offsets, .adaptive, .show_caches gibi instance attribute’larına
#   göre formatlar ve yazdırır.
# • Yani Bytecode.dis(), Bytecode sınıfının sunduğu özelleştirme imkanlarını kullanır. 🎛️
#
# Kullanım:
#   bc = dis.Bytecode(func)
#   bc.show_offsets = False
#   bc.dis()   # Özelleştirilmiş disassembly çıktısı

# ------------------------------------------------------------
# ⚖️ Farkları Özetleyelim
# ------------------------------------------------------------
# 1. dis.dis():
#    - Global fonksiyon
#    - Doğrudan get_instructions() çıktısını yazar
#    - Özelleştirme yok
#    - Döndürdüğü şey yok (None)
#    - Hızlı, tek seferlik inceleme için uygun
#
# 2. Bytecode.dis():
#    - Bytecode instance metodudur
#    - Aynı şekilde get_instructions()’a dayanır ama
#      instance attribute’larıyla çıktıyı kontrol edebilirsin
#      (show_offsets, adaptive, show_caches, flags…)
#    - Bytecode nesnesi üzerinde daha derin analiz yapabilirsin
#    - Eğitim, optimizasyon ve ileri seviye debugging için uygundur
#
# .codeobj
# 👉 Analiz edilen kod nesnesi (types.CodeType).
#    Asıl bytecode burada saklıdır: .co_code, .co_consts, .co_names...
#    Yani Bytecode'un kaynağı aslında buradadır.

# .first_line
# 👉 Fonksiyon veya kod bloğunun başladığı satır numarası.
#    Hata ayıklama ve doğru satır eşleme için kullanılır. 🐞

# ._line_offset   (private)
# 👉 Satır numaralarını hizalamak için kullanılan kaydırma değeri.
#    İç mekanizma için var; normal kullanıcı pek dokunmaz.

# ._linestarts   (private)
# 👉 Bytecode offset → kaynak satır eşlemesini tutar (dict).
#    Örn: {0: 1, 4: 2} → 0. byte satır 1, 4. byte satır 2.
#    Bu sayede Instruction.starts_line doldurulur. 📌

# ._original_object   (private)
# 👉 dis.Bytecode(...) içine verdiğin orijinal obje.
#    Fonksiyon, method, string olabilir. CodeType’a dönüştürülür
#    ama referans olarak burada saklanır. 🗂️

# .current_offset
# 👉 Iterable olarak dolaşırken şu anda hangi byte offset’inde olduğunu tutar.
#    for instr in bc: sırasında her adımda güncellenir. 🔁

# .exception_entries
# 👉 Python 3.11+ ile gelen exception handling tablosu.
#    try/except/finally bloklarının hangi offset’leri kapsadığını gösterir.
#    Zero-cost exception mekanizmasının parçası. ⚡

# .adaptive
# 👉 Python 3.11+ adaptive bytecode özelliği.
#    Runtime’da optimize edilmiş opcode varyantlarını da gösterir
#    (ör: LOAD_ATTR_ADAPTIVE). Yorumlayıcının hız optimizasyonlarını
#    çıplak gözle görmeni sağlar. 🔬

# .show_offsets
# 👉 Disassembly çıktısında offset değerlerini gösterip göstermeme seçeneği.
#    True → her instruction’ın offset’i görünür (0, 2, 4…).
#    False → sadece opcode isimlerini listeler. 👀

# ============================================================
# 💡 Özet:
# - Kullanıcıya dönük: .codeobj, .first_line, .show_caches, .adaptive, .show_offsets
# - Dahili/private: ._line_offset, ._linestarts, ._original_object,
#                   .current_offset, .exception_entries
# - Amaç: disassembly çıktısının satır numarası, cache, optimizasyon
#   ve offset bilgilerini kontrol etmek.
