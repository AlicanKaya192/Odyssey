Dockerfile'da kullanılabilen talimatların hepsi. Çoğunu patikanın ilerleyen
bölümlerinde ayrıntısıyla göreceksin; sağ sütun nerede.

## Temel talimatlar

| Talimat | Ne yapar? | Örnek | Bölüm |
|---|---|---|---|
| `FROM` | Taban imajı seçer. Her Dockerfile bununla başlar. | `FROM python:3.13-slim` | 04 |
| `WORKDIR` | Çalışma klasörünü ayarlar (yoksa oluşturur). | `WORKDIR /app` | 04 |
| `COPY` | Bağlamdaki dosyaları imaja kopyalar. | `COPY . .` | 04 |
| `RUN` | Derleme sırasında komut çalıştırır; sonuç yeni katman. | `RUN pip install -r requirements.txt` | 04 |
| `CMD` | Konteyner çalışınca varsayılan komut. | `CMD ["python", "app.py"]` | 04, 06 |
| `ENTRYPOINT` | Konteynerin değişmeyen giriş komutu. | `ENTRYPOINT ["python", "cli.py"]` | 06 |

## Ayar talimatları

| Talimat | Ne yapar? | Örnek | Bölüm |
|---|---|---|---|
| `ENV` | Ortam değişkeni tanımlar (çalışırken de geçerli). | `ENV APP_ENV=production` | 08 |
| `ARG` | Yalnızca derleme sırasında geçerli değişken. | `ARG VERSION=1.0` | 08 |
| `EXPOSE` | Programın dinlediği portu belgeler. | `EXPOSE 8000` | 07 |
| `USER` | Sonraki komutları hangi kullanıcının çalıştıracağı. | `USER app` | 13 |
| `VOLUME` | Verinin saklanacağı klasörü işaretler. | `VOLUME /data` | 09 |
| `LABEL` | İmaja bilgi etiketi ekler (yazar, sürüm). | `LABEL version="1.0"` | — |
| `HEALTHCHECK` | Konteynerin sağlıklı olup olmadığını denetleyen komut. | `HEALTHCHECK CMD curl -f http://localhost/` | 11 |

## Az kullanılanlar

| Talimat | Ne yapar? |
|---|---|
| `ADD` | `COPY` gibi, ama sıkıştırılmış dosyaları açabilir ve adresten indirebilir. Gerekmedikçe `COPY` tercih edilir. |
| `SHELL` | `RUN`'ın hangi kabukla çalışacağını değiştirir. |
| `STOPSIGNAL` | `docker stop`'un gönderdiği sinyali değiştirir. |
| `ONBUILD` | Bu imajdan başka bir imaj kurulurken çalışacak talimat. |

## Sık yapılan hatalar

- **`FROM` ilk satırda değil.** Dockerfile (yorumlar ve `ARG` dışında) `FROM`
  ile başlamalı.
- **Yazım hatası:** `FORM`, `COPPY`, `WORKIDR`. Docker "unknown instruction"
  der; Odyssey hangi satır olduğunu söylüyor.
- **Programı `RUN` ile çalıştırmak.** Program imaj kurulurken bir kez
  çalışır; konteyner açılınca çalışacak olan `CMD`.
- **Birden fazla `CMD`.** Yalnızca sonuncusu geçerli; öncekiler sessizce yok
  sayılıyor.
