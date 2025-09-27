import dis

# 🧩 dis.opname
# ------------------------------------------------------------
# Tüm opcode’ların isimlerini içeren bir liste.
# Her indeks, bir opcode’un sayısal değerini temsil eder.
# Bu liste sayesinde bytecode çıktısındaki sayısal opcode’ları okunabilir hale getirebiliriz.
# Genellikle dis.get_instructions() veya dis.Bytecode() ile elde edilen opcode değerlerini çözümlemek için kullanılır.
# Örneğin: dis.opname[100] → 'LOAD_CONST'
print(dis.opname[100])  # Sabit değer yükleme komutu

# 🧩 dis.opmap
# ------------------------------------------------------------
# Opcode isimlerini sayısal bytecode değerlerine eşleyen bir sözlük.
# dis.opname’in tersidir: burada isimden sayıya geçilir.
# Özellikle opcode filtreleme, karşılaştırma ve özel bytecode üretimi için kullanılır.
# Örneğin: dis.opmap['RETURN_VALUE'] → 83
print(dis.opmap['LOAD_FAST'])  # Yerel değişkeni yükleme komutu

# 🧩 dis.COMPILER_FLAG_NAMES
# ------------------------------------------------------------
# Derleyici bayraklarının sayısal değerlerini açıklayan bir sözlük.
# Python derleyicisi bazı fonksiyonlara özel bayraklar ekler: generator, async, nested gibi.
# Bu bayraklar kod nesnesinin co_flags alanında tutulur.
# Örneğin: dis.COMPILER_FLAG_NAMES[64] → 'CO_GENERATOR'
print(dis.COMPILER_FLAG_NAMES[64])  # Generator fonksiyon bayrağı

# 🧩 dis.hasconst
# ------------------------------------------------------------
# Sabit değerle çalışan opcode’ların listesi.
# Bu opcode’lar genellikle co_consts tablosuyla etkileşim kurar.
# Sabit yükleme, karşılaştırma, sabit dönüş gibi işlemleri içerir.
# Örneğin: LOAD_CONST, RETURN_CONST
print(100 in dis.hasconst)  # True → LOAD_CONST sabit kullanıyor

# 🧩 dis.hasname
# ------------------------------------------------------------
# İsim tablosuna erişen opcode’ların listesi.
# co_names üzerinden çalışan komutları tanımak için kullanılır.
# Global isimler, fonksiyonlar, modül düzeyindeki değişkenler bu tabloya girer.
# Örneğin: LOAD_NAME, STORE_NAME, DELETE_NAME
print(dis.opmap['LOAD_NAME'] in dis.hasname)  # True → isimle çalışıyor

# 🧩 dis.haslocal
# ------------------------------------------------------------
# Yerel değişkenlerle çalışan opcode’ların listesi.
# co_varnames üzerinden işlem yapan komutları ayırt etmek için kullanılır.
# Fonksiyon içindeki değişkenler burada tutulur.
# Örneğin: LOAD_FAST, STORE_FAST
print(dis.opmap['LOAD_FAST'] in dis.haslocal)  # True → yerel değişkenle çalışıyor

# 🧩 dis.hasjrel & dis.hasjabs
# ------------------------------------------------------------
# Atlama (jump) komutlarını sınıflandırır:
# - hasjrel: göreli atlama (offset’e göre)
# - hasjabs: mutlak atlama (doğrudan hedef adres)
# Döngü, koşul ve hata yakalama bloklarında kullanılır.
# Örneğin: FOR_ITER, JUMP_FORWARD, JUMP_ABSOLUTE
print(dis.opmap['FOR_ITER'] in dis.hasjrel)  # True → döngü adımı göreli atlama içeriyor

# 🧩 dis.hascompare
# ------------------------------------------------------------
# Karşılaştırma yapan opcode’ların listesi.
# Koşul ifadeleri ve boolean mantık işlemlerini analiz etmek için kullanılır.
# Örneğin: COMPARE_OP → ==, <, > gibi işlemler
print(dis.opmap['COMPARE_OP'] in dis.hascompare)  # True → karşılaştırma komutu


# 🧩 dis.Instruction
# ------------------------------------------------------------
# dis.get_instructions() çıktısındaki her satırı temsil eden veri yapısı.
# Özellikleri:
# - opname: komutun adı (örneğin 'LOAD_FAST')
# - opcode: sayısal değeri (örneğin 124)
# - arg: argüman indeksi (örneğin 0)
# - argval: argümanın gerçek değeri (örneğin 'x')
# - offset: bytecode içindeki konumu
# - starts_line: kaynak kod satırı
# - is_jump_target: atlama hedefi mi?
for instr in dis.get_instructions(örnek):
    print(instr.opname, instr.argval, instr.offset)

# 🧩 dis.show_code(obj)
# ------------------------------------------------------------
# Hem kod nesnesinin yapısını hem de bytecode’unu birlikte gösterir.
# Özellikle REPL veya terminalde hızlı analiz için kullanılır.
# Kodun argümanları, sabitleri, isimleri ve bytecode’u tek ekranda görünür.
dis.show_code(örnek)

# 🧩 dis.code_info(obj)
# ------------------------------------------------------------
# Kod nesnesi hakkında özet bilgi verir.
# Argüman sayısı, değişkenler, sabitler, isimler gibi meta verileri içerir.
# Özellikle kod nesnesinin yapısını anlamak için kullanılır.
print(dis.code_info(örnek))
