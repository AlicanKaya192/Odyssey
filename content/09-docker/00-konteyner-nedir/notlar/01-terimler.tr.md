Patika boyunca sık geçecek kelimeler. İlk okumada hepsini ezberlemen
gerekmiyor; takıldığında bu sayfaya dön.

## Temel kavramlar

| Terim | Anlamı |
|---|---|
| **Konteyner** (container) | Kendi küçük dünyasında çalışan program: kendi dosyaları, paketleri, ayarları var. |
| **İmaj** (image) | Konteynerin kalıbı. Değişmeyen, diskte duran paket; ondan istediğin kadar konteyner çalıştırılır. |
| **Dockerfile** | İmajın tarifi: hangi imajdan başlanacağı, hangi dosyaların kopyalanacağı, hangi komutun çalışacağı. |
| **Derlemek** (build) | Dockerfile'dan imaj kurmak: `docker build`. |
| **Çalıştırmak** (run) | İmajdan konteyner başlatmak: `docker run`. |
| **Talimat** (instruction) | Dockerfile'ın her satırının başındaki büyük harfli kelime: `FROM`, `COPY`, `RUN`, `CMD`. |

## İmajlarla ilgili

| Terim | Anlamı |
|---|---|
| **Taban imaj** (base image) | `FROM` satırında başlanan hazır imaj, ör. `python:3.13-slim`. |
| **Etiket** (tag) | İmaj adının `:` sonrasındaki kısmı; genellikle sürüm: `python:3.13-slim`'de `3.13-slim`. |
| **Katman** (layer) | İmajı oluşturan üst üste dilimler; her talimat bir dilim ekler. |
| **Kayıt** (registry) | İmajların saklandığı ve indirildiği yer. En bilineni **Docker Hub**. |
| **Çekmek** (pull) | Kayıttan imaj indirmek: `docker pull`. |

## Docker'ın parçaları

| Terim | Anlamı |
|---|---|
| **Docker Engine** | Konteynerleri gerçekten çalıştıran, arka planda bekleyen servis (daemon). |
| **docker komutu** (CLI) | Terminalde yazdığın `docker ...` komutları; Engine'e ne yapacağını söyler. |
| **Docker Desktop** | Windows ve Mac'te Engine'i kuran ve yöneten masaüstü programı. |
| **Ana makine** (host) | Konteynerlerin üzerinde çalıştığı bilgisayar; burada senin bilgisayarın. |
| **Çekirdek** (kernel) | İşletim sisteminin en alttaki parçası; konteynerler ana makinenin çekirdeğini ortak kullanır. |

## İleride göreceklerin

| Terim | Anlamı | Bölüm |
|---|---|---|
| **Port** | Konteynerdeki bir programa dışarıdan ulaşılan kapı numarası. | 07 |
| **Ortam değişkeni** | Programa dışarıdan verilen ayar (`APP_ENV=production`). | 08 |
| **Volume** | Konteyner silinse de kalan veri alanı. | 09 |
| **Compose** | Birden çok konteyneri tek dosyayla birlikte çalıştırma aracı. | 10 |

## Sık karıştırılanlar

- **İmaj ≠ konteyner.** İmaj kalıp, konteyner ondan çalıştırılan kopya.
  Konteyneri silmek imajı silmez.
- **Docker ≠ sanal makine.** Konteyner ayrı bir işletim sistemi taşımaz.
- **Docker Desktop ≠ Docker Engine.** Desktop yalnızca Engine'i Windows'ta
  çalıştıran pencere; asıl işi Engine yapar.
