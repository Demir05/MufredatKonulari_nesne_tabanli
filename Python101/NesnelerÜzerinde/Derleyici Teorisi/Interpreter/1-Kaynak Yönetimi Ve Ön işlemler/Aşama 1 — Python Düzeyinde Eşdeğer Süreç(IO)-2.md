## ⚙️ I/O — “Input / Output” Kavramı - 2

---

#### 🧑‍🎓 **Yeni başlayan (CS öğrencisi)**
#### 🕒 **Tahmini Süre: 180dk**

---

### 🧭 Python I/O Öğrenme Haritası

| 🔢 Katman No | 🧩 Katman Adı                                           | 🎯 Açıklama                                                                 |
|-------------|---------------------------------------------------------|------------------------------------------------------------------------------|
| 1️⃣          | <span style="color: green;">Temel Kavram Katmanı</span> | I/O, stream, buffer ve encoding kavramlarının temelleri.                    |
| 2️⃣          | <span style="color: green;">Soyut Sınıf Katmanı</span>  | Tüm I/O türlerinin dayandığı ortak arayüzler (`IOBase`, `RawIOBase`...).    |
| 3️⃣          | <span style="color: yellow;">Uygulama Katmanı</span>    | Gerçek dünyadaki I/O sınıfları (`FileIO`, `BufferedIO`, `TextIOWrapper`).   |
| 4️⃣          | Ortak Metodlar Katmanı                                  | `read()`, `write()`, `seek()` gibi her akışta ortak davranışlar.            |
| 5️⃣          | Buffer & Performans Katmanı                             | I/O hızını belirleyen buffer yönetimi ve optimizasyonlar.                   |
| 6️⃣          | Modül Fonksiyonları Katmanı                             | `open()`, `io.StringIO()`, `io.BytesIO()` gibi üst seviye API’ler.          |
| 7️⃣          | Deneysel / Ustalık Katmanı                              | Kendi I/O sınıflarını ve sanal dosya sistemlerini tasarlama.                |
---

## ⚙️ 3️⃣ — Uygulama Katmanı (Concrete Layer)
Bu katman, `IOBase`, `RawIOBase`, `BufferedIOBase`, `TextIOBase` soyut sınıflarını temel alarak,
**gerçek dünyada kullanılabilen I/O nesnelerini** üretir.

Python’un `open()` fonksiyonunun perde arkasında çalışan sınıflar da tam olarak bunlardır:
- `FileIO`  → Diskle doğrudan (OS düzeyinde) byte I/O
- `BufferedReader` / `BufferedWriter` → Bellek tamponlama
- `TextIOWrapper` → Unicode dönüştürme + satır yönetimi

---

### ⚙️ FileIO — Ham Dosya Erişimi (Raw File Interface)

`io.FileIO`, Python’un I/O sisteminde **dosya sistemine en yakın** çalışan sınıftır.  
Bu sınıf, `RawIOBase`’ten türetilir ve **doğrudan işletim sistemi çağrılarını** (örneğin `open()`, `read()`, `write()`, `close()`) kullanarak byte düzeyinde dosya işlemleri yapar.  

`FileIO` buffer kullanmaz — yani her `read()` veya `write()` çağrısı **doğrudan diskle iletişime geçer**.  
Bu da onu **en düşük seviye** ve **en performanslı (ancak buffer’sız)** I/O katmanı yapar.  

Çoğu kullanıcı `open()` fonksiyonunu çağırdığında `FileIO`’yu doğrudan görmez,  
çünkü `open()` bunu `BufferedReader` veya `TextIOWrapper` gibi üst katman sınıflara sarar.  
Yine de, `FileIO` Python’un tüm dosya mimarisinin temel taşıdır.

---

#### 📘 Öne Çıkan Metodlar

|🛠️ Metod | Açıklama |
|:--|:--|
| `read(size=-1)` | Dosyadan belirtilen miktarda **byte** okur. |
| `write(b)` | Byte dizisini doğrudan diske yazar. |
| `close()` | Dosya tanıtıcısını (`file descriptor`) kapatır. |
| `fileno()` | Altta yatan OS dosya tanıtıcısını döndürür (ör. `3`, `4` gibi). |
| `isatty()` | Dosyanın bir terminal (TTY) olup olmadığını kontrol eder. |
| `seek(offset, whence=0)` | Dosya imlecini belirtilen konuma taşır. |
| `tell()` | Mevcut dosya imleç konumunu döndürür. |
| `truncate(size=None)` | Dosya boyutunu kısaltır veya uzatır. |

---

#### 🧠 Önemli Dunder Metodları

| Dunder | Rol |
|:--|:--|
| `__enter__`, `__exit__` | Context manager desteği sağlar (`with FileIO(...) as f:`). Kaynak sızıntısını önler. |
| `__iter__`, `__next__` | Satır bazlı okuma imkânı verir (`for line in f:`). |
| `__del__` | Nesne silinirken `close()` çağırarak dosyayı güvenli biçimde kapatır. |
| `__repr__` | Dosya nesnesinin tanımlayıcı temsili (`<FileIO name='data.bin' mode='rb'>`). |

---

#### ⚙️ Sözdizimi (İmza)

```python
io.FileIO(file, mode='r', closefd=True, opener=None)
```
#### 🏷️ Parametreler
**file:**          Açılacak dosyanın adı (`str`) veya dosya tanımlayıcısı (`int`). 
 
**mode:**          Dosyanın açılma modu: `'r'`, `'w'`, `'a'`, `'x'`, `'rb'`, `'wb'` gibi. 

**closefd:**       `file` bir dosya tanımlayıcısı (`int`) ise, dosya kapatıldığında `fd` de kapatılsın mı? Varsayılan: `True`. 

**opener:**        Özel bir dosya açma fonksiyonu. `open()` yerine alternatif bir açıcı belirtmek için kullanılır. 

---

### 🧠 Detaylı Notlar

- `file` olarak bir `str` verirsen → dosya adı üzerinden açılır.  
  `int` verirsen → doğrudan dosya tanımlayıcısı (`fd`) üzerinden işlem yapılır.


- `mode` parametresi sadece `'b'` (binary) modlarını destekler.  
  Çünkü `FileIO`, metin (`str`) değil, bayt (`bytes`) ile çalışır.


- `closefd=False` dersen → `FileIO` nesnesi kapandığında dosya tanımlayıcısı açık kalır.  
  Bu, dosya tanımlayıcısını başka yerlerde kullanmak istiyorsan faydalıdır.


- `opener` parametresi, `open()` fonksiyonunun `opener` argümanıyla aynı mantıkta çalışır.  
  Örneğin `os.open` gibi bir sistem çağrısı ile dosya açmak istiyorsan burada kullanabilirsin.

---



### 💡 Kullanım Alanları

`FileIO`, Python’un **ham (raw) I/O katmanı** olduğu için özellikle **performans** veya **düşük seviye sistem etkileşimi** gerektiren durumlarda tercih edilir.  
Üst düzey `open()` fonksiyonunun soyutlamalarına girmeden, işletim sisteminin dosya descriptor düzeyinde çalışır.

| Kullanım Senaryosu | Açıklama |
|:--|:--|
| 🧩 **Ham veri işlemleri** | Görsel, ses, ağ paketleri gibi binary (ikili) dosyaların okunması ve yazılması. |
| ⚙️ **Sistem seviyesi entegrasyonlar** | `os.pipe()`, `os.dup()` gibi düşük seviye file descriptor’larla doğrudan etkileşim. |
| 🧮 **Performans testleri** | Buffer’lama olmadan doğrudan disk I/O ölçümleri yapılabilir. |
| 💾 **Veri tabanı / dosya tabanlı cache sistemleri** | Buffer yönetimini manuel kontrol etme imkânı sağlar. |
| 🧠 **Gelişmiş I/O zincirleri** | `BufferedReader` veya `TextIOWrapper` gibi üst katmanlara sarılarak özel akış zincirleri oluşturulabilir. |

> **Not:** `FileIO`, genellikle doğrudan son kullanıcı tarafından değil, `open()` veya `io.BufferedReader` gibi üst katman soyutlamalar tarafından dolaylı biçimde kullanılır.

---

### ⚠️ Dikkat Edilmesi Gerekenler

`FileIO` düşük seviyeli olduğu için yüksek esneklik sağlasa da, bazı önemli sınırlamalara ve risklere sahiptir:

| Durum | Dikkat Noktası |
|:--|:--|
| 🔒 **Kaynak Yönetimi** | Dosya kapatılmadan nesne yok edilirse, sistem kaynak sızıntısı (file descriptor leak) oluşabilir. `with` bloğu her zaman tercih edilmelidir. |
| ⚡ **Buffer Yok** | Her `read()` veya `write()` çağrısı **doğrudan diske gider** — bu nedenle küçük verilerle sık I/O yapmak performansı düşürür. |
| 🧷 **Sadece Bytes Desteği** | Metin (`str`) yazılamaz. Tüm veriler `bytes` veya `bytearray` olmalıdır. |
| 🚫 **Thread-Safe Değil** | Aynı `FileIO` nesnesine birden fazla thread’den erişim veri tutarsızlığına yol açabilir. |
| 💥 **Kapatılmış Nesne** | `close()` sonrası yapılan her işlem `ValueError: I/O operation on closed file.` hatası üretir. |
| 🧩 **Platform Farklılıkları** | `fileno()`, `os-level` descriptor olduğu için bazı platformlarda (ör. Windows <-> Unix) farklı davranabilir. |
| 🧱 **Senkron Çalışma** | Asenkron dosya işlemleri (`asyncio`) ile uyumlu değildir. Bunun yerine `aiofiles` gibi modüller kullanılmalıdır. |

> **Kısaca:**  
> `FileIO` kullanıyorsan, doğrudan işletim sistemiyle konuşuyorsun demektir —  
> bu da hem **güç** hem **sorumluluk** getirir ⚙️

---


### 🧪 Temel Kullanım

```python
import io
f = io.FileIO("data.bin", mode="rb")
data = f.read()
f.close()
```

--- 

#### Örnek 1 — FileIO ile Düşük Seviyeli Binary Okuma/Yazma
   
```python
from io import FileIO

# Düşük seviyeli I/O — buffer yok, her işlem doğrudan diske gider
with FileIO("ham_veri.bin", mode="w") as f:
    # bytes zorunlu! string yazarsan TypeError alırsın
    f.write(b"\x41\x42\x43\x44")  # 'ABCD' ASCII karşılığı

# Şimdi aynı dosyayı okuyalım
with FileIO("ham_veri.bin", mode="r") as f:
    veri = f.read()   # tüm dosyayı byte olarak oku
    print(veri)       # b'ABCD'

```
#### 💡 Açıklama:
- FileIO, doğrudan OS file descriptor’ı üzerinden çalışır.

- **f.write() →** doğrudan write(2) sistem çağrısını tetikler (C düzeyinde).
- **Buffer yok →** her çağrı diske gider (yavaş ama kesin).
- **Metin değil,** binary veriyle çalışılır (bytes, bytearray).


---

#### ⚙️ Örnek 2 — BufferedWriter ile Performanslı Yazma

```python
from io import FileIO

# Düşük seviyeli I/O — buffer yok, her işlem doğrudan diske gider
with FileIO("ham_veri.bin", mode="w") as f:
    # bytes zorunlu! string yazarsan TypeError alırsın
    f.write(b"\x41\x42\x43\x44")  # 'ABCD' ASCII karşılığı

# Şimdi aynı dosyayı okuyalım
with FileIO("ham_veri.bin", mode="r") as f:
    veri = f.read()   # tüm dosyayı byte olarak oku
    print(veri)       # b'ABCD'
```

#### 💡 Açıklama: 
- **FileIO**, doğrudan OS file descriptor’ı üzerinden çalışır.
- **f.write() →** doğrudan write(2) sistem çağrısını tetikler (C düzeyinde).
- **Buffer yok →** her çağrı diske gider (yavaş ama kesin).
- **Metin değil**, binary veriyle çalışılır (bytes, bytearray).

---

#### 📜 Örnek 3 — TextIOWrapper: Unicode Katmanı 

```python
from io import FileIO, BufferedWriter, TextIOWrapper

# Alt zincir: FileIO (disk) -> BufferedWriter (bellek) -> TextIOWrapper (metin)
with TextIOWrapper(BufferedWriter(FileIO("metin.txt", mode="w")),
                   encoding="utf-8") as txt:
    txt.write("Merhaba Dünya 🌍\n")
    txt.write("Python I/O mimarisi 🚀")
```
#### 🧠 Açıklama:
`TextIOWrapper`, Unicode → bytes dönüşümünü yapar.

`BufferedWriter’a` UTF-8 kodlanmış baytlar gönderir.

`FileIO` da bunları diske yazar.

**Zincir şöyle işler:**
```pgsql
TextIOWrapper.write("X")  
   ↓
encode('utf-8')
   ↓
BufferedWriter.write(b'X')
   ↓
FileIO.write()  → OS → Disk
```

---

## ⚙️ BufferedReader — Bellek Üzerinden Verimli Okuma Katmanı

`io.BufferedReader`, Python’un **Buffered I/O** mimarisinde
okuma (read) işlemlerine odaklanan somut (concrete) bir sınıftır.  
`BufferedIOBase`’ten türetilmiştir ve alt katmanda genellikle bir `RawIOBase`
nesnesi (örneğin `FileIO`) bulunur.

Bu sınıf, diskten okuma işlemlerini RAM üzerinde optimize eder.  
Her `read()` çağrısında doğrudan diske erişmek yerine,
veriler önce **okuma tamponuna (read buffer)** alınır,
daha sonra istenen miktarda veri bu tampondan döndürülür.

---

### 🔹 Genel Tanım

`BufferedReader`, **okuma performansını artırmak** ve
**disk I/O maliyetini azaltmak** için geliştirilmiş bir sınıftır.  
Python’un `open("dosya.txt", "rb")` fonksiyonu çağrıldığında
arka planda otomatik olarak bir `BufferedReader` örneği oluşturulur.

Bir `BufferedReader`, bir **alt akış (raw stream)** üzerinde çalışır —
örneğin:

```python
from io import FileIO, BufferedReader
raw = FileIO("veri.txt", "rb")
reader = BufferedReader(raw)
```

---
### 🧠 İleri Tanım — `BufferedReader` Sınıfı

`BufferedReader`, CPython düzeyinde `Modules/_io/buffered.c` içinde tanımlanmış bir sınıftır.  
Python I/O mimarisinde yalnızca **okuma yönlü** buffer sağlayan bir soyutlamadır.  
Yazma işlemi yapmaz — bunun tam karşılığı `BufferedWriter` sınıfıdır.

---

### 🧩 Soyut Hiyerarşi

```text
IOBase
└── RawIOBase
    └── BufferedIOBase
        └── BufferedReader  ← sadece okuma
        └── BufferedWriter  ← sadece yazma
```
---

### ⚙️ Teknik Özellikler — `BufferedReader` (Python Düzeyinde)

| 🔧 Özellik                | 🎯 Açıklama                                                                 |
|--------------------------|------------------------------------------------------------------------------|
| 🧱 Varsayılan buffer boyutu | `8192 byte` (8 KiB) — okuma işlemleri bu boyutta bloklanır.                 |
| 🔗 Alt akış gereksinimi     | Her zaman `RawIOBase` türevi bir nesne olmalıdır (`FileIO`, `BytesIO` vs.). |
| ⚡ Non-blocking desteği     | Bloklamayan modda çalışabilir — özellikle soketler için uygundur.           |
| 🔒 Thread-safe değil        | Ancak Python’un GIL mekanizması sayesinde atomic davranabilir.              |

---

### 🧩 Sözdizimi — `BufferedReader` Yapıcısı (`__init__`)

```python
io.BufferedReader(raw, buffer_size=io.DEFAULT_BUFFER_SIZE)
```
#### 🔧 Parametre Açıklamaları — `BufferedReader`

| 🏷️ Parametre     | 🎯 Açıklama                                                                 |
|------------------|------------------------------------------------------------------------------|
| `raw`            | Alt katman I/O nesnesi. Genellikle `FileIO`, `BytesIO` veya `RawIOBase` türevi bir nesne olmalıdır. |
| `buffer_size`    | Buffer kapasitesi (varsayılan: `8192 byte` → `io.DEFAULT_BUFFER_SIZE`). Okuma işlemleri bu boyutta bloklanır. |

---

### 🧠 Mimari Notlar

- `BufferedReader`, `RawIOBase` soyutlamasını saran bir **performans katmanıdır**.  
- Dosya açma işlemi `FileIO` gibi alt sınıflara bırakılır — bu sayede `BufferedReader` test edilebilir ve yeniden kullanılabilir hale gelir.  
- Buffer boyutu, okuma performansını doğrudan etkiler.  
  Büyük dosyalarda `buffer_size` artırılarak I/O verimi yükseltilebilir.

> 💡 Bu yapı, Python I/O mimarisinde **modülerlik**, **katmanlı soyutlama** ve **performans optimizasyonu** ilkelerini bir araya getirir.

---
### 🧪 Kullanım Örnekleri

#### 🔹 1. Temel Okuma
```python
import io

raw = io.FileIO("data.txt", mode="rb")
buffered = io.BufferedReader(raw)

data = buffered.read(1024)  # 1024 baytlık okuma
```
#### 💡 Açıklama:
- **read(1024) →** buffer doluysa doğrudan okur, değilse raw.read() ile doldurur

- **Performans:** disk erişimi azaltılır, okuma hızlanır

---

####🔹 2. Satır Satır Okuma
```python
for line in buffered:
    print(line)
```
#### 💡 Açıklama:

- **BufferedReader** iterator protokolünü destekler

- **Satır bazlı okuma** için readline() çağrısı yapılır

- **Özellikle lexer veya parser** öncesi kaynak satırlarını almak için idealdir

---

#### 🔹 3. peek() ile Önizleme

```python
preview = buffered.peek(64)
print(preview[:10])  # İlk 10 baytı göster
```
#### 💡 Açıklama:
- `peek(n)` -> buffer’daki veriyi okutmadan gösterir

- **Lexer** gibi “önce bak, sonra karar ver” mantığı için çok uygundur
---

#### 🔹 4. read1() ile Parça Parça Okuma

```python
chunk = buffered.read1(4096)
```
#### 💡 Açıklama:
- `read1()` → sadece buffer’daki mevcut veriyi döndürür

- **Disk erişimi yapılmaz** → hızlı ama sınırlı

---


## ⚙️ BufferedWriter — Bellek Üzerinden Verimli Yazma Katmanı

`io.BufferedWriter`, Python’un **Buffered I/O** mimarisinde
**yazma (write)** işlemlerine odaklanan somut bir sınıftır.  
`BufferedIOBase`’ten türetilmiştir ve alt katmanda genellikle bir `RawIOBase`
nesnesi (örneğin `FileIO`) bulunur.

Bu sınıf, belleğe alınan verileri toplu biçimde diske yazarak
**I/O performansını artırır** ve **disk erişim sayısını azaltır**.

---

### 🔹 Genel Tanım

`BufferedWriter`, bir dosya veya çıktı akışına yazma işlemi yapılmadan önce,
verilerin geçici olarak bellekte tutulduğu bir “yazma buffer’ı” yönetir.  

Yani `write()` çağrısı yapıldığında veri hemen diske gitmez —  
önce buffer’a yazılır, buffer dolduğunda veya `flush()` çağrıldığında
gerçek disk yazımı gerçekleşir.

Örnek:
```python
from io import FileIO, BufferedWriter
raw = FileIO("output.log", "wb")
writer = BufferedWriter(raw)

writer.write(b"Merhaba, dünya!")  # Henüz diske yazılmaz
writer.flush()                    # Şimdi disk I/O yapılır
```

---

### 🧠 İleri Tanım — `BufferedWriter` Sınıfı

`BufferedWriter`, CPython içinde `Modules/_io/buffered.c` dosyasında tanımlanmış bir sınıftır.  
Python I/O mimarisinde **yalnızca yazma yönlü** buffer sağlayan somut bir sınıftır.  
Okuma işlemi yapmaz — bunun tam karşılığı `BufferedReader` sınıfıdır.

---

#### 🧩 Sınıf Hiyerarşisi

```text
IOBase
└── RawIOBase
    └── BufferedIOBase
        └── BufferedWriter  ← sadece yazma
        └── BufferedReader  ← sadece okuma
```
---

### 🧩 Sözdizimi — `BufferedWriter` Yapıcısı (`__init__`)

```python
io.BufferedWriter(raw, buffer_size=io.DEFAULT_BUFFER_SIZE)
```

#### 🔧 Parametre Açıklamaları — `BufferedWriter`

| 🏷️ Parametre     | 🎯 Açıklama                                                                 |
|------------------|------------------------------------------------------------------------------|
| `raw`            | Alt düzey (raw) I/O nesnesi. Genellikle `FileIO`, `BytesIO` veya `RawIOBase` türevi bir nesne olmalıdır. |
| `buffer_size`    | Buffer kapasitesi (varsayılan: `8192 byte` → `io.DEFAULT_BUFFER_SIZE`). Yazma işlemleri bu boyutta bloklanır. |

---

### 🧩 BufferedWriter — Çalışma Mantığı ve İç Mimari

#### ⚙️ Çalışma Mantığı

- Kullanıcı `write(data)` çağrısı yapar.  
- Veri doğrudan diske değil, **buffer’a yazılır**.  
- Buffer dolduğunda, otomatik olarak alt katmandaki `raw.write()` çağrılır.  
- `flush()` metodu çağrıldığında, buffer’daki tüm veriler **diske aktarılır**.  
- `close()` çağrıldığında hem `flush()` yapılır hem dosya **güvenli biçimde kapanır**.

Bu yapı sayesinde:

- Küçük ve sık `write()` çağrıları birleştirilir  
- Disk erişimi azaltılır  
- I/O performansı belirgin şekilde artar

---

#### 🧩 İç Mantık (C düzeyinde)

- `BufferedWriter_write()` → veriyi buffer’a kopyalar  
- Buffer dolarsa → `_bufferedwriter_flush_unlocked()` tetiklenir  
- Bu fonksiyon:  
  `PyObject_CallMethod(raw, "write", ...)` ile **gerçek disk I/O çağrısını** yapar

> 💡 Bu mimari, Python’daki `write()` çağrısını C düzeyinde `fwrite()` sistem çağrısına dönüştürerek yüksek performans sağlar.

---

### 🔍 Kullanım Alanları — `BufferedWriter`

| 🧩 Alan                        | 🎯 Açıklama                                                                 |
|-------------------------------|------------------------------------------------------------------------------|
| 📄 Log sistemleri             | Çok sık yazma yapılan log dosyalarında buffer sayesinde performans artar.   |
| 📦 Veri çıktısı               | Binary dosyalar, büyük veri setleri, ağ paketleri gibi yüksek hacimli yazımlar. |
| ⚙️ Performans odaklı işlemler | Buffer sayesinde I/O darboğazı engellenir, sistem çağrısı sayısı azalır.    |
| 🌐 Stream yönlendirme         | `stdout` veya network socket gibi akışlara veri yazarken buffer kullanımı.  |

---

### ⚠️ Dikkat Edilmesi Gerekenler

- `BufferedWriter` yalnızca **yazma işlemleri** içindir.  
  Okuma gerekiyorsa `BufferedReader` veya `BufferedRandom` kullanılmalıdır.

- Buffer dolmadan veri **diske gitmez**.  
  Bu nedenle:

  - Uygulama ani kapanırsa **veri kaybı** olabilir  
  - Yazılan veri buffer’da kalabilir, diske ulaşmaz

#### ✅ Çözüm Önerileri

- `flush()` çağrısı ile buffer’daki veriyi manuel olarak diske aktar  
- Veya `with` bloğu kullanarak `close()` çağrısını garanti altına al:

```python
from io import FileIO, BufferedWriter

with BufferedWriter(FileIO("log.txt", "wb")) as f:
    f.write(b"Log verisi...\n")  # flush otomatik yapılır
```
- seek() çağrısı buffer’ı sıfırlar; yeni konuma geçilir.

- Çok büyük buffer boyutları RAM tüketimini artırabilir,
- çok küçük buffer ise performansı düşürür.

- Thread güvenliği sınırlıdır; aynı nesneye birden fazla thread yazmamalı.

---

### 🧪 Kullanım Örnekleri — `BufferedWriter`

---

#### 🔹 1. Temel Yazma İşlemi

```python
from io import FileIO, BufferedWriter

raw = FileIO("output.bin", mode="wb")
buffered = BufferedWriter(raw)

buffered.write(b"Merhaba Python!\n")
buffered.flush()  # Buffer’daki veriyi diske aktar
buffered.close()
````
#### 💡 Açıklama:
- `write()` → veriyi buffer’a yazar, diske gitmez

- `flush()` → buffer’daki veriyi diske gönderir

- `close()` → önce flush(), sonra kaynak serbest bırakılır

---

#### 🔹 2. Büyük Veri Yazımı (Performans Testi)
```python
from io import FileIO, BufferedWriter

with BufferedWriter(FileIO("veri_dump.bin", "wb"), buffer_size=16384) as f:
    for _ in range(10000):
        f.write(b"X" * 1024)  # 1KB veri
```

#### 💡 Açıklama:
- **buffer_size=16384** → 16KB buffer kullanılır

- **10.000 × 1KB veri** → 10MB dosya

- **Buffer** sayesinde sistem çağrısı sayısı azalır → performans artar

---

## 🧩 TextIOWrapper — Metin (Unicode) Katmanı

`io.TextIOWrapper`, Python’un **text-based (Unicode)** I/O sisteminin merkezinde yer alan sınıftır.  
`BufferedReader` ve `BufferedWriter` sınıflarının üzerine oturur;  
**ham byte akışlarını Unicode karakter dizilerine** dönüştürür ve tam tersi işlemi yapar.  

Bu sayede Python, diskle bayt düzeyinde iletişim kurarken bile geliştiriciye
“karakter odaklı” bir API sunar.

---

### 🎯 Genel Tanım

`TextIOWrapper`, dosya veya akış nesnesine **metin düzeyinde erişim** sağlar.  
Alt katmanında bir `BufferedReader` veya `BufferedWriter` bulunur.  
Bu alt katmandan gelen ham byte’lar `encoding` parametresiyle decode edilir.  
Yazma işlemlerinde ise tersine — karakterler encode edilip byte olarak iletilir.

**Yani:**  
> ✅`BufferedIO` performansı sağlar,  

>✅ `TextIOWrapper` ise insan okunabilirliği sağlar.

Örnek:
```python
from io import TextIOWrapper, FileIO
raw = FileIO("hello.txt", "w+b")
text = TextIOWrapper(raw, encoding="utf-8")

text.write("Merhaba Dünya\n")
text.seek(0)
text.flush()
text.read()  # "Merhaba Dünya\n"
```
---

### 🧠 İleri Tanım — `TextIOWrapper` Sınıfı

`TextIOWrapper`, CPython’ın `Modules/_io/textio.c` dosyasında tanımlanmış bir sınıftır.  
Python I/O mimarisinde en üst düzeyde yer alır ve **Unicode tabanlı metin işlemlerini** yönetir.  
Alt katmanında genellikle `BufferedWriter` veya `BufferedReader` bulunur.

---

#### 🧩 Sınıf Hiyerarşisi

```text
IOBase
└── BufferedIOBase
    └── TextIOBase
        └── TextIOWrapper
```
---

### 🔧 Ana Sorumluluklar — `TextIOWrapper`

```python
io.TextIOWrapper(buffer, encoding=None, errors=None, newline=None, line_buffering=False)
```
---

#### ⚙️ Encoding / Decoding Yönetimi

- `encoding` parametresiyle belirlenir (örn. `"utf-8"`, `"latin-1"`, `"ascii"`).
- Her `read()` çağrısında: **byte → karakter** dönüşümü yapılır.
- Her `write()` çağrısında: **karakter → byte** dönüşümü yapılır.
- Bu dönüşümler, Python’un **Unicode temelli mimarisini** destekler.
- Özellikle çok dilli kaynaklarda doğru encoding seçimi, veri bütünlüğü açısından kritiktir.

---

#### ⚙️ Newline Dönüşümü

- `newline` parametresi ile kontrol edilir: `None`, `"\n"`, `"\r\n"`, `""` gibi değerler alabilir.
- Python, farklı platformlardaki satır sonlarını **tek biçime (`\n`)** dönüştürerek taşınabilirliği sağlar.
- Bu dönüşüm, `TextIOWrapper` tarafından **otomatik olarak** yapılır.
- Böylece `INDENT`, `DEDENT`, `NEWLINE` gibi lexer token’ları platformdan bağımsız hale gelir.

---

#### ⚙️ Error Handling

- `errors` parametresiyle belirlenir: `"strict"`, `"ignore"`, `"replace"` gibi stratejiler.
- Encoding veya decoding sırasında oluşabilecek hatalarda **ne yapılacağını** kontrol eder:

| Strateji     | Davranış Açıklaması                                      |
|--------------|----------------------------------------------------------|
| `"strict"`   | Hatalı karakterde `UnicodeDecodeError` fırlatır          |
| `"ignore"`   | Hatalı karakteri **atlar**, sessizce geçer               |
| `"replace"`  | Hatalı karakteri `�` gibi **geçici bir simgeyle değiştirir** |

> 💡 Bu yapı, özellikle dış kaynaklardan gelen verilerde (ağ, dosya, kullanıcı girişi) **hata toleransı** ve **kontrollü bozulma** sağlar.

---

### ⚙️ Çalışma Mantığı — `TextIOWrapper`

- Kullanıcı `text.write("merhaba")` çağrısı yapar  
- Karakterler `encode(encoding)` ile **byte dizisine** çevrilir  
- Alt katmandaki `BufferedWriter.write()` çağrılır → veri buffer’a yazılır  
- `flush()` çağrıldığında → buffer’daki tüm byte verileri **diske aktarılır**  
- `close()` çağrıldığında → hem `TextIOWrapper`, hem `BufferedWriter`, hem `FileIO` **kapatılır**

---

- `text.read()` çağrıldığında:  
  - `BufferedReader.read()` üzerinden byte verisi alınır  
  - `decode(encoding)` ile **Unicode karakterlere** dönüştürülür  
  - Satır sonları `newline` parametresine göre normalize edilir

> 💡 Bu yapı, Python’un Unicode temelli mimarisiyle uyumlu, platform bağımsız ve insan-okunabilir metin akışı sağlar.

---

### 🔍 Kullanım Alanları — `TextIOWrapper`

| 🧩 Alan                             | 🎯 Açıklama                                                                 |
|------------------------------------|------------------------------------------------------------------------------|
| 📄 Metin dosyaları                 | `.txt`, `.csv`, `.json` gibi karakter tabanlı dosyalar                      |
| 🌐 Platform bağımsız satır sonu    | Windows, Linux, macOS fark etmeksizin aynı biçimde okuma/yazma              |
| 🌍 Unicode destekli uygulamalar    | Çok dilli içerikler, kullanıcı girişleri, metin tabanlı veri işleme         |
| 🧠 `open()` fonksiyonu             | `open(..., encoding="utf-8")` çağrısı aslında `TextIOWrapper` oluşturur     |

---

### ⚠️ Dikkat Edilmesi Gerekenler

- `TextIOWrapper`, **sadece karakterlerle** çalışır  
  → doğrudan `bytes` yazmak veya okumak `TypeError` üretir

```python
text.write(b"bytes")  # ❌ TypeError
```

```python
text.write("bytes") # ✅
```

- **encoding yanlış seçilirse karakterler bozulu**r → Özellikle UTF-8 / Latin-1 farkı kritik

- **newline davranışı platforma göre farklılık gösterebilir** → Windows: \r\n, Linux/macOS: \n

- **Performans açısından TextIOWrapper, BufferedWriter’a göre biraz daha yavaştır** → Çünkü her işlemde encode / decode yapılır

- **Encoding değiştirilmek istenirse** `reconfigure()` metodu kullanılmalıdır (Python 3.7+):

---

###  🧩 Karşılaştırma — `BufferedReader` / `BufferedWriter` vs `TextIOWrapper`

| 🧩 Özellik             | `BufferedReader` / `BufferedWriter` | `TextIOWrapper`                          |
|------------------------|--------------------------------------|------------------------------------------|
| 📦 Katman              | Byte düzeyi                         | Karakter düzeyi                          |
| 🔤 Veri türü           | `bytes`                             | `str` (Unicode)                          |
| 🎯 Amaç                | Performans                          | İnsan-okunabilirlik                      |
| 🔧 Encoding            | Yok                                 | Var (`utf-8`, `latin-1` vb.)             |
| 🔁 Newline dönüşümü    | Hayır                               | Evet                                     |
| 📄 Kullanım            | Binary dosyalar, ağ I/O             | Metin dosyaları, kullanıcı girdileri     |

