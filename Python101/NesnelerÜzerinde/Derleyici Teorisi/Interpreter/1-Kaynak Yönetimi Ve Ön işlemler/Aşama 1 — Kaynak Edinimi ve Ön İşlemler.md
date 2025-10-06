# 🧩 1. AŞAMA — KAYNAK EDİNİMİ & ÖN İŞLEMLER


---
#### 🧑‍🎓 Yeni başlayan (CS öğrencisi)
#### 🕒 **Tahmini Süre*: 90dk*

---

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

### 📜 Ne Zaman Oluyor?

🔍 Bunu anlamak için veri akışını şöyle düşünebilirsin:
```scss
Diskteki dosya  ──>  open("file.py", "rb")  ──>  FILE*  ──>  
_PyTokenizer_FromFile()  ──>  tok_nextc()  ──>  Lexer (tok_get)
```
---

## 📜 1.5 — Satır Bazlı Okuma Akışı (Readline Stream) Hazırlanması

Python’un **lexer’ı (tokenizer)**, kaynak kodu bir bütün olarak değil, **satır satır işler**. Bunun temel nedeni, Python’un sözdiziminin (syntax) doğrudan satır yapısına dayanmasıdır:

- Her satır bir `NEWLINE` token’ı ile sonlanır.
- Girintiler `INDENT` / `DEDENT` token’ları ile temsil edilir ve bu girintiler satır başlarındaki boşluklarla belirlenir.
- REPL gibi etkileşimli ortamlarda kullanıcı her satır girdiğinde ayrı bir analiz yapılır.

Dolayısıyla, Python’un lexer’ı **satır temelli bir akış (stream)** olmadan çalışamaz. Bu akış, kaynak kodun satır satır okunmasını ve her satırın bağımsız olarak token’lara ayrılmasını sağlar. Satır bazlı okuma, hem girinti mantığını hem de etkileşimli analizleri mümkün kılar.

---

## 🎯 Amaç

Bu aşamanın hedefi:

> “Normalize edilmiş Unicode metni, satır satır okunabilir bir veri kaynağına dönüştürmek.”

Python, kaynak kodu bir kerede hafızaya yüklemek yerine, **her seferinde bir satır okuyan bir arabirim (readline)** oluşturur. Bu yaklaşım, Python’un satır temelli sözdizimiyle doğrudan örtüşür.

---

### 🧭 Lexer Bu Akışla Ne Yapar?

- Her seferinde `readline()` çağırarak yeni bir satır alır.
- Satırdaki karakterleri tek tek sınıflandırır.
- Satır sonuna ulaştığında, o satıra ait token dizisini tamamlar.

Bu yapı sayesinde lexer, hem girinti mantığını hem de etkileşimli ortamları (REPL gibi) doğru şekilde işleyebilir.

---

### ⚙️ CPython Düzeyinde Ne Olur?

Bu mekanizma, C düzeyinde `tokenizer.c` dosyasında tanımlanmış `_PyTokenizer_FromFile()` fonksiyonuyla başlatılır.

- Bu fonksiyon, lexer’a **“nasıl satır okunacağını”** söyleyen arabirimi sağlar.
- Kaynak dosya, satır satır okunabilir hale getirilir.
- Tokenizer, bu arabirim üzerinden satırları alarak analiz eder.

Bu yapı, Python’un REPL davranışını, girinti mantığını ve satır sonu tokenizasyonunu mümkün kılan temel mimari bileşendir.

---

## 🧱 Mimari Yapı

Python lexer’ının satır bazlı çalışabilmesi için, her kaynak akışının içinde bir **“okuma fonksiyonu”** bulunur. Bu mimari, lexer’a satır satır veri sağlayan soyut bir arabirim oluşturur.

### 🔌 C Düzeyinde Akış Fonksiyonları

- `_PyTokenizer_FromFile()` → `fp_readline()`  
- `_PyTokenizer_FromString()` → `string_readline()`

Bu fonksiyonlar, **pointer olarak `tok_nextc()` fonksiyonuna verilir**.  
`tok_nextc()` her çağrıldığında:

- Eğer mevcut satır bitmişse,
- `readline()` fonksiyonu ile yeni bir satır alınır.


---
### 📦 Bellek Dostu ve Etkileşimli Tasarım

Bu yapı sayesinde lexer:

- Dosyayı **asla tamamını okumaz**.
- Yalnızca ihtiyaç oldukça yeni satır getirir.
- REPL gibi etkileşimli ortamlarda **her satır ayrı ayrı işlenebilir**.

Bu mimari, hem bellek verimliliği sağlar hem de REPL gibi satır bazlı analiz gerektiren ortamları destekler.

---

### 🔁 Python Düzeyinde Karşılığı

Aynı mantık Python tarafında da gözlemlenebilir:

```python
import io

kaynak = "x = 10\nprint(x)\n"
akış = io.StringIO(kaynak)

print(akış.readline())  # 'x = 10\n'
print(akış.readline())  # 'print(x)\n'
```

>✅  Bu basit örnek, lexer’ın kullandığı “stream abstraction”ın Python’daki karşılığıdır.
 Her readline() çağrısı bir satır döndürür,
 ve lexer bu satırdaki karakterleri tek tek analiz eder.

---

## 🧩 Neden Satır Bazlı?

Python, **girinti tabanlı (indentation-sensitive)** bir dildir.  
Yani:

- Kod blokları `{}` yerine **girintilerle** belirlenir.
- Bu da lexer’ın **satır sınırlarını mutlak biçimde bilmesini** zorunlu kılar.
- `readline()` akışı, Python dilinin sözdizimsel doğasıyla **birebir uyumludur**.
- Her satır, dilin **yapısal birimi** haline gelir.

Bu mimari, hem dilin semantiği hem de yorumlayıcının çalışma şekli açısından kritik önemdedir.

### 💡 Avantajlar

|🧩 Özellik                     | 📌 Açıklama                                                                     |
|-----------------------------|---------------------------------------------------------------------------------|
| 🧠 Bellek dostu             | Kaynağın tamamını değil, **satır satır işler**.                                 |
| 📍 Hata konumlama kolaylığı | Satır numaraları (`lineno`) **akıştan otomatik hesaplanır**.                    |
| 💬 REPL desteği             | Kullanıcıdan gelen **her satır anında lexer’a verilebilir**.                    |
| 🌐 Platform bağımsızlığı    | Satır sonları normalize edildiği için (`\n`), **tüm sistemlerde aynı** çalışır. |

---
### ⚙️ Nasıl Çalışır?

Python l**exer’ı**, kaynak kodu Unicode karakterler hâline getirdikten sonra **satır bazlı bir okuma akışı** üzerinden işlemeye başlar. Bu akış, hem C düzeyinde hem de Python düzeyinde benzer mantıkla işler.

### 🔹 1. Akışın Oluşturulması

- Kaynak kod artık **normalize edilmiş Unicode metin** hâlindedir.
- Bu metin, `readline()` benzeri bir **akış arabirimi** ile lexer’a sunulur.

### 🛠️ C Düzeyinde Akış Mantığı

| Fonksiyon               | Görev                                                                 |
|------------------------|-----------------------------------------------------------------------|
| `fp_readline()`        | Her çağrıda bir satır okur.                                           |
| `tok_state.buf`        | Okunan satır bu buffer’a yerleştirilir.                               |
| `tok_nextc()`          | Buffer’dan karakter karakter okuma işlemini gerçekleştirir.           |

Bu yapı sayesinde lexer, **satır sonlarını**, **girinti seviyelerini** ve **token sınırlarını** doğru şekilde analiz edebilir.

### 🐍 Python Düzeyinde Karşılığı

```python
import io

kaynak = "x = 10\nprint(x)\n"
akış = io.StringIO(kaynak)

print(akış.readline())  # 'x = 10\n'
print(akış.readline())  # 'print(x)\n'
```

---

### 🔹 2. Satır Sınırlarının Belirlenmesi

Python lexer’ı, her satır sonunda özel token’lar üretir. Bu token’lar, dilin yapısal mantığını tanımlamak için kritik önemdedir:

| Token     | Açıklama                                                                 |
|-----------|--------------------------------------------------------------------------|
| `NEWLINE` | Mantıksal bir satırın sonunu belirtir.                                   |
| `NL`      | Fiziksel satır sonu (örneğin parantez içinde kesilen satırlar).          |
| `INDENT`  | Yeni girinti seviyesi (örneğin `def`, `if`, `for` blokları).             |
| `DEDENT`  | Girinti azalması (blok sonu).                                            |

Bu token’lar **Python’a özgüdür** — C, Java veya JavaScript gibi dillerde bu tür yapısal girinti token’ları bulunmaz.

---

### 🔹 3. Girintilerin (Indentation) Ölçülmesi

Lexer, her satırın başındaki boşluk veya tab karakterlerini sayarak girinti mantığını uygular:

- Yeni satırın girinti seviyesi **öncekinden büyükse** → `INDENT`
- **Küçükse** → bir veya daha fazla `DEDENT`
- **Aynıysa** → hiçbir şey üretmez

#### ⚙️ C Düzeyinde Girinti Analizi

Bu işlem `tok_get()` fonksiyonu içinde gerçekleşir. Her satırın başında lexer:

- `tok->line_start` konumundan itibaren boşlukları okur.
- Girinti yığınını (`indent_stack`) günceller.
- Uygun sayıda `INDENT` veya `DEDENT` token’ı üretir.

Bu yapı, Python’un girinti tabanlı sözdizimini doğru şekilde analiz edebilmesi için zorunludur.

---

### 🔹 4. Bu Yapı Neden `readline()`’a Bağlı?

Çünkü lexer, **satırları tek tek değerlendirmelidir**.  
Eğer tüm dosya bir defada okunsaydı:

- Satır sonlarını, girintileri ve blok sınırlarını **yönetmek imkânsız olurdu**.
- Özellikle REPL (etkileşimli mod) **doğru çalışmazdı**.

#### ✅ `readline()` Akışının Sağladıkları

- Satır bazlı işleme
- Realtime (anlık) çalışma
- Dosya ve REPL için **ortak mantık**

Bu mimari, Python’un hem dosya tabanlı hem de etkileşimli yorumlama yeteneklerini mümkün kılar.

---

### 🧩 CPython İçinde Neler Olur?

C düzeyinde bu işlemler sırasıyla şu şekilde gerçekleşir:

| 🛠️ Fonksiyon                | 🎯 Görev                                                               |
|---------------------------|----------------------------------------------------------------------|
| `_PyTokenizer_FromFile()` | `tok_state` yapısını oluşturur, `readline` fonksiyonunu referanslar. |
| `fp_readline()`           | C’nin `fgets()` fonksiyonunu kullanarak satırı okur.                 |
| `tok_nextc()`             | Buffer’dan karakter karakter okur.                                   |
| `tok_get()`               | Satır başındaki girinti miktarını ölçer, `INDENT` / `DEDENT` üretir. |

Bu yapı, lexer’ın satır bazlı ve girinti duyarlı çalışmasını sağlayan temel mimari bileşenlerdir.

---

### 💡 Neden Bu Kadar Kritik?

Çünkü Python’da **girinti yalnızca görsel bir biçim değildir** —  
dil gramerinin **semantik parçasıdır**.

Örneğin:

```python
def örnek():
    if True:
        print("merhaba")
    print("bitti")
```
#### Lexer bunu şu sırayla tokenize eder:
```scss
NAME('def'), NAME('örnek'), LPAR, RPAR, COLON, NEWLINE,
INDENT,
NAME('if'), NAME('True'), COLON, NEWLINE,
INDENT,
NAME('print'), ... , NEWLINE,
DEDENT,
NAME('print'), ... , NEWLINE,
DEDENT,
ENDMARKER
```
> ✅ **`INDENT/DEDENT`**→ kod bloklarını tanımlar

> ✅ **`NEWLINE`** → ifadeleri sınırlar

> 💡 Bu sistem olmadan Python’un sözdizimi `def`, `if`, `while` blokları mümkün olmazdı.
**Kısacası: readline akışı, Python dilinin kalp atışıdır.**