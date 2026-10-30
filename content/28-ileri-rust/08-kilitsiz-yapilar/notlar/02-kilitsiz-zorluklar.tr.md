## Üç söz

| Söz | Anlamı |
|---|---|
| Kilit tabanlı | Kilit tutan durursa herkes durur |
| Kilitsiz (lock-free) | En az bir kol hep ilerler |
| Beklemesiz (wait-free) | Her kol sınırlı adımda bitirir |

Kilitsiz, "hızlı" demek değildir. Çekişme altında tekrar denemeler kilitten yavaş olabilir. Kazancı uyutulan kolun kimseyi bekletmemesidir.

## Bellek geri kazanımı

| Yöntem | Fikir |
|---|---|
| Hiç silmemek | Basit, bellek sızar; kısa programda kabul edilebilir |
| Hazard pointer | Kol "şuna bakıyorum" diye ilan eder, silen bekler |
| Epoch | Dönemler sayılır, eski dönemdekiler topluca silinir |
| `Arc` ile | Kolay ama atomik sayaç maliyeti var |

`crossbeam-epoch` crate'i bunu yapar.

## ABA nasıl önlenir?

| Yöntem | Fikir |
|---|---|
| Sürüm sayacı | İşaretçinin yanında artan sayı |
| Bellek geri kazanımı | Baktığın düğüm silinmezse aynı adres gelmez |
| Tasarımla kaçınmak | `take_all` gibi |

## Ne zaman yazmalı?

Neredeyse hiç. `Mutex` ölçülmüş bir darboğaz değilse kilitsiz yapı karmaşıklığı karşılamaz. Hazır olanlar:

| Crate | İçerik |
|---|---|
| `crossbeam` | Kanal, deque, epoch |
| `dashmap` | Parçalı kilitli harita |
| `arc-swap` | Atomik `Arc` değişimi |

Bu patikada kurulu değiller, adlarını bilmen yeter.

## Test

Eşzamanlı kod testi tek çalıştırmayla doğrulanamaz. `loom` crate'i bütün sıralamaları deneyerek sıralama hatalarını bulur; kilitsiz yazıyorsan gerekli.
