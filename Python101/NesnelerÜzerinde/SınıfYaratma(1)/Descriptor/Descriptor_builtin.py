
# Python'da descriptor kavramı, attribute erişimini özelleştirmek için kullanılır.
# Built-in descriptor'lar, CPython tarafından performans ve iç yapı optimizasyonu için tanımlanmış özel sınıflardır.
# Aşağıda en yaygın built-in descriptor türlerini ve neden var olduklarını açıklıyoruz.

# ✅ getset_descriptor
# Tanım: C seviyesinde tanımlanmış, hem __get__ hem __set__ içeren sistem attribute'larıdır.
# Kullanım: object.__doc__, type.__name__ gibi core metadata'larda bulunur.
# Neden ayrı?: Çünkü CPython bu alanlar için özel yapı (`PyGetSetDef`) kullanır. Performans ve hafıza verimliliği için.
example_getset = object.__class__.__dict__['__doc__']
print(f"getset_descriptor: {type(example_getset)}")

# ✅ member_descriptor
# Tanım: __slots__ ile tanımlanan sınıf attribute'larıdır.
# Kullanım: Normal attribute yerine hafıza tasarrufu sağlayan slot sistemi için.
# Neden ayrı?: CPython `PyMemberDef` adında ayrı bir C yapısı kullanır. Normal __dict__ erişimi yerine offset ile erişir.
class SlotExample:
    __slots__ = ['x']

member_descr = SlotExample.__dict__['x']
print(f"member_descriptor: {type(member_descr)}")

# ✅ method_descriptor
# Tanım: C'de tanımlı metotlar için descriptor’dır (örneğin list.append).
# Kullanım: bound method üretimi sağlar ama sadece __get__ içerir → non-data descriptor'dır.
# Neden ayrı?: C fonksiyonları ile Python metotları arasında ayrım yapılmasını sağlar. Performans için.
method_descr = list.__dict__['append']
print(f"method_descriptor: {type(method_descr)}")

# ✅ wrapper_descriptor
# Tanım: Magic method’lar (örn. __add__, __str__) için kullanılır.
# Kullanım: operator overloading işlemleri için özel davranış sağlar.
# Neden ayrı?: Bu metotlar C'de override edildiğinden, özel olarak tanımlanmış ve hızlı erişim için farklı tutulur.
wrapper_descr = int.__dict__['__add__']
print(f"wrapper_descriptor: {type(wrapper_descr)}")

# ✅ builtin_function_or_method
# Tanım: Global scope’ta tanımlı C fonksiyonlarıdır. (örn. len, abs)
# Kullanım: Fonksiyon olarak davranır ama descriptor değildir (genellikle).
# Neden ayrı?: Bunlar sınıfa değil, modüle ait fonksiyonlardır. Özellikle çağrılabilir objeler olarak tanımlanır.
builtin_func = len
print(f"builtin_function_or_method: {type(builtin_func)}")

# ✅ property
# Tanım: Python dilinde yazılmış en yaygın descriptor türü.
# Kullanım: __get__, __set__, __delete__ gibi metodlarla tamamen özelleştirilebilir.
# Neden ayrı?: Python geliştiricilerine esneklik sağlamak için user-level descriptor olarak tasarlandı.
class PropertyExample:
    @property
    def foo(self):
        return 'bar'

property_descr = PropertyExample.__dict__['foo']
print(f"property: {type(property_descr)}")


import timeit

# Bu dosya, neden built-in fonksiyonların (örneğin len, list.append)
# Python'da tanımlanmış fonksiyonlardan daha hızlı olduğunu açıklar.

# 🔹 1. Python fonksiyonu tanımlıyoruz
def square(x):
    return x * x

# Bu fonksiyon normal bir Python fonksiyonudur.
# Çalıştığında:
# - Python interpreter bir stack frame oluşturur
# - Argümanları işler
# - Bytecode yorumlanır
# Bu işlem, C'de yazılmış bir fonksiyona göre daha yavaştır.

# 🔹 2. Built-in fonksiyon örneği
# 'len' fonksiyonu C ile yazılmıştır ve PyCFunctionObject türündedir.
# Python interpreter, 'len' için direkt native C kodunu çağırır, bytecode yorumlaması gerekmez.
# Bu nedenle inanılmaz hızlıdır.

# 🔹 3. Zaman ölçümü
# timeit: Aynı işlemi çok sayıda kez yaparak süreyi ölçer

# Python fonksiyonu 1 milyon kez çağrılıyor
python_time = timeit.timeit('square(10)', globals=globals(), number=1_000_000)

# Built-in len fonksiyonu 1 milyon kez çağrılıyor
builtin_time = timeit.timeit('len([1,2,3])', number=1_000_000)

print("Python fonksiyonu zamanı: ", python_time)
print("Built-in len zamanı     : ", builtin_time)

# 🔍 Not: len() gibi fonksiyonlar `builtin_function_or_method` türündedir
# >>> type(len) → <class 'builtin_function_or_method'>

# Bu türler CPython'da doğrudan `PyCFunction` yapılarına bağlıdır.
# Her çağrıda interpreter:
# - Python fonksiyonu için function object yaratır
# - Frame hazırlar
# - Local/global scope yönetir

# Ama built-in fonksiyonlarda:
# - Argümanlar minimum kontrolle parse edilir
# - Doğrudan C fonksiyonu çağrılır (stack frame yok)
# - Geri dönüş değeri native olarak döner

# 🧠 Özet:
# Built-in fonksiyonlar:
# ✅ C ile yazıldığı için daha hızlı
# ✅ Descriptor tipi sayesinde doğrudan çözümlenir
# ✅ Interpreter'ın overhead'ine takılmaz

# Bunlar sayesinde performance-critical kodlar için müthiş fark yaratırlar!
