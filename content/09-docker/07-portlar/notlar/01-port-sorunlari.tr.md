Konteynerdeki sunucuya ulaşamıyorsan bu sırayla bak. Her adım bir öncekini
eliyor.

## 1. Konteyner çalışıyor mu?

```text
docker ps
```

Listede yoksa program başlar başlamaz çökmüş. `docker ps -a` ile durumuna,
`docker logs ad` ile son yazdıklarına bak.

## 2. Port yayınlanmış mı?

`docker ps`'in PORTS sütunu:

| Görünen | Anlamı |
|---|---|
| `0.0.0.0:8080->8000/tcp` | Yayınlanmış: bilgisayarın 8080'i → konteynerin 8000'i |
| `8000/tcp` | Yalnızca `EXPOSE` edilmiş, **yayınlanmamış** (`-p` unutulmuş) |
| (boş) | Ne EXPOSE ne `-p` |

## 3. Doğru porta mı gidiyorsun?

Tarayıcıya **sol taraftaki** numarayı yazıyorsun: `-p 8080:8000` ise
`localhost:8080`. Sağdaki numara konteynerin içi için.

## 4. Program doğru portu mu dinliyor?

`-p 8080:8000` yazdın ama program 5000'i dinliyorsa istek boşluğa gidiyor.
Programın kendi günlüğüne bak; çoğu sunucu açılırken portunu yazıyor:

```text
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

## 5. Program 0.0.0.0'ı mı dinliyor?

Günlükte `127.0.0.1` ya da `localhost` görüyorsan sorun bu:

| Hata | Büyük ihtimalle |
|---|---|
| `Could not connect to server` | Port yayınlanmamış ya da konteyner çalışmıyor |
| `Empty reply from server` / `connection reset` | Port yayınlanmış ama program 127.0.0.1'i dinliyor |
| `port is already allocated` | Ana makine portu başkası tarafından tutuluyor |

## 6. İçeriden dene

Konteynerin içinden istek atmak sorunun dışarıda mı içeride mi olduğunu
ayırıyor:

```text
docker exec -it web python
>>> import urllib.request
>>> urllib.request.urlopen("http://127.0.0.1:8000").status
200
>>> exit()
```

İçeriden `200` geliyorsa program çalışıyor; sorun yayınlamada ya da dinlenen adreste.

## Odyssey'de

Odyssey HTTP kontrolünde konteyneri rastgele boş bir ana makine portuna
yayınlıyor ve istek atıyor. "Ulaşılamadı" mesajı alırsan önce 4. ve 5.
adımlara bak.
