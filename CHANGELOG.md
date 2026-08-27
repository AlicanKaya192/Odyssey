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
- **Başlangıç** bölümü: Python nedir, ilk program, uygulamanın nasıl çalıştığı ve kurulum notu.
- **Koşul Durumları** bölümü: if / elif / else, koşul sırası, doğruluk değerleri.
- **Döngüler** bölümü: for, while, range, break ve continue notlarıyla.
- Operatörler bölümüne iki ders notu: aritmetik operatörler, atama ve karşılaştırma.

### Değişti
- Python Temelleri modülü yeniden düzenlendi. Sıra artık: Başlangıç, Değişkenler, Operatörler, Koşullar, Döngüler.
- Döngüler operatörlerden ayrılıp kendi bölümü oldu; ikisi tek bölüme sığmıyordu.
- Operatörler bölümünün ders notu PDF yerine metin olarak açılıyor.
- Sınavlardaki açıklamalar artık ders anlatımındaki ipucu kutusuyla aynı görünümde.

### Düzeltildi
- Değişkenler bölümünün ikinci alıştırması fonksiyon yazmayı istiyordu, ama fonksiyonlar o noktada henüz anlatılmamıştı. Alıştırma o dersin gerçekten öğrettiği şeyle değiştirildi: metinden sayıya dönüşüm.
- Sürüm notlarındaki kalın yazı ve kod işaretleri ekranda ham görünüyordu; artık biçimlendirilmiş olarak çiziliyor.
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
