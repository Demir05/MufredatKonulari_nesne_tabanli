# 🧠 Binary Data Model — Genel Tanım

**Binary Data Model**,  
Python’un bellekte tuttuğu veriyi, dosya ve donanım düzeyinde **ikili (binary)** biçimde temsil eden  
ve nesnelerin bu veriye nasıl erişip paylaştığını belirleyen yapıdır.

> 🧩 **Binary Data Model** = Python nesnelerinin RAM üzerindeki **gerçek byte temsili**  
> ve bu byte’ların **nasıl taşındığını** tanımlayan sistemdir.

---

### ⚙️ Temel Amacı

- 🔁 Veriyi **kopyalamadan paylaşmak** (*zero-copy*)  
- 🔌 I/O (dosya, ağ, disk) ile **ham byte seviyesinde** iletişim kurmak  
- 🧱 Python nesnelerini **C tabanlı sistemlerle uyumlu** hale getirmek  
- 🧮 `bytes`, `bytearray`, `memoryview`, `array`, `struct`, `mmap` gibi türler üzerinden  
  **bellek yönetimi optimizasyonu** sağlamak  

---

### 💾 Ne Zaman Devreye Girer?

Binary Data Model tipik olarak şu durumlarda devreye girer:

- 📂 Dosya veya soket işlemleri (okuma / yazma → byte)  
- 🧠 NumPy, PIL gibi **C uzantılı kütüphanelerde** veri aktarımı  
- 🗺️ **Bellek haritalama** (`mmap`) ve buffer paylaşımı  
- 🔄 Python ↔ C modülü arasında **doğrudan bellek transferi**  
- ⚡ `readinto()` / `memoryview()` gibi **zero-copy** operasyonlar  

---

## 📘 Binary Data Model — Konu Haritası

Aşağıdaki tablo, bu modelin tüm parçalarını sistematik biçimde gösterir.  
Her satır, bir bileşeni ve öğrenme amacını temsil eder.

| 🔢 Sıra | 🧩 Başlık | 📖 Açıklama | 🧠 Anahtar Kavramlar | 🎯 Beklenen Kazanım |
|----------|------------|-------------|-----------------------|---------------------|
| 1️⃣ | **Bit ve Byte Temeli** | Bit, byte, binary sistemin yapıtaşları | 8-bit yapı, ASCII, ikili gösterim | Belleğin en küçük birimini kavrama |
| 2️⃣ | **`bytes` Türü** | Salt okunur byte dizisi | Immutable, `to_bytes()`, `from_bytes()` | Byte temsili, sayısal dönüşüm ilişkisi |
| 3️⃣ | **`bytearray` Türü** | Yazılabilir byte dizisi | Mutable buffer, slicing, in-place değişim | Buffer’a yazma mantığını öğrenme |
| 4️⃣ | **`array` Modülü** | C tarzı sabit tipte dizi | Homojen veri, typecode, contiguous memory | C bellek düzenine uygun veri tutma |
| 5️⃣ | **`memoryview`** | Belleğe pencere açan görünüm | Zero-copy, slicing, writable flag | Aynı RAM alanını paylaşmayı öğrenme |
| 6️⃣ | **Buffer Protocol (PEP 3118)** | Nesneler arası bellek paylaşım arayüzü | `Py_buffer`, `bf_getbuffer`, `bf_releasebuffer` | C seviyesi arayüz kavrayışı |
| 7️⃣ | **`struct` Modülü** | C veri tiplerini byte’lara dönüştürme | Endianness, alignment, format codes | Byte ↔ C veri dönüşümünü anlamak |
| 8️⃣ | **`mmap` Modülü** | Dosya ve RAM arasında eşleme | Memory-mapped I/O, page caching | Disk ve bellek arası performanslı erişim |
| 9️⃣ | **Zero-Copy Data Flow** | Veriyi kopyalamadan taşımak | `readinto()`, `recv_into()`, `memoryview` | Performans odaklı veri aktarımı |
| 🔟 | **Binary I/O Performansı** | Buffer boyutu, cache locality | Flush, buffering, syscall optimizasyonları | CPU–RAM–Disk etkileşimini anlamak |

---

## 🧠 Nihai Amaç

Bu modeli kavradığında:

- 🧩 **Python nesnelerinin C düzeyindeki bellek karşılığını** anlayabileceksin.  
  Her nesnenin RAM’de nasıl tutulduğunu, `PyObject` yapılarının nasıl davrandığını  
  ve buffer protokolünün bu yapılarla nasıl etkileştiğini çözebileceksin.

- ⚙️ **Veri aktarımı ve performans optimizasyonu** konularında tam kontrolün olacak.  
  Kopyasız veri aktarımı (*zero-copy*), bellek haritalama (`mmap`),  
  buffer yönetimi ve sistem çağrısı optimizasyonları senin elinde olacak.

- 🧠 **Kendi yazdığın üst seviye yapılar**  
  (`Finder`, `Loader`, özel `AST` analiz araçları, `metaclass` sistemleri)  
  artık **byte tabanlı dosya / bellek yönetimiyle doğrudan entegre** olabilir hale gelecek.

---