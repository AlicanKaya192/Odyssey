Bu bölümün bütün komutları tek sayfada. Ezberlemen gerekmiyor; zamanla
parmakların öğrenecek.

## Çalıştırmak: `docker run`

```text
docker run [seçenekler] imaj [komut]
```

| Seçenek | Uzun adı | Ne yapar? |
|---|---|---|
| `--name web` | | Konteynere ad verir. |
| `--rm` | | Konteyner bitince kendiliğinden siler. |
| `-d` | `--detach` | Arka planda çalıştırır, terminali geri verir. |
| `-i` | `--interactive` | Klavyeden yazılanı konteynere iletir. |
| `-t` | `--tty` | Konteynere terminal verir. |
| `-it` | | `-i` ve `-t` birlikte: içine girmek için. |

Kısa seçenekler birleştirilebilir: `-d -i -t` yerine `-dit`. Seçenekler
**imajın adından önce** yazılır; imajdan sonra gelen her şey konteynerin
komutu sayılır.

```text
docker run --rm alpine:3.22 echo hi        # doğru: --rm Docker'ın seçeneği
docker run alpine:3.22 --rm echo hi        # yanlış: --rm konteynere komut olarak gider
```

## Listelemek

| Komut | Ne gösterir? |
|---|---|
| `docker ps` | Çalışan konteynerler |
| `docker ps -a` | Bitmişler dahil hepsi |
| `docker ps -q` | Yalnızca kimlikler (başka komutlara vermek için) |

## Çalışan konteynerle

| Komut | Ne yapar? |
|---|---|
| `docker logs ad` | Konteynerin bugüne kadarki çıktısı |
| `docker logs -f ad` | Çıktıyı canlı izler (Ctrl+C ile çık) |
| `docker logs --tail 20 ad` | Yalnızca son 20 satır |
| `docker exec ad komut` | Çalışan konteynerde bir komut çalıştırır |
| `docker exec -it ad sh` | Çalışan konteynerin içine kabukla girer |

## Durdurmak ve silmek

| Komut | Ne yapar? |
|---|---|
| `docker stop ad` | Durdurur (programa kapanması için süre verir) |
| `docker start ad` | Durmuş konteyneri yeniden başlatır |
| `docker restart ad` | Durdurup yeniden başlatır |
| `docker rm ad` | Durmuş konteyneri siler |
| `docker rm -f ad` | Çalışıyor olsa da zorla siler |
| `docker container prune` | Durmuş konteynerlerin hepsini siler (onay ister) |

## Konteyneri göstermenin yolları

Bir konteyneri üç biçimde gösterebilirsin:

- adıyla: `docker stop sleeper`,
- kimliğinin tamamıyla,
- kimliğinin başıyla: `docker stop 3b8f` (başka bir kimlik aynı harflerle
  başlamadıkça).

## `run` mı, `start` mı, `exec` mi?

- `run` → **yeni** bir konteyner oluşturur ve çalıştırır.
- `start` → **var olan, durmuş** bir konteyneri yeniden çalıştırır.
- `exec` → **var olan, çalışan** bir konteynerin içinde ek bir komut
  çalıştırır.
