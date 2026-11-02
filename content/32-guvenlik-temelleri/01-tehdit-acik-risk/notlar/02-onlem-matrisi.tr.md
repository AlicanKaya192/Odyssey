Önlemler iki ayrı soruyla sınıflanır. **Ne zaman** çalışıyor (önleyici,
tespit edici, düzeltici) ve **ne türden** (teknik, idari, fiziksel)?

- **Teknik** (technical): yazılım ya da donanımla uygulanan önlem.
- **İdari** (administrative): kural, süreç, eğitim; insanların ne
  yapacağını söyleyen önlem.
- **Fiziksel** (physical): kapı, kilit, kamera; bir yere girmeyi
  sınırlayan önlem.

İki soru birlikte bir tablo kurar. Her hücre için bir örnek:

| | Önleyici | Tespit edici | Düzeltici |
|---|---|---|---|
| **Teknik** | Parola, şifreleme, güvenlik duvarı | Kayıt (log) incelemesi, saldırı tespit sistemi | Yedekten geri yükleme, yama |
| **İdari** | Parola politikası, güvenlik eğitimi | Düzenli denetim, erişim gözden geçirme | Olay müdahale planı |
| **Fiziksel** | Kilitli sunucu odası, kartlı giriş | Güvenlik kamerası, kapı alarmı | Yangın söndürme sistemi |

## Nasıl kullanılır?

Bir riski ele alırken satırlara ve sütunlara bak: hepsi aynı hücrede mi
duruyor? Örneğin "çalışan dizüstü bilgisayarını kaybetti" riski için:

- **Önleyici, teknik:** diski şifrelemek.
- **Tespit edici, idari:** kaybın hemen bildirilmesi kuralı.
- **Düzeltici, teknik:** cihazı uzaktan kilitleyip silmek, yedekten yeni
  cihaz kurmak.

Tek bir hücreye yığılmış önlemler, o hücre aşıldığında bütün sistemi
savunmasız bırakır. Önlemleri farklı hücrelere yaymanın adı
**derinlemesine savunmadır**; Güvenlik İlkeleri bölümünde ayrıntısıyla
geliyor.

## Bazen eklenen türler

- **Caydırıcı** (deterrent): saldırganı vazgeçirmeye çalışır; "bu alan
  kamerayla izleniyor" tabelası.
- **Telafi edici** (compensating): asıl önlem uygulanamadığında yerine
  konan önlem; eski bir sistem yamalanamıyorsa onu ağdan ayırmak.
