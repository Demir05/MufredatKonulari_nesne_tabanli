## ⚙️ `bytes` Sınıfı

---

### 🧩 1️⃣ Tanım

`bytes`, Python’da verinin **ham (binary)** biçimini temsil eden sınıftır.  
Bu tür, 0 ile 255 arasındaki tamsayılardan oluşan **immutable (değiştirilemez)** bir dizidir.  
Her bir öğe 8 bit uzunluğundadır ve bellekteki gerçek byte değerini taşır.  

Bir `bytes` nesnesi oluşturulduğunda, Python bellekte **byte dizisini** doğrudan tahsis eder.  
Bu yapı, verinin disk, ağ veya bellek arasında taşınmasında kullanılır.  

> 🧠 1 byte = 8 bit  
> Python tarafında her eleman 0–255 arası bir `int`’tir.  
> Yani `bytes([65, 66, 67])` bellekte `0b01000001 0b01000010 0b01000011` olarak tutulur  
> ve bu ASCII düzeyinde `"ABC"` anlamına gelir.

`bytes` türü immutable olduğu için doğrudan değiştirilemez.  
Eğer içeriğin değiştirilebilmesi gerekiyorsa bunun karşılığı `bytearray` sınıfıdır.  

---

### ⚙️  Bit ↔ Byte ↔ Bytes ↔ Int İlişkisi

| Katman | Tanım | Python Karşılığı | Açıklama |
|--------|-------|------------------|-----------|
| **Bit** | `0` veya `1` | Doğrudan tipi yok | Bilginin en küçük birimi, donanımın dili |
| **Byte** | 8 bit | Doğrudan tipi yok | Donanımın en küçük adreslenebilir belleği |
| **Bytes** | N adet byte | `bytes` sınıfı | Verinin ham temsili (immutable) |
| **Int** | Sınırsız bit uzunluğu | `int` sınıfı | Sayısal soyutlama, bytes’ın mantıksal karşılığı |

> 💡 `int` bir değeri temsil eder,  
> `bytes` o değerin bellekteki **fiziksel hâlini** taşır.

Örneğin:
```python
x = 65
b = x.to_bytes(1, "big")      # b'\x41'
print(int.from_bytes(b, "big"))  # 65
```
---

#### ⚙️ CPython Düzeyi — PyBytesObject

```c
Python’un bytes türü C tarafında PyBytesObject yapısıyla temsil edilir:
typedef struct {
    PyObject_VAR_HEAD           // referans sayısı, type ptr, boyut bilgisi
    Py_ssize_t ob_shash;        // hash değeri (cache edilir)
    char ob_sval[1];            // asıl byte dizisi (C char*)
} PyBytesObject;
```
| 🧩 Alan             | 📘 Açıklama                                                                 |
|---------------------|------------------------------------------------------------------------------|
| `PyObject_VAR_HEAD` | Python nesne başlığıdır. Referans sayacı (`ob_refcnt`), tür pointer’ı (`ob_type`) ve boyut (`ob_size`) içerir. |
| `ob_shash`          | `hash(b'data')` çağrısı sonucu burada önbelleğe alınır. Hesaplanan hash değeri tekrar kullanılmak üzere saklanır. |
| `ob_sval`           | Gerçek byte verisini tutar. C tarafında `char[]` olarak tanımlanmıştır. `b'data'` gibi içerikler burada saklanır. |

> 💡 Bu yapı, `bytes` nesnesinin hem Python hem C düzeyinde hızlı ve verimli çalışmasını sağlar.

---

### 🧱 4 bytes — int — disk zinciri

Python’un veri akışı bu şekilde işler:

```css
     [Python Seviyesi]
          ↓
   int / str / list ...
          ↓
   ──► bytes() ◄───  (ortak ham veri katmanı)
          ↓
   file.write(b) / socket.send(b)
          ↓
     [Disk veya Ağ Katmanı]
```
---

### 🔢 `bytes[i]` → `int` Davranışı

### 📘 Tanım

Python’daki `bytes` nesnesi, her elemanını **tamsayı (`int`) olarak döndüren** özel bir dizidir.  
Yani `bytes` nesnesi, görünüşte bir karakter dizisi gibi dursa da, işlevsel olarak bir **`int` dizisi** gibi davranır.  
Her eleman, 0 ile 255 arasında bir sayıdır ve bellekteki gerçek byte değerini temsil eder.

---

### 🧠 Davranış Özeti

- `bytes` nesnesi **sequence protokolünü** uygular: `__len__`, `__getitem__`, `__iter__`
- Bu protokol sayesinde:
  - `b[i]` → `int` döner
  - `for x in b:` → her `x` bir `int` olur
  - `list(b)` → `int`’lerden oluşan bir liste döner

> 💡 `bytes` → görünüşte metin, davranışta sayı dizisidir.  
> Bu ikili doğa, hem metinsel hem sayısal işlemlerde kullanılmasını sağlar.

---

### 🧬 Bellek Temsili

- Her `bytes` elemanı, C tarafında `char` (1 byte) olarak tutulur.
- Python tarafında ise bu `char` değeri, `int` olarak yorumlanır.
- Bu dönüşüm, `ob_sval[i]` → `int` şeklinde gerçekleşir.

---

### 🔍 Karşılaştırmalı Bakış

| İfade             | Açıklama                                 |
|-------------------|------------------------------------------|
| `b = b'ABC'`       | 3 byte’lık sabit dizi (`65, 66, 67`)     |
| `b[0]`             | `65` döner → `'A'` karakterinin ASCII değeri |
| `list(b)`          | `[65, 66, 67]` → her eleman bir `int`    |
| `for x in b:`      | `x` her seferinde bir `int` olur         |
| `b'\x41' == b'A'`  | `True` → her ikisi de `65` değerini taşır |

---

### 🧪 Örnek

```python
b = b'ABC'

print(b[0])          # 👉 65
print(type(b[0]))    # 👉 <class 'int'>

for byte in b:
    print(byte)      # 👉 65, 66, 67
```


Python'da `bytes` türü, yüksek seviyeli soyutlamalar ile düşük seviyeli sistem çağrıları arasında bir **köprü** görevi görür.  
Bu yapı, hem Python nesneleriyle uyumlu çalışır hem de dosya ve ağ işlemleri için gerekli olan ham veri formatını sağlar.



#### 🔹 1️⃣ Python Nesne Katmanı

Yüksek seviyeli veri türleriyle başlar:

- `int`, `str`, `list`, `dict`, `float`, `bool` gibi Python nesneleri
- Bunlar insan odaklı soyutlamalardır; doğrudan sistemle konuşamazlar

---

#### 🔹 2️⃣ `bytes()` — Ortak Ham Veri Katmanı

Bu nesneler, sistemle iletişim kurabilmek için `bytes` biçimine dönüştürülür:

- `bytes()` → sabit, immutable byte dizisi üretir
- Bu dizi, RAM’de `PyBytesObject` olarak tutulur
- İçeriği C düzeyinde `char[]` olarak temsil edilir (`ob_sval`)

> 🎯 `bytes` → Python nesnelerinin sistem düzeyinde taşınabilir hale gelmesini sağlar

---

#### 🔹 3️⃣ Dosya ve Ağ Katmanı

`bytes` nesnesi, sistem çağrılarıyla dış dünyaya aktarılır:

- `file.write(b)` → byte dizisi diske yazılır
- `socket.send(b)` → byte dizisi ağ üzerinden gönderilir

Bu işlemler, CPython’da `write()` ve `send()` gibi C API fonksiyonlarına bağlanır  
ve işletim sisteminin I/O mekanizmalarını tetikler (`fwrite`, `send`, `write`, vs.)

---

#### 🔹 4️⃣ Fiziksel Katman

Son aşamada veri:

- Diskte bir dosya olarak saklanır
- Ağ üzerinden paketlenip iletilir

Bu noktada artık Python nesnesi değil, **ham byte dizisi** vardır — işletim sistemi düzeyinde işlenir.

> 🧠 **bit donanımın sinyali,**
**byte** donanımın kelimesi,
`bytes` Python’un fiziksel temsili,
`int` ise o temsile anlam veren soyutlamadır.
`bytes`, bu zincirin en alt halkasıdır
ve Python’daki tüm nesnelerin gerçek yüzünü temsil eder.

---

### 🧩 `bytes` Sınıfının Attribute ve Dunder Metotları

Python’daki `bytes` sınıfı, **binary veri protokolünü** uygular  
ve immutable diziler için tanımlanmış özel metotların çoğunu içerir.  
Bu yapı hem **sequence protokolünü** hem de **buffer protokolünü** destekler.  

Aşağıdaki tablo, `bytes` sınıfının temel attribute’larını ve dunder metotlarını  
öğrenme sırasına göre kategorilere ayrılmış şekilde gösterir.  

---

| 🧱 Kategori | ⚙️ Attribute / Metot | 🧠 Açıklama |
|-------------|----------------------|-------------|
| 📘 **Bilgi / Temel İşlevler** | `__class__`, `__doc__` | Sınıfın tipi ve açıklaması |
| | `__new__` | Yeni bytes nesnesi oluşturur (immutable yapı nedeniyle `__init__` kullanılmaz) |
| | `__len__`, `__getitem__`, `__iter__` | Sequence protokolü: uzunluk, erişim ve yineleme davranışları |
| 🧮 **Dizi Davranışları** | `__contains__`, `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__` | Karşılaştırma ve içerik kontrolü |
| | `__add__`, `__mul__`, `__rmul__` | Concatenation (birleştirme) ve tekrar (repeat) işlemleri |
| | `__hash__` | Immutable olduğu için hashlenebilir (set/dict anahtarı olabilir) |
| 🧠 **Veri Dönüşümleri** | `__bytes__` | `bytes(obj)` çağrıldığında dönen değer; genelde kendisini döndürür |
| | `__repr__`, `__str__` | Metin temsili (`b'...'` biçiminde gösterim) |
| | `__format__` | Formatlama davranışı (normalde `str` için geçerli ama `bytes` da destekler) |
| 💾 **Bellek & Buffer** | `__sizeof__()` | Nesnenin RAM boyutunu verir |
| | `__getbuffer__`, `__releasebuffer__` | C düzeyinde buffer paylaşımına izin verir (PEP 3118) |
| 🧩 **Yapılandırma Metotları** | `fromhex(string)` (classmethod) | Hex string’ten bytes oluşturur |
| | `hex()` | Bytes dizisini 16’lık tabanda döndürür (`b'\x41'` → `'41'`) |
| | `decode(encoding='utf-8')` | Byte dizisini string’e dönüştürür |
| | `split()`, `join()`, `find()`, `replace()` | Dizi manipülasyonu metotları (string benzeri davranışlar) |
| ⚙️ **Matematiksel Olmayan Operasyonlar** | `__mod__`, `__rmod__` | `%` operatörü ile formatlama (C tarzı biçimlendirme) |
| 🧠 **Immutable Davranışlar** | `__setitem__`, `__delitem__` | Tanımlı değildir — `TypeError` fırlatır (immutable yapı) |
| 🔄 **Dönüşüm Bağlantıları** | `int.to_bytes()`, `int.from_bytes()` | Sayısal veri ile doğrudan dönüşüm protokolü |
| 🧬 **Sınıf Özellikleri** | `__bases__` | `(object,)` çünkü doğrudan `object`’ten türetilir |
| 🎯 **Sürpriz Davranışlar** | `__reduce__`, `__reduce_ex__` | Pickle işlemlerinde kullanılır |
| | `__getnewargs__` | Bytes nesnesinin yeniden oluşturulması için argümanları döner |

---

### 🧭 Önerilen Öğrenme Sırası

## 🧩 `bytes` Sınıfının Öğrenme Adımları

| 🔢 Adım | 🧠 Başlık                                                      | 📘 Açıklama |
|--------|----------------------------------------------------------------|-------------|
| 1️⃣     | <span style="color: yellow;">`bytes` nesnesi oluşturma </span> | Nasıl `bytes` sınıfının örneğini oluşturacağını anla |
| 2️⃣     | `bytes` nesnesinin yapısı ve immutable doğası                  | Neden değiştirilemez olduğunu kavra |
| 3️⃣     | Sequence protokolü (`__len__`, `__getitem__`, `__iter__`)      | Dizisel davranışları kavra |
| 4️⃣     | Binary dönüşümler (`fromhex`, `hex`, `decode`)                 | Bytes ↔ Str ↔ Hex arasındaki ilişkiyi öğren |
| 5️⃣     | Buffer protokolü (`__getbuffer__`)                             | `memoryview`, `numpy`, `mmap` gibi yapılarla ilişkisini gör |
| 6️⃣     | `int` ile dönüşüm (`to_bytes`, `from_bytes`)                   | Sayısal karşılıkları kavra |
| 7️⃣     | Hashleme ve karşılaştırma metotları                            | Immutable veri olarak nasıl davrandığını öğren |
| 8️⃣     | `bytearray` farkı                                              | Mutable versiyonla arasındaki farkları analiz et |

### 🧠 Not

> `bytes`, Python’da `int` kadar temel bir sınıftır.  
> Ancak farkı, aritmetik değil **fiziksel veri manipülasyonu** sağlamasıdır.  
>  
> Bu nedenle `bytes` öğrenimi, `int`’in soyut değer sisteminden  
> Python’un **Binary Data Model** katmanına geçiş anlamına gelir.  
>  
> Kısacası, `int` “ne”yi temsil eder,  
> `bytes` ise “nasıl” tutulduğunu gösterir.

---

## ⚙️ Bytes Oluşturma Mekanizması

### 🧩 1️⃣ `bytes()` — Sınıf Çağrısı Yoluyla Oluşturma

#### 📘 Tanım

`bytes()` fonksiyonu, Python’daki `bytes` sınıfının doğrudan çağrılmasıyla bir `bytes` nesnesi oluşturur.  
Bu işlem yüzeyde bir “constructor call” gibi görünse de, CPython yorumlayıcısında C düzeyinde optimize edilmiş bir işlem zinciriyle yürütülür.

- Python düzeyinde: `bytes([iterable])`, `bytes(size)` veya `bytes()` şeklinde çağrılır.
- CPython düzeyinde: `type_call()` → `bytes_new()` → `PyBytes_FromStringAndSize()` zinciri tetiklenir.
- Bellek tahsisi sırasında `ob_sval` dizisi oluşturulur ve genellikle sıfır (`\0`) ile doldurulur.
- `bytes` nesnesi immutable olduğu için içerik sadece oluşturulurken yazılır, sonrasında değiştirilemez.

> 💡 Bu mekanizma sayesinde `bytes` nesneleri hem Python API’siyle uyumlu hem de C düzeyinde yüksek performanslı hale gelir.

---

### ⚙️ `bytes(iterable_or_string, encoding=None, errors=None)` — İmza Açıklaması

Bu imza, Python’daki `bytes` sınıfının **constructor çağrısı** gibi görünse de, teknik olarak `bytes.__new__()` metodunun imzasıdır.  
Yani `bytes(...)` ifadesi, aslında `bytes.__new__(cls, ...)` çağrısını tetikler — `__init__` değil, doğrudan nesne oluşturma aşamasıdır.

---

#### 🧩 Parametreler

| Parametre            | Açıklama |
|----------------------|----------|
| `iterable_or_string` | Byte üretilecek kaynak. Bu ya bir iterable (`[65, 66, 67]`) ya da `str` olabilir. |
| `encoding`           | Eğer kaynak bir `str` ise, hangi karakter kodlamasıyla `bytes`’a çevrileceğini belirtir. Örn: `'utf-8'`, `'ascii'`. |
| `errors`             | Kodlama sırasında hata yönetimi stratejisi. Örn: `'strict'`, `'ignore'`, `'replace'`. |

> 🔍 Eğer `encoding` belirtilirse, `iterable_or_string` mutlaka `str` olmalıdır.  
> Aksi takdirde `TypeError: string argument without an encoding` hatası alınır.

⚙️ **Python bunu şu şekilde değerlendirir:**
Bu çağrıyı `CALL_FUNCTION` opcode’una çevirir.
Ancak `bytes` sınıfı, **C** tarafında tanımlı bir **built-in type** olduğu için
bu çağrı Python protokol zincirini atlar,
yani `__call__`, `__new__,` `__init__ `gibi metotlar devreye girmez.

---


### 🧠  C Düzeyinde Tanım

Kaynak dosya: Objects/bytesobject.c
```c
PyTypeObject PyBytes_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0) // Tür başlığı: base type = PyType_Type, boyut = 0 (değişken uzunluklu nesne)
    "bytes",                               // Tür adı: Python'da görünen isim
    sizeof(PyBytesObject),                // Bellekteki nesne boyutu
    0,                                    // itemsize → sadece sabit boyutlu dizilerde kullanılır, burada gerek yok > sıfır
    (destructor)bytes_dealloc,            // Nesne yok edici (refcount sıfırlandığında çağrılır)
    0,                                    // print → Python 2'de vardı, artık kullanılmıyor > sıfır
    0,                                    // getattr → özel attribute erişimi için, `__getattr__` gibi > sıfır
    0,                                    // setattr → özel attribute yazımı için, `__setattr__` gibi > sıfır
    0,                                    // compare → Python 2'de vardı, artık kullanılmıyor > sıfır
    (reprfunc)bytes_repr,                 // `repr()` çıktısı üretici → `b'...'` biçiminde gösterim
    0,                                    // as_number → sayısal protokol (int, float, vb.) > bytes için geçerli değil > sıfır
    0,                                    // as_sequence → `__len__`, `__getitem__`, `__iter__` gibi > burada ayrı tanımlanır > sıfır
    0,                                    // as_mapping → `__getitem__` key/value gibi davranışlar > bytes için geçerli değil > sıfır
    0,                                    // hash → `__hash__` metodu, burada ayrı tanımlanmış > sıfır
    0,                                    // call → `__call__` davranışı, bytes çağrılabilir değil > sıfır
    (hashfunc)bytes_hash,                 // Hash fonksiyonu → `hash(b'data')` için
    0,                                    // richcompare → `__eq__`, `__lt__`, vb. > burada ayrı tanımlanır > sıfır
    0,                                    // weaklistoffset → zayıf referanslar için offset > bytes desteklemez > sıfır
    (reprfunc)bytes_str,                  // `str()` çıktısı üretici → genellikle `repr()` ile aynıdır
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, // Tür bayrakları: varsayılan + subclass edilebilir
    bytes_doc,                            // Yardım metni (docstring)
    0,                                    // traverse → GC için, bytes GC'ye ihtiyaç duymaz > sıfır
    0,                                    // clear → GC için temizlik fonksiyonu > sıfır
    0,                                    // richcompare → tekrar tanımlanabilir ama burada yok > sıfır
    0,                                    // tp_iter → iterable davranışı burada tanımlanmadı > sıfır
    0,                                    // iternext → iterator ilerletme > bytes doğrudan iterator değil > sıfır
    (newfunc)bytes_new,                   // ✅ Nesne oluşturucu → `bytes()` çağrıldığında tetiklenir
};
```
> 🔍 **Neden Bu Kadar `0` Var?**
>
> CPython’daki `PyTypeObject` yapısı oldukça geniştir: tüm protokolleri (number, sequence, mapping, buffer, GC, subclassing, vs.) desteklemek üzere tasarlanmıştır.
>
> Ancak her tür bu alanların hepsini kullanmaz. `bytes` gibi sabit, immutable ve sade türler için çoğu alan gereksizdir → bu yüzden `0` ile doldurulur.
>
> Bu `0` değerleri, CPython yorumlayıcısına “bu davranış tanımlı değil” demek için kullanılır.
>
> 💡 `0` → davranış yok, slot boş, varsayılan işlem uygulanmasın.

#### ⚙️ `bytes_new()` — CPython’da `__new__` Davranışının C Karşılığı

Python’da `bytes(...)` ifadesi, yüzeyde bir sınıf çağrısı gibi görünse de, teknik olarak `bytes.__new__()` metodunu tetikler.  
Bu çağrı, CPython yorumlayıcısında doğrudan `bytes_new()` adlı C fonksiyonuna yönlendirilir.  
Yani `__new__` metodu Python katmanında görünmez; tüm iş C düzeyinde gerçekleşir.

---

#### 🧩 `bytes_new()` Fonksiyonunun C Tanımı

```c
static PyObject *
bytes_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    PyObject *x = NULL;
    const char *encoding = NULL, *errors = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|Oss:bytes", &x, &encoding, &errors))
        return NULL;

    if (x == NULL)
        return PyBytes_FromStringAndSize("", 0); // b''

    if (PyUnicode_Check(x))
        return PyUnicode_EncodeFSDefault(x); // encode ile string -> bytes dönüşümü

    if (PyObject_CheckBuffer(x))
        return PyBytes_FromObject(x); // buffer protokolünden
}
```
> 🔍 **Fonksiyonun Davranışı**
>
> - `PyArg_ParseTupleAndKeywords(...)` → Python argümanlarını C değişkenlerine dönüştürür.
> - `x == NULL` → Argüman verilmemişse boş `bytes` döner (`b''`).
> - `PyUnicode_Check(x)` → `str` verilmişse `encoding` kullanılarak `bytes`’a çevrilir.
> - `PyObject_CheckBuffer(x)` → Buffer protokolünü destekleyen nesnelerden doğrudan `bytes` oluşturulur.
>
> 💡 Bu fonksiyon, `bytes()` çağrısının tüm olası yollarını C düzeyinde karşılar.

🧩 **Python Temsili**

```python
bytes()                    # → b''
bytes([65, 66, 67])        # → b'ABC'
bytes('ABC', 'ascii')      # → b'ABC'
bytes(b'\xff\xaa')         # → b'\xff\xaa'
```
> Tüm dönüşümler **C-- düzeyinde `PyBytes_From...()` fonksiyonlarıyla yapılır
---

#### ⚠️ `bytes()` — Dikkat Edilmesi Gerekenler

| 🔍 Durum                          | 📘 Açıklama                                                       |
|----------------------------------|-------------------------------------------------------------------|
| `bytes()` parametresiz çağrılırsa | Boş singleton `b''` döner.                                       |
| `bytes("ABC")`                   | `TypeError`: encoding belirtilmedi.                              |
| `bytes("ABC", "utf-8")`          | Geçerli: string encode edilip byte dizisi döner.                 |
| `bytes([300])`                   | `ValueError`: byte değeri `0–255` aralığında olmalı.             |
| `bytes(bytearray(...))`          | `bytearray`’ın kopyası oluşturulur → immutable `bytes` döner.    |

> 💡 Bu kurallar, `bytes()` fonksiyonunun farklı veri türleriyle nasıl davrandığını anlamak için kritiktir.


---

### 🧩 2️⃣ Bytes Literal — Derleme Zamanında Oluşturma

#### 📘 Tanım

**Bytes literal**, Python kaynak kodunda doğrudan yazılan ve derleme (parse) aşamasında sabit olarak oluşturulan `bytes` nesnesidir.  
Bu tür nesneler, yorumlayıcı çalışmadan önce AST → bytecode dönüşümünde sabit (`const`) olarak yerleştirilir.

---

#### 🔹 Örnekler

```python
b = b"ABC"         # bytes literal
b = b'\x41\x42\x43' # aynı içerik, hexadecimal gösterim
```
> 💡 Bu yazım, doğrudan **derleyici** tarafından `PyBytes_FromStringAndSize()` fonksiyonuna dönüştürülür,
dolayısıyla çalışma zamanında `bytes()` çağrısı yapılmaz.

### ⚙️ C Düzeyinde Oluşum

Derleyici (Parser) aşamasında,
`b'...'` veya `B'...'` tespit edildiğinde, **CPython** aşağıdaki fonksiyonu çağırır:
```c
PyObject *
PyBytes_FromStringAndSize(const char *str, Py_ssize_t size)
{
    PyBytesObject *op;

    // Gerekli boyutta bellek tahsis edilir:
    // PyBytesObject yapısı + 'size' kadar veri + 1 byte null terminatör için
    op = (PyBytesObject *)PyObject_MALLOC(sizeof(PyBytesObject) + size + 1);

    // Nesne başlığı ve boyut bilgisi başlatılır:
    // PyObject_VAR_HEAD makrosu → refcount, type pointer, size
    PyObject_INIT_VAR(op, &PyBytes_Type, size);

    // Eğer kaynak string varsa, içerik ob_sval dizisine kopyalanır
    if (str)
        memcpy(op->ob_sval, str, size);

    // Dizinin sonuna null terminatör eklenir (C string uyumluluğu için)
    op->ob_sval[size] = '\0';

    // Hazırlanan bytes nesnesi PyObject* olarak döndürülür
    return (PyObject *)op;
}
```
#### 🧬 `op->ob_sval` — Bytes Nesnesinin Bellekteki Temsili

- `op->ob_sval` → Gerçek byte dizisini tutar. C tarafında `char[]` olarak tanımlanmıştır.
- Sonuna her zaman `\0` (null byte) eklenir, ancak bu karakter `len(b)` hesaplamasına dahil edilmez.
- Python, bytes literal’lerini **constant pool** içinde saklar → aynı içerikteki literal yeniden oluşturulmaz, paylaşılır.

> 💡 Bu yapı sayesinde hem C string uyumluluğu sağlanır hem de bellek verimliliği artırılır.

---

### 🧠 Bytes Literal — Çalışma Mantığı

Python’da `b'...'` biçiminde yazılan `bytes` literal’leri, yorumlayıcı başlatıldığında sabit nesneler olarak önbelleğe alınır.  
Bu nesneler, **singleton** olarak davranır — yani aynı içerikteki literal birden fazla kez yazılsa bile bellekte tek bir nesne kullanılır.

#### 🔹 Derleme Zamanı Sabitleme

- `b'abc'`, `b'\xff'` gibi literal’ler Python’un derleyici aşamasında sabit (`const`) olarak tanımlanır.
- Bu sabitler, doğrudan **code object** içine gömülür ve `LOAD_CONST` opcode’u ile erişilir.
- Bu süreçte `bytes.__new__` çağrısı yapılmaz; çünkü literal oluşturma tamamen C tabanlıdır ve yorumlayıcı düzeyinde optimize edilmiştir.

#### 🔹 Karakter Sınırlamaları

- `b'...'` ifadesi yalnızca **ASCII karakterleri** ve `\xhh` biçimindeki **byte kaçışlarını** kabul eder.
- Non-ASCII karakterler (`b'Ş'`, `b'ç'`, `b'€'` gibi) literal içinde kullanılamaz → `SyntaxError` oluşur.
- Büyük harfli `B'...'` biçimi de geçerlidir; Python burada harf büyüklüğünü ayırt etmez.

---

### 🧩 Örnek Literaller

| Literal        | Anlamı             | Açıklama                                      |
|----------------|--------------------|-----------------------------------------------|
| `b''`          | Boş bytes nesnesi  | 0 byte uzunlukta, singleton olarak saklanır   |
| `b'ABC'`       | 3 byte’lık dizi    | ASCII “A”, “B”, “C” karakterlerinden oluşur    |
| `b'\xff\xaa'`  | 2 byte’lık veri    | Sayısal değerler: 255 (`0xFF`), 170 (`0xAA`)   |
| `B'Python'`    | Aynı               | Büyük harf fark etmez, `b'Python'` ile eşdeğer |
| `b'Ş'`         | ❌ SyntaxError      | Non-ASCII karakter içerdiği için geçersiz     |

> 💡 Bu literal’ler, hem performans hem bellek açısından en verimli `bytes` üretim yöntemidir.  
> Özellikle sabit verilerle çalışan sistemlerde `b'...'` kullanımı tercih edilir.

### 🧩 AST (Soyut Sözdizim Ağacı) Temsili
```python
import ast
print(ast.dump(ast.parse("b'ABC'"), indent=2))
```
**çıktı:**
```less
Module(
  body=[
    Expr(
      value=Constant(value=b'ABC')
    )
  ]
)
```
> 💡 Görüldüğü gibi literal, `Constant` node olarak derleniyor.
`bytes()` çağrısı gibi bir Call ifadesi yok.
 
### ⚠️ Bytes Literal — Dikkat Edilmesi Gerekenler

| 🔍 Durum                          | 📘 Açıklama                                                  |
|----------------------------------|--------------------------------------------------------------|
| Literal’da Unicode karakterler olamaz | Yalnızca ASCII karakterleri ve `\x00–\xff` arası escape’ler kullanılabilir. |
| `b'' is b''`                     | `True` — boş `bytes` nesnesi singleton olarak paylaşılır.    |
| `b'ABC' is b'ABC'`               | `True` — aynı içerikteki literal’ler constant pool’dan gelir. |
| `bytes('ABC', 'utf-8') is b'ABC'`| `False` — içerik eşit olsa da farklı nesneler oluşturulur.   |
| `b'\x41' == b'A'`                | `True` — her ikisi de aynı byte değerini (`65`) temsil eder. |

> 💡 Literal’ler derleme zamanında sabitlenir, `bytes()` ise çalışma zamanında yeni nesne üretir.
---

### 📘 Sonuç: `bytes()` vs `b'...'` Literal — Karşılaştırmalı Özellikler

| 🧩 Özellik             | `bytes()`                          | `b'...'` Literal                          |
|------------------------|------------------------------------|-------------------------------------------|
| Oluşturulma zamanı     | Çalışma zamanı                     | Derleme zamanı                            |
| Yürütüldüğü katman     | Python / C                         | Derleyici / C                             |
| `__new__` çağrısı      | Evet (ama C tabanlı)               | Hayır                                     |
| Kaynak fonksiyon       | `bytes_new`                        | `PyBytes_FromStringAndSize`              |
| Bellek yönetimi        | Heap                               | Constant pool                             |
| Immutable              | Evet                               | Evet                                      |
| Kullanım alanı         | Dinamik üretim                     | Sabit veri, kaynak içi binary temsili     |

> 💡 `bytes()` esnek ve çalışma zamanlıdır, `b'...'` ise sabit ve derleme zamanında optimize edilir.

> 🔍 **Bellek yönetimi notu:**  
> `bytes()` çağrısı her seferinde heap üzerinde yeni bir `PyBytesObject` üretir.  
> Buna karşılık `b'...'` literal’leri derleme aşamasında sabitlenir ve Python’un **constant pool** yapısında saklanır.  
> Bu sayede aynı içerikteki literal’ler bellekte paylaşılır (`b'ABC' is b'ABC' → True`) ve yeniden oluşturulmaz.

---

### ⚙️ `__new__` — `bytes` Nesnesi Oluşturucu Metodu

### 📘 Tanım

`__new__`, `bytes` sınıfının asıl **kurucu metodudur** (constructor).  
`bytes` immutable (değiştirilemez) olduğu için, `__init__` aşaması devre dışıdır —  
tüm veri işleme ve bellek tahsisi doğrudan `__new__` içinde gerçekleşir.

---

### 🧩 Davranış Özeti

| 🔧 İşlem Aşaması | 📘 Açıklama                                                                 |
|------------------|------------------------------------------------------------------------------|
| `__new__` çağrısı | Python yorumlayıcısı `bytes(...)` ifadesini gördüğünde `__new__` metodunu tetikler. |
| Girdi türleri     | `int`, `str`, `iterable`, `buffer` gibi kaynaklar kabul edilir.             |
| Dönüşüm işlemi    | Girdi, ham byte dizisine çevrilir (`PyBytes_From...` fonksiyonlarıyla).     |
| Dönüş değeri      | Sabit (`immutable`) bir `bytes` nesnesi döner.                             |

> 💡 `__new__` → gelen girdiyi ham byte dizisine çevirir  
> ve sabit (değiştirilemez) bir `bytes` nesnesi döndürür.

---

### 🧪 Örnek

```python
b1 = bytes([65, 66, 67])         # b'ABC'
b2 = bytes('ABC', 'ascii')       # b'ABC'
b3 = bytes(bytearray(b'XYZ'))    # b'XYZ'
```

---

## 🧠 `bytes.__new__` — Sözdizimsel Açıklama

### 📘 Sözel Tanım

`__new__`, `bytes` sınıfının gerçek kurucu metodudur.  
Immutable (değiştirilemez) yapılar için `__init__` çağrısı yapılmaz;  
tüm nesne oluşturma işlemi doğrudan `__new__` içinde gerçekleşir.

Bu metot, gelen girdiyi (`int`, `str`, `iterable`, `buffer`)  
ham byte dizisine dönüştürür ve sabit bir `bytes` nesnesi döndürür.

> 💡 `bytes(...)` ifadesi aslında `bytes.__new__(...)` çağrısını tetikler.

---

### 🧾 İmza

```python
bytes.__new__(cls, source='', encoding=None, errors=None) → bytes
```
### 🔧 `bytes.__new__` — Parametreler

| 🧩 Parametre | 🧬 Tür                        | 📘 Açıklama                                                                 |
|--------------|------------------------------|------------------------------------------------------------------------------|
| `cls`        | `type`                       | Sınıf referansı (`bytes`), otomatik olarak verilir.                         |
| `source`     | `str`, `int`, `iterable`, `buffer` | Byte dizisine dönüştürülecek kaynak veri.                             |
| `encoding`   | `str`                        | Eğer `source` bir `str` ise, hangi karakter kodlamasıyla çevrileceği.       |
| `errors`     | `str`                        | Kodlama sırasında hata yönetimi stratejisi (`'strict'`, `'ignore'`, vb.)    |

---

### 🔁 Dönüş Değeri

| 🔙 Dönüş     | 📘 Açıklama                                                                 |
|--------------|------------------------------------------------------------------------------|
| `bytes`      | Yeni oluşturulmuş, immutable byte dizisi (`PyBytesObject`) döner.           |

> 💡 Bu dönüş, CPython’da `bytes_new()` → `PyBytes_FromStringAndSize()` zinciriyle gerçekleştirilir.
 
### 🔬 İleri Tanım — CPython'da `bytes` Oluşturma Davranışı

---

#### ⚙️ C Tarafında Oluşturma Fonksiyonu

Python'da `bytes(...)` ifadesi çağrıldığında, CPython yorumlayıcısı bunu doğrudan C düzeyindeki şu fonksiyona yönlendirir:

```c
PyObject *PyBytes_FromStringAndSize(const char *str, Py_ssize_t size);
```
#### 🧩 `PyBytes_FromStringAndSize()` — Fonksiyon Açıklaması

| 🔧 Alan   | 📘 Açıklama                                                                 |
|-----------|------------------------------------------------------------------------------|
| `str`     | Belleğe yazılacak kaynak byte dizisi (`char*`)                              |
| `size`    | Byte dizisinin uzunluğu (`Py_ssize_t`)                                      |
| Dönüş     | Yeni oluşturulmuş `PyBytesObject` → Python'da `bytes` nesnesi olarak görünür |

> 💡 Bu fonksiyon, hem `bytes()` çağrılarında hem de `b'...'` literal’lerinde C düzeyinde byte dizisi üretmek için kullanılır.

---

### ⚠️ Dikkat Edilmesi Gerekenler — `bytes.__new__`

| 🔍 Durum                | 📘 Açıklama                                                                 |
|-------------------------|------------------------------------------------------------------------------|
| **Immutable**           | `bytes` değiştirilemez; dilimleme (`b[1:3]`) yeni bir `bytes` nesnesi üretir. |
| **0–255 Aralığı**       | `iterable` içindeki her sayı `0–255` aralığında olmalı, aksi halde `ValueError` oluşur. |
| **Encoding zorunlu**    | `source` bir `str` ise, `encoding` parametresi mutlaka belirtilmelidir.      |
| **Hatalı kullanım**     | `bytes("ABC")` → `TypeError: string argument without an encoding` hatası alınır. |
| **Bellek optimizasyonu**| C tarafında `PyBytesObject` doğrudan heap üzerinde tahsis edilir.            |
| **`bytearray` farkı**   | `bytearray()` aynı mantıkla çalışır fakat değiştirilebilir (`mutable`) nesne döndürür. |

> 💡 Bu kurallar, hem Python hem C düzeyinde `bytes` nesnesinin güvenli ve doğru şekilde oluşturulmasını sağlar.

---

### 🧩 `bytes.fromhex()` — Tanım

`bytes.fromhex(s)`, hexadecimal (16’lık) karakterlerden oluşan bir metni alır  
ve bunu `bytes` nesnesine çevirir.  

Her iki hexadecimal karakter → 1 byte eder.  
Yani `"41"` → `b'A'`, çünkü `0x41` = `65` = `'A'`

> 💡 Bu yöntem, metin tabanlı hex verilerini doğrudan RAM’e çevirmek için kullanılır.

---

#### 🧠 Sözdizimi

```python
bytes.fromhex(string: str) → bytes
```
#### 📌 `bytes.fromhex()` — Parametreler

| 🔧 Parametre | 🧬 Tür | 📘 Açıklama                                                  |
|--------------|--------|---------------------------------------------------------------|
| `string`     | `str`  | Hexadecimal karakterlerden oluşan metin (`'41 42 43'`)        |

---

#### 🔁 Dönüş Değeri

| 🔙 Dönüş | 📘 Açıklama                                                  |
|----------|---------------------------------------------------------------|
| `bytes`  | Hex verisinin karşılığı olan `bytes` nesnesi döner (`b'ABC'`) |

> 💡 Her iki hex karakter → 1 byte. Boşluklar çiftleri ayırmak için kullanılabilir.

#### 🔧 `bytes.fromhex()` — Kullanım Alanları (Kısa)

| 🧩 Senaryo                              | 📘 Açıklama                                                                 |
|----------------------------------------|------------------------------------------------------------------------------|
| Hex dump’tan byte üretimi              | Metin tabanlı hex veriyi gerçek `bytes` nesnesine dönüştürmek için kullanılır. |
| Ağ/ikili protokol testleri             | Paket verilerini hex formatında tanımlayıp RAM’e çevirmek mümkündür.         |
| Şifreleme/kripto test vektörleri       | Kriptografik örneklerde hex tabanlı test girdileri oluşturmak için idealdir. |
| Dosya imzası (magic bytes) üretimi     | Dosya türlerini tanımlayan sabit byte dizilerini string olarak yazıp çevirmek. |

---

#### ⚠️ Dikkat Edilecekler — `bytes.fromhex()`

| 🔍 Durum                    | 📘 Açıklama                                                                 |
|-----------------------------|------------------------------------------------------------------------------|
| Boşluklar serbest           | `'41 42 43'` → `b'ABC'` ✅                                                  |
| Büyük/küçük harf fark etmez | `'aa' == 'AA'` → `b'\xaa'` ✅                                               |
| Çift sayı zorunlu           | `'f'` → ❌ `ValueError` (tek karakter eksik)                                |
| `0x` öneki yasak            | `'0x41'` → ❌ `ValueError` (hex literal değil, sadece karakter dizisi olmalı) |
| Geçersiz karakter           | `'zz'` → ❌ `ValueError` (hex olmayan karakterler)                          |
| Kardeşi                     | `bytearray.fromhex(...)` → aynı işlev, ama yazılabilir nesne döndürür       |

> 💡 Hex veriyi RAM’e aktarmak için hızlı, güvenli ve okunabilir bir yol sunar.

---

###  🧪 Temel kullanımlar

---
```python
bytes.fromhex('41 42 43')         # b'ABC'
bytes.fromhex('414243')           # b'ABC'
bytes.fromhex('00 ff 10')         # b'\x00\xff\x10'
bytes.fromhex('DE AD BE EF')      # b'\xde\xad\xbe\xef'

# Boşluk, satır sonu, tab hepsi yok sayılır
bytes.fromhex('41\t42\n43')       # b'ABC'

# Hata örnekleri
# bytes.fromhex('f')              # ValueError: non-hexadecimal number...
# bytes.fromhex('0x41')           # ValueError

# Doğrulama: .hex() tam tersi yönde çalışır
b = bytes.fromhex('deadbeef')
b.hex()                           # 'deadbeef'
```

```python
bytes.fromhex(string)
---------------------
Bir hexadecimal (16’lık) karakter dizisini bytes nesnesine dönüştürür.
Her iki hex karakter = 1 byte. Boşluklar yok sayılır.


# Temel kullanım
b = bytes.fromhex('41 42 43')
print(b)  # b'ABC'


Her iki karakter (ör. '41') bir byte oluşturur:
'41' = 0x41 = 65 = 'A'
'42' = 0x42 = 66 = 'B'
'43' = 0x43 = 67 = 'C'


# Boşluk, tab ve satır sonları göz ardı edilir
b = bytes.fromhex('41\t42\n43')
print(b)  # b'ABC'

# Geçersiz karakter veya tek haneli hex değeri hataya yol açar.


# Hatalı kullanım örnekleri
bytes.fromhex('f')     # ValueError: non-hexadecimal number found
bytes.fromhex('0x41')  # ValueError: 'x' geçersiz karakter


#İki yönlü dönüşüm mümkündür:
.hex()  # metodu bytes → hex string dönüşümü sağlar.


b = bytes.fromhex('DE AD BE EF')
print(b)          # b'\xde\xad\xbe\xef'
print(b.hex())    # 'deadbeef'
```
```python
"""
1️⃣  Dosya imzası (Magic Bytes) tespiti
--------------------------------------
Her dosya türünün başında onu tanımlayan özel birkaç byte bulunur.
Bunlara "magic bytes" denir.
Örneğin PDF dosyaları %PDF (0x25 0x50 0x44 0x46) ile başlar.
"""

pdf_signature = bytes.fromhex('25 50 44 46')  # %PDF
with open('example.pdf', 'rb') as f:
    header = f.read(4)
    if header == pdf_signature:
        print("PDF dosyası tespit edildi!")  # ✅
    else:
        print("PDF değil.")
```
```python
"""
2️⃣  Şifreleme / Hash kontrol testlerinde referans karşılaştırması
------------------------------------------------------------------
Kripto veya hash fonksiyonlarının belgelerinde sonuç genelde hex formatında verilir.
Biz bu çıktıyı bytes'a çevirerek programatik olarak doğrulayabiliriz.
"""

import hashlib

# Beklenen SHA256 çıktısı (hex formatında)
ref_hash = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
expected = bytes.fromhex(ref_hash)

# Gerçek hash sonucu
real = hashlib.sha256(b'hello').digest()

print(real == expected)  # ✅ True
```
```python
"""
4️⃣  Bellek veya opcode analizlerinde
------------------------------------
Disassembled bytecode çıktısı genellikle hex olarak verilir.
Bu çıktıyı tekrar yürütülebilir hale getirmek için bytes.fromhex() kullanılabilir.
"""

import dis

code = compile("x = 1 + 2", "<string>", "exec")
print(code.co_code.hex())  # bytecode’un hex gösterimi

# Bu hex verisini tekrar bytes’a çevirebiliriz
byte_stream = bytes.fromhex(code.co_code.hex())
print(byte_stream == code.co_code)  # ✅ True
```

---

### 🔧 `bytes.maketrans()` ve `bytes.translate()` — Bayt Dönüşüm Araçları

---

### 🧩 `bytes.maketrans()` — Dönüşüm Tablosu Oluşturucu

### 📘 Tanım

`bytes.maketrans()` metodu, baytlar arasında eşleme yapan bir dönüşüm tablosu oluşturur.  
Bu tablo, `bytes.translate()` ile birlikte kullanılarak bayt dizisindeki verilerin toplu şekilde dönüştürülmesini sağlar.

### 🧠 Sözdizimi

```python
bytes.maketrans(from: bytes, to: bytes) → dict
```

### 📌 Parametreler

| 🔧 Parametre | 🧬 Tür   | 📘 Açıklama                                                         |
|--------------|---------|----------------------------------------------------------------------|
| `from`       | `bytes` | Değiştirilecek baytlar (`b'abc'`)                                    |
| `to`         | `bytes` | Yeni baytlar (`b'ABC'`) — uzunlukları eşit olmalı                    |


### 🔁 Dönüş Değeri

| 🔙 Dönüş | 📘 Açıklama                                                                 |
|----------|------------------------------------------------------------------------------|
| `dict`   | Bayt kod noktalarını eşleyen dönüşüm tablosu (`{97: 65, 98: 66, 99: 67}`)   |

---

### 🧩 Kullanım Alanları

| 🎯 Senaryo                      | 📘 Açıklama                                                                 |
|--------------------------------|------------------------------------------------------------------------------|
| ASCII karakter dönüşümü        | Küçük harfleri büyük harfe çevirme gibi işlemler (`b'abc'` → `b'ABC'`)       |
| Şifreleme / kodlama            | Basit karakter bazlı şifreleme algoritmaları için dönüşüm tablosu üretimi    |
| Veri temizleme                 | Belirli baytları silmek veya dönüştürmek için `translate()` ile birlikte kullanılır |
| Protokol uyarlamaları          | Ağ veya dosya protokollerinde karakter eşlemeleri için kullanılabilir        |



### ⚠️ Dikkat Edilmesi Gerekenler

| 🔍 Durum                     | 📘 Açıklama                                                                 |
|------------------------------|------------------------------------------------------------------------------|
| Uzunluk eşitliği zorunlu     | `from` ve `to` bayt dizilerinin uzunlukları aynı olmalıdır (`len(from) == len(to)`) |
| Sadece `bytes` nesneleri     | Hem `from` hem `to` parametreleri `bytes` olmalıdır, `str` kabul edilmez     |
| Unicode değil, bayt düzeyi   | Bu dönüşüm `str.translate()` gibi Unicode karakterlerle değil, bayt kodlarıyla çalışır |
| `bytearray` ile uyumlu       | Oluşturulan tablo hem `bytes.translate()` hem `bytearray.translate()` ile kullanılabilir |

---
```python
# bytes_translate_examples.py

# 🔧 Örnek 1: Küçük harfleri büyük harfe çevirme
table = bytes.maketrans(b'abc', b'ABC')  # a→A, b→B, c→C
data = b'abcxyz'
result = data.translate(table)
print(result)  # b'ABCxyz'

# 🔧 Örnek 2: Belirli baytları silme
table = bytes.maketrans(b'', b'')        # boş dönüşüm tablosu
data = b'abcxyz'
result = data.translate(table, delete=b'xz')  # x ve z silinir
print(result)  # b'abcy'

# 🔧 Örnek 3: ASCII şifreleme — basit karakter kaydırma
# a→d, b→e, c→f
table = bytes.maketrans(b'abc', b'def')
data = b'abcabc'
result = data.translate(table)
print(result)  # b'defdef'

# 🔧 Örnek 4: Ters çevirme — büyük harfleri küçük harfe
table = bytes.maketrans(b'ABC', b'abc')
data = b'ABCXYZ'
result = data.translate(table)
print(result)  # b'abcXYZ'

# 🔧 Örnek 5: bytearray ile aynı tabloyu kullanma
table = bytes.maketrans(b'123', b'321')
ba = bytearray(b'112233')
ba_result = ba.translate(table)
print(ba_result)  # bytearray(b'331122')
```
---

### 🧩 `bytes.translate()` — Bayt Dizisi Dönüştürücü

---

### 📘 Tanım

`bytes.translate()` metodu, bir dönüşüm tablosu kullanarak bayt dizisindeki verileri dönüştürür.  
Bu yöntem, karakter değiştirme, filtreleme veya şifreleme gibi işlemler için idealdir.

---

### 🧠 Sözdizimi

```python
b.translate(table: dict, delete: Optional[bytes] = None) → bytes
```

### 📌 Parametreler

| 🔧 Parametre | 🧬 Tür   | 📘 Açıklama                                                                 |
|--------------|---------|------------------------------------------------------------------------------|
| `table`      | `dict`  | `bytes.maketrans()` ile oluşturulmuş dönüşüm tablosu                         |
| `delete`     | `bytes` | Silinecek baytlar (isteğe bağlı)                                            |



### 🔁 Dönüş Değeri

| 🔙 Dönüş | 📘 Açıklama                                                                 |
|----------|------------------------------------------------------------------------------|
| `bytes`  | Dönüştürülmüş yeni `bytes` nesnesi                                          |


---

### 🎯 Kullanım Alanları

| Senaryo               | Açıklama                                                                 |
|------------------------|--------------------------------------------------------------------------|
| Karakter dönüşümü      | ASCII karakterleri topluca değiştirme (`b'abc'` → `b'ABC'`)              |
| Veri filtreleme        | Belirli baytları silme (`delete=b'xz'`)                                  |
| Şifreleme / kodlama    | Basit karakter bazlı şifreleme algoritmaları (`ROT13`, `Caesar`, vb.)    |
| Protokol uyarlamaları  | Bayt düzeyinde veri dönüştürme (örneğin ağ protokollerinde)              |
| Veri temizleme         | ASCII dışı karakterleri ayıklama veya normalize etme                     |


### ⚠️ Dikkat Edilmesi Gerekenler

| Durum                    | Açıklama                                                                 |
|---------------------------|--------------------------------------------------------------------------|
| `table` zorunlu           | Dönüşüm tablosu belirtilmeden `translate()` çağrısı yapılamaz            |
| `delete` opsiyoneldir     | Belirtilirse, listedeki baytlar silinir                                  |
| `bytes` nesnesi değişmez  | `translate()` yeni bir `bytes` nesnesi döndürür, orijinal veri değişmez  |
| `table` → `dict[int, int]`| Anahtar ve değerler bayt kod noktaları (`ord(b'a')` → `ord(b'A')`)       |
| Unicode değil, bayt düzeyi| Bu metod `str.translate()` gibi Unicode karakterlerle değil, baytlarla çalışır |

> 💡 `bytes.translate()` → hızlı, doğrudan ve bellek dostu bayt dönüşüm aracıdır.

---
```python
# bytes_translate_examples.py

# 🔧 Örnek 1: Küçük harfleri büyük harfe çevirme
# 'a' → 'A', 'b' → 'B', 'c' → 'C'
table = bytes.maketrans(b'abc', b'ABC')
data = b'abcxyz'
result = data.translate(table)
print(result)  # b'ABCxyz'

# 🔧 Örnek 2: Belirli baytları silme
# 'x' ve 'z' karakterleri silinir
table = bytes.maketrans(b'', b'')  # boş dönüşüm tablosu
data = b'abcxyz'
result = data.translate(table, delete=b'xz')
print(result)  # b'abcy'

# 🔧 Örnek 3: ASCII şifreleme — Caesar tarzı kaydırma
# 'a' → 'd', 'b' → 'e', 'c' → 'f'
table = bytes.maketrans(b'abc', b'def')
data = b'abcabc'
result = data.translate(table)
print(result)  # b'defdef'

# 🔧 Örnek 4: Ters çevirme — büyük harfleri küçük harfe
# 'A' → 'a', 'B' → 'b', 'C' → 'c'
table = bytes.maketrans(b'ABC', b'abc')
data = b'ABCXYZ'
result = data.translate(table)
print(result)  # b'abcXYZ'

# 🔧 Örnek 5: bytearray ile aynı tabloyu kullanma
# '1' → '3', '2' → '2', '3' → '1'
table = bytes.maketrans(b'123', b'321')
ba = bytearray(b'112233')
ba_result = ba.translate(table)
print(ba_result)  # bytearray(b'331122')

# 🔧 Örnek 6: ASCII dışı karakterleri filtreleme
# Türkçe karakterleri silmek için delete parametresi kullanılır
data = 'Merhaba, dünya!'.encode('utf-8')
delete = 'çşğüöı'.encode('utf-8')  # silinecek karakterler
table = bytes.maketrans(b'', b'')  # dönüşüm yapılmayacak
filtered = data.translate(table, delete=delete)
print(filtered.decode('utf-8', errors='ignore'))  # Merhaba, dnya!
```
---

### 🧩 `bytes.decode()` — Bayt Dizisini Metne Çevirme

---

### 📘 Tanım

`bytes.decode()` metodu, bayt dizisini belirtilen karakter kodlamasına göre `str` (metin) nesnesine dönüştürür.  
Bu işlem, baytların hangi karakterleri temsil ettiğini çözümlemek için kullanılır.

---

### 🧠 Sözdizimi

```python
b.decode(encoding='utf-8', errors='strict') → str
```

### 📌 Parametreler

| 🔧 Parametre | 🧬 Tür   | 📘 Açıklama                                                                 |
|--------------|---------|------------------------------------------------------------------------------|
| `encoding`   | `str`   | Kullanılacak karakter kodlaması (varsayılan: `'utf-8'`)                      |
| `errors`     | `str`   | Hata işleme stratejisi (`'strict'`, `'ignore'`, `'replace'`, vb.)            |



### 🔁 Dönüş Değeri

| 🔙 Dönüş | 📘 Açıklama                                                                 |
|----------|------------------------------------------------------------------------------|
| `str`    | Bayt dizisinin karakter kodlamasına göre çözülmüş metin hali                |

---

### 🎯 Kullanım Alanları

| Senaryo                 | 📘 Açıklama                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| Dosya okuma              | Bayt olarak okunan veriyi metne çevirmek için (`rb` → `.decode()`)          |
| Ağ verisi çözümleme      | Socket üzerinden gelen baytları metne dönüştürmek                           |
| Şifreleme sonrası çözüm  | Şifrelenmiş veriyi çözümleyip okunabilir hale getirme                       |
| Unicode dönüşümü         | UTF-8, UTF-16 gibi kodlamalardan metin elde etme                            |
| API/JSON işleme          | Bayt olarak gelen JSON verisini string’e çevirip `json.loads()` ile işlemek |



### ⚠️ Dikkat Edilmesi Gerekenler

| Durum                    | 📘 Açıklama                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| Kodlama uyumsuzluğu       | Yanlış encoding seçilirse `UnicodeDecodeError` oluşabilir                   |
| Varsayılan UTF-8          | Kodlama belirtilmezse `'utf-8'` kullanılır                                  |
| Hata stratejisi önemli    | `'strict'` → hata fırlatır, `'ignore'` → hatalı karakteri atlar, `'replace'` → `�` ile değiştirir |
| Sadece `bytes` için geçerli| `str` nesnelerinde `.decode()` yoktur; sadece `bytes` nesnelerinde çalışır |

> 💡 `decode()` → baytları anlamlı metne dönüştürmenin temel yoludur.