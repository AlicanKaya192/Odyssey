## `CORSMiddleware` ayarları

| Ayar | Ne demek? |
|---|---|
| `allow_origins=["https://site.com"]` | Hangi sitelerin sayfaları çağırabilir |
| `allow_methods=["GET", "POST"]` | Hangi yöntemlere izin var |
| `allow_headers=["*"]` | Hangi başlıklar gönderilebilir (`Authorization` gibi) |
| `allow_credentials=True` | Çerez/kimlik bilgisiyle istek; o zaman `allow_origins` `*` olamaz |

**Köken** (origin) = şema + ad + port: `https://library.example.com` ile
`http://library.example.com` farklı kökenler; `http://127.0.0.1:8000` ile
`http://127.0.0.1:5173` de.

## Ön soru (preflight)

Tarayıcı `POST` + JSON gibi "basit olmayan" isteklerden önce aynı adrese
`OPTIONS` gönderir: "bu yöntemle, bu başlıklarla gelebilir miyim?"
Ölçtük: izinli kökene `200` ve `access-control-allow-methods: GET, POST`,
izinsiz kökene `400 Disallowed CORS origin`. Ön soru düşerse tarayıcı asıl
isteği hiç göndermez.

## CORS hatası görünce

Tarayıcının geliştirici konsolunda "blocked by CORS policy" yazıyorsa:

1. Sayfanın kökeni `allow_origins`'te mi (port dahil)?
2. Yöntem `allow_methods`'ta mı?
3. Gönderilen başlık (`Authorization`) `allow_headers`'ta mı?

## Ara katmanın sırası

```python
@app.middleware("http")
async def mw(request, call_next):
    # 1) istek uç noktaya gitmeden önce
    response = await call_next(request)
    # 2) cevap istemciye gitmeden önce
    return response
```

Birden fazla ara katman varsa en son eklenen en dışta çalışır: isteği ilk
o görür, cevabı en son o. Hata yakalayıcılar ve bağımlılıklar ara katmanın
**içinde** çalışır.

## Ara katman mı, bağımlılık mı?

| İş | Uygun olan |
|---|---|
| Her cevaba başlık eklemek, süre ölçmek | Ara katman |
| Bazı uç noktalarda anahtar denetimi | Bağımlılık |
| Kullanıcıyı bulup uç noktaya vermek | Bağımlılık |
