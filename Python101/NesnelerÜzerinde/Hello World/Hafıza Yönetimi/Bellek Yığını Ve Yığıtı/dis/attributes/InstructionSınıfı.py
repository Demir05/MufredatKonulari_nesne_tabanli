import dis


# 🧩 Instruction Sınıfı Nedir?
# ------------------------------------------------------------
# dis.Instruction, Python’un dis modülünde yer alan bir veri yapısıdır.
# Bytecode analizinde her opcode, bir Instruction nesnesi olarak temsil edilir.
# Bu nesne, sadece komutun ne olduğunu değil, onunla ilgili tüm bağlamsal bilgileri içerir.


# ------------------------------------------------------------
# 🧩 dis.Instruction Nesnesi Özellikleri
# instr.opname      → Komutun adı (örneğin 'LOAD_FAST')
# instr.opcode      → Sayısal opcode değeri (örneğin 124)
# instr.arg         → Argüman indeksi (örneğin 0)
# instr.argval      → Argümanın gerçek değeri (örneğin 'x')
# instr.argrepr     → Argümanın yazdırılabilir hali (örneğin '(x)')
# instr.offset      → Bytecode içindeki konumu
# instr.starts_line → Kaynak kod satırı (None değilse yeni satır başı)
# instr.is_jump_target → Bu komut bir atlama hedefi mi?


# ------------------------------------------------------------
# 🧪 Örnek Fonksiyon
def örnek(x):
    return x + 1


# ------------------------------------------------------------
# 🔍 Instruction Nesneleri Üzerinde Dolaşmak
for instr in dis.Bytecode(örnek):
    # Her instr bir Instruction nesnesidir.
    print(f"""
    🧩 Instruction Nesnesi:
    ----------------------------------------
    instr.opname       → {instr.opname}       # Komutun adı (örneğin 'LOAD_FAST')
    instr.opcode       → {instr.opcode}       # Sayısal opcode değeri (örneğin 124)
    instr.arg          → {instr.arg}          # Argüman indeksi (örneğin 0)
    instr.argval       → {instr.argval}       # Argümanın gerçek değeri (örneğin 'x')
    instr.argrepr      → {instr.argrepr}      # Argümanın yazdırılabilir hali (örneğin '(x)')
    instr.offset        → {instr.offset}       # Bytecode içindeki konumu (örneğin 0, 2, 4...)
    instr.starts_line   → {instr.starts_line}  # Kaynak kod satırı (örneğin 2)
    instr.is_jump_target→ {instr.is_jump_target} # Bu komut bir atlama hedefi mi? (True/False)
    """)
