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

# ──────────────────────────────────────────────────────────────
# 🧠 CodeType Sınıfının Descriptor Tabanlı Mimari Yapısı
# ──────────────────────────────────────────────────────────────

# CodeType sınıfı, CPython yorumlayıcısında C diliyle tanımlanmış yerleşik bir sınıftır.
# Bu nedenle sahip olduğu attribute'ların çoğu descriptor tabanlıdır.
# Descriptor kullanımı, attribute erişimini hızlandırmak ve daha kontrollü hale getirmek için tercih edilir.

# Bu descriptor'lar arasında member descriptor da bulunur.
# Normalde Python sınıflarında __slots__ tanımlandığında member descriptor oluşur.
# Ancak CodeType gibi C tabanlı sınıflarda __slots__ bulunmaz.
# Bunun yerine CPython, attribute tanımları için PyMemberDef adlı özel bir C yapısı kullanır.

# Örneğin co_code, co_name gibi attribute'lara eriştiğimizde descriptor protokolü devreye girer.
# Bu attribute'lar data descriptor olarak tanımlanmıştır — yani hem __get__ hem __set__ metoduna sahiptirler.
# Ancak CodeType sınıfı immutable olduğu için bu attribute'lar doğrudan değiştirilemez.
# __set__ metodunun varlığı, bu attribute'ların manipüle edilebilir olması için değil,
# attribute çözümlemesinde (lookup) öncelik kazanması içindir.

# Data descriptor'lar, Python'da attribute çözümleme sıralamasında en yüksek önceliğe sahiptir.
# Bu sayede instance seviyesindeki değerler override edilemez (shadowing engellenir).
# Ayrıca yorumlayıcı daha az opcode yürütür, eval-loop daha az çalışır ve performans artar.

# Sonuç olarak, CodeType sınıfındaki attribute'lar descriptor olsa bile,
# __set__ metodunun varlığı, doğrudan atama için değil — çözümleme sırasında öncelik kazanmak içindir.

"""
__new__ ------> <class 'builtin_function_or_method'> __set__: False
__repr__ ------> <class 'wrapper_descriptor'> __set__: False
__hash__ ------> <class 'wrapper_descriptor'> __set__: False
__lt__ ------> <class 'wrapper_descriptor'> __set__: False
__le__ ------> <class 'wrapper_descriptor'> __set__: False
__eq__ ------> <class 'wrapper_descriptor'> __set__: False
__ne__ ------> <class 'wrapper_descriptor'> __set__: False
__gt__ ------> <class 'wrapper_descriptor'> __set__: False
__ge__ ------> <class 'wrapper_descriptor'> __set__: False
__sizeof__ ------> <class 'method_descriptor'> __set__: False
co_lines ------> <class 'method_descriptor'> __set__: False
co_positions ------> <class 'method_descriptor'> __set__: False
replace ------> <class 'method_descriptor'> __set__: False
_varname_from_oparg ------> <class 'method_descriptor'> __set__: False
__replace__ ------> <class 'method_descriptor'> __set__: False
co_argcount ------> <class 'member_descriptor'> __set__: True
co_posonlyargcount ------> <class 'member_descriptor'> __set__: True
co_kwonlyargcount ------> <class 'member_descriptor'> __set__: True
co_stacksize ------> <class 'member_descriptor'> __set__: True
co_flags ------> <class 'member_descriptor'> __set__: True
co_nlocals ------> <class 'member_descriptor'> __set__: True
co_consts ------> <class 'member_descriptor'> __set__: True
co_names ------> <class 'member_descriptor'> __set__: True
co_filename ------> <class 'member_descriptor'> __set__: True
co_name ------> <class 'member_descriptor'> __set__: True
co_qualname ------> <class 'member_descriptor'> __set__: True
co_firstlineno ------> <class 'member_descriptor'> __set__: True
co_linetable ------> <class 'member_descriptor'> __set__: True
co_exceptiontable ------> <class 'member_descriptor'> __set__: True
co_lnotab ------> <class 'getset_descriptor'> __set__: True
_co_code_adaptive ------> <class 'getset_descriptor'> __set__: True
co_varnames ------> <class 'getset_descriptor'> __set__: True
co_cellvars ------> <class 'getset_descriptor'> __set__: True
co_freevars ------> <class 'getset_descriptor'> __set__: True
co_code ------> <class 'getset_descriptor'> __set__: True
__doc__ ------> <class 'str'> __set__: False

"""

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
