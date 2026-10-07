# Docker Compose'a Giriş

Bir web uygulamasını çalıştıran komut büyüdükçe büyüyor:

```text
docker run -d --name web -p 8080:8000 -e APP_ENV=production `
  -e DB_PATH=/data/app.db -v appdata:/data --restart unless-stopped notesapi
```

Her seferinde bunu doğru yazmak zor, bir yere not etmek gerekiyor ve iki
üç konteyner birlikte çalışacaksa (uygulama + veritabanı + önbellek) iş
içinden çıkılmaz hâle geliyor. **Docker Compose** bütün bunları tek bir
dosyada, okunabilir biçimde topluyor ve tek komutla çalıştırıyor.

## İlk compose.yaml

Proje klasöründe `Dockerfile`'ın yanına `compose.yaml`:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8000"
    environment:
      APP_ENV: production
```

- `services:` çalışacak konteynerlerin listesi. Her birine **servis**
  deniyor; burada tek servis var: `web`.
- `build: .` imajı bu klasördeki Dockerfile'dan kur (`docker build .`).
- `ports:` `-p` ile aynı: `"bilgisayar:konteyner"`.
- `environment:` `-e` ile aynı.

Çalıştır:

```text
docker compose up -d --build
```

```text
 Network notesapi_default Created
 Container notesapi-web-1 Created
 Container notesapi-web-1 Started
```

`up` imajı kurdu (`--build`: değiştiyse yeniden kur), bir **ağ** oluşturdu ve
konteyneri arka planda (`-d`) başlattı. Tarayıcıda `localhost:8080`.

## Adlar nereden geliyor?

- **Proje adı:** compose.yaml'ın bulunduğu klasörün adı (`notesapi`).
- **Konteyner:** `proje-servis-numara` → `notesapi-web-1`.
- **İmaj:** `proje-servis` → `notesapi-web`.
- **Ağ:** `proje_default` → `notesapi_default`. Servisler bu ağda birbirini
  görüyor (bir sonraki bölüm).

## YAML'ı okumak

compose.yaml **YAML** biçiminde: girintiyle iç içe yazılan ayarlar.

<figure class="fig">
  <div class="anat">
    <div class="sig"><code>services: / web: / ports: / - "8090:8000"</code></div>
    <div class="anat-row"><span>services:</span><span>En üst düzey anahtar; girintisiz.</span></div>
    <div class="anat-row"><span>  web:</span><span>Servisin adı; iki boşluk içeride. Adı sen seçiyorsun.</span></div>
    <div class="anat-row"><span>    ports:</span><span>web'in bir ayarı; dört boşluk içeride.</span></div>
    <div class="anat-row"><span>      - "8090:8000"</span><span>Listenin bir öğesi; <code>- </code> ile başlıyor, tırnak içinde.</span></div>
  </div>
  <figcaption>Girinti kimin kimin içinde olduğunu söylüyor. Sekme değil boşluk.</figcaption>
</figure>

Kurallar:

- Girinti **boşlukla**, sekmeyle (Tab) değil. Aynı düzeydeki satırlar aynı
  sütunda başlar. Genellikle iki boşluk.
- `anahtar: değer` (iki noktadan sonra bir boşluk).
- Liste öğesi `- ` ile başlar.
- `"8080:8000"` gibi iki noktalı sayıları **tırnak içinde** yaz: YAML bazı
  durumlarda `22:22` gibi değerleri saat/dakika sayısına çevirebiliyor.

Girinti bozulunca Compose ne dediğini anlayamıyor:

```text
go-yaml load error in parser (while parsing a block mapping) at L2.C3-L4.C4:
did not find expected key
```

`L4` → 4. satır. Odyssey de aynı hatayı satır numarasıyla gösteriyor.

## Temel komutlar

| Komut | Ne yapar? | Tek konteynerdeki karşılığı |
|---|---|---|
| `docker compose up -d` | Bütün servisleri arka planda başlatır | `docker run -d ...` |
| `docker compose up -d --build` | Önce imajları (gerekiyorsa) kurar | `docker build` + `run` |
| `docker compose ps` | Projenin konteynerleri | `docker ps` |
| `docker compose logs -f web` | Bir servisin günlüğü (canlı) | `docker logs -f` |
| `docker compose exec web sh` | Çalışan servisin içinde komut | `docker exec -it` |
| `docker compose down` | Konteynerleri ve ağı siler | `docker rm -f` |
| `docker compose down -v` | Volume'ları da siler (**veri gider**) | |
| `docker compose config` | Dosyayı denetleyip tam hâlini yazar | |

`docker compose ps`:

```text
NAME             IMAGE          SERVICE   STATUS          PORTS
notesapi-web-1   notesapi-web   web       Up 2 seconds    0.0.0.0:8080->8000/tcp
```

(Sığsın diye `COMMAND` ve `CREATED` sütunlarını çıkardık.)

`docker compose logs` satırların başına servisin adını koyuyor; birden çok
servis olunca kimin ne yazdığı belli oluyor:

```text
web-1  | 172.18.0.1 - - [06/Oct/2026 19:58:57] "GET / HTTP/1.1" 200 -
```

## `docker run` → compose.yaml

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>-p 8080:8000</span><span><code>ports: ["8080:8000"]</code></span></div>
    <div class="anat-row"><span>-e APP_ENV=production</span><span><code>environment: { APP_ENV: production }</code></span></div>
    <div class="anat-row"><span>--env-file .env</span><span><code>env_file: .env</code></span></div>
    <div class="anat-row"><span>-v appdata:/data</span><span><code>volumes: ["appdata:/data"]</code> + en altta <code>volumes: { appdata: }</code></span></div>
    <div class="anat-row"><span>--restart unless-stopped</span><span><code>restart: unless-stopped</code></span></div>
    <div class="anat-row"><span>imaj adı / docker build .</span><span><code>image: ...</code> ya da <code>build: .</code></span></div>
  </div>
  <figcaption>Her <code>docker run</code> seçeneğinin compose.yaml'da bir anahtarı var.</figcaption>
</figure>

Uzun `docker run` komutunun bütün parçalarının compose.yaml'da bir karşılığı
var:

```yaml
services:
  web:
    build: .
    ports:
      - "8080:8000"
    environment:
      APP_ENV: production
      DB_PATH: /data/app.db
    volumes:
      - appdata:/data
    restart: unless-stopped

volumes:
  appdata:
```

- `volumes:` (servisin altında) `-v` ile aynı. Adlı volume kullanılıyorsa
  dosyanın **en altında** da `volumes:` altında adı yazılıyor.
- `restart: unless-stopped` konteyner çökerse ya da bilgisayar yeniden
  başlarsa onu tekrar başlat (sen `stop` demedikçe).
- `env_file: .env` bir dosyadan ortam değişkeni (`--env-file`).
- `image: python:3.13-slim` kurmak yerine hazır bir imaj kullan.

## `down` ne siler, ne bırakır?

- `docker compose down` konteynerleri ve ağı siliyor; **imajlar ve
  volume'lar kalıyor**. Bir sonraki `up` aynı veriyle başlıyor.
- `docker compose down -v` volume'ları da siliyor: veritabanı sıfırlanıyor.
  Bilerek kullan.

## Özet

- Compose, `docker run`'ın bütün seçeneklerini bir dosyada (`compose.yaml`)
  topluyor; dosya projeyle birlikte saklanıyor.
- `services:` altında her servis: `build` ya da `image`, `ports`,
  `environment`, `volumes`, `restart`.
- `docker compose up -d --build` başlatır, `ps` / `logs` / `exec` izler,
  `down` siler (`-v` volume'larla birlikte).
- Adlar: proje = klasör, konteyner `proje-servis-1`, ağ `proje_default`.
- YAML: boşlukla girinti, `anahtar: değer`, liste `- `, iki noktalı sayılar
  tırnakta. `docker compose config` dosyayı denetler.
