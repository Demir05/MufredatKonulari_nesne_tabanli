# ===============================================================
# 📘 PYTHON YORUMLAYICISI (CPython) — ATTRIBUTE TANIMA & PERFORMANS
# ===============================================================

# 🔹 Bu rehber, yorumlayıcının bazı attribute'ları nasıl tanıdığını,
#     bu tanımanın çalışma mantığını nasıl değiştirdiğini ve
#     performansa olan etkilerini açıklar.

# ---------------------------------------------------------------
# ✅ 1. CPython bazı attribute'ları doğrudan tanır
# ---------------------------------------------------------------

# ➤ Örnek: __add__, __len__, __getitem__, __iter__ gibi özel metotlar
#     → CPython, bu metotları C düzeyinde tanır ve optimize eder.

# ➤ Örnek: sum(), len(), isinstance(), id()
#     → Bunlar yerleşik fonksiyonlardır → C ile yazılmıştır → yorumlayıcı doğrudan tanır

# 🔍 Bu tanıma sayesinde:
#     - Fonksiyon çağrısı daha hızlı gerçekleşir
#     - Bytecode yorumlama süreci kısalır
#     - Sanal makine daha az iş yüküyle çalışır

# ---------------------------------------------------------------
# ✅ 2. Tanınan davranışlar nasıl işlenir?
# ---------------------------------------------------------------

# ➤ Python kodu yazıldığında → bytecode’a çevrilir
# ➤ Bytecode içinde yerleşik fonksiyonlar için özel opcode’lar kullanılır
# ➤ CPython, bu opcode’ları doğrudan tanır ve C düzeyinde çalıştırır

# 🔍 Örnek:
#     result = sum([1, 2, 3])
#     → Bytecode: LOAD_GLOBAL sum → CALL_FUNCTION
#     → CPython, sum fonksiyonunu doğrudan tanır → C kodu çalıştırılır

# ---------------------------------------------------------------
# ✅ 3. Tanınmayan davranışlar nasıl işlenir?
# ---------------------------------------------------------------

# ➤ Kullanıcı tanımlı fonksiyonlar veya sınıflar → yorumlayıcı tarafından tanınmaz
# ➤ Bunlar tamamen Python kodu olarak işlenir → bytecode’a çevrilir → eval loop içinde yürütülür

# 🔍 Bu durumda:
#     - Her adım yorumlayıcı döngüsünde tek tek işlenir
#     - Daha fazla bellek ve CPU kullanımı olabilir
#     - Yerleşik fonksiyonlara göre daha yavaş çalışabilir

# ---------------------------------------------------------------
# ✅ 4. Performans farkı nereden gelir?
# ---------------------------------------------------------------

# 🔸 Tanınan davranışlar:
#     - C ile yazılmıştır → doğrudan çalıştırılır
#     - Daha az bellek kullanır
#     - Daha hızlıdır

# 🔸 Tanınmayan davranışlar:
#     - Python ile yazılmıştır → yorumlanır
#     - Daha fazla bytecode üretir
#     - Daha yavaş çalışabilir

# 🔍 Bu fark, özellikle sıcak kodlarda (örneğin: sık çağrılan fonksiyonlar) belirgin hale gelir

# ---------------------------------------------------------------
# ✅ 5. Örnek Karşılaştırma
# ---------------------------------------------------------------

# ➤ Yerleşik sum() fonksiyonu → C ile yazılmış → hızlı
# ➤ Kullanıcı tanımlı my_sum() fonksiyonu → Python ile yazılmış → daha yavaş

# def my_sum(lst):
#     total = 0
#     for x in lst:
#         total += x
#     return total

# 🔍 Aynı işlevi yaparlar ama my_sum() yorumlayıcı döngüsünde daha fazla adım gerektirir

# ---------------------------------------------------------------
# ✅ 6. Yorumlayıcının attribute tanıması neyi değiştirir?
# ---------------------------------------------------------------

# ➤ Tanınan attribute’lar için:
#     - Özel opcode’lar kullanılır
#     - C düzeyinde işlem yapılır
#     - Sanal makine daha az yorulur

# ➤ Tanınmayan attribute’lar için:
#     - Genel opcode’lar kullanılır
#     - Eval loop daha fazla çalışır
#     - Performans düşebilir

# ---------------------------------------------------------------
# ✅ SONUÇ:
# ---------------------------------------------------------------

# ➤ CPython yorumlayıcısı, bazı attribute’ları doğrudan tanır çünkü bunlar C ile tanımlanmıştır.
# ➤ Bu tanıma, bytecode üretimini ve yürütme sürecini optimize eder.
# ➤ Tanınmayan davranışlar daha genel şekilde işlenir → daha fazla yorumlama → daha düşük performans.
# ➤ Bu fark, sıcak kodlarda ve sık çağrılan fonksiyonlarda belirgin hale gelir.
