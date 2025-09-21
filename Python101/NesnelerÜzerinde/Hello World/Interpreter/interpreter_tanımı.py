# ===============================================================
# 📘 PYTHON INTERPRETER (YORUMLAYICI) — TANIM VE MİMARİ
# ===============================================================

# 🔹 Bu rehber, Python yorumlayıcısının ne olduğunu, nasıl çalıştığını
#     ve hangi bileşenlerden oluştuğunu açıklar.

# ---------------------------------------------------------------
# ✅ 1. Yorumlayıcı nedir?
# ---------------------------------------------------------------

# ➤ Yorumlayıcı (interpreter), bir programlama dilinde yazılmış kaynak kodu
#     satır satır okuyup çalıştıran yazılımdır.
# her Interpreter,yazıldığı dilin Interpreter'i tarafından derlenir çünkü burda yazılımdam söz ediyoruz
# bu zincir sonsuz değildir ama çok katmanlıdır en sonunda makine diline kadar inilir.

# ➤ Python yorumlayıcısı, Python kodunu alır → bytecode’a çevirir → çalıştırır.

# 🔍 Python yorumlayıcısı = CPython (en yaygın versiyon)
#     → C diliyle yazılmıştır
#     → Python.org’dan indirilen Python aslında CPython’dır

# ---------------------------------------------------------------
# ✅ 2. Yorumlayıcının çalışma aşamaları
# ---------------------------------------------------------------

# ➤ 1. Kodun okunması:
#     - .py dosyasındaki kaynak kod satır satır analiz edilir

# ➤ 2. Bytecode üretimi:
#     - Kod, Python’un ara dili olan bytecode’a çevrilir
#     - Bu bytecode .pyc dosyalarında saklanabilir

# ➤ 3. Sanal makinede yürütme:
#     - Bytecode, yorumlayıcının içindeki sanal makine tarafından çalıştırılır
#     - Sanal makine = eval loop → bytecode komutlarını tek tek yürütür


# ---------------------------------------------------------------
# ✅ 3. Alternatif yorumlayıcılar
# ---------------------------------------------------------------

# ➤ CPython dışında başka yorumlayıcılar da vardır:
#     - PyPy → JIT destekli, daha hızlı
#     - Jython → Java ile yazılmış, JVM üzerinde çalışır
#     - IronPython → C# ile yazılmış, .NET üzerinde çalışır

# 🔍 Bunlar Python dilini farklı platformlarda çalıştırmak için geliştirilmiştir

# ---------------------------------------------------------------
# ✅ SONUÇ:
# ---------------------------------------------------------------

# ➤ Python yorumlayıcısı, kaynak kodu alır → bytecode’a çevirir → sanal makinede çalıştırır
# ➤ CPython, bu yorumlayıcının en yaygın ve resmi versiyonudur
# ➤ Tanınan davranışlar daha hızlı çalışır çünkü C ile tanımlanmıştır
# ➤ Tanınmayan davranışlar yorumlanır → daha fazla işlem gerektirir
# ➤ Yorumlayıcı, Python’un hem esnekliğini hem de taşınabilirliğini sağlayan temel bileşendir

