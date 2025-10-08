# 🧩 Magic Bytes ve BOM — Dosya Tanımlayıcıları Rehberi

---

## 🧩 1️⃣ Magic Bytes — “Dosya Türü Tanımlayıcıları”

**Magic bytes**, bir dosyanın hangi formatta olduğunu belirten özel bayt dizileridir.  
Dosyanın içeriğine değil, türüne dair bilgi verir. Yani “bu dosya bir PDF mi, PNG mi?” sorusunun cevabıdır.  
Dosyanın en başında yer alırlar ve genellikle sabittirler.

### 🔍 Ne işe yarar?

- Dosya türünü tanımlar, encoding’i değil.
- Tarayıcı, işletim sistemi veya yazılım, dosyayı nasıl işleyeceğine bu baytlara bakarak karar verir.
- MIME türü, açılacak uygulama veya güvenlik kontrolleri bu imzaya göre şekillenir.

### 📂 Örnekler

| Dosya Türü       | Magic Bytes (hex)             | ASCII Karşılığı | Açıklama                                 |
|------------------|-------------------------------|------------------|-------------------------------------------|
| PDF              | `25 50 44 46`                 | `%PDF`           | Her PDF bu imzayla başlar                 |
| PNG              | `89 50 4E 47 0D 0A 1A 0A`     | —                | Sabit PNG imzası                          |
| JPEG             | `FF D8 FF E0`                 | —                | JPEG başlatıcı                            |
| ZIP              | `50 4B 03 04`                 | `PK..`           | ZIP / DOCX / APK için kullanılır          |
| ELF (Linux)      | `7F 45 4C 46`                 | `.ELF`           | Linux çalıştırılabilir dosyası            |

> 💡 Amaç: Dosya formatını, MIME türünü veya çalışma ortamını belirlemek.  
> OS, tarayıcı veya program, “bu dosyayı nasıl açayım?” kararını buradan verir.

---

### 🧩 2️⃣ BOM — “Byte Order Mark”

**BOM (Byte Order Mark)**, bir metin dosyasının hangi karakter kodlamasıyla yazıldığını belirtmek için kullanılan özel bayt dizisidir.  
Dosyanın başında yer alır ve özellikle Unicode formatlarında önemlidir.

### 🔍 Ne işe yarar?

- Dosya türünü değil, **encoding** bilgisini verir.
- Özellikle UTF-16 ve UTF-32 gibi çok baytlı kodlamalarda **endianness** (bayt sırası) bilgisini taşır.
- Yazılımın metni doğru şekilde çözümleyebilmesi için gereklidir.

### 📘 Örnekler

| Encoding       | BOM (hex)           | Açıklama                                |
|----------------|---------------------|------------------------------------------|
| UTF-8          | `EF BB BF`          | Opsiyonel, genelde metin editörleri ekler|
| UTF-16 (LE)    | `FF FE`             | Little endian (küçükten büyüğe byte sırası) |
| UTF-16 (BE)    | `FE FF`             | Big endian                               |
| UTF-32 (LE)    | `FF FE 00 00`       | —                                        |
| UTF-32 (BE)    | `00 00 FE FF`       | —                                        |

> 💡 Amaç: Yazılımın metin dosyasını doğru şekilde decode edebilmesi.  
> Yani karakterlerin doğru okunması (örneğin Türkçe, Japonca, emoji gibi).

---

### ⚙️ 3️⃣ Magic Bytes vs BOM — Farkı Kısaca

| Özellik           | Magic Bytes                     | BOM                                      |
|-------------------|----------------------------------|-------------------------------------------|
| Ne işe yarar?     | Dosya türünü belirtir           | Encoding’i belirtir                       |
| Hangi dosyalarda? | Herhangi bir binary format      | Unicode metin dosyaları                   |
| Kim kullanır?     | OS, tarayıcı, yazılım           | Kodlayıcı / decoder                       |
| Örnek             | `%PDF` → PDF dosyası            | `EF BB BF` → UTF-8 dosyası                |
| PEP bağlantısı    | Yok                             | 📜 [PEP 263](https://peps.python.org/pep-0263/) — Source code encoding declarations |

---

### 🧠 4️⃣ PEP 263 ile İlişkisi

**PEP 263**, Python kaynak dosyalarında encoding bildirimi yapılmasını sağlayan bir standarttır.  
Ancak BOM ile değil — doğrudan kaynak kodun içine yazılan bir yorum satırıyla çalışır.

### 🔍 Örnek

```python
# -*- coding: utf-8 -*-
```
🧠 Bu satır **Python’a** “bu dosya **UTF-8** ile yazıldı” bilgisini verir. Eğer dosyada **BOM** varsa (örneğin UTF-8-BOM), Python 3 bunu otomatik olarak tanır ve işler. Yani BOM olmasa bile **PEP 263** satırı yeterlidir. **BOM** varsa, **PEP 263** olmasa da sorun çıkmaz.

> 💡 **BOM** -> dosyanın başında fiziksel **bayt dizisi PEP 263** → kaynak kodun içinde yazılı mantıksal bildirim

---
