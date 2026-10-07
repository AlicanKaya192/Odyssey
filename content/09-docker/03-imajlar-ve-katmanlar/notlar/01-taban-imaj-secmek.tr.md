Bir Python programı için `FROM` satırına ne yazılır? Üç yaygın seçenek ve
ne zaman hangisi.

## Üç aile

| | `python:3.13` | `python:3.13-slim` | `python:3.13-alpine` |
|---|---|---|---|
| Altındaki Linux | Geniş Debian | Küçültülmüş Debian | Alpine |
| Boyut (açılmış) | ~1 GB | ~180 MB | ~50 MB |
| Derleme araçları (gcc vb.) | Var | Yok | Yok |
| C kütüphanesi | glibc | glibc | musl |
| Paket yöneticisi | `apt-get` | `apt-get` | `apk` |

## Ne zaman hangisi?

- **`-slim` çoğu zaman en iyi başlangıç.** Küçük, ama sıradan Debian; pip
  paketlerinin neredeyse hepsi hazır derlenmiş hâliyle (wheel) sorunsuz
  kuruluyor. Bu patika onu kullanıyor.
- **Tam imaj (`python:3.13`)**, kuracağın bir paketin hazır derlenmiş hâli
  yoksa ve kaynaktan derlenmesi gerekiyorsa. Kolay ama büyük; çok aşamalı
  derlemeyle (ileride) bu büyüklükten kurtuluyorsun.
- **`-alpine`** en küçüğü, ama dikkat: Alpine `glibc` yerine `musl` adında
  başka bir C kütüphanesi kullanıyor. NumPy, pandas gibi paketlerin hazır
  derlenmiş hâlleri çoğu zaman glibc için; Alpine'da kaynaktan derlenmeye
  çalışılıyor, kurulum dakikalar sürüyor ya da düşüyor. Saf Python
  programları için sorun yok.

## Etiketi ne kadar sabitlemeli?

| Yazım | Ne olur? |
|---|---|
| `python` | `latest`: her an başka sürüm. **Yazma.** |
| `python:3` | Python 3'ün en yenisi: 3.13 bugün, 3.14 yarın. |
| `python:3.13-slim` | 3.13'ün en yeni yaması (3.13.16, 3.13.17...). Güvenlik düzeltmeleri gelir, davranış değişmez. **Önerilen.** |
| `python:3.13.16-slim` | Tam olarak bu sürüm; düzeltme gelmez. |
| `python@sha256:...` | Birebir aynı imaj; en kesini. |

Çoğu proje için `3.13-slim` gibi "küçük sürüm" sabitlemesi iyi bir denge:
hata düzeltmeleri kendiliğinden geliyor, beklenmedik bir büyük sürüm
gelmiyor.

## İşlemci mimarisi

İmajlar belli bir işlemci türü için kuruluyor. Çoğu bilgisayar **amd64**
(x86_64); Apple'ın M serisi ve bazı yeni dizüstüler **arm64**. Resmî
imajların çoğu iki mimari için de yayınlanıyor ve Docker bilgisayarına
uyanı kendisi seçiyor. Bir imaj senin mimarin için yoksa şu uyarıyı
görürsün:

```text
WARNING: The requested image's platform (linux/arm64) does not match
the detected host platform (linux/amd64)
```

## Kendine sor

1. Programım saf Python mı, yoksa derlenmesi gereken paketler mi var?
2. İmaj boyutu önemli mi (sık indirilecek mi)?
3. Takımda herkes aynı sürümü mü kullanmalı?

Cevaplar çoğu zaman `python:3.13-slim`'e çıkıyor.
