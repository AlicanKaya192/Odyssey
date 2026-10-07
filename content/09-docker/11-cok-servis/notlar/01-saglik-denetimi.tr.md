Sağlık denetimi bir servisin "çalışıyor" değil "işini yapabiliyor" olduğunu
söylüyor. Yazarken işe yarayan kalıplar.

## İki yerde yazılabilir

**compose.yaml'da** (bu bölümdeki gibi), ya da **Dockerfile'da** `HEALTHCHECK`
talimatıyla; o zaman imajın kendisi denetimi taşıyor ve her yerde geçerli:

```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8000/health')"
```

İkisi birden varsa compose.yaml'daki geçerli.

## Durumlar

| Durum | Anlamı |
|---|---|
| `starting` | `start_period` içinde; henüz karar yok |
| `healthy` | Son denemeler başarılı |
| `unhealthy` | `retries` kadar art arda başarısız |

`docker ps` ve `docker compose ps` durumu yazıyor: `Up 2 minutes (healthy)`.
Ayrıntı, denemelerin çıktılarıyla birlikte:

```text
docker inspect --format "{{json .State.Health}}" shop-api-1
```

## Neyi denetlemeli?

- Web servisi için: kendi `/health` adresi; `200` dönüyorsa sağlıklı.
- `/health` ucunu programın içinde ucuz tut: veritabanına bağlanabiliyor mu,
  gerekli dosya var mı. Ağır bir iş yapma; birkaç saniyede bir çalışıyor.
- Komut **denetlenen konteynerin içinde** çalışıyor: `localhost` doğru adres.

## `curl` yoksa

`python:3.13-slim` ve `alpine` imajlarında `curl` yok (alpine'da `wget`
var). Python imajlarında en kolayı:

```text
python -c "import urllib.request as u; u.urlopen('http://localhost:8000/health')"
```

Yanıt 4xx/5xx ise ya da bağlanamazsa `urlopen` hata fırlatıyor, Python 1
koduyla çıkıyor → denetim başarısız.

## Sağlıksız olunca ne olur?

Docker kendiliğinden **yeniden başlatmıyor**; yalnızca durumu yazıyor.
`depends_on: condition: service_healthy` bekleyen servis başlamıyor. Büyük
sistemler (Kubernetes gibi) sağlıksız konteyneri yeniden başlatıyor; Compose
tek başına yapmıyor.
