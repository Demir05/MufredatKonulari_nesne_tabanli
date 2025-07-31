# ============================================================
# 🧠 PYTHON'DA NESTED CLASS (İÇ İÇE SINIF) YAPISI
# ============================================================


# ✅ Nasıl tanımlanır?
# --------------------
# - Tıpkı fonksiyonlar gibi, bir sınıfın gövdesinde başka bir `class` yazılır.
# - Python bunu işlerken iç sınıfı dış sınıfın namespace'ine ekler.

# ✅ Erişim nasıl yapılır?
# ------------------------
# - `DışSınıf.İçSınıf` şeklinde sınıf düzeyinde erişilir.
# - Örnek üstünden erişilmek istenirse: `type(obj).İçSınıf` veya `obj.__class__.İçSınıf`

# ✅ Sınıf oluşturulmadan, iç sınıf “yaşamaz”
# ------------------------------------------
# - Yani nested sınıf dış sınıfın tanımlanması sırasında derlenir, bağımsız bir sınıf değildir.
# - Bu nedenle dış sınıfın “tanımlandığı” anda iç sınıf da belleğe alınır.

# ============================================================
# ✅ ÖRNEK 1: Basit Nested Class
# ============================================================

class Dış:
    class İç:
        def selam(self):
            return "Merhaba iç sınıftan!"

# Erişim:
print(Dış.İç().selam())  # ✅ Merhaba iç sınıftan!

# ============================================================
# ✅ ÖRNEK 2: Dış sınıf örneğinden iç sınıfa erişmek
# ============================================================

class Kitap:
    class Meta:
        tür = "Roman"
        yıl = 2024

    def info(self):
        return f"{self.Meta.tür} ({self.Meta.yıl})"

k = Kitap()
print(k.info())  # ✅ Roman (2024)

# Alternatif:
print(type(k).Meta.tür)  # ✅ Roman

# ============================================================
# ⚠️ UYARILAR
# ============================================================

# - İç sınıflar dış sınıfın örneğiyle doğrudan ilişkilendirilmez (instance bağlı değil).
# - Bu sınıflar static gibi davranır. Dış sınıfın instance'ına bağlanmak için özel çözüm gerekir.
# - Sık karşılaşılan yapılar değildir ama bazı frameworklerde sıkça kullanılır (örnek: Django `Meta`).

# ============================================================
# ✅ KULLANIM ALANLARI
# ============================================================

# 1. ORM yapılandırmaları (Django gibi)
# 2. Konfigürasyon sınıfları
# 3. Enum/Constants benzeri yapı kümeleri
# 4. Static ayırıcı yapılar: Yalnızca dış sınıfa özel içerik tutma


# ========================================================
# 🎯 NESTED CONTEXT-AWARE STATE MACHINE: TEORİK AÇIKLAMA
# ========================================================
#
# Bu yapı, bir nesnenin (outer) davranışının anlık "durum"una göre değiştiği
# ve her durumun, outer nesneyle bağ kurarak ona göre çalıştığı bir modeldir.
#
# Nested class'lar burada her bir "State" (durum) için kullanılır.
# Böylece:
#   - Her state kendi davranışını kapsülleyebilir
#   - Outer nesne (context) state'lere geçirilerek dış veriye erişim sağlanabilir
#   - State geçişleri açık, tip güvenli ve izole olur
#
# Bu yapı özellikle GUI, oyunlar, protokol yönetimi ve robotik gibi alanlarda kullanılır.

# =========================================
# 🟢 ÖRNEK: Trafik Lambası State Makinesi
# =========================================
class TrafficLight:
    def __init__(self):
        # Başlangıçta sistem 'Red' durumundadır
        # State class'ına outer context (self) verilir
        self.state = self.Red(self)

    def change(self):
        """State değiştir: bir sonraki duruma geç"""
        self.state = self.state.next()

    def show(self):
        """Mevcut durumun göstergesini al"""
        return self.state.display()

    # ==========================
    # 🔴 Durum: Kırmızı Işık
    # ==========================
    class Red:
        def __init__(self, outer):
            self.outer = outer  # bağlam: TrafficLight nesnesine erişim

        def next(self):
            # Gelecek durum: Yeşil
            return self.outer.Green(self.outer)

        def display(self):
            return "🔴 DUR"

    # ==========================
    # 🟢 Durum: Yeşil Işık
    # ==========================
    class Green:
        def __init__(self, outer):
            self.outer = outer

        def next(self):
            # Gelecek durum: Sarı
            return self.outer.Yellow(self.outer)

        def display(self):
            return "🟢 GEÇ"

    # ==========================
    # 🟡 Durum: Sarı Işık
    # ==========================
    class Yellow:
        def __init__(self, outer):
            self.outer = outer

        def next(self):
            # Gelecek durum: Kırmızı
            return self.outer.Red(self.outer)

        def display(self):
            return "🟡 BEKLE"

# =========================================
# 🔍 KULLANIM ÖRNEĞİ
# =========================================
tl = TrafficLight()

print(tl.show())  # 🔴 DUR
tl.change()

print(tl.show())  # 🟢 GEÇ
tl.change()

print(tl.show())  # 🟡 BEKLE
tl.change()

print(tl.show())  # 🔴 DUR (başlangıca döner)

