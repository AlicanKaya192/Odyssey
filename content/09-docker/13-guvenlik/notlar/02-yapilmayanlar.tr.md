Kısayol gibi görünen ama güvenliği ortadan kaldıran şeyler. Bir
yönergede ya da internette görürsen iki kez düşün.

| Yapılan | Neden tehlikeli? | Yerine |
|---|---|---|
| `docker run --privileged` | Konteyner bilgisayarın neredeyse bütün yetkilerini alıyor. | Gereken tek yetkiyi `--cap-add` ile ver. |
| `-v /var/run/docker.sock:/var/run/docker.sock` | Konteyner Docker'ı yönetebiliyor: istediği konteyneri, istediği yetkiyle başlatabilir. | Gerçekten gerekmedikçe yapma. |
| `-v /:/host` | Bilgisayarın bütün diski konteynerde. | Yalnızca gereken klasörü bağla, mümkünse `:ro`. |
| `ENV PASSWORD=...` | Şifre `docker image inspect`'te görünüyor. | Çalıştırırken `--env-file`. |
| `FROM someone/random-image` | İçinde ne olduğu bilinmiyor. | Resmî ya da doğrulanmış imaj. |
| `FROM python` | `latest`; ne kurulduğu belli değil. | `FROM python:3.13-slim`. |
| `chmod -R 777 /app` | Herkes her şeye yazabilir. | `chown app:app` yalnızca yazılan klasöre. |
| `curl ... \| sh` (Dockerfile'da) | İndirilen betiği bakmadan çalıştırmak. | Sürümü sabit, özeti denetlenen paket. |
| `-p 0.0.0.0:5432:5432` (veritabanı) | Veritabanı ağdaki herkese açık. | Port yayınlama; aynı ağdan ulaşılsın. |

## Kendine sor

- Bu konteyner ele geçirilse saldırgan neye ulaşır?
- Bu dosya imajda olmasa program çalışır mı? (Çalışırsa çıkar.)
- Bu port dışarıya gerçekten açık olmalı mı?
- Bu imaj en son ne zaman yeniden kuruldu?
