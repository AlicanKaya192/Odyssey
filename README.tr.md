<div align="right">
  <b>Türkçe</b> · <a href="./README.md">English</a>
</div>

# Odyssey

Data Science ve Machine Learning konularını bölüm bölüm öğreten, tamamen çevrimdışı çalışan bir masaüstü uygulaması.

Her bölümde konu anlatımı, ders notları ve alıştırmalar var. Bölümü tamamlamak için sınavı geçmen ve kod alıştırmalarını çözmen gerekiyor. Kodu uygulamanın içinde yazıyorsun, program onu çalıştırıp çıktısını ve sonucunu kontrol ediyor. Yapay zeka kullanılmıyor; kontroller önceden tanımlı ve deterministik.

## Durum

Erken geliştirme aşaması (`0.2.0`). Uygulama uçtan uca çalışıyor ama içerik henüz başlangıç seviyesinde.

**Çalışanlar:** öğrenme yolu, konu anlatımı, ders notları, sınav, kod alıştırmaları ve otomatik kontrol, kademeli ipuçları, hata açıklamaları, kalıcı ilerleme kaydı, Türkçe/İngilizce arayüz ve içerik, açık/koyu tema.

**Henüz yok:** müfredatın tamamı (şu an Python Temelleri modülünün sekiz bölümü var, hedef 23 modül), rozetler, kullanıcının kendi not alanı, uygulama içi güncelleme sistemi.

Yol haritası [CHANGELOG.md](CHANGELOG.md) dosyasında ilerliyor.

## Kurulum

Python kurmak istemiyorsan [Releases](https://github.com/AlicanKaya192/Odyssey/releases) sayfasından hazır paketi indir, klasörü aç ve `Odyssey.exe` dosyasını çalıştır. Kuruluma, yönetici hakkına veya Python'a gerek yok.

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

Arayüz ve içerik Türkçe ve İngilizce. Ayarlardan istediğin an değiştirebilirsin, uygulamayı yeniden başlatmana gerek yok. Bir bölümün İngilizce çevirisi henüz yoksa Türkçesi gösterilir ve üstte bunu belirten bir uyarı çıkar.

## Verilerin nerede duruyor?

İlerlemen, sınav notların, yazdığın kodlar, notların ve profilin `%APPDATA%\Odyssey\` klasöründeki veritabanında tutulur. Uygulamayı güncellediğinde veya silip yeniden kurduğunda bu klasöre dokunulmaz, ilerlemen kaybolmaz.

## Alıştırmalar nasıl kontrol ediliyor?

Kodun ayrı bir işlemde, izole bir çalışma klasöründe çalıştırılır. Ardından çıktısı, oluşturduğu değişkenler ve tanımladığı fonksiyonlar beklenen değerlerle karşılaştırılır. Kontrollerin tamamı önceden tanımlıdır; kod değerlendirmesinde herhangi bir dış servis kullanılmaz.

**Not:** Bu bir güvenlik sandbox'ı değildir. Kendi yazdığın kodu kendi bilgisayarında çalıştırıyorsun. Sistemin sağladığı şey izole bir çalışma klasörü, zaman aşımı sınırı, çıktı sınırı ve kodun hata vermesi durumunda uygulamanın çökmemesidir.

## İnternet

Uygulama tamamen çevrimdışı çalışır. Şu an hiçbir ağ çağrısı yapmıyor.

İleride açılışta bir güncelleme kontrolü eklenecek (yeni sürüm var mı diye bakmak için); geldiğinde ayarlardan kapatılabilir olacak. Henüz yok.

"Bağlantılar ve Projeler" bölümündeki adresler uygulamanın içinde açılmaz; tıkladığında sistemin tarayıcısına gider. Yani uygulama kendi başına ağa çıkmaz, yalnızca senin açık isteğinle bir adres açılır.

## Katkıda bulunma

Issue ve pull request'ler açıktır. Önce [CONTRIBUTING.md](CONTRIBUTING.md) ve [Davranış Kuralları](CODE_OF_CONDUCT.md) dosyalarını okumanı rica ederim.

## Lisans

MIT Lisansı — Copyright (c) 2026 Alican Kaya. Ayrıntılar için [LICENSE](LICENSE) dosyasına bak.

Ders içeriği [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) projesinden geliyor ve aynı lisansa tabi.
