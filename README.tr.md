<div align="right">
  <b>Türkçe</b> · <a href="./README.md">English</a>
</div>

# Odyssey

Data Science ve Machine Learning konularını bölüm bölüm öğreten, tamamen çevrimdışı çalışan bir masaüstü uygulaması.

Her bölümde konu anlatımı, ders notları, sınav ve kod alıştırmaları var. Bir bölümü tamamlamak için sınavı geçmek ve alıştırmaları çözmek gerekiyor. Kod uygulamanın içinde yazılıyor; program onu çalıştırıyor, ardından çıktısını, oluşturduğu değişkenleri ve tanımladığı fonksiyonları kontrol ediyor. Yapay zeka kullanılmıyor — her kontrol önceden tanımlıdır ve deterministik olarak değerlendirilir, yani aynı kod her zaman aynı sonucu verir.

## Durum

Erken geliştirme aşaması (`0.4.0`). Uygulama uçtan uca çalışıyor. Motor — öğrenme yolları, konu anlatımı, sınavlar, alıştırma çalıştırıcısı, ilerleme kaydı — yerinde; müfredat ise henüz başlangıçta.

**Bugünkü içerik:** Python Temelleri modülü **tamamlandı** — on beş bölüm, ilk programdan veritabanına kadar. 250 sınav sorusu, 65 kod alıştırması ve 34 ders notu; tamamı Türkçe ve İngilizce.

**Altı öğrenme patikası** tanımlı: Python açık; Veri Bilimi, Makine Öğrenmesi, SQL, API ve Docker içerikleri hazırlanana kadar kilitli görünüyor.

**Çalışanlar:** öğrenme patikaları, bölüm içi başlık listesi ve okuma takibiyle konu anlatımı, ders notları, süreli sınavlar, otomatik kontrollü kod alıştırmaları, kademeli ipuçları, hata açıklamaları, sırayla açılan bölümler, kalıcı ilerleme kaydı, kendi fotoğrafınızı seçebildiğiniz profil, Türkçe/İngilizce arayüz ve içerik, açık/koyu tema, kilidi ve sınav süresini kaldırma seçenekleri.

**Henüz yok:** diğer patikaların içeriği (23 modül planlanıyor), rozetler, kullanıcının kendi not alanı, uygulama içi güncelleme sistemi.

Yol haritası [CHANGELOG.md](CHANGELOG.md) dosyasında ilerliyor.

## Kurulum

Python kurmak istemiyorsanız [Releases](https://github.com/AlicanKaya192/Odyssey/releases) sayfasından hazır paketi indirin, klasörü açın ve `Odyssey.exe` dosyasını çalıştırın. Kuruluma, yönetici hakkına veya Python'a gerek yok.

## Gereksinimler (kaynaktan çalıştırmak için)

- Windows 10 / 11
- Python 3.10 – 3.14 (temiz bir CPython kurulumu)

Anaconda'nın Python'u ile kurmayın. Anaconda kendi MSVC runtime kütüphanelerini taşıyor ve Qt'nin DLL'leri bunları yüklediğinde uygulama açılmıyor.

## Kurulum (geliştirme)

```bash
py -3.14 tools/setup_env.py
```

Bu komut hem uygulamanın çalıştığı ortamı hem de alıştırmaların çalıştığı ayrı ortamı kurar. Ardından:

```bash
.venv\Scripts\python app\main.py
```

## Diller

Arayüz ve içerik Türkçe ve İngilizce. Ayarlardan istediğiniz an değiştirebilirsiniz, uygulamayı yeniden başlatmaya gerek yok. Bir bölümün İngilizce çevirisi henüz yoksa Türkçesi gösterilir ve üstte bunu belirten bir uyarı çıkar.

## Verileriniz nerede duruyor?

İlerlemeniz, sınav notlarınız, yazdığınız kodlar, notlarınız, profiliniz ve seçtiğiniz fotoğraf `%APPDATA%\Odyssey\` klasöründe tutulur. Uygulamayı güncellediğinizde veya silip yeniden kurduğunuzda bu klasöre dokunulmaz, ilerlemeniz kaybolmaz.

## Alıştırmalar nasıl kontrol ediliyor?

Kodunuz ayrı bir işlemde, izole bir çalışma klasöründe çalıştırılır. Ardından çıktısı, oluşturduğu değişkenler ve tanımladığı fonksiyonlar beklenen değerlerle karşılaştırılır. Kontrollerin tamamı önceden tanımlıdır; kod değerlendirmesinde herhangi bir dış servis kullanılmaz.

**Not:** Bu bir güvenlik sandbox'ı değildir. Kendi yazdığınız kodu kendi bilgisayarınızda çalıştırıyorsunuz. Sistemin sağladığı şey izole bir çalışma klasörü, zaman aşımı sınırı, çıktı sınırı ve kodun hata vermesi durumunda uygulamanın çökmemesidir.

## İnternet

Uygulama tamamen çevrimdışı çalışır. Hiçbir ağ çağrısı yapmaz.

İleride açılışta bir güncelleme kontrolü eklenecek (yeni sürüm var mı diye bakmak için); geldiğinde ayarlardan kapatılabilir olacak. Henüz yok.

"Bağlantılarım" ve "Ekstra İçerikler" sekmelerindeki adresler uygulamanın içinde açılmaz; tıklandığında sistemin tarayıcısına devredilir. Uygulama kendi başına ağa çıkmaz; bir adres yalnızca sizin isteğinizle açılır.

## Katkıda bulunma

Issue ve pull request'ler açıktır. Önce [CONTRIBUTING.tr.md](CONTRIBUTING.tr.md) ve [Davranış Kuralları](CODE_OF_CONDUCT.tr.md) dosyalarını okumanızı rica ederim. Güvenlik bildirimlerinin ayrı bir yolu var: [SECURITY.tr.md](SECURITY.tr.md).

## Lisans

MIT Lisansı — Copyright (c) 2026 Alican Kaya. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.

Ders içeriği [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) projesinden geliyor ve aynı lisansa tabi.
