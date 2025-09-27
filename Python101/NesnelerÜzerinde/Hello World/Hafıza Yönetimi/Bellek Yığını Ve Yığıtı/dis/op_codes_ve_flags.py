import dis
import inspect

# 🧩 OPCODE vs COMPILER FLAG — NEDİR, FARKLARI NELERDİR?
# ------------------------------------------------------------

# 🔹 OPCODE (Operation Code):
# Python kodu derlendiğinde, her işlem bir opcode ile temsil edilir.
# Örneğin: LOAD_FAST, STORE_NAME, RETURN_VALUE gibi komutlar.
# Bunlar Python yorumlayıcısının çalıştırdığı **bytecode talimatlarıdır**.

# 🧩 SORU: Neden opcode’lar doğrudan sayı olarak değil de Instruction nesnesi olarak temsil ediliyor?

# 🔹 CEVAP:
# Çünkü bir opcode’un kendisi tek başına yeterli bilgi taşımaz.
# Python yorumlayıcısı için önemli olan sadece "hangi komut" olduğu değil,
# aynı zamanda:
# - hangi argümanla çalıştığı
# - hangi satırda yer aldığı
# - hangi isim/sabit/değişkenle ilişkili olduğu
# - atlama hedefi olup olmadığı
# gibi bilgiler de gereklidir.

# 🔍 Bu yüzden dis modülü, her bytecode komutunu bir Instruction nesnesi olarak temsil eder.
# Instruction nesnesi, opcode’un etrafındaki tüm bağlamsal bilgileri içerir.


# 🔹 COMPILER FLAG:
# Python derleyicisi, bir fonksiyonun yapısal özelliklerini bayraklarla işaretler.
# Örneğin: fonksiyon bir generator mı, coroutine mi, nested mı?
# Bu bayraklar `func.__code__.co_flags` alanında **bitmask** olarak saklanır.

# 🔍 OPCODE’lar → ne yapılıyor?
# 🔍 FLAG’lar → nasıl bir yapı?

# ------------------------------------------------------------
# ✅ OPCODE Örneği:
# dis.opmap['LOAD_FAST'] → 124
# dis.opname[124] → 'LOAD_FAST'
# Bu, yerel bir değişkenin stack’e yüklenmesini temsil eder.

# ✅ FLAG Örneği:
# CO_GENERATOR = 0x20 → 32
# Bu, fonksiyonun bir generator olduğunu belirtir.

# ------------------------------------------------------------
# ⚠️ FARKLAR:
# - OPCODE’lar bytecode içinde satır satır görünür.
# - FLAG’lar ise fonksiyonun meta verisinde saklanır.
# - OPCODE’lar değişebilir (sürümle birlikte), FLAG’lar sabittir.

# ------------------------------------------------------------
# 🧪 ÖRNEK: Generator fonksiyonun opcode ve flag analizi

def gen():
    yield 1

# Bytecode analizi
print("\n🔍 Bytecode Komutları:")
for instr in dis.Bytecode(gen):
    print(f"{instr.opcode:<3} {instr.opname:<20} {instr.argrepr}")

# Flag analizi
print("\n🔍 Compiler Flag Analizi:")
flags = gen.__code__.co_flags
for flag_value, flag_name in dis.COMPILER_FLAG_NAMES.items():
    aktif = "✅" if flags & flag_value else "❌"
    print(f"{flag_name:<25} {aktif} ({flag_value})")

# inspect ile doğrulama
print("\n🔍 inspect.isgeneratorfunction:", inspect.isgeneratorfunction(gen))

# ------------------------------------------------------------
# 🎯 ÖZET:
# - OPCODE’lar: Python yorumlayıcısının çalıştırdığı talimatlardır.
# - FLAG’lar: Python derleyicisinin fonksiyon hakkında tuttuğu meta bilgilerdir.
# - OPCODE’lar değişebilir, FLAG’lar sabittir.
# - FLAG’lar, fonksiyonun davranışsal yapısını tanımlar (örneğin generator mı?)
# - OPCODE’lar, fonksiyonun nasıl çalıştığını gösterir (örneğin yield kullanımı)

# ✅ OPCODE → işlem düzeyi
# ✅ FLAG   → yapı düzeyi

# Bu ikisi aynı şey değildir ama birbirini tamamlar.
# FLAG, opcode’un varlığını işaret edebilir (örneğin YIELD_VALUE varsa → CO_GENERATOR aktif olur).
