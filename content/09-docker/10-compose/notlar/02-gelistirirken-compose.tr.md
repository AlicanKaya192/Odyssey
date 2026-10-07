Compose yalnızca yayın için değil, geliştirirken de günlük aracın. Birkaç
alışkanlık.

## Kod değişince ne yapmalı?

Kodu imaja `COPY` ile koyuyorsan değişiklik ancak yeniden kurunca görünür:

```text
docker compose up -d --build
```

Önbellek sayesinde yalnızca değişen katman yeniden kuruluyor; birkaç saniye.

## Geliştirirken bind mount

Her değişiklikte kurmak istemiyorsan kodu bind mount ile bağla:

```yaml
services:
  web:
    build: .
    volumes:
      - ./:/app
```

Compose'da `./` compose.yaml'ın bulunduğu klasör; Windows'ta da çalışıyor.
Kodu düzenleyip yalnızca konteyneri yeniden başlatmak yetiyor
(`docker compose restart web`).

## Geliştirme ve yayın ayrı dosyada

Aynı projede iki ayrı ayar gerekiyorsa:

- `compose.yaml`: her yerde ortak olan.
- `compose.override.yaml`: yalnızca geliştirme (bind mount, ayrıntılı
  günlük). Compose bu dosyayı **kendiliğinden** okuyup üstüne ekliyor.

Yayında yalnızca ana dosyayı kullanmak için:
`docker compose -f compose.yaml up -d`.

## Tek seferlik komutlar: `run`

Bir servisin imajında tek seferlik bir iş:

```text
docker compose run --rm web python manage.py migrate
```

`exec` çalışan konteynerde, `run` yeni bir konteynerde çalıştırıyor (aynı
`docker exec` / `docker run` farkı).

## Sık hatalar

| Belirti | Sebep |
|---|---|
| `port is already allocated` | Aynı port başka bir projede ya da programda açık. |
| `undefined volume` | Adlı volume en alttaki `volumes:` altında yazılmamış. |
| Değişikliğim görünmüyor | `--build` unutuldu ya da kod imaja `COPY` ile kopyalanıyor. |
| `did not find expected key` | YAML girintisi bozuk (sekme ya da kayık satır). |
| Servis hemen `Exited` | `docker compose logs servis` ile son satırlara bak. |

## Her şeyi temizlemek

```text
docker compose down --rmi local -v
```

Konteynerler, ağ, Compose'un kurduğu imajlar ve volume'lar: proje sıfırdan
başlar. Veri de gider; dikkat.
