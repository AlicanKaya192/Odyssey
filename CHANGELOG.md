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
