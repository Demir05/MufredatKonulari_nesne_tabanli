# ======================================================
# 🔄 __reversed__() METODU NEDİR? NEDEN VAR? NE İŞE YARAR?
# ======================================================
from typing import Any


# 🔹 Python'da `reversed(obj)` fonksiyonu çağrıldığında, objenin __reversed__() özel metoduna bakılır.
# 🔸 Bu metod objenin tersten gezilebilir olup olmadığını bildirir.
# 🔸 Yani: ters sırayla iterable üretmek için kullanılır.

# 📌 Eğer __reversed__ tanımlı değilse, Python __len__ ve __getitem__ metodlarını kullanarak tersten iterasyon yapmaya çalışır.
# Ancak bu sadece indekslenebilir (sequence) yapılar için geçerlidir!

# ➕ __reversed__() metodu iterable objelere tersinden ulaşmak için daha hızlı ve kontrollü bir yol sunar.

# ======================================================
# 🧠 NEDEN GEREKLİ?
# ======================================================
# 1️⃣ Liste, tuple gibi yapılarda reversed() doğrudan çalışır → çünkü bu yapıların __reversed__() metodları vardır.
# 2️⃣ Kendi sınıflarımızda reversed(obj) kullanılmasını istiyorsak, __reversed__() metodunu tanımlamamız gerekir.
# 3️⃣ Alternatif olarak __len__ ve __getitem__ kullanarak da reversed() çalıştırılabilir ama bu daha dolaylıdır.

# ======================================================
# 🧾 SÖZDİZİMİ:
# ======================================================
# class MyClass:
#     def __reversed__(self):
#         # ters sırayla eleman üretmek
#         yield from reversed(self.data)

# ======================================================
# ✅ ÖRNEK SINIF: __reversed__() KULLANIMI
# ======================================================

class MyBag:
    def __init__(self, *items):
        self.items = list(items)

    def __repr__(self):
        return f"MyBag({self.items})"

    def __iter__(self):  # normal iterasyon
        return iter(self.items)

    def __reversed__(self):  # 👈 ters iterasyon
        print("__reversed__ çalıştı!")
        return reversed(self.items)

# 👇 Normal iterasyon:
mybag = MyBag("elma", "armut", "muz")
for item in mybag:
    print(item)  # elma → armut → muz

# 👇 Ters iterasyon:
for item in reversed(mybag):  # __reversed__ çağrılır
    print(item)  # muz → armut → elma

# ======================================================
# 📍 reversed() vs __reversed__ İLİŞKİSİ
# ======================================================
# reversed(obj) çağrıldığında:
# 🔸 Eğer obj.__reversed__ tanımlıysa → doğrudan o metod çağrılır
# 🔸 Tanımlı değilse:
#     🔹 obj.__len__() ve obj.__getitem__(index) metodları tanımlıysa,
#     🔹 Python bu metodları kullanarak tersten iter etmeye çalışır

# 💥 Ancak bu ikinci yöntem biraz daha maliyetlidir ve sadece index tabanlı dizilerde çalışır.

# ======================================================
# 🧠 METOD ÇÖZÜMLEMESİ (EN DÜŞÜK SEVİYEDE)
# reversed(myobj) çağrıldığında:
# 🔽

# 1- type(obj).__dict__['__reversed__'].__call__(obj)
#
# Yoksa;
#
# 1- for i in range(type(obj).__dict__['__len__'].__call__(obj)-1,-1,-1):
#         type(obj).__getitem__(i)

# ======================================================
# 💡 __reversed__ tanımlayarak iterable sınıflara ekstra güç kazandırırsın!
# Bu metodun kullanılması kodun hem performansını artırır hem de okunabilirliğini.

# 🛠️ Pro tip:
# Eğer bir sınıf "koleksiyon" gibi davranacaksa (__iter__ tanımlıysa), __reversed__ eklemek güçlü bir tamamlayıcıdır.

class MyBag:
    def __init__(self, *items):
        self.items = list(items)

    def __len__(self): return len(self.items)

    def __getitem__(self,index:int) -> Any:
        return self.items[index]


bag = MyBag("elma", "armut", "muz")
for item in reversed(bag):
    print(item)


for i in range(bag.__class__.__dict__["__len__"].__call__(bag)-1,-1,-1):
    print(bag.__class__.__dict__["__getitem__"].__call__(bag,i))