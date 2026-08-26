# Proje A

Data Science ve Machine Learning konularını bölüm bölüm öğreten, tamamen çevrimdışı çalışan bir masaüstü uygulaması.

Her bölümde konu anlatımı, görseller, PDF ders notları ve kendi notlarını tutabileceğin bir alan var. Bölümü tamamlamak için sınavı geçmen ve kod alıştırmalarını çözmen gerekiyor. Alıştırmalarda kodu uygulamanın içinde yazıyorsun, program kodu çalıştırıp çıktısını ve sonucunu kontrol ediyor.

## Durum

Geliştirme aşamasında. Şu an temel iskelet kuruluyor.

## Gereksinimler

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

İlerlemen, sınav notların, yazdığın kodlar, notların ve profilin `%APPDATA%\ProjeA\` klasöründeki veritabanında tutulur. Uygulamayı güncellediğinde veya silip yeniden kurduğunda bu klasöre dokunulmaz, ilerlemen kaybolmaz.

## Alıştırmalar nasıl kontrol ediliyor?

Kodun ayrı bir işlemde, izole bir çalışma klasöründe çalıştırılır. Ardından çıktısı, oluşturduğu değişkenler ve tanımladığı fonksiyonlar beklenen değerlerle karşılaştırılır. Kontrollerin tamamı önceden tanımlıdır; kod değerlendirmesinde herhangi bir dış servis kullanılmaz.

**Not:** Bu bir güvenlik sandbox'ı değildir. Kendi yazdığın kodu kendi bilgisayarında çalıştırıyorsun. Sistemin sağladığı şey izole bir çalışma klasörü, zaman aşımı sınırı, çıktı sınırı ve kodun hata vermesi durumunda uygulamanın çökmemesidir.

## İnternet

Uygulama çevrimdışı çalışır. Tek istisna, açılışta yapılan güncelleme kontrolüdür; bu da ayarlardan kapatılabilir.

"Bağlantılar ve Projeler" bölümündeki adresler uygulamanın içinde açılmaz; tıkladığında sistemin tarayıcısına gider. Yani uygulama kendi başına ağa çıkmaz, yalnızca senin açık isteğinle bir adres açılır.

## Lisans

MIT Lisansı — Copyright (c) 2026 Alican Kaya. Ayrıntılar için [LICENSE](LICENSE) dosyasına bak.

Ders içeriği [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) projesinden geliyor ve aynı lisansa tabi.
