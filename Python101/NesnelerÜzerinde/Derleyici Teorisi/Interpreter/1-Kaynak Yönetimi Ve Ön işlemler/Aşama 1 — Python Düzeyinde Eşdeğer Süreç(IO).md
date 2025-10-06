## ⚙️ I/O — “Input / Output” Kavramı

---

#### 🧑‍🎓 **Yeni başlayan (CS öğrencisi)**
#### 🕒 **Tahmini Süre: 140dk**

---

### 🧭 Python I/O Öğrenme Haritası

| 🔢 Katman No | 🧩 Katman Adı                                            | 🎯 Açıklama                                                                 |
|-------------|----------------------------------------------------------|------------------------------------------------------------------------------|
| 1️⃣          | <span style="color: yellow;">Temel Kavram Katmanı</span> | I/O, stream, buffer ve encoding kavramlarının temelleri.                    |
| 2️⃣          | <span style="color: yellow;">Soyut Sınıf Katmanı</span>  | Tüm I/O türlerinin dayandığı ortak arayüzler (`IOBase`, `RawIOBase`...).    |
| 3️⃣          | Uygulama Katmanı                                         | Gerçek dünyadaki I/O sınıfları (`FileIO`, `BufferedIO`, `TextIOWrapper`).   |
| 4️⃣          | Ortak Metodlar Katmanı                                   | `read()`, `write()`, `seek()` gibi her akışta ortak davranışlar.            |
| 5️⃣          | Buffer & Performans Katmanı                              | I/O hızını belirleyen buffer yönetimi ve optimizasyonlar.                   |
| 6️⃣          | Modül Fonksiyonları Katmanı                              | `open()`, `io.StringIO()`, `io.BytesIO()` gibi üst seviye API’ler.          |
| 7️⃣          | Deneysel / Ustalık Katmanı                               | Kendi I/O sınıflarını ve sanal dosya sistemlerini tasarlama.                |
---

### 🔹1️⃣.1️⃣ Genel Tanım

**I/O (Input / Output)**, bir bilgisayar programının dış dünya ile veri alışverişini ifade eden temel kavramdır.  
Adı “Input / Output” (girdi / çıktı) kelimelerinin kısaltmasıdır.

#### 📥 Input (Girdi)
Programın dışarıdan aldığı veri:  
- Dosya içeriği  
- Klavye girdisi  
- Ağ mesajı  
- stdin (standart giriş)

#### 📤 Output (Çıktı)
Programın dış dünyaya gönderdiği veri:  
- Ekrana yazı  
- Dosyaya kayıt  
- Ağ cevabı  
- stdout / stderr

> 🧠 Basitçe:  
> “I/O, bir programın kendisi dışındaki kaynaklarla konuşma biçimidir.”

Python açısından I/O, sadece dosya okumak/yazmak anlamına gelmez.  
Her türlü **veri akışı (stream)** bir I/O işlemidir:

- 📄 Dosya
- 🌐 Ağ soketi
- 🔗 Pipe
- 🖥️ Terminal
- 📥 stdin / 📤 stdout

---

### 🔹 1️⃣.2️⃣ İleri Tanım

Bilgisayar bilimi düzeyinde, I/O iki ana ilkeye dayanır:

#### 🧱 a) Soyutlama Katmanı (Abstraction Layer)

Program, disk veya ağ donanımını **doğrudan yönetmez**.  
Bunun yerine, I/O soyutlamaları üzerinden erişim sağlar:

| 🧩 Soyutlama       | 🎯 Görev                                                                 |
|--------------------|--------------------------------------------------------------------------|
| `file descriptor`  | İşletim sistemi düzeyinde dosya tanımlayıcısıdır.                        |
| `buffer`           | Bellek içi geçici veri deposudur (örneğin 4KB bloklar).                  |
| `stream`           | Akış temelli veri erişimi sağlar (satır satır, bayt bayt vs.).           |

Python bu soyutlamayı şu şekilde uygular:

- `open()` → `TextIOWrapper` üzerinden yüksek seviyeli stream oluşturur.
- `sys.stdin`, `sys.stdout` → terminal I/O erişimi sağlar.
- `socket.makefile()` → ağ soketlerini stream gibi kullanır.

**Her katman belirli bir sorumluluk taşır:**
> 💡**Python katmanı:** Unicode, encoding, hata yönetimi, line buffering
> 
> 💡**C katmanı:** FILE akışları, **`fopen`** / **`fread`** / **`fwrite`**
> 💡**OS katmanı:** read() / write() sistem çağrıları
> 
> 💡**Donanım:** Gerçek disk, ağ arabirimi veya bellek
> 
> 🧠**Bu zincir sayesinde Python, her platformda aynı API ile çalışabilen bir I/O sistemi sunar**.

---

### 🔹 1️⃣.3️⃣ I/O Türleri

Python’da I/O işlemleri farklı kaynaklara ve veri biçimlerine göre sınıflandırılır.  
Ancak tüm bu türler, Python’un I/O mimarisinde **“akış” (stream)** soyutlaması altında birleşir.

| ⚙️ Tür              | 🎯 Açıklama                                               | 🧪 Örnek                          |
|---------------------|-----------------------------------------------------------|----------------------------------|
| 📄 File I/O         | Diskteki dosyaların okunması / yazılması                 | `open("data.txt")`              |
| 🌊 Stream I/O       | Bellek veya ağ üzerinden akan veri                        | `sys.stdin`, `socket.recv()`    |
| 📝 Text I/O         | Unicode karakterlerle çalışır                             | `io.TextIOWrapper`              |
| 🧱 Binary I/O       | Ham bayt düzeyinde veri işlemi                            | `open("image.png", "rb")`       |
| ⚡ Asynchronous I/O | I/O işlemlerinin bloklamadan yürütülmesi                 | `await stream.read()`           |

> 💡 Python’da bu türlerin tamamı aynı soyutlama üzerinde birleşir:  
> Her biri bir **“akış” (stream)** olarak değerlendirilir ve `read()`, `write()`, `readline()` gibi ortak arabirimlerle yönetilir.

---
### 🔹 1️⃣.4️⃣ Neden Adı “I/O”?

“I/O” kavramı yalnızca yazılıma özgü değildir —  
donanım, işletim sistemi ve yazılım katmanlarının **tamamında** geçerlidir.

- 📜 Tarihsel kökeni: 1950’lerdeki **Input/Output Channels** (girdi/çıktı kanalları) kavramına dayanır.
- 🖥️ O dönemde her cihaz (klavye, disk sürücüsü, printer) ayrı bir I/O kanalına sahipti.
- 🧬 Modern dillerde bu miras sürer:  
  Python’un “I/O stream” kavramı, bu eski kanal yapısının **mantıksal devamıdır**.

---

### 🔹 1️⃣.5️⃣ Kullanım Alanları

Python’da I/O, sistemle etkileşimin temelidir.  
Her `print()`, `input()`, `open()` çağrısı aslında bir I/O işlemidir.

| 🧩 Alan                    | 🎯 Açıklama                                                       |
|---------------------------|--------------------------------------------------------------------|
| 📄 Dosya sistemleri        | Metin dosyası, binary dosya, log, config okuma/yazma              |
| 🌐 Veri akışı              | Socket (TCP/UDP), HTTP stream, pipe’lar                           |
| 🖥️ Standart giriş/çıkış    | `stdin`, `stdout`, `stderr` yönetimi                              |
| 🧠 Bellek tabanlı I/O      | `io.StringIO`, `io.BytesIO` → sanal dosyalar                      |
| ⚡ Asenkron I/O            | `asyncio` ile non-blocking veri aktarımı                          |
| 🔗 Inter-process communication (IPC) | Process’ler arası veri alışverişi                        |

---

### 🔹 1️⃣.6️⃣ Dikkat Edilmesi Gerekenler

#### ⚠️ Bloklama (Blocking I/O)
- Standart I/O işlemleri (örneğin `open().read()`) **bloklayıcıdır**.
- Büyük dosyalarda veya ağ işlemlerinde performans kaybı yaşanabilir.
- 💡 Çözüm: `asyncio`, `aiofiles` gibi **non-blocking** yapılar kullanmak.

#### ⚠️ Buffer Yönetimi
- I/O işlemleri pahalıdır (disk/ağ erişimi milisaniyeler sürer).
- Python, veriyi **buffer’layarak** okur/yazar.
- Yanlış buffer boyutu → performans düşüşü.

#### ⚠️ Encoding / Newline Uyumu
- Text I/O işlemlerinde `encoding` ve `newline` parametreleri kritik önemdedir.
- Yanlış ayar → `UnicodeDecodeError` veya okuma/yazma hataları.

---

### 🔹 1️⃣.7️⃣ Ekstra Bilgiler

| 🛠️ Bileşen                | 📌 Açıklama                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| 📁 CPython Kaynak Kodu     | I/O altyapısı `Modules/_io/` dizininde yer alır.                            |
| 🧱 Katman Dosyaları        | `textio.c`, `bufferedio.c`, `fileio.c` → I/O katmanlarını uygular.          |
| 📦 io Modülü               | `open()` fonksiyonunun arkasındaki sınıflar burada tanımlıdır.              |
| 🧠 Bellek Kullanımı        | Her I/O akışı için 4–8 KB buffer ayrılır → hız ve veri bütünlüğü sağlar.    |
| 🔁 Evrensel Yeni Satır     | `TextIOWrapper` → `\r`, `\r\n`, `\n` ayrımını ortadan kaldırır.             |

---

### 🔹 1️⃣.8️⃣ Özet

| 🧩 Özellik                 | 🎯 Açıklama                                                                 |
|---------------------------|------------------------------------------------------------------------------|
| 📖 Açılımı                 | Input / Output                                                              |
| 🎯 Amaç                    | Programın dış dünyayla veri alışverişi                                      |
| 🧬 Python’daki Temsili     | Stream nesneleri (`TextIO`, `BufferedIO`, `RawIO`)                          |
| 🏗️ Çalışma Şekli           | Çok katmanlı soyutlama (Python → C → OS → Donanım)                          |
| 🧪 Örnekler                | Dosya okuma/yazma, `print()`, `input()`, `socket`, `stdin` / `stdout`       |
| ⚡ Performans Prensibi     | Buffering, lazy read/write, non-blocking opsiyonlar                         |


---

## 🧱 2️⃣ — Soyut Sınıf Katmanı (Abstract Layer)

Python’un I/O mimarisi, soyut sınıflar üzerine inşa edilmiş bir **katmanlı sistemdir**.  
Bu katman, tüm dosya, akış ve bellek I/O sınıflarının **ortak davranışlarını tanımlar**.  
Yani her I/O türü (`FileIO`, `StringIO`, `TextIOWrapper`…) bu temel sınıflardan kalıtım alarak çalışır.

---

### 🎯 Amaç

Soyut sınıf katmanı, “nasıl yapılacağını” değil, “ne yapılacağını” tanımlar.  
Yani bu katman kodu yazmaz, kuralları belirler.  
Alt sınıflar (örneğin `FileIO`, `BufferedReader`) bu kuralları uygular.

---

### 🧩 Katman Hiyerarşisi

| Katman | Sınıf | Görev |
|:--|:--|:--|
| **1️⃣ Temel Taban** | `IOBase` | Tüm I/O sistemlerinin ortak kökü. (Açma, kapama, konum kontrolü) |
| **2️⃣ Ham Katman (Raw)** | `RawIOBase` | Byte düzeyinde düşük seviye dosya işlemleri (readinto, write) |
| **3️⃣ Buffer Katmanı** | `BufferedIOBase` | Performans için tamponlama sağlar |
| **4️⃣ Metin Katmanı** | `TextIOBase` | Unicode ve satır bazlı okuma/yazma yönetimi |

Her biri kendi alt sınıfları için iskelet niteliğindedir.  
Gerçek davranışlar (“ne yapar”) **uygulama katmanında** gelir, ama **arayüz** burada tanımlanır.

---

> ⚙️ **Teknik Not — I/O Sınıflarının Gerçek Doğası**

`IOBase`, `FileIO`, `BufferedReader` ve `TextIOWrapper` gibi sınıflar saf Python sınıfları değil,  
**C tabanlı extension type**’lardır.  
Bu yüzden çağrıldıklarında Python bytecode yerine doğrudan **C fonksiyonları (PyCFunction)** çalışır.

---

### 🔩 Çağrı Zinciri (Basitleştirilmiş)

| Katman | İşlev | Örnek |
|:--|:--|:--|
| **Python opcode** | `CALL_METHOD`, `LOAD_METHOD` metodu çözer | `f.write("Hi")` |
| **C API** | `tp_methods` tablosundan C fonksiyonunu bulur | `fileio_write()` |
| **OS seviyesi** | Gerçek sistem çağrısı | `write(fd, buf, size)` |

---

### ⚙️ Örnek Akış: `f.write("data")`

1️⃣ `LOAD_METHOD` → `write` metodunu bulur  
2️⃣ `CALL_METHOD` → `PyCFunction_Call` tetiklenir  
3️⃣ `fileio_write()` → C düzeyinde I/O  
4️⃣ `write()` → Kernel sistem çağrısı  
5️⃣ Veri diske yazılır  

---

### 🚀 Performans Etkisi

- Python seviyesi yalnızca yönlendirme yapar (dispatch).  
- Gerçek iş C ve OS düzeyinde yürütülür.  
- Bu sayede I/O işlemleri **saf Python fonksiyonlarına göre yüzlerce kat daha hızlıdır.**

---

### 💡 Özet

| Katman | Ne yapar | Avantaj |
|:--|:--|:--|
| Python | Metot çözümleme (`CALL_METHOD`) | Güvenli soyutlama |
| C | I/O işlemini yürütür (`fileio_write`) | Yüksek hız |
| OS | Donanımla etkileşim | Gerçek I/O gerçekleşir |


🧠 **Sonuç:**  
`f.write()` gibi bir çağrı aslında Python kodu değil,  
CPython çekirdeğindeki `fileio_write()` fonksiyonuna yapılan **dolaylı bir C çağrısıdır** —  
ve bu, Python’un dosya işlemlerinde gösterdiği olağanüstü hızın temel nedenidir.
---

### ⚙️ IOBase — Tüm I/O Sınıflarının Tabanı

`io.IOBase` sınıfı, tüm akış türlerinin ortak metodlarını içerir.  
Bu sınıf genellikle doğrudan kullanılmaz, ancak tüm diğer sınıfların miras aldığı tabandır.

#### 📘 Öne Çıkan Metodlar

| Metod | Açıklama |
|:--|:--|
| `close()` | Akışı kapatır, sistem kaynaklarını serbest bırakır. |
| `flush()` | Buffer’daki veriyi diske aktarır. |
| `seek(offset, whence=0)` | Dosya imlecini taşıma. |
| `tell()` | Mevcut imleç konumunu döndürür. |
| `readable()`, `writable()`, `seekable()` | Akışın desteklediği özellikleri bildirir. |

### 🧠 Önemli Dunder Metodları

| Dunder | Rol |
|:--|:--|
| `__enter__`, `__exit__` | Context manager desteği sağlar (`with open(...) as f:`) |
| `__iter__`, `__next__` | Satır satır okuma imkânı verir (`for line in f:`) |
| `__del__` | Nesne silindiğinde otomatik `close()` çağırır. |


#### ⚙️ ️️️Temsili Kodlardır:

```python
from typing import Self, Optional
from types import TracebackType

class IOBase:
    """Temsili IOBase sınıfı — gerçek CPython sürümünün Python eşleniği.
    
    - Context manager davranışı (`with`).
    - Iterator davranışı (`for line in file:`).
    """

    def __enter__(self: Self) -> Self:
        """Kaynak açıldığında self döndürür."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> bool:
        """Çıkarken dosyayı kapatır ve hatayı bastırmaz."""
        self.close()
        return False

    def __iter__(self: Self) -> Self:
        """Iterator protokolü: self'ı döndürür."""
        return self

    def __next__(self) -> str:
        """Bir sonraki satırı döndürür. EOF'ta StopIteration yükseltir."""
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    # --- Temsili yöntemler ---
    def readline(self) -> str:
        """Simüle edilmiş readline."""
        # Gerçekte bu, buffer'dan veya OS çağrısından okur.
        return ""

    def close(self) -> None:
        """Kaynağı serbest bırakır."""
        # Gerçekte dosya descriptor'u kapatır.
        print("Kaynak kapatıldı.")

```
>💡 **Not:** Bu dunder metodları sayesinde I/O nesneleri Python’un tüm protokollerine uyum sağlar (context, iteration, cleanup).

---

### ⚙️ RawIOBase — Byte Seviyesinde Erişim

Bu sınıf, işletim sistemine **en yakın** olan katmandır.  
Dosyayı “karakter” olarak değil, “ham byte dizisi” olarak ele alır.

#### 📘 Öne Çıkan Metodlar

| Metod | Açıklama |
|:--|:--|
| `read(size=-1)` | Belirtilen kadar byte okur. |
| `readinto(b)` | Veriyi doğrudan verilen bytearray içine yazar. |
| `write(b)` | Byte verisini diske yazar. |

### 🧠 Önemli Dunder Metodları

| Dunder | Rol |
|:--|:--|
| `__bytes__` | Akışın içeriğini byte dizisine dönüştürür. |
| `__len__` | (Opsiyonel) Buffer uzunluğu bilgisi verebilir. |

📚 *Raw katman genellikle doğrudan kullanılmaz; üst katmanlar tarafından sarılır (ör. `BufferedReader`).*

```python
class RawIOBase:
   
    def read(self, size: int = -1) -> bytes:
        """
        📖 Ham byte verisini okur.

        Args:
            size (int): Okunacak byte sayısı. Varsayılan -1, yani tamamı.

        Returns:
            bytes: Okunan ham byte dizisi.

        Not:
            Gerçek sistemde bu işlem `os.read(fd, size)` çağrısına eşdeğerdir.
        """
        print(f"{size} byte okundu (temsili).")
        return b""

    def readinto(self, b: bytearray) -> int:
        """
        📥 Byte verisini doğrudan verilen `bytearray` içerisine yazar.

        Args:
            b (bytearray): Hedef buffer.

        Returns:
            int: Yazılan byte sayısı.

        Bu yöntem, ek bellek tahsisini önler — performans için önemlidir.
        """
        n = min(len(b), 4)
        b[:n] = b"\x00" * n
        print(f"{n} byte buffer'a yazıldı (temsili).")
        return n

    def write(self, b: bytes) -> int:
        """
        ✏️ Ham byte dizisini hedefe (örneğin diske) yazar.

        Args:
            b (bytes): Yazılacak veriler.

        Returns:
            int: Yazılan byte sayısı.

        Not:
            Gerçekte bu işlem `os.write(fd, b)` sistem çağrısına karşılık gelir.
        """
        print(f"{len(b)} byte yazıldı (temsili).")
        return len(b)

    # --- Dunder Metodlar ---
    def __bytes__(self) -> bytes:
        """
        🔄 Akışın içeriğini byte dizisine dönüştürür.
        Genellikle `bytes(stream)` ifadesinde çağrılır.
        """
        return self.read()

    def __len__(self) -> int:
        """
        📏 (Opsiyonel) Buffer uzunluğunu döndürebilir.
        Bu metod, bazı özel Raw I/O türlerinde override edilir.
        """
        return 0
````

---

### ⚙️ BufferedIOBase — Performans Katmanı

Okuma/yazma işlemleri, diske doğrudan yapılırsa yavaştır.  
`BufferedIOBase`, bellekte geçici bir **buffer (tampon)** tutarak işlemleri hızlandırır.

#### 📘 Öne Çıkan Metodlar

| Metod | Açıklama |
|:--|:--|
| `read(size=-1)` | Buffer’dan okur, gerekirse diske başvurur. |
| `write(b)` | Buffer’a yazar; buffer dolduğunda diske aktarır. |
| `flush()` | Buffer’daki veriyi zorla yazar. |

### 🧠 Önemli Dunder Metodları

| Dunder | Rol |
|:--|:--|
| `__getbuffer__` | Buffer nesnesini döndürür (C API’de kullanılır). |
| `__del__` | Nesne silinirken buffer’ı boşaltır. |

💡 **Not:** Bu katman `read1()` ve `peek()` gibi ek metotlarla **parça parça okuma** ve **önbellek önizleme** sağlar.


### ⚙️ BufferedIOBase — Tamponlu (Buffered) I/O Katmanı

Bu sınıf, `RawIOBase` üzerine inşa edilmiştir.  
Verileri doğrudan diske göndermek yerine önce **bellekte geçici bir buffer (tampon)** içinde tutar.  
Bu sayede I/O işlemleri çok daha hızlı ve verimli hale gelir.

```python
class BufferedIOBase:
   

    def read(self, size: int = -1) -> bytes:
        """
        📖 Buffer üzerinden veri okur.

        Args:
            size (int): Okunacak maksimum byte miktarı. Varsayılan -1 → tüm buffer.

        Returns:
            bytes: Buffer’dan okunan veri.

        Not:
            Eğer buffer boşsa, sistem çağrısı (ör. os.read) yapılır ve buffer doldurulur.
        """
        print(f"{size} byte buffer'dan okundu (temsili).")
        return b"data"

    def read1(self, size: int = -1) -> bytes:
        """
        📘 Buffer’dan *yalnızca mevcut* veriyi okur (sisteme dokunmaz).

        Args:
            size (int): Okunacak byte sayısı.

        Returns:
            bytes: Buffer içeriği (kısmi olabilir).

        Fark:
            `read()` → gerekirse diske gider.
            `read1()` → sadece buffer’ı kullanır.
        """
        print(f"{size} byte doğrudan buffer'dan okundu (read1, temsili).")
        return b"buf"

    def write(self, data: bytes) -> int:
        """
        ✏️ Veriyi buffer’a yazar (hemen diske gitmez).

        Args:
            data (bytes): Yazılacak veri.

        Returns:
            int: Buffer’a yazılan byte miktarı.

        Not:
            Gerçek yazma işlemi `flush()` çağrıldığında gerçekleşir.
        """
        print(f"{len(data)} byte buffer'a yazıldı (temsili).")
        return len(data)

    def flush(self) -> None:
        """
        🚀 Buffer’daki veriyi diske aktarır.

        Bu işlem, dosya kapatılmadan önce çağrılır.
        """
        print("Buffer diske aktarıldı (flush).")

    def close(self) -> None:
        """
        🔒 Akışı güvenli biçimde kapatır.
        Flush çağrısı yapıldıktan sonra kaynak serbest bırakılır.
        """
        self.flush()
        print("Buffered I/O kapatıldı.")


````
---


### ⚙️ TextIOBase — Unicode & Metin Katmanı

Bu katman, “ham byte” verisini artık “karakter” olarak yorumlar.  
Encoding, newline yönetimi, hata işleme (`errors='ignore'`) gibi davranışlar burada yönetilir.

#### 📘 Öne Çıkan Metodlar

| Metod | Açıklama |
|:--|:--|
| `read(size=-1)` | Unicode karakter dizisi döndürür. |
| `write(s)` | Unicode string’i encoding’e göre byte’lara dönüştürüp yazar. |
| `readline()` | Satır bazlı okuma. |
| `seek(offset)` | Dosya imlecini taşır. |
| `encoding`, `errors`, `newlines` | Önemli attribute’lar. |

### 🧠 Önemli Dunder Metodları

| Dunder | Rol |
|:--|:--|
| `__str__` | Nesnenin okunabilir temsili (`<TextIOWrapper name='file.txt'>`). |
| `__repr__` | Teknik bilgi içerikli temsili döndürür. |

📚 *Bu katman, `open()` fonksiyonunun oluşturduğu nesnede en üstteki soyutlama katmanıdır.*


### 📝 TextIOBase — Unicode ve Satır Odaklı Metin Katmanı

Bu sınıf, `BufferedIOBase` üzerine kurulur ve byte verisini **Unicode metne dönüştürür**.  
Artık ham byte dizileri değil, `str` nesneleriyle çalışır.  
Ayrıca satır sonu (`\n`, `\r\n`) yönetimini otomatik yapar.

```python
class TextIOBase:

    def __init__(self, encoding: str = "utf-8", errors: str = "strict"):
        """
        Args:
            encoding (str): Kullanılacak karakter kodlaması.
            errors (str): Hata işleme stratejisi ('ignore', 'replace', 'strict').
        """
        self.encoding = encoding
        self.errors = errors
        self.buffer = ""
        print(f"TextIOBase başlatıldı → encoding={encoding}")

    def read(self, size: int = -1) -> str:
        """
        📖 Unicode metin okur.

        Args:
            size (int): Okunacak karakter sayısı. Varsayılan -1 → tüm içerik.

        Returns:
            str: Decode edilmiş Unicode metin.
        """
        print(f"{size} karakter okundu (temsili).")
        return "örnek metin"

    def readline(self) -> str:
        """
        📜 Tek bir satır okur (satır sonuna kadar).
        """
        print("Bir satır okundu (readline).")
        return "satır\n"

    def write(self, s: str) -> int:
        """
        ✏️ Unicode metni yazar, buffer’a ekler.

        Args:
            s (str): Yazılacak Unicode metin.

        Returns:
            int: Yazılan karakter sayısı.
        """
        self.buffer += s
        print(f"{len(s)} karakter yazıldı (temsili).")
        return len(s)

    def flush(self) -> None:
        """
        🚀 Buffer’daki veriyi kodlayıp (encode) diske aktarır.
        """
        print("Text buffer diske aktarıldı (flush).")

    def close(self) -> None:
        """
        🔒 Akışı kapatır, buffer’ı temizler ve kaynakları serbest bırakır.
        """
        self.flush()
        print("Text I/O kapatıldı.")

```
---

## 🔗 Özet Akış

