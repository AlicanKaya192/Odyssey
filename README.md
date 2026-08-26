# Proje A

Data Science ve Machine Learning konularını bölüm bölüm öğreten, tamamen çevrimdışı çalışan bir masaüstü uygulaması.

Her bölümde konu anlatımı, görseller, PDF ders notları ve kendi notlarını tutabileceğin bir alan var. Bölümü tamamlamak için sınavı geçmen ve kod alıştırmalarını çözmen gerekiyor. Alıştırmalarda kodu uygulamanın içinde yazıyorsun, program kodu çalıştırıp çıktısını ve sonucunu kontrol ediyor.

## Durum

Geliştirme aşamasında. Şu an temel iskelet kuruluyor.

## Gereksinimler

- Windows 10 / 11
- Python 3.12 veya 3.13

## Kurulum (geliştirme)

```bash
py -3.13 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python app\main.py
```

Alıştırmaların çalıştığı ortam ayrıdır ve uygulama ilk açılışta onu kendisi kurar.

## Diller

Arayüz ve içerik Türkçe ve İngilizce. Ayarlardan istediğin an değiştirebilirsin, uygulamayı yeniden başlatmana gerek yok. Bir bölümün İngilizce çevirisi henüz yoksa Türkçesi gösterilir ve üstte bunu belirten bir uyarı çıkar.

## Verilerin nerede duruyor?

İlerlemen, sınav notların, yazdığın kodlar, notların ve profilin `%APPDATA%\ProjeA\` klasöründeki veritabanında tutulur. Uygulamayı güncellediğinde veya silip yeniden kurduğunda bu klasöre dokunulmaz, ilerlemen kaybolmaz.

## Alıştırmalar nasıl kontrol ediliyor?

Kodun ayrı bir işlemde, izole bir çalışma klasöründe çalıştırılır. Ardından çıktısı, oluşturduğu değişkenler ve tanımladığı fonksiyonlar beklenen değerlerle karşılaştırılır. Kontrollerin tamamı önceden tanımlıdır; kod değerlendirmesinde herhangi bir dış servis kullanılmaz.

**Not:** Bu bir güvenlik sandbox'ı değildir. Kendi yazdığın kodu kendi bilgisayarında çalıştırıyorsun. Sistemin sağladığı şey izole bir çalışma klasörü, zaman aşımı sınırı, çıktı sınırı ve kodun hata vermesi durumunda uygulamanın çökmemesidir.

## İnternet

Uygulama çevrimdışı çalışır. Tek istisna, açılışta yapılan güncelleme kontrolüdür; bu da ayarlardan kapatılabilir.

## Lisans

Belirlenecek.
