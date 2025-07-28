# -----------------------------------------------
# 🧠 __annotations__ — Sınıflar İçin Nihai Tanım
# -----------------------------------------------

# 📖 TANIM:
# __annotations__, Python'da bir sınıf (veya fonksiyon) içinde
# yapılan type hint tanımlarını tutan özel bir sözlüktür (dict).
# Bu sözlük, Python'un çalışma zamanında type hint bilgilerini
# yorumlayabilmesi için tutulur.

# ---------------------------------------------------
# 🏗️ SÖZDİZİMİ (class içinde)
# ---------------------------------------------------

# class MyClass:
#     attr1: int
#     attr2: str = "default"
#     attr3: float

# Burada __annotations__ otomatik olarak oluşur:
# {
#     'attr1': <class 'int'>,
#     'attr2': <class 'str'>,
#     'attr3': <class 'float'>
# }

# 🟡 Not: Değer atansa da atanmasa da her type hint buraya girer
# 🔴 Ancak __dict__ içinde sadece değeri olanlar yer alır

# ---------------------------------------------------
# 🔬 DAVRANIŞ: __dict__ vs __annotations__
# ---------------------------------------------------

# • Sadece tip belirtildiyse → __annotations__ içinde olur
# • Tip + değer varsa → __annotations__ + __dict__ içinde olur
# • Değersiz tanım → sadece type bilgisidir, gerçek attribute değildir

# ---------------------------------------------------
# ✅ KULLANIM ALANLARI:
# ---------------------------------------------------

# • __slots__ tanımlamak için
# • Otomatik __init__ jeneratörleri (dataclass alternatifi gibi)
# • ORM, form builder, serializer gibi sistemlerde field extraction
# • IDE’lere statik analiz, autocomplete sağlamak için

# ---------------------------------------------------
# 🧬 SINIFLAR İÇİN ÖZELLİKLER
# ---------------------------------------------------

# 📌 __annotations__ sadece class body’deki type hint’leri içerir
# 📌 Kapsadığı alan: class-level (üst düzey, metot dışında)

# ⚠️ __annotations__ içinde yer almak → gerçek bir attribute olmak anlamına gelmez
# (örneğin: __dict__ içinde görünmeyebilir)

# 🎯 Bu sayede __slots__ gibi mekanizmalarla memory-safe yapılar kurulabilir

# ---------------------------------------------------
# 🧩 FONKSİYONLARDA FARKI NEDİR?
# ---------------------------------------------------

# Fonksiyonlarda __annotations__ şöyle işler:

# def foo(x: int, y: str) -> bool:
#     ...

# foo.__annotations__:
# {'x': <class 'int'>, 'y': <class 'str'>, 'return': <class 'bool'>}

# ✅ Fonksiyonlar için:
# - Parametreler ve dönüş tipi ayrı ayrı tutulur
# - "return" key'i dönüş tipini temsil eder
# - Yalnızca type hint olan parametreler görünür

# ⛔ Fonksiyonlarda değerin olup olmaması önemli değildir — sadece hint ilgilidir

# ---------------------------------------------------
# 🔄 FARK ÖZET TABLOSU
# ---------------------------------------------------

# Özellik               | Sınıf                         | Fonksiyon
# ----------------------|-------------------------------|----------------------------
# Hangi tanımlar?       | Üst düzey attribute hint'leri | Parametre + return tipi
# return key?           | ❌ Yok                         | ✅ return
# Default value etkisi? | Değer varsa __dict__'e girer  | ❌ Etkisi yok
# Gerçek attribute mi?  | Hayır, sadece hint            | Hayır, sadece hint
# IDE etkisi?           | ✅ Statik analiz sağlar       | ✅ Otocompletion sağlar

# ---------------------------------------------------
# 🧠 AKILDA KALSIN:
# __annotations__ = "Bu isim şunu temsil etmeli... ama gerçek attribute değilim."



class A:
    name: str
    age: int

print(getattr(A,"__annotations__")) # {'name': <class 'str'>, 'age': <class 'int'>}

print(A.__dict__) # {'__module__': '__main__', '__firstlineno__': 96, '__annotations__': {'name': <class 'str'>, 'age': <class 'int'>}, '__static_attributes__': (), '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>, '__doc__': None}
# Gördüğün üzere sınıfın sözlüğünde yoklar çünkü onlar sadece type hint,değersiz tanımlar yani gerçek attribute değiller
# bu nedenle de sınıfın sözlüğünde olmazlar ancak değeri olan veriler yazılır

class A1:
    name: str = "demir"
    age: int = 20

print(getattr(A1,"__annotations__")) # {'name': <class 'str'>, 'age': <class 'int'>}
print(A1.__dict__) # {'__module__': '__main__', '__firstlineno__': 106, '__annotations__': {'name': <class 'str'>, 'age': <class 'int'>}, 'name': 'demir', 'age': 20, '__static_attributes__': (), '__dict__': <attribute '__dict__' of 'A1' objects>, '__weakref__': <attribute '__weakref__' of 'A1' objects>, '__doc__': None}
