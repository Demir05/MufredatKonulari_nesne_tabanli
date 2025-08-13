# ============================================================
# 📌 EXCEPTION NEDİR?
# ============================================================
# Exception (istisna), Python yorumlayıcısının bir kod parçasını
# çalıştırırken beklenmedik veya olağan dışı bir durumla karşılaştığında
# programın normal akışını durdurup, özel bir “hata sinyali” göndermesidir.
#
# 🧠 Daha net düşünmek için:
#   - "Exception" bir nesnedir (sınıfı Exception veya onun alt sınıflarından türemiştir)
#   - Bir hata veya olağandışı durumun **temsilidir**, sadece metin değil, tip + veri içerir
#   - Exception fırlatıldığında (raise), o noktadan itibaren normal akış kesilir
#
# 💡 Exception sadece “hata” demek değildir:
#   - Genellikle hata sinyali olarak kullanılır (ZeroDivisionError, FileNotFoundError)
#   - Ama bazen normal akışın kontrolü için de kullanılır (StopIteration gibi)
#
# ============================================================
# 📌 EXCEPTION HANDLING NEDİR?
# ============================================================
# Exception handling (istisna yakalama), fırlatılan (raise edilen)
# exception nesnelerini **kontrollü bir şekilde karşılayıp** programın
# çökmesini engelleme veya özel bir tepki verme sürecidir.
#
# 🧠 Mantık:
#   1. Kod çalışırken exception oluşur.
#   2. Python yorumlayıcısı bu exception'ı yukarı doğru (call stack boyunca) iletir.
#   3. Yol üzerinde uygun bir “yakalama noktası” (handler) bulunursa, kontrol oraya geçer.
#   4. Handler exception'ı işleyip akışı kontrol altına alabilir veya yeniden fırlatabilir.
#   5. Eğer hiçbir yerde yakalanmazsa, program sona erer (Traceback ile).
#
# 💡 Exception handling, programın “hata toleransını” arttırır:
#   - Hata olduğunda kullanıcıya anlamlı mesajlar verilebilir
#   - Kritik işlemler sonrası kaynaklar temizlenebilir (dosya kapatma vb.)
#   - Alternatif yollar denenebilir
#
# ============================================================
# 📌 NEREDE KULLANILIR?
# ============================================================
# - Kullanıcıdan gelen verilerin doğrulanmasında
# - Dosya, ağ veya veri tabanı işlemlerinde (dış kaynaklar hata yapabilir)
# - API çağrılarında beklenmeyen yanıt durumlarında
# - Kritik görevlerde hata sonrası temizleme (cleanup) yapılması gerektiğinde
# - Geliştirme aşamasında, hataları daha kolay bulmak ve loglamak için
#
# ============================================================
# 📌 DİKKAT EDİLMESİ GEREKENLER
# ============================================================
# 1) **Spesifik Yakalama**:
#    - Sadece beklediğin hata tipini yakala (ör. FileNotFoundError).
#    - "except:" veya "except Exception:" ile her şeyi yutma (aksi halde hata gizlenir).
#
# 2) **Hataları Yutma**:
#    - Exception'ı yakalayıp hiçbir şey yapmamak, ileride debug'u zorlaştırır.
#    - Exception'ı yutuyorsan mutlaka log kaydı bırak.
#
# 3) **Doğru Seviye**:
#    - Exception'ı olabildiğince uygun (en yakın) seviyede yakala.
#    - Çok yukarıda yakalamak bazen kök nedeni bulmayı zorlaştırır.
#
# 4) **Temizlik (Cleanup)**:
#    - Exception oluşsa da kaynaklar (dosya, ağ bağlantısı, bellek) serbest bırakılmalı.
#    - Bunun için özel bloklar veya context manager kullanılır.
#
# 5) **Gereksiz Kullanım**:
#    - Normal akış için exception kullanma (performans düşer).
#    - Örn: if yerine sürekli try/except ile kontrol yapmak mantıklı olmayabilir.
#
# ============================================================
# 📝 ÖZET
# ============================================================
# Exception = Hata veya özel durumun nesne olarak temsili.
# Exception handling = Bu durumları kontrollü bir şekilde yakalama ve yönetme süreci.
# Doğru yapıldığında programın dayanıklılığını arttırır.
# Yanlış yapıldığında hataları gizler ve bakım maliyetini yükseltir.
