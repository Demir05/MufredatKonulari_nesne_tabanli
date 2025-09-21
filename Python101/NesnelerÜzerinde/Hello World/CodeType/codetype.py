# 🧩 CodeType Nedir?
# ------------------------------------------------------------
# • CodeType, Python'un "derlenmiş kod nesnesini" temsil eden dahili bir sınıftır.
# • Bir Python fonksiyonu, modülü veya lambda ifadesi derlendiğinde
#   ortaya çıkan sonuç aslında bir CodeType örneğidir.
# • Yani CodeType = Python kaynak kodunun bytecode ve tüm bağlam bilgileriyle
#   paketlenmiş hali. 📦

# ------------------------------------------------------------
# 📌 Neden Python'da Bir Karşılığı Var?
# • Çünkü Python "her şey nesnedir" felsefesini izler. 🔑
# • Derlenmiş kod bile bir nesneye dönüştürülür → bu da CodeType.
# • Bu sayede derlenmiş kod introspection (kendini inceleme) ile erişilebilir,
#   manipüle edilebilir, serialize edilip dosyaya yazılabilir (.pyc).
# • Interpreter, çalıştıracağı bytecode'u doğrudan CodeType içinden alır.

# ------------------------------------------------------------
# ⚙️ CodeType İçinde Neler Var?
# • .co_code      → ham bytecode (opcode'ların byte dizisi)
# • .co_consts    → fonksiyonun sabitleri (sayısal değerler, stringler, inner function'lar)
# • .co_varnames  → yerel değişkenlerin isimleri
# • .co_names     → global isimler (print, range gibi çağrılar)
# • .co_firstlineno → kaynak dosyadaki ilk satır numarası
# • .co_filename  → kodun geldiği dosya adı
# • .co_flags     → fonksiyon tipi bayrakları (generator, coroutine, async vb.)
# • ve daha fazlası (co_freevars, co_cellvars...) closure ve scope yönetimi için vardır. 🧩

# ------------------------------------------------------------
# 🎯 Kullanım Alanları
# • Debugging: Bir fonksiyonun bytecode'unu incelemek için.
# • Performans Analizi: Hangi opcode'ların üretildiğini görmek için.
# • Eğitim: Python'un derleme aşamalarını anlamak için.
# • Meta-programlama: compile() ile üretilen CodeType nesnesini
#   dinamik olarak çalıştırmak veya manipüle etmek için.
# • Araç geliştirme: dis, tracemalloc, coverage gibi modüller
#   CodeType üzerinden analiz yapar. 🔍

# ------------------------------------------------------------
# 🔍 Interpreter ile İlişkisi
# • Interpreter, Python kodunu çalıştırırken doğrudan CodeType içindeki
#   .co_code alanını kullanır.
# • Yani eval loop (ceval.c) → CodeType.co_code içindeki byte’ları okur
#   ve her opcode'u sırasıyla yürütür.
# • Bu nedenle CodeType, kaynak kod ile interpreter arasında
#   köprü görevi görür. 🌉

# ------------------------------------------------------------
# 💡 Özet
# • CodeType = Derlenmiş Python kodunun resmi temsilcisi.
# • İçinde bytecode + sabitler + değişken isimleri + bağlam bilgisi saklanır.
# • Interpreter bunu yürütür, biz de dis veya introspection yoluyla inceleyebiliriz.
# • Python’un "her şey bir nesnedir" yaklaşımının bytecode seviyesindeki karşılığıdır.
