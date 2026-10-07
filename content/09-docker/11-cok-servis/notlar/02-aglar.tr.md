Compose'un varsayılan ağı çoğu proje için yeterli. Daha fazlası gerektiğinde
bilmen gerekenler.

## Ağları ayırmak

Web servisi API'ye, API veritabanına ulaşmalı; ama web servisi veritabanına
**doğrudan** ulaşmamalı. İki ağla:

```yaml
services:
  web:
    build: ./web
    networks: [frontend]
  api:
    build: ./api
    networks: [frontend, backend]
  db:
    image: postgres:17
    networks: [backend]

networks:
  frontend:
  backend:
```

`api` iki ağda birden; `web` ile `db` ortak bir ağda olmadığı için birbirini
göremiyor. Bir saldırgan web servisini ele geçirse bile veritabanına giden
yol kapalı.

## Konteynerden bilgisayarına ulaşmak

Konteynerin içinde `localhost` konteynerin kendisi. Bilgisayarında çalışan
bir programa (ör. Docker dışında kurulu bir veritabanı) ulaşmak için Docker
Desktop özel bir ad veriyor:

```text
http://host.docker.internal:5432
```

Linux'ta bu ad kendiliğinden yok; `--add-host=host.docker.internal:host-gateway`
ile ekleniyor.

## Ağ komutları

| Komut | Ne yapar? |
|---|---|
| `docker network ls` | Ağları listeler (`bridge`, `host`, `none` hazır gelir) |
| `docker network create ad` | Yeni ağ |
| `docker network inspect ad` | Bağlı konteynerler ve adresleri |
| `docker network connect ad konteyner` | Çalışan konteyneri bir ağa da bağlar |
| `docker network rm ad` | Siler (bağlı konteyner yoksa) |
| `docker network prune` | Kullanılmayan ağları siler |

## Hazır ağlar

- **bridge**: `--network` verilmeyen konteynerlerin ağı. Ad çözümü yok;
  konteynerler birbirini adıyla bulamıyor.
- **host**: konteyner bilgisayarın ağını doğrudan kullanır (Linux'ta); ayrılık
  kalkar. Odyssey alıştırmalarında izin verilmiyor.
- **none**: hiç ağ yok.

## Hata ayıklama

İki servis birbirine ulaşamıyorsa:

1. İkisi de aynı ağda mı? `docker network inspect proje_default`.
2. Adı doğru mu? (`apii` değil `api`.)
3. Hedef servis `0.0.0.0`'ı mı dinliyor? (Portlar bölümü.)
4. Hedef servis hazır mı? (`healthcheck`.)
