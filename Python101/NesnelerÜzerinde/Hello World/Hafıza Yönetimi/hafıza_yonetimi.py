

# ===============================================
# 🔐 CLOSURE (Kapanış) NEDİR?
# ===============================================
# ➤ Closure, bir iç fonksiyonun, tanımlandığı dış fonksiyondaki değişkenlere erişimini
#   koruyarak yaşamaya devam etmesidir.
#
# ➤ Bu sayede iç fonksiyon dış fonksiyon kapansa bile o değişkenleri hatırlar.
#
# 📌 Python'da bir fonksiyonun __closure__ özniteliği bu mekanizmayı taşır.
#    Eğer iç fonksiyon dış scope'tan değişken alıyorsa __closure__ boş olmaz.
#
# 🧠 Unutma: Closure oluşması için inner fonksiyon, dış fonksiyondaki bir değişkene
# erişmeli ama tanımlamamalı.

def kapatici(x):
    def carp(y):
        return x * y

    return carp


iki_ile_carp = kapatici(2)
print(iki_ile_carp(10))  # 20

# burada carp() fonksiyonu, x değişkenine dış scope’tan erişebiliyor.
# kapanış (closure) bu değişkeni __closure__ içinde saklar.
# dış fonksiyon bitse bile carp(), x=2 bilgisini unutmaz.
print(iki_ile_carp.__closure__[0].cell_contents)  # 2


# ===============================================
# ⚠️ Mutable Nesneler Closure'da Neden Sorunsuz?
# ===============================================
# ➤ Python, iç fonksiyonların enclosing scope’ta yer alan değişkenlere erişmesini sağlar,
#    ancak onları "yeniden tanımlamaya" çalışırsa hata verebilir (UnboundLocalError).

# ➤ Eğer değişken mutable ise, yeniden tanımlama gerekmeden üzerinde değişiklik yapılabilir.
#    Bu da hatayı engeller. Örnek:

def kapanis():
    liste = []

    def ekle(x):
        liste.append(x)  # ✅ mutable, yeniden tanım gerekmez, doğrudan değiştirilebilir

    ekle(5)
    return liste


print(kapanis())  # [5]


# ===============================================
# 🏗️ SINIFLARDA HAFIZA VE SCOPE YÖNETİMİ
# ===============================================
# ➤ Her sınıf bir tür nesne şablonudur. Tanımlandığında class objesi oluşur (heap).
# ➤ Sınıf içi methodlar fonksiyon olarak stack'te çalışır ama self gibi bağlantılar heap'e referans sağlar.

# 🔄 Sınıf örnekleri (instance) heap'te saklanır.
# 📌 self => o anki örneği temsil eder, heap'teki nesneye doğrudan referans sağlar.

class K:
    def __init__(self, veri):
        self.veri = veri  # self üzerinden heap'teki veri alanına bağlanır

    def yazdir(self):
        print(self.veri)  # stack -> self -> heap'teki veri


k1 = K("Merhaba")
k1.yazdir()  # "Merhaba"

print(__name__)


def a():
    x = "demir"

    def b():
        nonlocal x
        print(x)
        print(b.__closure__[0].cell_contents)

        x = "aslı"
        print(x)

    return b()


a()
