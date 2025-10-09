## 🎬 BAŞLANGIÇ: Python kodunda bir sınıf çağırıyoruz
```python
class MyClass:
    def __init__(self, x):
        self.x = x
```
**Ve bunu kullanıyoruz:**
```python
obj = Myclass(5)
```
- **🍼 Bu çağrı bize dışarıdan çok basit görünüyor.**

  - Ama arka planda neler olduğunu anlamak için parça parça ilerleyelim 👇
---

### 🧭 ADIM 1: Python yorumlayıcısı (MyClass(5)) ifadesini işler

Python yorumlayıcısı bu çağrıyı gördüğünde şunu anlamlandırır:

❓ "MyClass, bir sınıf mı? Evet. O zaman onu çağırmam gerekiyor."

Bu işlem sırasında **Python yorumlayıcı,** `CALL` isimli bir opcode üretir. Bu, Python’un çalıştırdığı bytecode’lardan biridir.

---

### ⚙️ ADIM 2: CALL opcode çalıştırılır

Yani `CALL_FUNCTION`, `CALL`, `CALL_METHOD` gibi opcode’lar çalıştırılır.
> 🧩 *Not:* Bu opcode’lar Python sürümüne göre farklılık gösterebilir.  
> Örneğin **Python 3.10** öncesinde `CALL_FUNCTION`, `CALL_METHOD`, `CALL_FUNCTION_KW` gibi ayrı opcode’lar kullanılırken,  
> **Python 3.11** ve sonrasında bu çağrılar `CALL`, `PRECALL`, `KW_NAMES` gibi daha sadeleştirilmiş ve optimize edilmiş opcode’larla temsil edilir.  
> Bu değişim, CPython’ın bytecode mimarisini sadeleştirme ve performans artırma hedefinin bir parçasıdır.

**Bu opcode, C dilinde tanımlı şu fonksiyonu tetikler:**
```c
PyObject_Call(callable, args, kwargs)
```
#### ⚙️ `PyObject_Call(callable, args, kwargs)` — Parametre Açıklama Tablosu

| 🧩 Parametre | 🧠 Tür | 🎯 Açıklama |
|-------------|--------|-------------|
| `callable`  | `PyObject*` | Çağrılabilir nesne (örneğin bir sınıf, fonksiyon, bound method). `PyCallable_Check()` ile doğrulanabilir. |
| `args`      | `PyObject*` (tuple) | Konumsal argümanları içeren `PyTupleObject`. Boşsa `PyTuple_New(0)` ile oluşturulabilir. |
| `kwargs`    | `PyObject*` (dict veya NULL) | Anahtar-değer çiftlerini içeren `PyDictObject`. Yoksa `NULL` geçilebilir. |

> 💡 Bu fonksiyon, yorumlayıcının `CALL` opcode’u tarafından tetiklenir ve `tp_call` slot’una yönlendirilir.  
> Hem sınıf örnekleme (`MyClass(5)`), hem fonksiyon çağrısı (`func(x, y)`), hem de dekoratör gibi yapılar bu mekanizma üzerinden çalışır.
> Bu fonksiyon, CPython'un temel çağrı yöneticisidir. Python’da bir şeyi çağırmak istiyorsan, bu fonksiyondan geçmek **zorundasın.** ❗ 

>**💡 MyClass(5) ifadesinde:**
>- `callable` = MyClass
>- `kwargs` = {}

---

### 🧰 ADIM 3: `PyObject_Call` fonksiyonu ne yapar?

Bu fonksiyonun ilk işi şu soruyu sormaktır:

> ❓ **"Bu callable objesi, `tp_call` fonksiyonu tanımlamış mı?"**

Yani `PyObject_Call()` çağrıldığında, yorumlayıcı şu kontrolü yapar:

```c
if (callable->ob_type->tp_call != NULL) {
    return callable->ob_type->tp_call(callable, args, kwargs);
}
```
Yani: `MyClass` bir sınıf (yani bir type objesi), ve type tipinin `tp_call` slot’u vardır. Bu slot `type_call` fonksiyonudur.

---

### 🏭 ADIM 4: `type_call` fonksiyonu devreye girer

Şimdi CPython `type_call()` fonksiyonuna geçer.  
Bu, bir sınıf çağrıldığında ne yapılacağını tanımlar.
```c
static PyObject *
type_call(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *obj;

    /* __new__ çağrısı */
    obj = type->tp_new(type, args, kwds);
    if (obj == NULL) {
        return NULL;
    }

    /* Dönüş tipi kontrolü: obj, type ile uyumlu mu? */
    if (!PyObject_IsInstance(obj, (PyObject *)type)) {
        PyErr_Format(PyExc_TypeError,
                     "__new__() returned non-%s (type %s)",
                     type->tp_name,
                     obj->ob_type->tp_name);
        Py_DECREF(obj);
        return NULL;
    }

    /* __init__ çağrısı */
    if (type->tp_init != NULL) {
        if (type->tp_init(obj, args, kwds) < 0) {
            Py_DECREF(obj);
            return NULL;
        }
    }

    return obj;
}

```
> 🎯 **Bu nokta çok kritik:**  
> `tp_new` → Python'daki `__new__` fonksiyonudur → nesneyi oluşturur (bellek tahsisi).  
> `tp_init` → Python'daki `__init__` fonksiyonudur → nesneyi başlatır (özellikleri ayarlar).  
> Bu ayrım, CPython’ın sınıf çağrısı mimarisinde hem bellek hem davranış düzeyinde kontrol sağlar.

---

### 🧬 ADIM 5: `tp_new` çalışır → Bellek burada tahsis edilir

`tp_new`, nesneyi oluşturur — yani belleği tahsis eden ilk adımdır.  
Bu aşamada Python yorumlayıcısı, sınıfın `__new__` metoduna karşılık gelen `tp_new` slot’unu çağırır.

- Eğer sınıf **built-in** ise (örneğin `int`, `list`) → özel bir `tp_new` fonksiyonu vardır (`long_new`, `list_new` gibi).
- Eğer sınıf **user-defined** ise → `object_new` kullanılır. Bu da `type->tp_alloc` fonksiyonunu çağırarak belleği ayırır.

> 💡 Bu adımda Python nesnesi RAM üzerinde fiziksel olarak tahsis edilmiş olur, ancak henüz yapılandırılmamıştır.

---

### 🔧 ADIM 6: `tp_init` çalışır → Nesne burada başlatılır

`tp_init`, nesnenin `__init__()` metoduna karşılık gelir ve yapılandırma işlemini gerçekleştirir.  
Bu metot, mevcut nesne üzerinde işlem yapar ama yeni bir nesne oluşturmaz.

- Örneğin: `self.x = x` gibi özellik atamaları burada yapılır.
- Bellek zaten tahsis edilmiştir; bu adım sadece davranışsal başlatmadır.

> 🧩 `tp_init` çağrısı, `tp_new` ile oluşturulmuş nesneye anlam kazandırır.

---

### 🎁 ADIM 7: Oluşturulan nesne geri döner

Son olarak `type_call()` fonksiyonu, yapılandırılmış `obj` nesnesini döner.  
Bu nesne, `MyClass(5)` ifadesinin sonucu olur.

- Yani `obj = MyClass(5)` satırı tamamlanmış olur.
- Bellek tahsis edilmiş, `__init__` çalıştırılmış ve nesne kullanıma hazırdır.

> 🎯 Bu üç adım (`tp_new` → `tp_init` → return) Python’daki sınıf çağrısının C düzeyindeki temel zincirini oluşturur.

---

```vbnet
### 🔁 ÖZET ZİNCİR: MyClass(5) çağrısı ne yapar?

Python Kod:       MyClass(5)
↓
Opcode:           CALL
↓
C Fonksiyonu:     PyObject_Call(MyClass, args)
↓
Slot Fonksiyonu:  MyClass->tp_call = type_call
↓
Zincir:
    - type->tp_new → __new__ → bellek tahsisi
    - type->tp_init → __init__ → örnek başlatma
↓
Sonuç:            obj (MyClass örneği)
```
---

## 🧬 KONU: Miraslı sınıflarda __new__ ve object.__new__ nasıl çalışır?

### Örnek sınıf yapımız şu olsun:
```python
class MyInt(int):
    def __new__(cls, value):
        print("MyInt __new__")
        return super().__new__(cls, value)

    def __init__(self, value):
        print("MyInt __init__")
```
**ve çağrımız:**
```python
x = MyInt(5)
```
---

### 🎬 1. Python düzeyinde ne oluyor?

Adım adım:

- `MyInt(5)` çağrısı yapılır → `CALL` opcode çalışır  
- `MyInt` bir sınıftır → `PyObject_Call(MyInt, args)`  
- `MyInt`’in `tp_call` slot’u → `type_call()` çalışır  

`type_call` içinde:

- `MyInt.__new__()` çağrılır  
- `MyInt.__init__()` çağrılır

---

### 🧠 Şimdi `__new__` devreye girdi

Kodumuzda şu satır yer alıyor:

```python
return super().__new__(cls, value)
```

#### ✨ Bu satırın anlamı:

🔍 `super()` → MRO (Method Resolution Order) zincirine bakar  
🏗️ `MyInt`’in üst sınıfı `int` → `int.__new__` çağrılır  
⚙️ `int` built-in bir sınıftır → onun `tp_new` fonksiyonu `long_new`’dur  

➡️ Yani `super().__new__(cls, value)` ifadesi CPython’da şu çağrıya karşılık gelir:  
🧩 `long_new(cls, args)` → `_PyLong_New()` → bellekte bir `PyLongObject` tahsis edilir

---

### ❓ Peki `object.__new__` ne zaman devreye girer?

Bu soru çok yerinde. 👇

Şöyle olur:

🧬 `int` sınıfı, `object` sınıfından türemiştir  
🛠️ Eğer biz `int`’in değil, doğrudan `object`’in subclass’ını yazarsak → `object.__new__` devreye girer  
⚙️ Bu durumda `tp_new` → `object_new` olur → `type->tp_alloc` üzerinden bellek tahsisi yapılır
```python
class A(object):
    def __new__(cls):
        print("A __new__")
        return super().__new__(cls)
```
Burada `super().__new__(cls)` → `object.__new__(cls)` çağrılır.🧬 

### 🔎 object.__new__ gerçekte ne yapar?

**Python’da:**
```python
object.__new__(cls)
```
**C'de:**
```c
object_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    return type->tp_alloc(type, 0);  // Bellek ayırma burada olur
}
```
> Yani `object.__new__` doğrudan belleği ayırır, ama başka hiçbir şey yapmaz.

---

### 📍 Miras Zinciri (Örnek: `MyInt(int)`)

| 🪜 Aşama            | ⚙️ Fonksiyon                  | 🧠 Açıklama                                      |
|---------------------|------------------------------|--------------------------------------------------|
| `MyInt(5)`          | `type_call`                  | Sınıf çağrılır                                   |
| `__new__` çağrısı   | `MyInt.__new__`              | Override edilmiş                                 |
| `super().__new__`   | `int.__new__` → `long_new`   | Özel `tp_new` fonksiyonu                         |
| `object.__new__`    | ❌ çağrılmaz                  | `int` zaten kendi bellek yöneticisini kullanır   |
| `__init__` çağrısı  | `MyInt.__init__`             | Kullanıcı başlatması                             |

---

### 🔁 Diğer Durum: object.__new__'ün son nokta olduğu zincir
```python
class A:
    def __new__(cls):
        print("A __new__")
        return super().__new__(cls)
```
#### 🧩 Burada `A` bir `object` subclass’ıdır

🔗 `super().__new__()` → `object.__new__()` → `object_new()` çalışır  
🧱 `tp_alloc` ile bellek tahsis edilir  
🚀 Ardından `__init__()` ile nesne başlatılır

---

### 🎯 Sonuç

`super().__new__(cls)` çağrısı, sınıfın MRO'suna bakarak uygun `__new__` metodunu bulur.  
Bu metod, built-in sınıflarda `tp_new` → C fonksiyonlarına bağlıdır.  
Zincirin en sonunda her zaman bir `tp_alloc` çağrısı vardır (bellek ayırma noktası).  
`object.__new__` bu zincirin en genel ve temel noktasıdır.

---

### 💡 Kural Gibi Akılda Tut

🧠 Her `__new__` zinciri, ister doğrudan ister dolaylı, en sonunda belleği ayırmak için bir `tp_alloc` çağrısı içerir.  
Eğer özel bir `tp_new` tanımlıysa (`int`, `float`, vb.) zincir orada sona erer.  
Eğer yoksa, zincir `object.__new__()`'e kadar gider.
