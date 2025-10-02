# 🧩 opcode MODÜLÜ — Attribute Tanımları (Detaylı)
# =============================================================================
# Bu bölümde opcode modülündeki temel attribute’lar daha açıklayıcı şekilde anlatılıyor.
# Amaç: sadece “ne işe yarıyor?” değil, “neden var?” ve “nerede işine yarar?”ı netleştirmek.

# -----------------------------------------------------------------------------
# 1) opcode.opmap
# 📌 Sözdizimi:
#     opcode.opmap["OPCODE_ADI"]
#
# 📌 Tanım:
#     Opcode adlarını (ör: "LOAD_CONST") opcode numaralarına (ör: 100) eşleyen sözlüktür.
#     Yani string → int çevirisi yapar.
#
# 📌 Amacı:
#     İnsanların kullandığı opcode adını, sanal makinenin çalıştırdığı sayısal kodla eşleştirmek.
#
# 📌 Kullanım Alanları:
#     - Bytecode üreten araçlarda → "LOAD_CONST" diyerek doğru numarayı almak
#     - Eğitim/analiz → "LOAD_CONST kaç numaraydı?" sorusuna hızlı cevap
#     - dis modülü de bunu kullanır → isimleri numaralara çevirip çözümleme yapar

import opcode
print(opcode.opmap["LOAD_CONST"])  # 100

# -----------------------------------------------------------------------------
# 2) opcode.opname
# 📌 Sözdizimi:
#     opcode.opname[numara]
#
# 📌 Tanım:
#     Opcode numaralarını opcode adlarına çeviren listedir (int → string).
#     Yani opmap’in tersidir.
#
# 📌 Amacı:
#     Sayısal bytecode değerlerini insan-dostu isimlere çevirmek.
#
# 📌 Kullanım Alanları:
#     - Bytecode analizinde → co_code içindeki 100 → 'LOAD_CONST' diye gösterilir
#     - dis modülü çıktılarında talimat isimlerini yazmak
#     - Farklı opcode numaralarının hangi komuta denk geldiğini görmek

print(opcode.opname[100])  # 'LOAD_CONST'

# -----------------------------------------------------------------------------
# 4) opcode.hasconst
# 📌 Sözdizimi:
#     opcode.hasconst
#
# 📌 Tanım:
#     Sabit (constant) havuzuyla (co_consts) etkileşimde bulunan opcode’ların listesidir.
#     Örn: LOAD_CONST → sabitlerden birini yükler.
#
# 📌 Amacı:
#     Hangi bytecode talimatlarının doğrudan sabitlerle uğraştığını ayırmak.
#
# 📌 Kullanım Alanları:
#     - "Bu fonksiyon sabit değer kullanıyor mu?" kontrolü
#     - Eğitim → sabitlerin bytecode’daki rolünü görmek
#     - Araç geliştirme → sabit bağımlılıklarını çıkarma

print([opcode.opname[i] for i in opcode.hasconst])  # ['LOAD_CONST', ...]

# -----------------------------------------------------------------------------
# 5) opcode.hasname
# 📌 Sözdizimi:
#     opcode.hasname
#
# 📌 Tanım:
#     İsim tablosu (globals/locals) üzerinden işlem yapan opcode’ların listesidir.
#     Örn: LOAD_NAME, STORE_NAME.
#
# 📌 Amacı:
#     Kodun hangi yerlerde isimlere (değişken/fonksiyon/ad) başvurduğunu bulmak.
#
# 📌 Kullanım Alanları:
#     - Global/Local değişken erişimini analiz etmek
#     - "Bu bytecode hangi isimlere ihtiyaç duyuyor?" sorusunu cevaplamak
#     - Kod bağımlılık analizleri

print([opcode.opname[i] for i in opcode.hasname][:5])

# -----------------------------------------------------------------------------
# 6) opcode.haslocal
# 📌 Sözdizimi:
#     opcode.haslocal
#
# 📌 Tanım:
#     Yerel değişkenlerle (local variables) ilgili işlem yapan opcode’ların listesidir.
#     Örn: LOAD_FAST, STORE_FAST.
#
# 📌 Amacı:
#     Fonksiyon içindeki lokallerle ilgili işlemleri ayırt etmek.
#
# 📌 Kullanım Alanları:
#     - Performans analizi → LOAD_FAST (lokal) vs LOAD_GLOBAL (global) farkını görmek
#     - Eğitim → Python’un local erişimi nasıl optimize ettiğini anlamak
#     - Bytecode optimizasyonu

print([opcode.opname[i] for i in opcode.haslocal])

# -----------------------------------------------------------------------------
# 7) opcode.hasjrel
# 📌 Sözdizimi:
#     opcode.hasjrel
#
# 📌 Tanım:
#     Relatif atlama yapan opcode’ların listesi (hedef = şimdiki offset + arg).
#     Örn: JUMP_FORWARD.
#
# 📌 Amacı:
#     Kontrol akışında döngü ve koşullu atlamaları bulmak.
#
# 📌 Kullanım Alanları:
#     - "Bu kodun kontrol akışı nasıl?" sorusunu yanıtlamak
#     - Eğitim → döngülerin ve if bloklarının bytecode’da nasıl temsil edildiğini göstermek

print([opcode.opname[i] for i in opcode.hasjrel])

# -----------------------------------------------------------------------------
# 8) opcode.hasjabs
# 📌 Sözdizimi:
#     opcode.hasjabs
#
# 📌 Tanım:
#     Mutlak atlama yapan opcode’ların listesi (hedef = bytecode’un belirli offseti).
#     Örn: JUMP_ABSOLUTE.
#
# 📌 Amacı:
#     Kontrol akışında sabit adresli sıçramaları bulmak.
#
# 📌 Kullanım Alanları:
#     - "Bu kod tam olarak nereye zıplıyor?"u anlamak
#     - Eğitim → relatif ve mutlak sıçramaların farkını göstermek
#     - Bytecode akışını görselleştirme

print([opcode.opname[i] for i in opcode.hasjabs])
