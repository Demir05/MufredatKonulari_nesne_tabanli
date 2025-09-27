# 📚 globals() — SÖZEL/TEORİK TANIM (yorum satırlarıyla)
# -----------------------------------------------------------------------------
# 🧩 TANIM
# • globals(), içinde bulunduğun modülün “küresel isim tablosunu” (global symbol table)
#   canlı (live) bir sözlük (dict) olarak döndüren yerleşik (built-in) bir fonksiyondur.
# • Bu sözlükte anahtarlar değişken/isim, değerler ise o isimlere karşılık gelen nesnelerdir. 🧠

# -----------------------------------------------------------------------------
# 🧾 SÖZDİZİMİ
# • d = globals()  →  d, modülün global isimlerini tutan “CANLI” bir dict’tir.
# • d["NAME"] = value  →  modül düzeyinde NAME isimli global tanımlanır/değişir.
# • Not: “canlı” olduğu için sözlüğe yazmak, modülün global alanını anında etkiler. ⚡

# -----------------------------------------------------------------------------
# 🎯 AMACI NE?
# • Çalışma zamanında (runtime) modülün global isimlerine erişmek/eklemek/silmek.
# • Dinamik yapılandırma, eklenti (plugin) kaydı, REPL/debug gibi introspektif işlemler.
# • exec/eval gibi dinamik yürütmelere ortam (namespace) sağlamak. 🧰

# -----------------------------------------------------------------------------
# 🧪 KULLANIM ALANLARI
# • Dinamik nesne kaydı: global bir REGISTRY sözlüğüne fonksiyon/sınıf eklemek.
# • REPL/araç geliştirme: mevcut global isimleri listelemek veya manipüle etmek.
# • exec/eval ile kod çalıştırırken küresel ortamı açıkça vermek.
# • Basit script’lerde koşullu olarak global sabit/flag üretmek. ✨

# -----------------------------------------------------------------------------
# 🚧 DİKKAT EDİLMESİ GEREKENLER
# • Okunabilirlik: globals() ile “sihirli” isim yaratmak kodu takip etmeyi zorlaştırır.
# • Test edilebilirlik: Dinamik global ekleme testte yan etkiler doğurabilir.
# • Güvenlik: exec/eval + globals() kombinasyonu kullanıcı girdisiyle ASLA kullanılmamalı. 🔒
# • Performans: Global lookup, lokal erişime göre daha maliyetlidir; sıcak kodda tercih etmeyin.
# • Etki alanı: Fonksiyon içinden globals()["x"]=... yazmak modüle yazar (global anahtarı “x”
#   artık modülde belirir). Bu, “global x” deyip atamaya göre daha direkt ve yan etkili bir yoldur.

# -----------------------------------------------------------------------------
# 🧭 MODÜL DÜZEYİNDE ATTRİBUTE ATAMASI: module.__dict__ vs globals()
# • module.__dict__  → İSTEDİĞİN modülün isim tablosunu günceller (hedef modülü sen seçersin).
#   Örn: import types; m = types.ModuleType("m"); m.__dict__["X"]=1 ⇒ m.X == 1  ✅
# • globals()        → YALNIZCA “bulunduğun” modülün isim tablosunu döndürür.
#   Örn: globals()["X"]=1 ⇒ şu anki modülde X oluşur; başka modülü ETKİLEMEZ.
# • Kısacası: “Herhangi bir modülün” globalini değiştirmek istiyorsan module.__dict__ kullan;
#   “bulunduğun modül” için hızlı yol istiyorsan globals() kullan. 🎯

# -----------------------------------------------------------------------------
# 🧠 ÖZET
# • globals() = içinde bulunulan modülün canlı global isim sözlüğü.
# • Dinamik, güçlü ama dikkat ve disiplin ister: okunabilirlik, test ve güvenlik önemlidir. ✅
# • Başka bir modülün global’ini değiştirmek için module.__dict__ tercih edilir. 🔧

# -----------------------------------------------------------------------------
# ⛳ UYGULAMALAR (kod)
# Aşağıdaki örnekler yorum DEĞİL, çalıştırılabilir koddur.
# -----------------------------------------------------------------------------

# 1) Basit: Mevcut global isimlerin bir kısmını görmek
print("🔎 İlk 5 global isim:", list(globals())[:5])

# 2) Dinamik global eklemek (bulunduğun modüle)
globals()["DYNAMIC_FLAG"] = True
print("DYNAMIC_FLAG var mı?", "DYNAMIC_FLAG" in globals(), "→", DYNAMIC_FLAG)

# 3) Fonksiyon içinden modül global’i yazmak (global bildirimi olmadan)
def inject_global():
    globals()["INJECTED_VALUE"] = 42

inject_global()
print("INJECTED_VALUE:", INJECTED_VALUE)

# 4) exec ile küresel ortamı açıkça verme
code = "NEW_CONST = 999"
exec(code, globals())  # bu modülün global alanına yazar
print("NEW_CONST:", NEW_CONST)

# 5) Başka bir modülün global’ini değiştirmek: module.__dict__ kullan
import types
m = types.ModuleType("mymod")
m.__dict__["VERSION"] = "1.0.0"
print("m.VERSION:", m.VERSION)

# 6) Küçük bir plugin kaydı (dinamik isimle)
def hello():
    return "hello"

globals().setdefault("REGISTRY", {})["hello"] = hello
print("REGISTRY keys:", list(REGISTRY.keys()), "→ çağrı:", REGISTRY["hello"]())


# 📚 locals() — SÖZEL/TEORİK TANIM (yorum satırlarıyla)
# -----------------------------------------------------------------------------
# 🧩 TANIM
# • locals(), "içinde bulunduğun KAPSAMIN" (scope) yerel isim tablosunu döndüren yerleşik (built-in) bir fonksiyondur.
# • Dönen değer bir sözlüktür (dict gibi davranan bir eşleme): {isim → nesne}. 🧠
# • “Yerel” kavramı, bulunduğun yere göre değişir: modül, fonksiyon, sınıf gövdesi vb.

# -----------------------------------------------------------------------------
# 🧾 SÖZDİZİMİ
# • d = locals()           → d: mevcut scope’un canlı isim tablosu (çoğu durumda anlık görünüm) ⚡
# • d["name"] = value      → (kapsama BAĞLI OLARAK) yerel isim tablosuna yazmaya çalışır
#   NOT: Fonksiyon kapsamı içinde locals()’a yazmak, yerel değişkenleri güncellemek ZORUNDA DEĞİLDİR.
#        (Uygulama detayı; CPython’da genelde yansımaz.) Dikkat! ⚠️

# -----------------------------------------------------------------------------
# 🎯 AMACI NE?
# • İçinde bulunulan kapsamın isim-nesne eşlemesini görselleştirmek (debug / introspection).
# • eval/exec gibi dinamik yürütmelere “yerel ortam” sağlamak.

# -----------------------------------------------------------------------------
# 🧪 KULLANIM ALANLARI
# • Fonksiyon içinde: o anki yerel değişkenleri hızlıca görmek (debug amaçlı).
# • Modül seviyesinde: modülün global/yerel isimlerine erişmek (modül kapsamında locals()==globals()).
# • Sınıf gövdesinde: sınıfın oluşturulma sürecindeki isimleri gözlemek (ileri seviye metaprogramlama). 🧰

# -----------------------------------------------------------------------------
# 🚧 DİKKAT EDİLMESİ GEREKENLER
# • Fonksiyon kapsamı: locals() sözlüğünü DEĞİŞTİRMEK, yerel değişkenleri güncellemek zorunda değildir (genelde güncellemez).
#   → Yerel bir ismi atamak istiyorsan normal atama yap (a = 1). globals()/nonlocal gibi anahtar sözcükleri kullan.
# • Modül kapsamı: locals() == globals(); burada locals()["X"]=1 yazmak genelde modül değişkenini oluşturur. ✅
# • Sınıf kapsamı: locals() çoğunlukla sınıf gövdesi isim tablosuna yansır; ama okunabilirlik için normal atamayı tercih et.
# • Güvenlik: eval/exec ile birleşince kullanıcı girdisini asla doğrudan kullanma. 🔒
# • Taşınabilirlik: locals()’a yazmanın etkisi bir “uygulama detayıdır”; farklı yorumlayıcı/optimizasyonlarda davranış değişebilir.

# -----------------------------------------------------------------------------
# 🧭 KAPSAMLARA GÖRE locals() ÖZETİ
# • Modül içinde   → locals() ≡ globals()  (yazmak genelde modül değişkenini oluşturur/değiştirir)
# • Fonksiyon içinde→ locals()  “anlık görünüm” verir; sözlüğe yazmak yereli değiştirmeyebilir (çoğu zaman ETKİSİZ)
# • Sınıf gövdesinde→ locals()  sınıf isim alanını temsil eder; değişiklikler sınıf niteliklerine yansıyabilir (yine de dikkat/tercihen normal atama)

# -----------------------------------------------------------------------------
# 🧠 globals() / module.__dict__ KARŞILAŞTIRMASI (bağlam açısından)
# • Modül düzeyinde: locals() == globals() → globals()["X"]=1 ile locals()["X"]=1 genelde aynı etkiyi yapar. ✅
# • Başka modülü güncellemek istiyorsan: hedef_modül.__dict__["X"] = 1 kullan; locals()/globals() sadece BULUNDUĞUN modüle etkiler.
# • locals(), içinde bulunulan kapsamın tablosu; globals(), modülün global tablosu; module.__dict__, belirli bir modülün tablosudur. 🎯
