

## 📘 Genel Tanım  
`int`, Python’daki **tamsayı (integer)** türüdür.  
Matematiksel olarak sonsuz aralıkta değerleri destekler,  
ancak donanımda bunlar **bellek boyutuyla sınırlıdır.**

> 🧩 `int` = Soyut bir tamsayı nesnesi  
> 💾 Gerçekte RAM’de, değişken uzunluklu bir *PyLongObject* olarak tutulur.  

`int` sınıfı Python’un en temel **sayısal veri tipi** olup,  
bit düzeyinde işlem yapabilen, immutable (değiştirilemez) bir nesnedir.

---

### 🧠 İleri Tanım  

#### 🔹 Soyutlama Katmanı
- `int`, Python’un **number protocol** arayüzünü (`__add__`, `__sub__`, `__and__`, …) uygular.  
- Bu sınıfın örnekleri, **matematiksel bütün sayıları** temsil eder (pozitif, negatif, sıfır).  
- C tarafında her `int` nesnesi, **`PyLongObject`** yapısının bir örneğidir.

#### 🔹 Özellikler
| ⚙️ Özellik              | 📘 Açıklama                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| **Immutable**           | `int` değerleri değiştirilemez — her işlem (`+`, `-`, `*`) yeni nesne üretir. |
| **Arbitrary precision** | 32/64-bit sınırı yoktur; Python gerekirse belleği büyütür (`ob_digit[]`).     |
| **Hashable**            | `int` nesneleri sözlük anahtarı olarak kullanılabilir.                        |
| **C tabanı**            | CPython’da `longobject.c` içinde tanımlıdır (`Include/longobject.h`).         |
| **İşaret yönetimi**     | `Py_SIZE()` pozitif/negatif işareti belirler; `long_add()` bunu kontrol eder. |
| **Küçük sayı optimizasyonu** | `MEDIUM_VALUE(a) + MEDIUM_VALUE(b)` ile hızlı toplama yapılır.               |
| **Çok basamaklı destek**| `x_add()` ve `x_sub()` fonksiyonları büyük sayılar için özel algoritmalar içerir. |
| **Bellek güvenliği**    | `Py_REFCNT(z) == 1` kontrolü ile in-place değişiklikler güvence altına alınır. |

> 🧠 Not: `long_add()` fonksiyonu, Python’daki `a + b` işleminin C düzeyindeki karşılığıdır.  
> Hem işaret hem de basamak sayısına göre farklı algoritmalar çağrılır

> 🧠 Büyük sayı işlemi, küçük sayıya göre yaklaşık **%11.96** daha yavaş çalışıyor. ⚡
---

---

## 🔢 Integer (int) Sınıfı — Nesne Düzeyi Tanım

---

### 📘 Tanım  
`int`, Python’un **sayısal veri türleri hiyerarşisinde temel sınıftır.**  
Tüm tamsayı değerler (`42`, `0b1010`, `0xFF`) bu sınıfın örnekleridir.  

`int` sınıfı:
- **immutable** (değiştirilemez),
- **C düzeyinde tanımlı (`PyLongObject`)**,
- **tüm matematiksel ve bit düzeyi operatörleri** destekleyen  
bir **built-in (yerleşik)** sınıftır.

> 🧩 `int` sınıfı, Binary Data Model’in “bit ve sayısal işlem” katmanının temel taşıdır.  
> Tüm `bytes`, `bool`, `float`, `complex` türleri, `int`’in davranış modelini miras alır.

> 🧠 Python’un sayısal veri modeli, bit düzeyindeki tüm türlerin davranışını `int` sınıfı üzerinden tanımlar; `bool`, `float`, `complex` gibi türler bu temel modeli miras alırken, `bytes` gibi türler onu dolaylı olarak kullanır.

---

### 🧠 İleri Tanım  
Python’da `int` sınıfı, **“number protocol”** ve **“object protocol”** arayüzlerini uygular.  
Bu sayede hem matematiksel, hem mantıksal, hem de bit düzeyinde davranış gösterebilir.  

`int`’in örnekleri immutable olduğu için:  
- Her işlem (örneğin `a + b`) yeni bir `int` nesnesi oluşturur.  
- Var olan nesnenin bellekteki değeri asla değişmez.  

Python `int` nesneleri C tarafında `PyLongObject` yapısı ile temsil edilir:  
```c
typedef struct {
    PyObject_VAR_HEAD
    digit ob_digit[1];  // değişken uzunluklu sayı bileşenleri
} PyLongObject;
```
- **Burada dikkat et:**
  - Nesnenin belleğinde yalnızca ob_digit[] vardır (yani sayısal veri). Herhangi bir “ek alan” veya “dict pointer” yoktur. Yani:
  
  > 🚫 `int` nesnesinin belleğinde `__dict__ `için yer ayrılmaz. Çünkü bu tipler **sabit bellek düzenine (fixed layout) sahip**  

### 🧩 1️⃣ Built-in `int` Nesnesi — Gerçekten Python Sınıfı Değil

---

Python'da `int` görünüşte sıradan bir sınıf gibi durur:

```python
>>> type(int)
<class 'type'>
```
Ama gerçekte bu sınıf Python koduyla tanımlanmamıştır.
`int`, **C** tarafında gömülü **(built-in)** bir tiptir:


### ⚙️ 2️⃣ int() Çağrıldığında Gerçekleşen Süreç (Opcode Düzeyi)

`int(5.8)` ifadesi **Python yorumlayıcısı** tarafından şu bytecode’a çevrilir:
```
LOAD_CONST 5.8
LOAD_NAME int
CALL_FUNCTION 1
STORE_NAME x
```

### 🧠 Python Bytecode — Basit Bir Atama İşleminin Çözümlemesi

Aşağıdaki işlem sırası, `x = int(5.8)` gibi bir ifadenin Python yorumlayıcısı tarafından nasıl yürütüldüğünü gösterir:

| 🔢 Aşama     | ⚙️ İşlem         | 🎯 Açıklama                                                                 |
|-------------|------------------|------------------------------------------------------------------------------|
| 1️⃣          | `LOAD_CONST`     | `5.8` sabitini yükler (literal float değeri).                               |
| 2️⃣          | `LOAD_NAME`      | Global isim alanından `int` nesnesini bulur.                                |
| 3️⃣          | `CALL_FUNCTION`  | `int` nesnesini 1 argümanla çağırır → `int(5.8)` işlemi gerçekleşir.         |
| 4️⃣          | `STORE_NAME`     | Elde edilen sonucu `x` değişkenine kaydeder.                                |

---

### ⚠️ Kritik Nokta — CALL_FUNCTION ve C Düzeyi Çağrı

> 👇 Bu işlem zincirinde en dikkat edilmesi gereken adım `CALL_FUNCTION`’dır.

- `CALL_FUNCTION`, Python yorumlayıcısında **`PyObject_Call()`** fonksiyonunu tetikler.
- `int` bir **built-in type** olduğundan, bu çağrı doğrudan **C tablosundaki `tp_call` pointer’ına** gider.
- Yani Python burada herhangi bir `__call__` override’ı veya Python düzeyinde dispatch yapmaz.
- Çağrı zinciri doğrudan C düzeyindeki `int.__new__()` veya `int.__call__()` fonksiyonuna bağlanır.

`int(5.8)` **çağrısı şu şekilde çalışır:**

```
PyObject_Call(int_type, (5.8,), NULL)
│
└──> tp_call(int_type)
      │
      └──> type_call()         ← C fonksiyonu
             │
             └──> int_type->tp_new = long_new()
                    │
                    └──> PyLong_FromDouble(5.8)
```
---

### 🧩 Sonuç

Bu yapı sayesinde Python, built-in türler için maksimum hızda çalışır.  
`int(5.8)` gibi basit bir çağrı bile, arka planda doğrudan C fonksiyonuna bağlanarak yorumlayıcının hızını artırır.

> 💡 Bu mekanizma, CPython’ın performans optimizasyonlarının temel taşlarından biridir.

> 🧠 `PyCallObject` ismi sanki çağrılabilir bir nesneyi tanımlıyormuş gibi görünse de, CPython’da çağrı bir işlem olduğu için `PyObject_Call` gibi eylem odaklı isimlendirme tercih edilir; bu, yorumlayıcının bir objeyi çağırma fonksiyonunu doğru şekilde yansıtır.

---

### 🧠 Python `int` Türü — Sistemsel Özellikler Tablosu

| 🔢 # | 🧩 Başlık                         | 📘 Açıklama |
|-----|----------------------------------|------------|
| 1️⃣  | **Bellek Sınırı**                | `int` matematiksel olarak sınırsızdır, ancak donanımda belleğin fiziksel sınırlarıyla sınırlıdır. |
| 2️⃣  | **Protokol Uyumu**               | `int`, hem `number protocol` hem `object protocol` arayüzlerini uygular; sayısal işlemlere katılır ve birinci sınıf nesne gibi davranır. |
| 3️⃣  | **C Temsili: `PyLongObject`**    | CPython’da her `int` örneği `PyLongObject` ile temsil edilir. `long_add()` gibi fonksiyonlar, `MEDIUM_VALUE` optimizasyonlarıyla küçük sayıları daha hızlı işler. |
| 4️⃣  | **Binary Modelin Temeli**        | `int`, Python’un binary veri modelinin temelidir. `bool` doğrudan miras alır; `float`, `complex`, `__index__`, `bytes` gibi türler dolaylı olarak kullanır. |
| 5️⃣  | **Sabit Bellek Düzeni**          | `PyLongObject` yalnızca `ob_digit[]` içerir; `__dict__` gibi genişletme alanları yoktur. Bu nedenle `int` nesneleri davranışsal olarak genişletilemez. |
| 6️⃣  | **Opcode Zinciri: `CALL_FUNCTION`** | `int()` çağrısı `CALL_FUNCTION` opcode’u ile başlar, `PyObject_Call()` fonksiyonunu tetikler ve doğrudan C düzeyindeki `tp_call` zincirine bağlanır; `__new__` ve `__call__` bypass edilir. |

---

### 🧩 `int` Sınıfının Attribute ve Dunder Metotları

Python’daki `int` sınıfı, hem **sayısal protokolü** hem **nesne protokolünü** uygular.  
Aşağıdaki tablo, sınıfın tüm temel attribute’larını ve özel metotlarını kategorilere ayrılmış şekilde gösterir.  

| 🧱 **Kategori** | ⚙️ **Attribute / Metot** | 🧠 **Açıklama** |
|-----------------|---------------------------|------------------|
| 📘 **Bilgi / Temel İşlevler** | `__class__` | Nesnenin tipi (`<class 'int'>`) |
|  | `__doc__` | Sınıf açıklama dökümanı |
|  | `__new__` | Nesne oluşturucu (**immutable** türlerde kullanılır) |
| ➕ **Matematiksel Operatörler** | `__add__`, `__sub__`, `__mul__`, `__floordiv__`, `__mod__`, `__pow__` | Aritmetik işlemler |
| ⚙️ **Bit Düzeyi Operatörler** | `__and__`, `__or__`, `__xor__`, `__invert__`, `__lshift__`, `__rshift__` | Bitwise işlemler |
| ⚖️ **Karşılaştırma Operatörleri** | `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__` | Karşılaştırma davranışları |
| 🔁 **Tür Dönüşümleri** | `__int__`, `__float__`, `__bool__`, `__index__` | Tür dönüşüm protokolleri |
| 🧩 **Temel Nesne Davranışları** | `__repr__`, `__str__`, `__hash__` | Metin gösterimi ve hashleme |
| 🧮 **Diğer Dunder’lar** | `__abs__`, `__neg__`, `__pos__` | İşaret, mutlak değer, pozitif işlem |
| 🧠 **Yapılandırma Metotları** | `bit_length()`, `bit_count()` | Bit düzeyinde bilgi alma |
|  | `to_bytes(length, byteorder, *, signed=False)` | Byte dizisine dönüştürür |
|  | `from_bytes(bytes, byteorder, *, signed=False)` *(classmethod)* | Byte dizisinden int oluşturur |
| 🔹 **Mantıksal / Boolean** | `__bool__()` | `0 → False`, diğer → `True` |
| 🧩 **Sınıf Özellikleri** | `__bases__` | (Boş tuple) çünkü doğrudan `object`’ten gelir |
| 💾 **Bellek Yönetimi** | `__sizeof__()` | Nesnenin RAM boyutunu verir |
| 🧬 **Miras Özelliği** | `__subclasshook__()` | ABC mekanizması için tanımlanmıştır |
| 🎯 **Sürpriz Davranışlar** | `__round__`, `__trunc__`, `__floor__`, `__ceil__` | Sayıların kesilmesiyle ilgili davranışlar |

---

> 💡 **Not:**  
> - `int` sınıfı **C düzeyinde tanımlı** olduğundan bu metotların çoğu Python’dan override edilemez.  
> - Ancak alt sınıflar (`class MyInt(int): ...`) tanımlanarak `__repr__`, `__add__`, `__hash__` gibi davranışlar özelleştirilebilir.  
> - `bit_length()` ve `bit_count()` metodları, Binary Data Model’in *bit düzeyi bilgi katmanı* ile doğrudan ilişkilidir.  

---

---

### 🧩 `__new__` — Nesne Oluşturucu Metot (int Sınıfı)

---

#### 📘 Tanım

`__new__`, `int` sınıfında **nesne oluşturma aşamasını yöneten** özel metottur.  
`int` immutable (değiştirilemez) bir tür olduğu için,  
bu sınıfta nesne yaratımı yalnızca `__new__` üzerinden gerçekleşir.  
Yani `__init__` aşaması, bellekteki değeri değiştiremez — sadece var olan nesne döner.

> 🧠 Kısaca: `__new__` → “RAM’de int nesnesi oluşturur”,  
> `__init__` → “var olan nesneyi başlatır (int’te etkisizdir)”.

---

#### ⚙️ İmza (int’e Özgü)

```python
def __new__(cls: type[int], 
            x: int | float | str | bytes | bytearray | bool = 0, 
            base: int = 10) -> int: ...
```
#### 📊 Parametre ve Dönüş Değeri Tablosu — `int()` Yapıcısı

| 🧩 Parametre | 🧠 Tür           | 🎯 Açıklama                                                                 |
|-------------|------------------|------------------------------------------------------------------------------|
| `cls`       | `type[int]`      | Sınıfın kendisi (`int` veya alt sınıfı). Genellikle `__new__` çağrılarında kullanılır. |
| `x`         | `int`, `float`, `str`, `bytes`, `bytearray` | Sayıya dönüştürülecek değer. `str`, `bytes`, `bytearray` için `base` gerekir. |
| `base`      | `int`            | Sadece `x` bir `str`, `bytes` veya `bytearray` ise kullanılır (örn. `int("101", 2)`). |
| `return`    | `int`            | Yeni oluşturulmuş `int` nesnesi döner.                                      |

#### 📊 `int()` Yapıcısında `base` Parametresi Davranış Tablosu

| 🧩 `x` Türü        | ⚙️ `base` Geçerli mi? | 🎯 Açıklama |
|-------------------|----------------------|-------------|
| `int`             | ❌ Hayır              | Zaten `int`, dönüşüm gerekmez; `base` kullanılamaz. |
| `float`           | ❌ Hayır              | Ondalıklı sayı tabanla yorumlanamaz; `base` geçersizdir. |
| `bool`            | ❌ Hayır              | `True → 1`, `False → 0` sabit dönüşüm; `base` etkisizdir. |
| `str`             | ✅ Evet               | `"101"` gibi metinler belirtilen tabana göre çözülür. |
| `bytes`           | ✅ Evet               | `b"77"` gibi bayt dizileri belirtilen tabana göre çözülür. |
| `bytearray`       | ✅ Evet               | `bytearray(b"FF")` gibi yapılar belirtilen tabana göre çözülür. |

> 🎯 **Amaç:** `base` parametresi, metin tabanlı sayıların hangi sayı sistemine göre çözümleneceğini belirtmek için kullanılır.  
> Bu sayede `"101"` gibi bir metin, ikilik (`base=2`), sekizlik (`base=8`), onaltılık (`base=16`) gibi farklı tabanlarda doğru şekilde sayıya dönüştürülebilir.

> 💡 **Not:** `base=0` özel bir moddur; bu durumda Python, `x`’in ön ekine göre tabanı otomatik seçer (`0b`, `0x`, `0o`).  
> Diğer türler için `base` kullanımı `TypeError` ile sonuçlanır.
.

---

#### ⚠️ Dikkat Edilmesi Gerekenler — `__new__` ve `int` Alt Sınıfları

| ⚠️ Durum                  | 💬 Açıklama                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| 🧱 **Immutable yapı**       | `__new__` tek geçerli oluşturucu aşamadır; `__init__` etkisizdir.           |
| 💾 **Değer atama**         | Değer yalnızca `super().__new__(cls, value)` içinde belirlenebilir.         |
| 🧩 **Alt sınıflarda zorunlu** | `int` alt sınıfı yazıyorsan `__new__` metodunu override etmek gerekir.     |
| ⚙️ **Built-in tiplerde**    | `__new__` doğrudan `long_new()` (C fonksiyonu) ile eşlenir.                 |
| ❌ **Yanlış dönüş tipi**    | `__new__` bir `int` döndürmezse → `TypeError` fırlatılır.                   |
| 🧠 **Caching**             | CPython `-5` ile `256` arasındaki sayılar için `__new__` sonucunu cache’ler.|
| 🔒 **Attribute erişimi**    | Built-in `int` → attribute lookup bypass edilir,  
user-defined alt sınıf → lookup zinciri devreye girer. |

> 💡 Bu kurallar, `int` gibi immutable built-in türlerin alt sınıflanmasında hem performans hem de güvenlik açısından kritik rol oynar.

> 🧠 **Not — CPython’da int Caching Mantığı**  
> CPython yorumlayıcısı, `-5` ile `256` arasındaki `int` değerlerini önceden oluşturur ve bellekte saklar.  
> Bu sayede bu aralıktaki sayılar tekrar tekrar oluşturulmaz, aynı nesne referansı kullanılır.  
> Örneğin `a = 42; b = 42` ifadesinde `a is b → True` olur çünkü `42` cache’lenmiş bir nesnedir.  
> Bu optimizasyon hem performansı artırır hem de bellek tasarrufu sağlar.  
> Ancak bu davranış sadece CPython’a özgüdür ve `int` alt sınıflarında devre dışı kalabilir.

> 🧠 **Not2 — `int` Alt Sınıfları ve Gerçek Davranış** 
> 
>tüm yapılandırma `__new__()` içinde yapılmalıdır.
>Eğer `__add__`, `__float__`, `__repr__` gibi metotlar override edilecekse, `self + other` gibi ifadeler **sonsuz döngü** oluşturabilir.  
>Çünkü `self + other` → `__add__` → `self + other` → ... şeklinde tekrar tekrar aynı metodu çağırır.
>Bu döngüyü kırmak için `int.__add__(self, other)` gibi **base sınıfın metodları doğrudan çağrılmalıdır**.
>Ek veri eklemek istenirse, `__new__()` içinde `obj.label = ...` gibi atamalar yapılabilir — ama bu sadece `int`’ten miras alınmış sınıflarda geçerlidir.
> ✅ Gerçek `int` davranışı istiyorsan, miras almak zorundasın.  
> Aksi halde sınıfın sadece görsel bir kılıf olur, semantik olarak `int` gibi davranmaz.


---

### ⚙️ Bit Düzeyinde Operatörler (`__and__`, `__or__`, `__xor__`, `__invert__`, `__lshift__`, `__rshift__`)

---

#### 📘 Tanım

Bit düzeyinde operatörler (`&`, `|`, `^`, `~`, `<<`, `>>`),  
`int` sınıfında tanımlı olan ve sayının **binary temsili** üzerinde işlem yapan özel metotlardır.

Bu operatörler `int` nesnesinin sayısal değerini **bit bit** ele alır;  
matematiksel toplama veya çıkarma işlemi değil, **mantıksal bit manipülasyonu** yaparlar.

> 🧠 Kısaca: “Bu metotlar sayıların RAM’deki 0–1 temsili üzerinde çalışır.”

---

#### ⚙️ Ortak İmza (int’e Özgü)

```python
def __and__(self: int, other: int) -> int: ...
def __or__(self: int, other: int) -> int: ...
def __xor__(self: int, other: int) -> int: ...
def __invert__(self: int) -> int: ...
def __lshift__(self: int, other: int) -> int: ...
def __rshift__(self: int, other: int) -> int: ...

```
#### 📊 Bit Düzeyli Özel Metotlar — Parametre Açıklamaları

| 🧩 Metot         | 📥 Parametreler             | 🎯 Açıklama                                                                 |
|------------------|-----------------------------|------------------------------------------------------------------------------|
| `__and__`        | `self: int`, `other: int`   | `self & other` → bit düzeyinde VE işlemi                                    |
| `__or__`         | `self: int`, `other: int`   | `self | other` → bit düzeyinde VEYA işlemi                                  |
| `__xor__`        | `self: int`, `other: int`   | `self ^ other` → bit düzeyinde XOR işlemi                                   |
| `__invert__`     | `self: int`                 | `~self` → bit düzeyinde tüm bitleri ters çevirir (tek operandlıdır)         |
| `__lshift__`     | `self: int`, `other: int`   | `self << other` → bitleri sola kaydırır                                     |
| `__rshift__`     | `self: int`, `other: int`   | `self >> other` → bitleri sağa kaydırır                                     |

> ⚠️ `other` parametresi tüm ikili işlemlerde zorunludur.  
> `__invert__` ise unary (tek operandlı) olduğu için yalnızca `self` alır.

---

#### ⚙️ Opcode Düzeyi Zincir — Bit Düzeyli Operatörler

| 🔣 Operatör | 🧩 Opcode         | ⚙️ C Fonksiyonu     |
|------------|------------------|---------------------|
| `&`        | `BINARY_AND`     | `long_and()`        |
| `|`        | `BINARY_OR`      | `long_or()`         |
| `^`        | `BINARY_XOR`     | `long_xor()`        |
| `~`        | `UNARY_INVERT`   | `long_invert()`     |
| `<<`       | `BINARY_LSHIFT`  | `long_lshift()`     |
| `>>`       | `BINARY_RSHIFT`  | `long_rshift()`     |

> 💡 Bu opcode’lar doğrudan C fonksiyonlarına bağlanır.  
> Yani built-in `int` tipi için Python düzeyinde attribute lookup yapılmaz — doğrudan **C slot’ları** çağrılır (`tp_as_number` üzerinden).

### 🧠 4️⃣ Peki “opcode düzeyi”nde ne oluyor?

- **CPython, bu işlemleri çalıştırırken doğrudan C seviyesindeki özel fonksiyonlara gider.**
    - Yani **evet** — bu işlemler özel opcode olarak derlenir.



```python
0b1010 & 0b0110

>>>

2           0 LOAD_CONST               2 (10)
            2 LOAD_CONST               3 (6)
            4 BINARY_AND
            6 RETURN_VALUE
```
- Böylece:

  - Python kodundaki `a & b`

  - Bytecode’daki `BINARY_AND`

  - C tarafındaki `PyNumber_And`

  - ve en sonunda `int`’in `nb_and` fonksiyon pointer’ına ulaşır

---

#### ⚠️ Dikkat Edilmesi Gerekenler — Bit Düzeyli `int` İşlemleri

| ⚠️ Durum                     | 💬 Açıklama                                                                 |
|------------------------------|------------------------------------------------------------------------------|
| 🧱 **Immutable yapı**         | Her işlem yeni bir `int` nesnesi üretir; mevcut nesne değiştirilemez.       |
| ⚙️ **Binary tabanlı işlem**   | İşlemler matematiksel değil, bit düzeyinde mantıksal olarak yürütülür.     |
| 🧩 **Negatif sayılar**        | Python `int`’leri sınırsız uzunlukta işler (two’s complement değil); bu yüzden `~x` → `-(x + 1)` olur. |
| 🧠 **Performans**             | C tabanlı `long_*` fonksiyonlarıyla çalıştığı için oldukça hızlıdır.       |
| ❌ **float veya str ile işlem** | Sadece `int` veya `bool` kabul edilir; aksi halde `TypeError` fırlatılır. |
| 🧮 **Kaydırma sınırı**        | `a << n` işleminde `n` negatifse → `ValueError` oluşur.                    |
| 💡 **bool uyumluluğu**        | `bool`, `int`’ten türediği için `True & False` gibi işlemler geçerlidir.   |
| 🧩 **User-defined alt sınıf** | Override edilirse Python düzeyinde attribute lookup devreye girer → C slot bypass edilmez. |

> 🧠 Bu kurallar, hem performans hem de güvenli subclassing açısından kritik öneme sahiptir.



---

### ⚖️ Karşılaştırma Operatörleri (`__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`,  `__ge__`)

---

#### 📘 Tanım

Karşılaştırma operatörleri, `int` nesnelerinin birbirine göre **eşitlik veya büyüklük ilişkisini**
belirlemek için kullanılan özel metotlardır.  

Bu metotlar, `==`, `!=`, `<`, `<=`, `>`, `>=` gibi operatörlerin arka planında çalışır  
ve sonuç olarak **boolean** (`True` veya `False`) değer döndürürler.  

> 🧠 `int` sınıfında bu işlemler doğrudan sayının **sayısal değerine** uygulanır;  
> yani herhangi bir “referans” veya “adres” karşılaştırması yapılmaz.

---

#### ⚙️ İmza (int’e Özgü)

```python
def __eq__(self: int, other: int | float | bool) -> bool: ...
def __ne__(self: int, other: int | float | bool) -> bool: ...
def __lt__(self: int, other: int | float | bool) -> bool: ...
def __le__(self: int, other: int | float | bool) -> bool: ...
def __gt__(self: int, other: int | float | bool) -> bool: ...
def __ge__(self: int, other: int | float | bool) -> bool: ...
```
#### 🔍 Karşılaştırma Metotları — Parametre Tablosu

| 🧩 Parametre | 🧬 Tür         | 💬 Açıklama                                 |
|-------------|---------------|---------------------------------------------|
| `self`      | `int`         | Sol operand                                 |
| `other`     | `int`, `float`| Sağ operand (karşılaştırılacak değer)       |
| `return`    | `bool`        | Karşılaştırma sonucu (`True` veya `False`)  |

> 💡 `bool` türü `int`’ten miras aldığı için (`True == 1`, `False == 0`),  
> karşılaştırmalarda `int` ile birlikte doğal olarak çalışabilir.

---
### 🧩 Kullanım Alanı — Karşılaştırma Metotları

Bu metotlar, sayısal büyüklük, eşitlik ve sıralama ilişkilerini kontrol etmek için kullanılır.  
`int` türü sıralanabilir (orderable) olduğu için bu karşılaştırma işlemleri her zaman tanımlıdır.

#### 🎯 Tipik Kullanım Senaryoları

- Kullanıcı girdilerini kontrol etmek  
- Sıralama algoritmaları yazmak  
- Veri aralıklarını sınırlandırmak

#### ⚙️ Python İç Mekanizmasında Kullanımı

Python’un yerleşik fonksiyonları da bu metotlara dayanır:

- `sorted()`  
- `min()`  
- `max()`  

> 💡 Bu metotlar, hem uygulama düzeyinde hem de Python’un çekirdek davranışlarında kritik rol oynar.

### 🧠 Çalışma Mantığı

Tüm karşılaştırma işlemleri, **C tarafında tanımlı olan** ` PyLong_RichCompare()`  fonksiyonu üzerinden yürütülür.
Bu fonksiyon, operandların tipine göre uygun işlemi seçer ve karşılaştırmayı düşük seviyede yapar.

**C düzeyinde zincir şu şekildedir:**

```sql
BINARY_OP (==, <, >, ...) opcode
│
└──> PyObject_RichCompare(left, right, op)
      │
      └──> PyLong_RichCompare(a, b, op)
            │
            └──> long_compare() → Py_RETURN_TRUE / FALSE
```

- **Bu işlem sırasında:**
    - **Her iki nesnenin de türü `int` ise →** doğrudan sayısal kıyaslama yapılır

    - **Eğer biri `float` ise** → float’a dönüştürülüp karşılaştırılır

    - **Eğer türler uyumsuzsa** → NotImplemented döndürülür (ve Python `__eq__` yerine `__req__` dener)
    
    > 💡 `PyLong_RichCompare()`  aslında `memcmp()` benzeri bir algoritmayla çalışır:
    önce işaretleri, sonra uzunluklarını (digit sayısı), en sonunda her ob_digit değerini karşılaştırır
  
#### ⚙️ Opcode Düzeyi Zincir — Karşılaştırma Operatörleri

| 🔣 Operatör | 🧩 Opcode         | ⚙️ C Fonksiyonu           |
|------------|------------------|---------------------------|
| `==`       | `COMPARE_OP (==)`| `PyLong_RichCompare()`    |
| `!=`       | `COMPARE_OP (!=)`| `PyLong_RichCompare()`    |
| `<`        | `COMPARE_OP (<)` | `PyLong_RichCompare()`    |
| `<=`       | `COMPARE_OP (<=)`| `PyLong_RichCompare()`    |
| `>`        | `COMPARE_OP (>)` | `PyLong_RichCompare()`    |
| `>=`       | `COMPARE_OP (>=)`| `PyLong_RichCompare()`    |

> 💡 Bu opcode’lar önce `PyObject_RichCompare()` fonksiyonunu çağırır.  
> Ardından ilgili tipin `tp_richcompare` slot’una gider — `int` için bu `PyLong_RichCompare()`’dır.

#### ⚠️ Dikkat Edilmesi Gerekenler — Karşılaştırma İşlemleri

| 🧩 Durum                  | 💬 Açıklama                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| 🧱 Immutable yapı          | Karşılaştırma nesneyi değiştirmez, sadece yeni bir `bool` döner.             |
| ⚙️ Performans              | C düzeyinde çalışır, çok hızlıdır (küçük sayılar cache’lendiği için ekstra hızlı). |
| 🧩 Tür uyumu               | `int` ↔ `float` karşılaştırması geçerlidir; `int` ↔ `str` geçersizdir (`TypeError`). |
| 🧠 bool davranışı          | `True == 1` ve `False == 0` → her zaman `True` döner.                        |
| ⚡ Küçük sayı cache etkisi | `-5` ile `256` arası sayılar önbelleklendiği için `is` karşılaştırması `True` olabilir. |
| 🧮 Sıralama işlemleri      | `sorted()`, `min()`, `max()` gibi fonksiyonlar bu dunder’ları doğrudan çağırır. |
| 🚫 NaN özel durumu         | `int` ile `float('nan')` karşılaştırması her zaman `False` döner.            |

> 💡 Bu metotlar hem Python’un iç mekanizmasında hem de uygulama düzeyinde kritik rol oynar.

---

## 🧩 1️⃣ Sağ (Reflected) Karşılaştırma Metotları Nedir?

Python’da `a < b` gibi bir karşılaştırma yapıldığında, önce sol operandın (`a`) ilgili özel metodu çağrılır.  
Eğer bu metod uygun değilse veya `NotImplemented` dönerse, Python ikinci bir şans verir:  
**sağ operandın reflected versiyonunu** çağırır.

### 🔁 Karşılaştırma Akışı

| 🔣 Operatör | ▶️ Sol Metot      | 🔄 Sağ Metot (Reflected) |
|------------|-------------------|---------------------------|
| `<`        | `a.__lt__(b)`     | `b.__gt__(a)`             |
| `<=`       | `a.__le__(b)`     | `b.__ge__(a)`             |
| `>`        | `a.__gt__(b)`     | `b.__lt__(a)`             |
| `>=`       | `a.__ge__(b)`     | `b.__le__(a)`             |
| `==`       | `a.__eq__(b)`     | `b.__eq__(a)`             |
| `!=`       | `a.__ne__(b)`     | `b.__ne__(a)`             |

Bu sisteme **reflected method** denir.  
Ancak dikkat: `__r*__` öneki (`__radd__`, `__rsub__` gibi) **aritmetik işlemler** için geçerlidir.  
Karşılaştırmalarda Python, **simetrik eşleştirme** kullanır — yani `__rlt__` gibi metotlar yoktur.

---

### 🧠 2️⃣ Fallback (Geri Dönüş) Mekanizması Nasıl Çalışır?

Karşılaştırma işlemi sırasında Python, metotlar `NotImplemented` dönerse alternatif yollar dener.

#### 🔍 Örnek Senaryo

İki farklı sınıf: `A` ve `B`

1. `A.__lt__(B)` çağrılır.  
2. Eğer `NotImplemented` dönerse → `B.__gt__(A)` denenir.  
3. Eğer bu da `NotImplemented` dönerse → işlem başarısız olur → `TypeError` yükseltilir.

> 💡 Bu mekanizma, farklı türler arasında karşılaştırma yapılabilmesini sağlar.  
> Özellikle `int`, `float`, `Decimal`, `Fraction` gibi türler arasında uyumlu çalışmayı mümkün kılar.

### ⚙️ 3️⃣ Sağ Taraf (Reflected) Karşılaştırmaların İsimleri

Karşılaştırma işlemleri için `__rlt__`, `__rgt__` gibi metotlar tanımlı değildir.  
Ancak Python bu davranışı **otomatik olarak uygular** — yani simetrik eşleştirme yapar.

#### 🔁 Reflected Karşılaştırma Akışı

| 🔣 Operatör | 🧩 Sol Metot            | 🔄 Python’un Çağırdığı Sağ Metot |
|------------|-------------------------|----------------------------------|
| `<`        | `a.__lt__(b)` → `NotImplemented` | `b.__gt__(a)`              |
| `>`        | `a.__gt__(b)` → `NotImplemented` | `b.__lt__(a)`              |
| `<=`       | `a.__le__(b)` → `NotImplemented` | `b.__ge__(a)`              |
| `>=`       | `a.__ge__(b)` → `NotImplemented` | `b.__le__(a)`              |
| `==`       | `a.__eq__(b)` → `NotImplemented` | `b.__eq__(a)`              |
| `!=`       | `a.__ne__(b)` → `NotImplemented` | `b.__ne__(a)`              |

> 🔍 Aritmetik operatörlerde (`__radd__`, `__rsub__` vb.) manuel olarak `__r*__` metotları tanımlanır.  
> Ancak karşılaştırmalarda Python bu simetrik eşleştirmeyi **kendisi otomatik olarak yapar**.

### 🧩 4️⃣ Bu Mekanizmanın Kökeni — İlgili PEP

Bu davranış, [PEP 207 – Rich Comparisons](https://peps.python.org/pep-0207/) tarafından tanımlanmıştır.  
Yazar: Guido van Rossum (Eylül 2000)

#### 📘 PEP 207 Özeti

- Karşılaştırmalar artık tek `__cmp__` yerine ayrı ayrı `__eq__`, `__lt__`, `__gt__` vb. metotlarla tanımlanır.
- Her karşılaştırma metodu birbirinden bağımsızdır.
- Eğer bir operand karşılaştırmayı desteklemiyorsa → `NotImplemented` döndürmelidir.
- Python bu durumda **karşı operandın simetrik metodunu** otomatik olarak dener (fallback).
- Eğer ikisi de `NotImplemented` dönerse → `TypeError` fırlatılır.

> 💡 PEP 207 ayrıca şunu belirtir:  
> Karşılaştırmaların **zorunlu olarak tutarlı olması gerekmez**.  
> Yani `a < b → True` olsa bile, `a == b` → `False` olabilir.  
> Bu tasarım Python’a esneklik kazandırmak için bilinçli olarak seçilmiştir.

### ⚠️ 6️⃣ Dikkat Edilmesi Gerekenler — Reflected Karşılaştırmalar

| 🧩 Durum                      | 💬 Açıklama                                                                 |
|------------------------------|------------------------------------------------------------------------------|
| ⚙️ NotImplemented dönüşü      | Python’a “diğer operandı dene” sinyali gönderir.                            |
| 🧠 Reflected otomatik eşleştirme | `<` ve `>` gibi işlemlerde Python otomatik olarak tersini dener.         |
| 🔁 Simetri zorunlu değil      | `a < b → True` iken `b > a → False` olabilir (kasıtlı tasarım).            |
| 🚫 Her iki taraf NotImplemented | Her iki operand `NotImplemented` dönerse → `TypeError` fırlatılır.       |
| 🧩 PEP 207 temeli             | Rich Comparison protokolü bu davranışı resmileştirmiştir.                  |
| ⚙️ Performans etkisi          | Karşı operand denenmesi küçük bir maliyet getirir, genelde ihmal edilebilir. |
| 💡 Custom sınıflarda          | `__lt__`, `__gt__` override edilerek özel sıralama kuralları tanımlanabilir. |

> 💡 Bu sistem, Python’un esnek ve genişletilebilir karşılaştırma modelinin temelini oluşturur.

---

### 🔁 Tür Dönüşümü Metodları

---

#### 📘  Tanım:

Python’da tür dönüşüm metotları, bir nesnenin **belirli bir türde nasıl temsil edileceğini** tanımlayan özel protokollerdir.  
Bu metotlar, `int(x)`, `float(x)`, `complex(x)`, `bool(x)`, `index(x)` gibi çağrılarda devreye girer.

Python’da bir nesneyi başka bir türde kullanmak istediğinde (örneğin `int(x)`),  
Python o nesneye sorar: “Senin tamsayı karşılığın nedir?”

Bu soruya cevap verebilmesi için her tür, **kendi dönüşüm metodunu tanımlar**.

#### 🔧 Ne Demek Bu?

Her veri türü, kendisini başka bir türde nasıl göstereceğini **kendi içinde tanımlar**:


Bu metodlar sayesinde bir nesne, farklı türlere dönüştürülerek çeşitli işlemlerde kullanılabilir.

#### 🔧 Otomatik Devreye Giren Dönüşümler

- `int(x)` → `x.__int__()`  
- `float(x)` → `x.__float__()`  
- `bool(x)` → `x.__bool__()`  
- `complex(x)` → `x.__complex__()`

#### 🧮 Tamsayı Gerektiren Yapılar

Bu dönüşüm metodları ayrıca aşağıdaki gibi yapılar içinde **otomatik olarak devreye girer**:

- `range(start, stop)`  
- `bin(x)`, `hex(x)`  
- `slice(start, stop, step)`

> 💡 Bu protokoller, Python’un esnek ve güvenli tür dönüşüm sisteminin temelini oluşturur.  
> Özellikle `int`, `float`, `bool` gibi türlerle uyumlu çalışmak isteyen custom sınıflar için kritik öneme sahiptir.

---


#### ⚠️ Sınıf Çağrısı Gibi Görünür Ama Değildir

Bu dönüşümler, **normal sınıf çağrısı gibi görünse de**, `metaclass.__call__` zincirine girmezler.  
Yani `int(x)` ifadesi, `int.__call__` veya `type.__call__` üzerinden yürütülmez.

#### ⚙️ Gerçekleşen Şey

Python bu çağrıları doğrudan **C düzeyindeki numeric conversion API** fonksiyonlarına bağlar:

- `PyNumber_Long(x)` → `int(x)`  
- `PyNumber_Float(x)` → `float(x)`  
- `PyObject_IsTrue(x)` → `bool(x)`  
- `PyNumber_Index(x)` → `index` dönüşümü  
- `PyNumber_Complex(x)` → `complex(x)`

#### 🎯 Sonuç

- `int(x)` → yeni bir `int` nesnesi oluşturmaz.  
- Bunun yerine `x` nesnesinin uygun `int` temsili döndürülür (`x.__int__()`).

> 💡 Bu sistem, Python’un türler arası uyumlu ve hızlı dönüşüm mekanizmasının temelidir.


#### 📌 Dikkat Edilmesi Gereken Ortak Noktalar

| 🚩 Durum                  | 📌 Açıklama                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| ✅ Dönüş tipi zorunluluğu | Her dönüşüm metodu, **belirli bir türü** döndürmelidir → aksi halde `TypeError`. |
| 🔁 Kimlik dönüşümü        | Eğer kaynak zaten hedef türse → `return self` yapılır.                      |
| ⚙️ Performans             | Bu dönüşümler C düzeyinde optimize edilmiştir → çok hızlıdır.               |
| 🧩 Protokol uyumu         | Her tür, dönüşüm protokolüne uymak için ilgili metodu tanımlar.             |
| 🚫 Sınıf çağrısı değildir | `int(x)` gibi çağrılar → `type.__call__` değil, doğrudan `x.__int__()` gibi çalışır. |

> 🧠 Bu yapı, Python’un **duck typing**, **explicit protocol** ve **extensibility** ilkeleriyle birebir örtüşür.

---

### 🧩 `int.__index__` — Tanım

`__index__` metodu, bir nesnenin **indeks olarak kullanılabilir tamsayı karşılığını** tanımlar.  
Bu metot, `int` sınıfında tanımlıdır ve `int` nesneleri için `index` bağlamlarında otomatik olarak devreye girer.

> 🎯 Amaç: `int` nesnelerinin `range()`, `slice()`, `bin()`, `hex()` gibi yapılar içinde **indeks** olarak kullanılabilmesini sağlamak.

#### ⚙️ `int.__index__` — İleri Tanım (C Düzeyi)

Python’un C API’sinde bu dönüşüm şu fonksiyonla gerçekleştirilir:

```c
PyNumber_Index(x)
```
- **Bu fonksiyon:**

    - `x.__index__()` metodunu çağırır.

    - **Eğer metod tanımlıysa** → dönüşüm yapılır.

    - **Tanımlı değilse** → `TypeError` fırlatılır.
    
    - **🔧 Bu dönüşüm, `__int__`’ten farklıdır: sadece indeks bağlamlarında çağrılır.**
---

#### 🧩 PEP 357 — `__index__` Protokolü ve Çağrı Zinciri

PEP 357, Python’da **indeks olarak kullanılabilir nesneler** için özel bir dönüşüm protokolü tanımlar.  
Bu protokol, `__index__()` metoduna dayanır ve `range()`, `slice()`, `bin()`, `hex()` gibi yapılar içinde devreye girer.

#### 🔁 Çağrı Zinciri — `index(x)` Nasıl Çalışır?

```text
🔹 index(x)
   │
   └──► 🛠️ PyNumber_Index(x)  ← C düzeyindeki dönüşüm fonksiyonu
         │
         ├──► ✅ Eğer x.__index__() varsa → çağır
         │       └── return int değer
         │
         └──► ❌ Yoksa → TypeError: 'type' object cannot be interpreted as an integer
```

#### 📘 PEP 357’in Getirdiği Yenilik

PEP 357, Python’da `__index__()` metodunu tanımlayarak **tam sayı gibi davranan nesnelerin indeks olarak kullanılmasını resmileştirir**.

Bu sayede:

- `int`, `bool`, `Fraction`, `Decimal` gibi yerleşik türler
- 🧩 Ve **kullanıcı tanımlı sınıflar** (`user-defined classes`)  
  → `__index__()` metodunu tanımlayarak `range()`, `slice()`, `bin()`, `hex()` gibi yapılarda **indeks olarak** kullanılabilir hale gelir.

#### 🔁 Karıştırılmaması Gereken Fark

| Metot         | Amaç                         | Kullanım Bağlamı                      |
|---------------|------------------------------|---------------------------------------|
| `__int__()`   | Genel tamsayı dönüşümü       | `int(x)` gibi sayısal dönüşümler      |
| `__index__()` | İndeks olarak temsil edilme  | `range(x)`, `slice(x)`, `bin(x)` gibi yapılar |

> 💡 PEP 357 sayesinde Python:
> - 🔐 Daha **güvenli**: yalnızca `__index__()` tanımlı nesneler indeks olabilir  
> - 🔧 Daha **genişletilebilir**: özel sınıflar da indeks bağlamına katılabilir  
> - 🧠 Daha **sezgisel**: `int` gibi davranan nesneler indeks olarak kullanılabilir

---
### 🧪 Örnek

---

```python
class MyCounter:
    def __init__(self, value):
        self.value = value

    def __index__(self):
        print(f"__index__ çağrıldı → {self.value}")
        return self.value
```
#### 🔧 Kullanım
```python
counter = MyCounter(5)

for i in range(counter):
    print(i)
```
---

### 🧮 İşaret (Unary) Operatör Dunder’ları

Python’da `__abs__`, `__neg__`, `__pos__` metotları, bir sayının **matematiksel yönünü** tanımlayan özel dunder’lardır.  
Bu metotlar, **tek operandlı (unary)** işlemlerin Python düzeyindeki karşılıklarıdır.

> 🎯 Amaç: Sayının değerini değiştirmeden, onun **işaretini** (pozitif/negatif/yönsüz) ifade etmek.

#### 🧩 1️⃣ Ortak Tanım

| Metot       | Anlamı                            | Açıklama                                               |
|-------------|-----------------------------------|--------------------------------------------------------|
| `__abs__()` | Mutlak değer                      | Sayının yönsüz hali → `abs(-5)` → `5`                 |
| `__neg__()` | Negatifleştirme                   | Sayının eksiyle çarpılmış hali → `-x` → `__neg__()`   |
| `__pos__()` | Pozitif kimliği koruma            | Sayının artı işaretiyle temsil edilmesi → `+x`        |

Bu metotlar şunlarda tanımlıdır:

- `int`, `float`, `complex`  
- `Fraction`, `Decimal`  
- Ve istenirse `user-defined`  sınıflarda

> 💡 Bu metotlar, sayının **değerini değil yönünü** tanımlar.


#### ⚙️ 2️⃣ İleri Tanım — C Düzeyinde Davranış

Python yorumlayıcısı bu işlemleri doğrudan C API üzerinden gerçekleştirir.  
Her biri `PyNumberMethods` adlı yapının **unary slot** alanlarına bağlıdır.

| Python Metodu | C API Fonksiyonu       | Slot Adı        |
|---------------|------------------------|-----------------|
| `__abs__()`   | `PyNumber_Absolute()`  | `nb_absolute`   |
| `__neg__()`   | `PyNumber_Negative()`  | `nb_negative`   |
| `__pos__()`   | `PyNumber_Positive()`  | `nb_positive`   |

> 🔧 Bu yapı sayesinde Python, sayısal türlerde işaret işlemlerini hızlı ve tutarlı şekilde uygular.

---

### 🧾 İşaret (Unary) Operatör Dunder’larının Ortak İmzaları

Bu üç metot — `__abs__`, `__neg__`, `__pos__` — aynı yapıda tanımlanır:  
Tek parametre alırlar (`self`) ve dönüş tipi sayısal (`int`, `float`, `complex` vs.) olmalıdır.

### 🔹 Ortak İmza Formatı

```python
def __abs__(self) -> Number:
    ...

def __neg__(self) -> Number:
    ...

def __pos__(self) -> Number:
    ...

```
#### 📋 İşaret Operatör Dunder’ları — Parametre Tablosu

| 🔣 Parametre | 🧮 Tür     | 📘 Açıklama                                           |
|--------------|------------|--------------------------------------------------------|
| `self`       | Sayısal    | İşlem uygulanacak nesne (`int`, `float`, `complex`, vs.) |
| `return`     | Sayısal    | İşlem sonucunda elde edilen yeni değer                |

> 💡 Her metot, sayının **yönünü değiştirir** ama **değerini korur** — pozitif, negatif veya mutlak temsil sağlar.

> 💡Tüm dönüş değerleri aynı türdendir — yani
>`int` → `int`, `float` → `float`, `complex` → `complex`.
>Bu, **“işlemin tür değiştirmediği”** anlamına gelir.

---


### 🧩 User-Defined Sınıflarda Kullanım

Bu metotlar yalnızca gömülü türlerle sınırlı değildir.  
Kendi tanımladığın sınıflarda da `__abs__`, `__neg__`, `__pos__` metodlarını override edebilirsin.

Python’un **duck typing** felsefesi gereği:

- Dönüş değerinin türü zorunlu değildir.
- Ancak **sayısal olarak anlamlı** olmalıdır:
  - ✅ `float`, `Decimal`, `Vector`, `Matrix` gibi türler uygundur.
  - ❌ `"negatifim"` gibi string dönerse → Python bunu hemen reddetmez,
    ama sonraki işlemlerde (`x + (-obj)`) → `TypeError` fırlatır.

> 🧠 Python, dönüşümün anlamlı olup olmadığını **kullanım bağlamında** değerlendirir.

#### ⚙️ Override Etmenin Sonuçları

Bu metotları override ettiğinde:

- Python artık C düzeyindeki `PyNumber_*` opcode zincirini kullanmaz.
- Bunun yerine **senin Python düzeyindeki metodun** çağrılır.
- Bu da:
  - 🔻 Bir miktar performans kaybı yaratabilir.
  - 🎯 Ama davranış tamamen senin kontrolüne geçer.

> 💡 Özellikle `__neg__` ve `__abs__` gibi işlemlerde özel mantık tanımlamak için bu esneklik çok değerlidir.

---

### 📌 Kullanım Örnekleri

```python
x = -7

abs(x)   # __abs__ → 7
-x       # __neg__ → -7
+x       # __pos__ → -7

```
Ama C tarafında:
```c
PyObject *PyNumber_Absolute(PyObject *o);
PyObject *PyNumber_Negative(PyObject *o);
PyObject *PyNumber_Positive(PyObject *o);
```
💡 **Yorumlayıcı**, nesnenin tipine (`PyLong_Type`, `PyFloat_Type`, vs.) bakarak
ilgili slot’u (`nb_absolute,` `nb_negative`, `nb_positive`) çağırır.

---

### 📦 `int.__sizeof__()` — Bellek Boyutu Dunder’ı

Python’daki `int` nesneleri sabit bitli değildir — büyüklüğe göre dinamik olarak genişler.  
`__sizeof__()` metodu, bir `int` nesnesinin bellekte kapladığı alanı **byte cinsinden** döndürür.

> 🎯 Amaç: Sayının bellekte kaç byte tuttuğunu ölçmek — özellikle büyük `int` değerlerinde.

---

#### 🧾 İmza

```python
def __sizeof__(self: int) -> int:
    ...
```

#### 📋 `int.__sizeof__()` — Parametre Tablosu

| 🔣 Parametre | 🧮 Tür | 📘 Açıklama                                |
|--------------|--------|--------------------------------------------|
| `self`       | `int`  | Bellek boyutu ölçülecek `int` nesnesi      |
| `return`     | `int`  | Byte cinsinden bellek boyutu (`int`)       |

> 💡 Bu metot, `int` nesnesinin bellekte kapladığı alanı ölçer — sayı büyüdükçe `digit` sayısı artar, boyut da büyür.

---

#### ⚙️ `int.__sizeof__()` — Çalışma Mantığı ve C Düzeyi İşleyiş

Python’daki `int` nesneleri, sabit bitli değil — büyüklüğe göre dinamik olarak genişleyen yapılardır.  
`__sizeof__()` metodu, bu nesnenin bellekte kapladığı alanı byte cinsinden döndürür.

#### 🧠 Python Düzeyinde Mantık

- `__sizeof__()` → Python’da `int` nesnesine ait özel bir dunder metottur.
- Çağrıldığında, nesnenin **dahili temsiline göre** bellek boyutunu hesaplar.
- Bu metot, `sys.getsizeof()` fonksiyonunun temelini oluşturur.

```python
x = 10**100
x.__sizeof__()  # → 72 byte gibi bir değer döner
```


---


#### 🧮 C Düzeyinde `__sizeof__()` Hesabı

CPython’da `int.__sizeof__()` metodu, dahili olarak `long_sizeof()` fonksiyonuna bağlanır
🧩 **Sayı büyüdükçe ob_size artar**→ daha fazla digit gerekir → daha fazla bellek kullanılır.


```c
static Py_ssize_t long_sizeof(PyLongObject *v) {
    return sizeof(PyLongObject) + v->ob_size * sizeof(digit);
}
```
#### 🧬 C Düzeyinde `ob_size` — Sayının Temsil Edilme Uzunluğu

Python’un `int` nesnesi, C tarafında `PyLongObject` yapısıyla temsil edilir.  
Bu yapının en kritik alanlarından biri: `ob_size`

#### 🔹 `ob_size` Nedir?

- `ob_size`, sayının kaç adet **30-bit’lik digit** ile temsil edildiğini belirtir.
- Yani sayı ne kadar büyükse → `ob_size` o kadar büyür.
- Bu değer, `ob_digit[]` dizisinin uzunluğunu belirler.

```c
typedef struct {
    PyObject_VAR_HEAD
    digit ob_digit[1];  // Sayının basamakları
} PyLongObject;
```
> 🔁 **İşaret Bilgisi:**
> 
> `b_size` **pozitif** → pozitif sayı
>
>`ob_size` **negatif** → negatif sayı
>
>Sayının işareti bile `ob_size` üzerinden kontrol edilir


---



### ⚙️ `int.__format__(self, format_spec: str) -> str`

---

#### 🧩 Tanım

`__format__()` metodu, `format()` fonksiyonu veya f-string (`f"{x}"`) kullanıldığında  
**nesnenin biçimlendirme (formatlama) davranışını** belirleyen özel (dunder) metottur.  

`int` sınıfı bu metodu **sayısal taban**, **dolgu**, **hizalama** ve **işaret** kontrolü için uygular.

> Örnek:
> ```python
> x = 42
> print(format(x, "b"))    # '101010'
> print(format(x, "x"))    # '2a'
> print(format(x, "+08d")) # '+0000042'
> ```

🧠 `int.__format__` → sayının biçimsel görünümünü üretir, değeri değiştirmez.

---

#### ⚙️ İleri Tanım

`int.__format__` metodu **`object.__format__`**’ı override eder  
ve `PyNumber_Format()` zincirine bağlıdır.
Python’daki `int.__format__` metodu, `format()` fonksiyonu veya `f-string` kullanıldığında otomatik olarak devreye girer.  
Bu metot, temel `object.__format__` metodunu override ederek `int` türüne özgü biçimlendirme kurallarını uygular.

Normalde `object.__format__` metodu, nesneyi `str()` ile dönüştürüp döner; yani biçimlendirme kurallarını dikkate almaz.  
Ancak `int` gibi sayısal türler, bu davranışı özelleştirerek format string’ine göre çıktı üretir.
CPython düzeyinde (kaynak: `Objects/longobject.c`):

```c
static PyObject*
long_format(PyObject *self, PyObject *args)
{
    // 1. format_spec alınır
    // 2. Eğer format_spec boşsa str() davranışı uygulanır
    // 3. format_spec'teki format karakterine göre uygun dönüşüm yapılır:
    //    'b' → _PyLong_Format(self, 2)
    //    'o' → _PyLong_Format(self, 8)
    //    'x' → _PyLong_Format(self, 16)
    //    'd' → _PyLong_Format(self, 10)
}
```
#### ⚠️ `int.__format__` — Dikkat Edilmesi Gerekenler

Python’daki `int.__format__` metodu, biçimlendirme işlemlerinde güçlü ve esnek bir araçtır.  
Ancak bazı sınırlamalar ve özel davranışlar içerir. Aşağıda bu metotla ilgili kritik noktalar listelenmiştir:



| ⚠️ Durum | 📌 Açıklama |
|----------|-------------|
| ⚙️ `format()` veya f-string içinde otomatik çağrılır | `__format__` metodu doğrudan çağrılmaz; `format(x, spec)` veya `f"{x:spec}"` kullanıldığında tetiklenir. |
| 🔢 `format_spec` yalnızca string olmalıdır | Format belirtimi (`spec`) string değilse → `TypeError` fırlatılır. Örneğin `format(42, 8)` geçersizdir. |
| 📐 Geçerli format kodları: `'b'`, `'o'`, `'x'`, `'X'`, `'d'` | Bunlar sırasıyla binary, octal, hexadecimal (küçük/büyük harf), ve decimal gösterimlerdir. |
| 🔡 `'c'` yalnızca tek karakterlik `int`’lerde geçerlidir | `'c'` formatı Unicode karakter dönüşümü yapar: `format(65, 'c')` → `'A'`. Ancak `format(1000, 'c')` geçersizdir. |
| 🧮 Sayısal olmayan türlerde davranış farklıdır | `float`, `complex`, `datetime` gibi türler kendi `__format__` metodlarını kullanır; `int`’in kuralları geçerli değildir. |
| 🧠 Her dönüşümün çıktısı `str` türündedir | Biçimlendirme işlemi her zaman `str` döner — asla `int` dönmez. Örneğin `format(42, 'b')` → `'101010'`, sayı değil metin. |

---

> 💡 Bu kurallar, `int.__format__` metodunun güvenli, tutarlı ve beklendiği gibi çalışmasını sağlar.  
> Özellikle `format_spec` türü, geçerli kodlar ve dönüşüm tipi, hata ayıklama ve görsel çıktı üretiminde kritik rol oynar.

---

### 🎯 Örnek:
#### 🔹 Normal kullanım (Python'un yaptığı şey)(temsilidir)
```python
x = 42

print(format(x, 'b'))   # '101010'
print(f"{x:x}")         # '2a'
print(f"{x:+08d}")      # '+0000042'

# Bu 3 satırın her biri aslında şuna denk:
print(x.__format__('b'))    # '101010'
print(x.__format__('x'))    # '2a'
print(x.__format__('+08d')) # '+0000042'
```
---




### ⚙️ Binary (2 Tabanı) — `0b` / `0B`

---

#### 🧩 Tanım

Binary (ikili) sistem, yalnızca `0` ve `1` rakamlarını kullanarak sayıları temsil eder.  
Python’da bir sayının binary biçimde yazıldığını belirtmek için `0b` veya `0B` öneki kullanılır.

> Örnek:
> ```python
> a = 0b1010
> print(a)  # 10 (decimal)
> ```

Bu ifade, “1×8 + 0×4 + 1×2 + 0×1” yani `10` anlamına gelir.  
Yani her binary literal, Python tarafından **int türüne** dönüştürülür.

---

#### 🧠 Mantık ve Çalışma Prensibi

- İkili sistem, bilgisayarların **donanım düzeyinde** veri işleme biçimidir.  
  Her bit (binary digit), bir **transistörün açık (1)** veya **kapalı (0)** olma durumunu temsil eder.

- Python derleyicisi (`ast.Constant`) binary literal gördüğünde onu doğrudan `int` nesnesine dönüştürür:
Bu dönüşüm, **AST (Abstract Syntax Tree)** düzeyinde gerçekleşir, çalışma zamanında değil.

---

### 🔢 Sözdizimi (Literal Formatı)

| Biçim | Açıklama | Örnek | Decimal Karşılığı |
|--------|-----------|--------|-------------------|
| `0b` | Küçük harf önek | `0b1010` | 10 |
| `0B` | Büyük harf önek | `0B1010` | 10 |

İki önek de aynı anlama gelir; sadece yazım tercihi farkıdır.

---

### 🎯 Kullanım Alanları

- **Bit maskeleri**: Birden fazla durumu tek sayı içinde tutmak için.
- Örn: `0b1010` → 10 (bayraklar: 1. ve 3. bit açık)
- **Donanım veya mikrodenetleyici programlama**
- **Sistem düzeyinde kontrol bayrakları**
- **Veri sıkıştırma veya bit düzeyinde iletişim**
- **Performanslı boolean diziler**

> Örnek kullanım:
> ```python
> FLAG_READ = 0b0001
> FLAG_WRITE = 0b0010
> FLAG_EXEC = 0b0100
> 
> permission = FLAG_READ | FLAG_WRITE
> if permission & FLAG_READ:
>     print("Okuma izni var")
> ```

---



### 🔢 Sayısal Dönüşüm Fonksiyonları — Python ve CPython Davranışları

Bu fonksiyonlar Python’da tür dönüşüm protokolünün parçasıdır.  
Her biri hem kullanıcıya açık bir API sunar, hem de CPython’da C düzeyinde optimize edilmiş şekilde tanımlanmıştır.

---

#### ⚙️ `bin()` Fonksiyonu

---

#### 🧩 Tanım

`bin(x)` fonksiyonu, verilen **tamsayıyı** (`int` türünü)  
**binary (ikilik) sistemdeki string karşılığına** dönüştürür.  
Dönen değer her zaman `'0b'` önekiyle başlar ve türü `str`’dir.

> Örnek:
> ```python
> bin(10)      # '0b1010'
> bin(255)     # '0b11111111'
> bin(-5)      # '-0b101'
> ```

🧠 Kısaca:  
`bin()` → `int` → `'0b...'` biçimli `str`

---

#### ⚙️ İleri Tanım

`bin()` aslında doğrudan C düzeyinde tanımlıdır:

```c
/* CPython kaynağında (Objects/longobject.c) */
PyObject* PyLong_FromLong(long ival);
PyObject* long_to_base(PyLongObject *v, int base);
```

---

🐍 Python temsili:
```python
def bin(x):
    if not hasattr(x, '__index__'):
        raise TypeError("bin() argument must be an integer")
    return format(x.__index__(), 'b').join(['0b', ''])
```


#### 🎯 `bin()` Fonksiyonunun Kullanım Alanları

Python’daki `bin()` fonksiyonu, tamsayıları ikilik (binary) gösterime çevirerek  
bit düzeyinde analiz ve görselleştirme yapmayı mümkün kılar.  
Aşağıda bu fonksiyonun öne çıkan kullanım alanları yer almaktadır:

##### ⚠️ `bin()` Fonksiyonu — Dikkat Edilmesi Gerekenler

`bin()` fonksiyonu, ikilik gösterim üretmek için oldukça kullanışlıdır.  
Ancak bazı sınırlamaları ve davranış özellikleri vardır. Aşağıda bu noktalar özetlenmiştir:

---

| 🔹 Durum | 📌 Açıklama |
|---------|-------------|
| **Sadece `int` veya `__index__` tanımlı nesnelerde çalışır** | `bin(3.5)` → `TypeError` fırlatır. `float`, `str`, `complex` gibi türler geçersizdir. |
| **Çıktı `str` türündedir** | Dönen değer bir sayı değil, `'0b...'` biçiminde bir metindir. Hesaplamalarda doğrudan kullanılamaz. |
| **Negatif sayılarda `'-0b...'` biçimi kullanılır** | Örneğin: `bin(-5)` → `'-0b101'`. İşaret `str` düzeyinde eklenir, two’s complement uygulanmaz. |
| **`bool` türü `int`’ten miras aldığı için çalışır** | `bin(True)` → `'0b1'`, `bin(False)` → `'0b0'`. Çünkü `bool` → `int`’in alt sınıfıdır. |
| **`bin()` sayıyı 2 tabanında gösterir ama hesaplamaz** | Sadece string üretir. Sayının değeri değişmez, sadece görünümü farklılaşır. |
| **Okunabilirlik için `format(x, 'b')` alternatifi vardır** | `'b'` formatı öneksiz döner: `format(10, 'b')` → `'1010'`. Özellikle görsel çıktılar için tercih edilir. |

---

> 💡 Bu özellikler, `bin()` fonksiyonunun güvenli ve doğru şekilde kullanılmasını sağlar.  
> Özellikle tür kontrolü ve dönüşüm biçimi, hata ayıklama ve görselleştirme süreçlerinde kritik rol oynar.

