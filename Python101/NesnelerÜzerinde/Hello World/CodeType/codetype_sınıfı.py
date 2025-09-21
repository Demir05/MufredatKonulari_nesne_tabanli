import types

# 🧩 CodeType Sınıfı Nedir?
# ------------------------------------------------------------
# • CodeType, Python’da derlenmiş kod nesnelerini temsil eden sınıftır.
# • Python’un compile aşamasında ürettiği “code object”ler aslında bu sınıfın örnekleridir.
# • Bu sınıf Python kodunun bytecode, sabitler, değişkenler ve tüm bağlam bilgilerini saklar.
# • Interpreter, çalıştırma sırasında CodeType içindeki bytecode’u yürütür.

# ------------------------------------------------------------
# 📌 Nerede Bulunur?
# • types modülünde: types.CodeType
# • Bir fonksiyonun __code__ attribute’u doğrudan bir CodeType örneğidir.
# • Doğrudan oluşturmak çok nadirdir (düşük seviye, genellikle compile() tercih edilir).
# • __code__, sadece yürütülebilir kod bloklarını temsil eder.

# ------------------------------------------------------------
# ⚙️ Önemli Özellikler (Attributes)
# • co_code      → ham bytecode (opcode’ların byte dizisi)
# • co_consts    → fonksiyonun sabitleri (ör: None, sayılar, stringler, iç fonksiyonlar)
# • co_varnames  → yerel değişken adları
# • co_names     → global isimler (print, range, vb.)
# • co_filename  → kodun geldiği dosya adı
# • co_firstlineno → kaynak dosyadaki ilk satır numarası
# • co_flags     → fonksiyon tipini tanımlayan bayraklar (ör: generator, async)
# • co_freevars / co_cellvars → closure değişkenleri için kullanılır
# • ve daha fazlası (co_stacksize, co_nlocals, co_lnotab...)

# ------------------------------------------------------------
# 🎯 Kullanım Alanları
# • Debugging: derlenmiş kodu analiz etmek.
# • Performans incelemesi: hangi opcode’ların üretildiğini görmek.
# • Eğitim: Python’un çalışma mantığını öğrenmek.
# • Meta-programlama: compile() ile yeni CodeType nesneleri üretip eval/exec ile çalıştırmak.
# • Araç geliştirme: dis, tracemalloc, coverage gibi modüller CodeType üzerinden çalışır.

# ------------------------------------------------------------
# 💡 Özet
# • CodeType = Python kaynak kodunun derlenmiş hali.
# • Interpreter → CodeType içindeki co_code’u çalıştırır.
# • Biz → introspection ve dis modülüyle bu nesneyi analiz edebiliriz.

# ------------------------------------------------------------
# 🧪 Örnek: Bir Fonksiyondan CodeType Elde Etmek
def topla(a, b):
    return a + b

code_obj = topla.__code__

print(type(code_obj))             # <class 'code'>
print(isinstance(code_obj, types.CodeType))  # True
print(code_obj.co_varnames)       # ('a', 'b')
print(code_obj.co_consts)         # (None,)
print(code_obj.co_code)           # b'|\x00|\x01\x17\x00S\x00'
