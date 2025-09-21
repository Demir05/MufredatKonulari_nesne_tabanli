import types, dis

def f(a, b):
    return a + b

orig = f.__code__

# 3.11+ alanlarını tek tek çekiyoruz
new_code = types.CodeType(
    orig.co_argcount,
    orig.co_posonlyargcount,
    orig.co_kwonlyargcount,
    orig.co_nlocals,
    orig.co_stacksize,
    orig.co_flags,
    orig.co_code,                 # ⚠️ ham bytecode'u aynen devralıyoruz
    orig.co_consts,
    orig.co_names,
    orig.co_varnames,
    "synthetic_file.py",          # ← co_filename'i değiştiriyoruz (örnek)
    "guncellenmis_f",             # ← co_name'i değiştiriyoruz (örnek)
    orig.co_qualname,
    orig.co_firstlineno,
    orig.co_linetable,            # 3.11+
    orig.co_exceptiontable,       # 3.11+
    orig.co_freevars,
    orig.co_cellvars,
)

# Bu "new_code" bir CodeType örneği:
print(type(new_code), new_code)

# Çalıştırmak için bir fonksiyon kabına sarabiliriz:
g = types.FunctionType(new_code, globals())
print(g(2, 3))  # 5

# İstersen bytecode'u gör:
print(dis.Bytecode(new_code).dis())


import types, dis

def h(x):
    return x * 2

c0 = h.__code__

# co_name ve co_filename'i güvenle değiştiriyoruz (diğer alanlar korunur)
c1 = c0.replace(co_name="ikiyle_carp", co_filename="virtual.py")

k = types.FunctionType(c1, globals())
print(k(10))  # 20

print(dis.Bytecode(c1).dis())


# 🧩 CodeType — Fonksiyon vs Modül Karşılaştırması (yorum satırlarıyla)
# =============================================================================
# Bu not, CodeType nesnesinin fonksiyon ve modül bağlamlarında nasıl göründüğünü
# yan yana anlatır. Tamamı yorum satırıdır; kopyala-oku-öğren. ✅

# -----------------------------------------------------------------------------
# 📌 Kısa Özet
# • Fonksiyon CodeType’ı: Çağrılabilir birimdir; ARGÜMAN ve LOKAL bilgileri doludur.
# • Modül CodeType’ı: Tüm dosyanın derlenmiş gövdesidir; argüman kavramı yoktur.
# • İkisi de bytecode’u (.co_code) ve metadatasını taşır; interpreter bu bytecode’u yürütür.

# -----------------------------------------------------------------------------
# 🧾 Ortak Temel Alanlar (ikisi de taşır)
# • co_code        → Ham bytecode baytları (opcode dizisi)
# • co_consts      → Sabitler havuzu (None, sayılar, stringler, iç code objeleri…)
# • co_names       → Global/isim havuzu (print, range, modül seviyesinde atanan isimler…)
# • co_filename    → Kaynak dosya adı
# • co_firstlineno → Kaynağın ilk satırı
# • co_stacksize   → VM yığın derinliği
# • co_flags       → Bayraklar (generator/coroutine/async gibi tür bilgileri)
# • (3.11+) co_linetable → Satır eşleme tablosu
# • (3.11+) co_exceptiontable → İstisna tablosu (zero-cost exception)
# • co_name / co_qualname → Kodun adı / nitelikli adı (modülde genelde "<module>")

# -----------------------------------------------------------------------------
# 📊 FONKSİYON vs MODÜL — Attribute Tablosu
# (🟢: tipik olarak dolu/önemli, ⚪: genelde 0/boş/ilgili değil)
#
# Attribute             | Fonksiyon CodeType                         | Modül CodeType
# ----------------------|---------------------------------------------|------------------------------
# co_argcount          | 🟢 Pozisyonel argüman sayısı                 | ⚪ 0 (modül çağrılmaz)
# co_posonlyargcount   | 🟢 Sadece pozisyonel arg sayısı (PEP 570)    | ⚪ 0
# co_kwonlyargcount    | 🟢 Sadece anahtar arg sayısı                 | ⚪ 0
# co_nlocals           | 🟢 Yerel değişken sayısı                     | ⚪ 0 (modül lokali yok; isimler global ad alanına gider)
# co_varnames          | 🟢 Yerel değişken adları (arg’lar dahil)     | ⚪ () (genelde boş)
# co_freevars          | 🟢 Closure serbest değişkenleri              | ⚪ () (tipik)
# co_cellvars          | 🟢 Closure hücre değişkenleri                | ⚪ () (tipik)
# co_consts            | 🟢 Sabitler (None, sayılar, inner code)      | 🟢 Sabitler (string sabitler, fonksiyon tanımları vb.)
# co_names             | 🟢 Global/attr isimleri                      | 🟢 Modül içindeki isimler (x, y, print…)
# co_code              | 🟢 Bytecode                                  | 🟢 Bytecode
# co_filename          | 🟢 Kaynak dosya adı                          | 🟢 Kaynak dosya adı
# co_firstlineno       | 🟢 İlk satır                                 | 🟢 İlk satır
# co_flags             | 🟢 Tür bayrakları (gen/async/coro vb.)       | 🟢 Genelde sıradan bayraklar (çağrılabilirlik yok)
# co_stacksize         | 🟢 VM yığın gereksinimi                      | 🟢 VM yığın gereksinimi
# (3.11+) co_linetable | 🟢 Satır eşleme                              | 🟢 Satır eşleme
# (3.11+) co_exceptiontable | 🟢 İstisna tablosu                      | 🟢 İstisna tablosu
# co_name              | 🟢 Fonksiyon adı ("foo")                     | 🟢 "<module>"
# co_qualname          | 🟢 Nitelikli isim (Cls.foo)                  | 🟢 "<module>"

# -----------------------------------------------------------------------------
# 🧠 Neden Modülde “argcount” yok?
# • Modül çağrılabilir değildir; import/çalıştırma sırasında “çağrı argümanı” almaz.
# • Bu yüzden co_argcount, co_kwonlyargcount, co_posonlyargcount → modülde 0’dır.
# • Modüldeki “x = 2” gibi satırlar, modülün co_code’unda opcode olarak yer alır
#   ve yürütülür; ama modül için ayrı “__code__” attribute’u kullanıcıya sunulmaz.
#   (İstersen compile(..., mode="exec") ile bu module-level CodeType’ı elde edebilirsin.)

# -----------------------------------------------------------------------------
# 🧩 Pratik İpuçları
# • Fonksiyonun derlenmiş koduna erişmek için: func.__code__  → types.CodeType
# • Modül gövdesi için CodeType görmek: compile(src, "<string>", "exec")
# • İnsan-dostu disassembly: dis.Bytecode(code_obj).dis()
# • Metadata’yı güvenle güncellemek: code_obj.replace(co_name="yeni_ad", ...)
# • Sürüm kırılgan ctor’dan kaçın: types.CodeType(...) yerine compile/replace tercih et.

# -----------------------------------------------------------------------------
# ✨ Mini Özet
# • Fonksiyon CodeType → “çağrılabilir” olduğundan argüman/lokal alanları doludur.
# • Modül CodeType → dosya gövdesinin derlenmiş halidir; argüman kavramı yoktur.
# • İkisinde de bytecode ve temel metadatalar vardır; interpreter .co_code’u yürütür.
