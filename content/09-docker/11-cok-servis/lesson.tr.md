# Çok Servisli Uygulamalar: Ağ ve Bağımlılıklar

Gerçek uygulamalar tek konteynerden oluşmuyor: bir web arayüzü, arkasında bir
API, onun arkasında bir veritabanı, belki bir önbellek. Her biri kendi
konteynerinde, kendi imajıyla. Bu bölümde servislerin birbirini nasıl
bulduğunu, hangisinin önce başlayacağını ve "hazır" olmanın ne demek
olduğunu öğreneceğiz.

## Proje

İki servisli küçük bir mağaza:

```text
shop/
├── compose.yaml
├── api/          # ürün sayısını JSON olarak veren API
│   ├── Dockerfile
│   └── server.py
└── web/          # API'ye istek atıp sonucu yazan istemci
    ├── Dockerfile
    └── client.py
```

```yaml
services:
  api:
    build: ./api
  web:
    build: ./web
```

`build: ./api` → imaj `api` klasöründeki Dockerfile'dan.

## Servisler birbirini adıyla bulur

Compose her projeye bir ağ kuruyor (`shop_default`) ve servisleri o ağa
bağlıyor. Ağın içinde **her servisin adı bir adres**: `web` konteyneri API'ye
şu adresle ulaşıyor:

```text
http://api:8000/
```

Docker'ın ağı içinde küçük bir **ad çözücü** (DNS) var: `api` adını o
servisin konteynerinin adresine çeviriyor. IP adresi bilmen gerekmiyor;
konteyner yeniden oluşturulup adresi değişse de ad aynı.

<figure class="fig">
  <div class="flow">
    <span class="node">web<br><small>http://api:8000</small></span><span class="arrow">→ ad çözücü →</span>
    <span class="node acc">api<br><small>shop_default ağında</small></span>
  </div>
  <div class="flow">
    <span class="node no">web<br><small>http://localhost:8000</small></span><span class="arrow">→</span>
    <span class="node no">web'in kendisi<br><small>Connection refused</small></span>
  </div>
  <figcaption>Aynı ağdaki servisler birbirini adıyla buluyor. <code>localhost</code> her konteynerde o konteynerin kendisi.</figcaption>
</figure>

Gerçek denemenin çıktısı (`web`, üç adrese istek attı; satır başlarındaki `web-1  |` öneklerini çıkardık):

```text
http://api:8000/ {'items': 3}
http://localhost:8000/ ERROR <urlopen error [Errno 111] Connection refused>
http://apii:8000/ ERROR <urlopen error [Errno -5] No address associated with hostname>
```

- `api` → çalıştı.
- `localhost` → **reddedildi.** `web` konteynerinde `localhost` `web`'in
  kendisi; orada 8000'i dinleyen kimse yok. En sık yapılan hata.
- `apii` → **böyle bir ad yok.** Yazım hatası; ad çözücü bulamadı.

## Dışarıya açmak gerekmiyor

`api`'nin `ports:` satırı yok, ama `web` ona ulaşıyor. Servisler aynı ağda
birbirinin **bütün portlarını** görüyor. `ports:` yalnızca **senin
bilgisayarından** (dışarıdan) ulaşılacak servis için gerekiyor; genellikle
yalnızca en öndeki web servisi.

Veritabanını dışarıya açmamak bir güvenlik kazancı: ona yalnızca aynı ağdaki
uygulama ulaşabiliyor.

## Başlama sırası: `depends_on`

`web` başlar başlamaz API'ye istek atıyorsa, API ondan önce başlamış
olmalı:

```yaml
  web:
    build: ./web
    depends_on:
      - api
```

Compose önce `api`'yi, sonra `web`'i başlatıyor. Ama dikkat: bu yalnızca
**başlatma** sırası. API konteynerinin başlaması, içindeki programın istek
kabul etmeye **hazır** olduğu anlamına gelmiyor. Bizim API'miz açılışta üç
saniye hazırlık yapıyor; bu sürede gelen istek reddediliyor.

## Hazır olmak: `healthcheck`

Bir servisin "hazır mı?" sorusuna cevap veren komut **sağlık denetimi**
(healthcheck). Docker bu komutu belli aralıklarla çalıştırıyor; komut
başarılıysa (0 koduyla bitiyorsa) servis **healthy** (sağlıklı) sayılıyor.

```yaml
  api:
    build: ./api
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - import urllib.request; urllib.request.urlopen('http://localhost:8000')
      interval: 2s
      timeout: 3s
      retries: 10
      start_period: 2s
```

- `test`: denetim komutu; liste biçiminde, her parça ayrı satırda (köşeli parantezli yazımla aynı). `python:3.13-slim`'de `curl` yok; Python'un kendi
  `urllib`'i kullanıldı. Burada `localhost` doğru: komut **API'nin kendi
  konteynerinde** çalışıyor.
- `interval`: kaç saniyede bir denensin.
- `timeout`: bir deneme en fazla ne kadar sürsün.
- `retries`: art arda kaç başarısızlıktan sonra "unhealthy" denecek.
- `start_period`: açılışta başarısızlıkların sayılmadığı süre.

Şimdi `web` API'nin **sağlıklı** olmasını beklesin:

```yaml
  web:
    build: ./web
    depends_on:
      api:
        condition: service_healthy
```

```text
 Container shop-api-1 Waiting
 Container shop-api-1 Healthy
 Container shop-web-1 Started
```

`docker compose ps` sağlık durumunu da gösteriyor:
`Up 9 seconds (healthy)`.

<figure class="fig">
  <div class="flow">
    <span class="node">api başladı<br><small>starting</small></span><span class="arrow">→ test başarılı →</span>
    <span class="node ok">api sağlıklı<br><small>healthy</small></span><span class="arrow">→</span>
    <span class="node acc">web başlıyor<br><small>condition: service_healthy</small></span>
  </div>
  <figcaption><code>depends_on</code> tek başına yalnızca sırayı veriyor; sağlık koşuluyla <code>web</code> API gerçekten hazır olana kadar bekliyor.</figcaption>
</figure>

## Compose olmadan ağ

Compose'un yaptığını elle de yapabilirsin:

```text
docker network create shopnet
docker run -d --name api --network shopnet shop-api
docker run --rm --network shopnet shop-web
```

Aynı ağa bağlanan konteynerler birbirini `--name` ile verilen adla buluyor.
Varsayılan ağda (adı `bridge`) ad çözümü **yok**; bu yüzden kendi ağını
oluşturmak gerekiyor. Compose bunu senin yerine yapıyor.

```text
docker network ls
docker network inspect shopnet
```

## Özet

- Compose her projeye bir ağ kurar; servisler birbirini **adıyla** bulur:
  `http://api:8000`.
- Konteynerde `localhost` o konteynerin kendisi: başka servis için
  `localhost` yazmak `Connection refused` verir.
- Servisler aynı ağda birbirinin portlarına ulaşır; `ports:` yalnızca
  dışarıdan ulaşılacak servis için.
- `depends_on` başlatma sırasını belirler; **hazır olmayı** beklemek için
  `healthcheck` + `condition: service_healthy`.
- Compose dışında: `docker network create` + `--network`.
