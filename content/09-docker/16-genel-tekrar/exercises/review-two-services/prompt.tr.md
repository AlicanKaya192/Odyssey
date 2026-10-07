`api` klasöründe Paketleme bölümündeki not API'si (Dockerfile'ında
`HEALTHCHECK` var), `client` klasöründe ona bir kez istek atıp sonucu
yazan bir program duruyor. `compose.yaml`'ı yaz.

**Yapman gerekenler:**

1. `api` servisi: `./api`'den kurulsun, `notes-data` volume'u `/data`'ya
   bağlansın.
2. `client` servisi: `./client`'tan kurulsun ve **api sağlıklı olunca**
   başlasın (`condition: service_healthy`).
3. `notes-data` volume'unu en altta tanımla.

`client` api hazır olmadan başlarsa `Connection refused` ile düşer.

**Beklenen çıktı (client):**

```
notes: 0 starts: 1
```
