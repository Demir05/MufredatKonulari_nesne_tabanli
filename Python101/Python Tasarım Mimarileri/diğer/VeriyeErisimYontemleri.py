# ===============================
# 📘 VERİ ERİŞİMİ & EVALUATION TİPLERİ
# ===============================


# --------------------------------------
# 🔹 LOOKUP – Veri Bulma İşlemleri
# --------------------------------------

# LookUp, bir veri yapısında bir anahtar, indeks veya koşula göre veri arama işlemidir.
# Bu işlem, listelerde eleman kontrolü, sözlüklerde anahtar veya değer arama gibi şekillerde uygulanabilir.
# Performansı, kullanılan veri yapısına bağlıdır.

# 🎯 Amaç: Belirli bir veriye erişmek

veri = ["demir", "aslı", "ozan"]
"demir" in veri  # Genel bir lookup işlemi (O(n))



# --------------------------------------
# 🔹 DIRECT LOOKUP – Doğrudan Erişim
# --------------------------------------

# Direct lookup, bir veri yapısında indeks veya anahtar gibi sabit referans noktalarıyla veriye doğrudan ulaşmaktır.
# Arama yapılmaz, dolayısıyla çok hızlıdır (O(1)).
# Listelerde indeks, dict'lerde key kullanılır.

# 🎯 Amaç: Veriye direkt ulaşmak

dict_ = dict(isim="demir", yas=20)
veri = ["demir", "aslı", "ozan"]

isim = dict_["isim"]       # dict key lookup (O(1))
yas = dict_.get("yas")     # alternatif key lookup
ikinci = veri[1]           # list index lookup (O(1))
anahtar_var_mi = "isim" in dict_  # hashing ile hızlı kontrol (O(1))



# --------------------------------------
# 🔹 LOOKUP TABLE – Hızlandırılmış Tablo
# --------------------------------------

# Lookup table, sık erişilecek verileri saklayan, doğrudan erişimi mümkün kılan özel veri yapılarıdır.
# Genellikle dict veya list olarak hazırlanır.
# Amaç, arama süresini sıfıra yakın hale getirmektir.

# 🎯 Amaç: Lookup işlemlerini hızlandırmak

gunler = {
    1: "Pazartesi",
    2: "Salı",
    3: "Çarşamba",
}
print(gunler[1])  # Direct lookup ile erişim



# --------------------------------------
# 🔹 METADATA LOOKUP – Üstveri Erişimi
# --------------------------------------

# Metadata, verinin kendisi değil, veriye dair yapısal ve tanımsal bilgilerdir.
# Metadata lookup ise bu bilgilere erişmektir (örneğin: türü, uzunluğu, özellikleri).
# Meta = hakkında, Data = veri → "veri hakkında bilgi"

# 🎯 Amaç: Veri hakkında veri elde etmek

liste = [1, 2, 3]
uzunluk = len(liste)             # metadata: eleman sayısı
tip = type(liste)                # metadata: veri tipi
ozellik_var_mi = hasattr(liste, "append")  # metadata: metot kontrolü



# --------------------------------------
# 🔹 LAZY EVALUATION – Tembel Hesaplama
# --------------------------------------

# Lazy Evaluation, bir ifade ancak gerektiğinde kullanıldığında hesaplanır.
# Bu yaklaşım, belleği ve işlemciyi verimli kullanmak için tercih edilir.
# Büyük veri kümeleri veya sürekli veri akışı için idealdir.
# Felsefesi: üret -> kullan -> unut

# 🎯 Amaç: Belleği verimli kullanmak

gen = (x * 2 for x in range(1, 10))  # generator expression (lazy)
toplam = sum(len(k) for k in dict_ if isinstance(k, str))  # sadece ihtiyaç olduğunda hesaplanır



# --------------------------------------
# 🔹 EAGER EVALUATION – Hemen Hesaplama
# --------------------------------------

# Eager Evaluation, bir ifadenin sonucu hemen hesaplanır ve saklanır.
# Avantajı veriye hızlı erişim, dezavantajı ise daha fazla bellek tüketimidir.
# Felsefesi: üret -> sakla -> kullan

# 🎯 Amaç: Hızlı kullanım ve veri manipülasyonu

liste = [i for i in range(10)]       # list comprehension (eager)
m = max([1, 12, 31, 4324, 24])       # eager olarak hesaplanır
[print(i) for i in range(3)]         # çıktılar anında hesaplanır



# ---------------


# =============================================
# 📘 PYTHON'DA LOOKUP – PERFORMANS VE YAPI FARKLARI
# =============================================


# 🔹 A) Lookup Zaman Karmaşıklığı
# ---------------------------------------------
# Farklı veri yapılarında `in`, `[]`, `.get()` gibi lookup işlemleri farklı hızlara sahiptir.

# Zaman karmaşıklığı tablosu:

# List:       x in my_list               → O(n)     → yavaş
# Tuple:      x in my_tuple              → O(n)     → yavaş
# Set:        x in my_set                → O(1)     → hızlı
# Dict:       key in my_dict             → O(1)     → çok hızlı
# DictValue:  x in my_dict.values()      → O(n)     → yavaş
# String:     "x" in my_str              → O(n)     → orta
# Range:      x in range(...)            → O(1~n)   → optimize edilmiş
# Generator:  x in gen                   → O(n)     → tek yönlü tarama
# Pandas:     x in df["col"]             → O(n)     → vektörel arama


# 🔹 B) Lookup Optimizasyonları
# ---------------------------------------------
# Lookup işlemini hızlandırmak için doğru veri yapısı seçilmelidir.

# 🔸 Anahtar-tabanlı aramalarda:
# → dict  = hızlı anahtar eşlemesi

# 🔸 Üyelik kontrolünde:
# → set   = O(1) üyelik sorgusu

# 🔸 Sıralı ve hızlı arama gerekiyorsa:
# → sorted list + bisect = ikili arama (O(log n))

# 🔸 Çok büyük veri setleri:
# → Bloom Filter, Trie gibi yapılarda O(1~log n) bellek dostu lookup

# 🔸 Tablolu verilere erişimde:
# → pandas.Series ve df.query() performanslı çözümler sağlar


# 🔹 C) Lookup vs Search vs Filter
# ---------------------------------------------

# ➕ Lookup:
# → Belirli bir anahtar/indeks/eleman doğrudan var mı?
# → Tekil, sabit yapı – genellikle dict, set, list[index]

# Örnek:
dict_ = {"isim": "demir", "yas": 20}
print("isim" in dict_)  # True (key lookup)
print(dict_["yas"])     # 20 (direct access)


# ➕ Search:
# → Belirli bir koşulu sağlayan ilk öğeyi bulmak
# → Generator ve next() ile yapılır, erken çıkar

# Örnek:
liste = [4, 5, 10, 20]
ilk_cift = next((x for x in liste if x % 2 == 0), None)
print(ilk_cift)  # 4


# ➕ Filter:
# → Koşulu sağlayan tüm elemanları bulmak
# → Yeni bir koleksiyon döner (list, set, gen)

# Örnek:
filtreli = [x for x in liste if x > 5]
print(filtreli)  # [10, 20]


# 🔸 Kıyas Özeti:

# Lookup:    → Tek değer → hızlı → sabit erişim → "x in my_dict"
# Search:    → Koşul → ilk eşleşme → generator → "next(...)"
# Filter:    → Koşul → çoklu eşleşme → list comp. → "[x for x in ...]"

