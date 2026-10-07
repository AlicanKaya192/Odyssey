Docker'ın en yaygın kullanımlarından biri, bir veritabanını bilgisayara
kurmadan konteynerde çalıştırmak. Verinin nerede durduğunu bilmek burada
hayati.

## Resmî veritabanı imajları verilerini nerede tutar?

| İmaj | Veri klasörü |
|---|---|
| `postgres` | `/var/lib/postgresql/data` |
| `mysql` | `/var/lib/mysql` |
| `mongo` | `/data/db` |
| `redis` | `/data` |

İmajın Docker Hub sayfası bunu yazıyor ("Where to Store Data"). O klasöre bir
volume bağlanmazsa veri konteynerin yazılabilir katmanında kalıyor ve
konteyner silinince gidiyor.

## Örnek: PostgreSQL

Bu komut bu patikada çalıştırılmıyor (`postgres` imajı ayrıca iniyor), ama
düzeni böyle:

```text
docker volume create pgdata
docker run -d --name db -e POSTGRES_PASSWORD=secret `
  -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres:17
```

- Veri `pgdata` volume'unda.
- `docker rm -f db` ve aynı komutla yeniden çalıştırmak: tablolar yerinde.
- Yeni bir PostgreSQL sürümüne geçmek: imajın etiketini değiştir, volume
  aynı.

## SQLite: dosya bir volume'da

Küçük uygulamalarda veritabanı tek bir dosya (SQLite). Kural aynı: dosyayı
volume'a bağlı bir klasöre koy.

```python
import sqlite3

con = sqlite3.connect("/data/app.db")
```

```text
docker run -d -v appdata:/data app
```

Dosya `/app/app.db` olsaydı her güncellemede sıfırlanırdı.

## Volume'u silmeden önce

- `docker volume rm` ve `docker volume prune` veriyi geri getirilemez
  şekilde siliyor.
- Önce yedek al (Volume dersindeki `tar` komutu).
- `docker compose down` volume'lara dokunmuyor; `docker compose down -v`
  siliyor (Compose bölümü).
