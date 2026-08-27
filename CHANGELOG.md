# Odyssey — Değişiklik Günlüğü

Uygulama içindeki Sürüm Notları ekranı bu dosyayı gösterir. Yeni bir sürüm
yayınlamadan önce buraya yazılır; hem GitHub'daki sürüm açıklaması hem
uygulamanın içindeki metin aynı kaynaktan gelir.

## Sürüm numaraları nasıl ilerliyor?

`BÜYÜK.ORTA.KÜÇÜK` — üç parça:

- **Küçük** (`0.1.0` → `0.1.1`): düzeltmeler ve küçük eklemeler. Geliştirme
  boyunca çoğunlukla burası artar.
- **Orta** (`0.1.x` → `0.2.0`): bir aşama tamamlandığında. Örneğin içerik
  aktarımı bittiğinde.
- **Büyük** (`0.x` → `1.0.0`): benden başkasının kullanabileceği ilk sürüm.

Ders içeriğinin ayrı bir sürümü var (`content_version`). Sadece bir ders notu
düzeltildiğinde uygulamanın tamamı yeniden indirilmiyor.

---

## [0.1.3] — 27 Ağustos 2026

### Eklendi
- Her bölümde artık **en az üç alıştırma** var; toplam 6'dan 18'e çıktı. Yeni alıştırmalar kolaydan zora sıralı ve yalnızca o bölüme kadar anlatılmış kavramları kullanıyor.
- Uygulama ilk açılışta bilgisayarın arayüz diline göre açılıyor: Windows'u Türkçe olan Türkçe, başka bir dilde olan İngilizce görüyor. Ayarlardan bir dil seçildiği anda bu devreye girmiyor, seçim geçerli oluyor.
- Açılışta kapalı beta uyarısı: uygulamanın kararsız çalışabileceği, hata ve çökme görülebileceği ve geri bildirimin nasıl iletileceği yazıyor. Sürüm başına bir kez çıkıyor.
- Lisans ekranı artık seçili dilde: Türkçede MIT Lisansı'nın Türkçe çevirisi, İngilizcede özgün metin görünüyor. İki dilde de ekranda tek bir lisans metni var.
- **Başlangıç** bölümü: Python nedir, ilk program, uygulamanın nasıl çalıştığı ve kurulum notu.
- **Koşul Durumları** bölümü: if / elif / else, koşul sırası, doğruluk değerleri.
- **Döngüler** bölümü: for, while, range, break ve continue notlarıyla.
- **Sözlükler ve Kümeler** bölümü: anahtar-değer mantığı, `in` ile anahtar sorgulama, ekleme ve güncelleme, `items()` ile döngü, kümelerin tekrar tutmaması ve `{}` tuzağı. Ders notlarında sözlük metotları ile dört veri yapısını karşılaştıran bir seçim rehberi var.
- **Listeler ve Demetler** bölümü: liste oluşturma, sıra numarası, negatif numara, dilimleme, `append`/`remove`/`pop`, `len` ve `in`, demetlerin değiştirilemezliği. Ders notlarında liste metotları ve dilimleme ayrıntısı var; kopya tuzağı da anlatılıyor.
- **Fonksiyonlar** bölümü: `def`, parametreler, `return`, varsayılan değerler. Ders notlarında konumsal/isimli argümanlar ve değişken kapsamı (yerel, global) var. `return` ile `print` farkı hem derste hem sınavda ayrıca ele alınıyor.
- Operatörler bölümüne iki ders notu: aritmetik operatörler, atama ve karşılaştırma.

### Değişti
- Sınav sorularındaki, şıklardaki ve açıklamalardaki kod parçaları artık kod olarak çiziliyor: tek aralıklı yazı ve zemin. Düz metin hâlinde `[20, 30]` ile bir cümleyi ayırt etmek zordu.
- Alıştırma şeridi belirginleşti: sayı kalın yazılıyor ve yanında numara düğmeleri duruyor. Bölümde kaç alıştırma olduğu ve hangilerinin çözüldüğü bakar bakmaz görünüyor; istediğine doğrudan atlanabiliyor. Önceki/Sonraki düğmeleri kaldırıldı.
- Sürüm notlarındaki sayfa numaraları ortalandı; "Sayfa 1 / 2" yazısı kaldırıldı, numaralar zaten aynı bilgiyi veriyordu.
- Sol şerit ikiye ayrıldı: üstte her gün girilen ekranlar (Öğrenme Yolu, Profilim, Ekstra İçerikler), altta ayar simgesinin hemen üstünde ara sıra açılanlar (Sürüm Notları, Bağlantılarım, Lisans).
- Sürüm numaralarının yanında kırmızı **ALPHA** rozeti çıkıyor. 1.0 öncesi her sürüm alpha sayılıyor; 1.0 çıktığında rozet kendiliğinden kalkacak.
- Sürüm notları sayfalara bölündü; bir sayfada en fazla üç sürüm görünüyor, altta sayfa düğmeleri var. Önceden bütün sürümler alt alta dizildiği için ekran uzayıp gidiyordu.
- Python Temelleri modülü yeniden düzenlendi. Sıra artık: Başlangıç, Değişkenler, Operatörler, Koşullar, Döngüler.
- Döngüler operatörlerden ayrılıp kendi bölümü oldu; ikisi tek bölüme sığmıyordu.
- Operatörler bölümünün ders notu PDF yerine metin olarak açılıyor.
- Sınavlardaki açıklamalar artık ders anlatımındaki ipucu kutusuyla aynı görünümde.
- Başlangıç sınavının son sorusu uygulamanın arayüzünü soruyordu; yerine dersin anlattığı bir konu kondu: Python'un yorumlanan bir dil olması ne demek.

### Düzeltildi
- Değişkenler bölümünün ikinci alıştırması fonksiyon yazmayı istiyordu, ama fonksiyonlar o noktada henüz anlatılmamıştı. Alıştırma o dersin gerçekten öğrettiği şeyle değiştirildi: metinden sayıya dönüşüm.
- Sürüm notlarındaki kalın yazı ve kod işaretleri ekranda ham görünüyordu; artık biçimlendirilmiş olarak çiziliyor.
- Paketlenmiş uygulamada Windows görev çubuğunda ve pencere başlığında uygulamanın simgesi yerine genel bir program simgesi çıkıyordu. Simge dosyası paketin içinde duruyordu ama uygulama onu yanlış klasörde arıyordu.
- Ders metnini sonuna kadar okumak "okundu" olarak işaretlenmiyordu. Sayfanın kendisi haber vermeye çalışıyordu ama tarayıcı motoru, kullanıcı tıklaması olmadan uygulamaya haber gönderilmesine izin vermiyor; bu yüzden bildirim sessizce düşüyordu. Artık uygulama sayfaya kendisi soruyor.
- Ders metninin altındaki ileri düğmesi, bölümde ders notu olsa bile doğrudan sınava atlıyordu. Artık sırayla gidiyor: konu anlatımı, ders notu, sınav, alıştırma.
- Ders notlarının sonuncusunda ileri düğmesi yoktu, okuyan kişi sınava geçmek için sekmelere dönmek zorundaydı. Son notun altında artık sınava götüren bir düğme var.
- Yeniden düzenleme sırasında iki alıştırma, içeriği tamamen değişmesine rağmen eski kimliğini korumuştu. Bu yüzden açtığınızda önceki alıştırmada yazdığınız kod karşınıza geliyordu. Kimlikler ayrıştırıldı, alıştırmalar artık boş başlıyor.

## [0.1.2] — 27 Ağustos 2026

### Eklendi
- Bağlantılar ve Projeler bölümü: GitHub, LinkedIn, portfolyo, Medium ve açık kaynak projeler.
- Lisans ekranı: MIT metni ve ders içeriğinin lisansı.
- Alıştırmalarda kademeli ipucu; kullanıcı ihtiyacı kadarını açıyor.
- Hata mesajlarının altında ne anlama geldikleri yazıyor.
- Windows için hazır paket: Python kurmadan çalışan `Odyssey.exe`.
- Uygulamanın kendi adı ve simgesi.

### Değişti
- Alıştırma kodu artık tamamen ASCII. İngilizce klavyede Türkçe karakter olmadığı için önceki alıştırmalar İngilizce kullananlar tarafından çözülemiyordu.
- İlerleme göstergesi gerçek durumu yansıtıyor; bölümü açmak artık "okundu" saymıyor.
- Sol şeritteki simgeler koyu temada daha okunaklı.

### Düzeltildi
- Son ders notundayken "Sonraki not" tıklanamaz hâlde görünüyordu, artık hiç çıkmıyor.
- Sürüm notlarında her başlık ayrı bir kart olarak çiziliyordu.

## [0.1.1] — 26 Ağustos 2026

### Eklendi
- Öğrenme yolu ekranı: modül kartları ve bölüm düğümleri.
- Profil ekranı: ad, soyad ve ilerleme istatistikleri.
- Ders notları PDF yerine metin olarak açılıyor; aranabiliyor ve kopyalanabiliyor.

### Değişti
- Ders metinleri Chromium ile çiziliyor: kod blokları renkli, köşeler yuvarlak, sayfa içi başlık listesi kaydırırken yerinde kalıyor.
- Bölümler kilitli değil; tamamlananlara istenildiğinde dönülebiliyor.

### Düzeltildi
- Ayarlar penceresi açılmıyordu.
- Ders notlarına geçince ikinci bir pencere açılıyordu.

## [0.1.0] — 26 Ağustos 2026

### Eklendi
- İlk çalışan sürüm: Python Temelleri modülü, konu anlatımı, sınav ve kod alıştırmaları.
- Kod çalıştırma motoru: beş kontrol tipi, zaman aşımı, anlaşılır hata mesajları.
- Türkçe ve İngilizce arayüz; yeniden başlatmadan değişiyor.
- İlerleme kalıcı olarak saklanıyor.
