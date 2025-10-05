# 🧩 1. AŞAMA — KAYNAK EDİNİMİ & ÖN İŞLEMLER

Python yorumlayıcısı **(Interpreter-CPython)** bir `.py` dosyasını çalıştırmaya başladığında,  
ilk yaptığı şey aslında **dosyayı açmak** değil, **onu anlamlandırmaya hazırlamak**<sup>[1]</sup> olur.

Bu aşamanın amacı; diskteki **ham baytları<sup>[2]</sup> (bytes)** alıp,  
Python’un **lexer<sup>[3]</sup>**’ının (ya da tokenizer’ının) işleyebileceği **standartlaştırılmış Unicode<sup>[4]</sup> metin** haline getirmektir.

Henüz “token”, “AST”, “bytecode” yoktur.  
Sadece **ham veriler (baytlar)** ve onları Python’un anlayabileceği biçime çevirme süreci vardır.

---

**[1]** Ham baytları doğru decoding’le Unicode’a çevirip BOM’u temizleyerek, satır sonlarını `\n`’e normalize edip lexer’ın kullanacağı satır-bazlı akışı oluşturma.  

**[2]** **Ham bayt**, bir dosyada karakterlerin encoding’e göre temsil edildiği 8-bitlik veri birimleridir. Python yorumlayıcısı bu baytları doğrudan anlamaz; önce encoding bilgisiyle decode edip Unicode karakterlere dönüştürmesi gerekir.

**[3]** **Lexer**, kaynak kodu bayt düzeyinden Unicode karakter dizisine (string) dönüştürülmüş metin olarak alır ve yalnızca bu karakterlerle çalışarak dilin sözdizimsel yapılarını tanımlar.

**[4]** **Unicode**, dünya üzerindeki tüm yazı sistemlerindeki karakterleri temsil etmek için geliştirilmiş evrensel bir standarttır.
Her karaktere benzersiz bir kod noktası (örneğin U+0061 → 'a') atar

>✅ **Encoding**, Unicode karakterleri bayt dizilerine dönüştüren protokoldür; dosya yazımı ve ağ iletişimi için gereklidir.bu karakterlerin bayt dizisi olarak nasıl saklandığını belirtir. 

>✅ **Decode**, bayt dizilerini belirli bir encoding'e göre Unicode karakterlere çevirerek metin haline getirir.**Encoding bilinmeden, baytlar Unicode’a çevrilemez → lexer çalışamaz.**

---

## 🎯 Amaç

Python’un diskteki dosyayı alıp, **platformdan bağımsız, temiz, normalize edilmiş bir kaynak metin** oluşturmasıdır.

Lexer **karakterlerle** çalışır, **baytlarla** değil.
O yüzden Python’un bu aşamadaki temel hedefi, **ham bayt akışını karakter tabanlı bir akışa çevirmek**tir.

Yani:

- Kodlama (encoding) bilgisini bulmak
- Gizli baytları (örneğin BOM) temizlemek
- Satır sonlarını normalize etmek
- Satır bazlı bir okuma mekanizması (`readline` akışı) hazırlamak

Bu aşama tamamlanmadan lexer tek bir token bile üretemez.

---

## 🧠 Python Bu İşi Nerede Yapar?

Bu süreç CPython’ın içinde, çoğunlukla şu C kaynak dosyalarında gerçekleşir:

- 🧩 **`Python/tokenizer.c`** → Asıl “tokenizer” motoru burada başlar, ama önce kaynak metin hazırlanır.
- 🧩 **`Parser/tokenizer_pgen.c`** → Eski parser için, ancak aynı mantıkta çalışır.
- 🧩 **`Python/pythonrun.c`** → Python’un çalıştırma döngüsünü (`run loop`) yönetir, dosyayı açar, akışı oluşturur.

Bu işlemler doğrudan şu fonksiyonlar üzerinden çağrılır:

- `PyParser_ASTFromFileObject()`
- `PyRun_InteractiveOneObject()`

---

## 🪄 1.1 — Dosyanın Okunması (Bayt Düzeyinde)

İlk aşama tamamen **dosya sistemi** düzeyindedir.
Python kaynak dosyayı **binary modda (`rb`)** açar — çünkü dosya sisteminde her şey **bayt** olarak saklanır.

```python
örnek_dosya = open("main.py", "rb")
veri = örnek_dosya.read()
print(veri[:20])  # b'# -*- coding: utf-8 -*-'
```

### C düzeyinde bu işlemi başlatan fonksiyonlar:

- `PyParser_ASTFromFileObject()` → Dosyayı çalıştırmak için
- `PyRun_InteractiveOneObject()` → REPL ortamında satır satır okumak için

---

## 🔍 1.2 — Kodlama (Encoding) Tespiti — PEP 263

Python, kaynağın hangi karakter setiyle yazıldığını anlamalıdır.
Her `.py` dosyası aslında Unicode karakterlerden oluşan bir metin olmalıdır.

### PEP 263’e göre:

- Dosyanın ilk iki satırı geçici olarak **ASCII<sup>[1]</sup>** kabul edilir
- Bu satırlarda encoding bildirimi aranır:

- **Konum**: Encoding bildirimi **yalnızca ilk iki satırda** geçerlidir.
- **Biçim**: `coding[:=]\s*([-\w.]+)`
- **Hatalı cookie örneği**:
```python
# coding utf8   # iki nokta/eşittir yok → Geçersiz

# -*- coding: utf-8 -*-
# coding: latin-1
```
**[1]** **ASCII**, bilgisayarların metin karakterlerini sayısal baytlarla temsil etmesini sağlayan 7 bitlik evrensel bir karakter kodlama sistemidir.encoding bildirimi ASCII karakterlerle yazıldığında, yorumlayıcı onu encoding bilgisi olmadan bile okuyabilir

> 💡 Not: **Kabul edilmesi** demek, eğer bu iki satırda **ASCII** olmayan bir metin varsa hata ver değil sadece bu satırları **ASCII** formatında okur.


**Uyumsuzluk Örneği:**  
Dosya başlığı: `# coding: latin-1`  
İçerik: UTF-8 Türkçe karakterler (`ş`, `ğ`)  
→ Decode sırasında `UnicodeDecodeError` veya sonrasında `SyntaxError` görülebilir.  
**Çözüm:** Doğru encoding’i bildir veya kaynak dosyayı uygun encoding ile kaydet.

## ⚡ 1.3 — BOM (Byte Order Mark) Kontrolü

Bazı Unicode dosyalarının başında özel bir işaret bulunur:

Bu işaret **BOM (Byte Order Mark)** olarak adlandırılır. Kodun bir parçası değildir, ama dosyanın Unicode olduğunu belirtir.

### Eğer BOM temizlenmezse:

```python
'\ufeffprint("selam")'
```
Lexer bunu geçersiz karakter olarak algılar:
```python
SyntaxError: invalid character in identifier
```

## ✅ BOM Tablosu (Byte Order Mark)

Unicode dosyalarının başında yer alabilen BOM (Byte Order Mark) imzaları, dosyanın encoding türünü ve byte sırasını belirtir. Python, bu imzaları tanır ve lexer başlamadan önce temizler.

| 🔤 Encoding     | 🔢 BOM (Hex)        | 📌 Açıklama                          |
|----------------|---------------------|--------------------------------------|
| **UTF-8**      | `EF BB BF`          | Opsiyonel; varsa atılır              |
| **UTF-16 LE**  | `FF FE`             | Little-endian sıralama belirtir     |
| **UTF-16 BE**  | `FE FF`             | Big-endian sıralama belirtir        |
| **UTF-32 LE**  | `FF FE 00 00`       | Little-endian sıralama belirtir     |
| **UTF-32 BE**  | `00 00 FE FF`       | Big-endian sıralama belirtir        |

> 💡 Not: Python, BOM'u gördüğünde encoding'i otomatik olarak belirler ve bu baytları lexer'a geçmeden önce temizler. Özellikle UTF-8 BOM (`EF BB BF`) yaygın olarak metin editörleri tarafından eklenir, ancak Python tarafından kodun parçası olarak kabul edilmez.


## 🔁 1.4 — Satır Sonlarının Normalize Edilmesi

Python’un lexer’ı (tokenizer) kaynak kodu işlerken satır bazında çalışır — çünkü dilin yapısında **girinti (indentation)<sup>[1]</sup>**, **blok sınırları** ve **ifade sonları** hep “satır sonu”na bağlıdır. Ancak farklı işletim sistemleri satır sonlarını farklı karakterlerle belirtir:

- **Windows:** `\r\n` (Carriage Return + Line Feed)  
- **Unix / Linux / macOS:** `\n` (Line Feed)  
- **Klasik Mac:** `\r` (Carriage Return)

Bu fark, eğer normalize edilmezse lexer’ın “satır bitti mi?” sorusuna tutarsız cevaplar vermesine yol açabilir.  
Örneğin `\r\n` içeren bir kaynakta Python `\r` karakterini görünmez, ama token sınırı zannedip hatalı bir `NEWLINE` üretebilir.

Bu yüzden CPython, **kaynak metin lexer’a ulaşmadan önce** tüm satır sonlarını **tek biçime (`\n`)** dönüştürür.  
Bu işlem “satır sonu normalizasyonu” olarak adlandırılır.

Bu sayede:
- `INDENT`, `DEDENT` ve `NEWLINE` token’ları her platformda aynı şekilde tanımlanır,  
- Kod taşınabilir hale gelir (Windows’ta yazılıp Linux’ta da çalışır),  
- Parser ve AST üretimi platformdan bağımsız olur.

Bu adım, **dilin girinti tabanlı doğası** nedeniyle kritik önemdedir;  
Python’un sözdizimsel bütünlüğü, bu normalize edilmiş satır sınırlarına dayanır.


de’a dönüştürülmesi, Python’un kaynak kodu anlamlandırma sürecinin ilk ve en kritik adımıdır. Bu dönüşüm sayesinde lexer, dilin gramerine uygun şekilde token üretmeye başlayabilir. Encoding tespiti, BOM temizliği ve satır normalizasyonu gibi alt adımlar bu sürecin ayrılmaz parçalarıdır. Python’un Unicode temelli mimarisi bu adımı zorunlu kılar.
>✅ **Girinti:** Python’da süslü parantezler yerine, kod bloklarını tanımlamak için kullanılan boşluk veya tab karakterlerinden oluşan yapısal bir işarettir
```python
# Girinti;
def greek():
    pass # burda 4 boşluk var
```

---
>✅ **Blok Sınırı:** Girinti seviyesinin değişmesiyle belirlenen yapısal geçiş noktasıdır
```python
# Blok Sınırları
for _ in range(10): # iki nokta for bloğunun başladığını belirtir
    pass
```
---
>✅ **İfade Sonu:** Her Python ifadesi satır sonuyla (\n) veya noktalı virgülle (;) sonlanır
```python
# İfade Sonları
name = "demir" # ifade sonu
age = 20 # ifade sonu
id = 12 ; city = istanbul # birden fazla ifadeyi : ile ayırdık
```
---
>💡 Python'da süslü parantezler yerine girintiler blok yapısını tanımlar; bu yüzden **lexer**, satır sonlarını ve boşluk karakterlerini yapısal ayrım için semantik olarak işler. Kaynak edinimi sırasında satır sonlarının normalize edilmemesi, **lexer’ın** girinti seviyelerini yanlış yorumlamasına ve `IndentationError` gibi yapısal hatalara yol açabilir.


### ⚙️ CPython Düzeyinde Satır Sonlarının Normalize Edilmesi

Satır sonlarının normalize edilmesi işlemi, Python yorumlayıcısının (CPython) **tokenizer** modülünde, yani `Python/tokenizer.c` dosyasında gerçekleşir.  
Bu işlem **lexer başlamadan hemen önce**, kaynak metin “okuma akışı” (readline stream) haline getirilirken yapılır.


