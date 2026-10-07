# Ortam Değişkenleri ve Yapılandırma

Aynı program farklı yerlerde farklı ayarlarla çalışıyor: senin
bilgisayarında deneme veritabanına, sunucuda gerçek veritabanına bağlanıyor;
geliştirirken ayrıntılı günlük yazıyor, yayında az. Bu ayarlar için her yere
ayrı imaj kurmak istemiyoruz. **Bir imaj, farklı ayarlar** demenin yolu
**ortam değişkenleri**.

## Ortam değişkeni nedir?

İşletim sisteminin bir programa başlarken verdiği **ad = değer** çiftleri.
Program bunları okuyup davranışını ayarlıyor. Python'da:

```python
import os

env = os.environ.get("APP_ENV", "development")
port = int(os.environ.get("PORT", "8000"))
print("env:", env, "port:", port)
```

- `os.environ.get("AD", "varsayılan")`: değişken yoksa varsayılan.
- Değerler **her zaman metin**; sayı gerekiyorsa `int(...)`.

## Çalıştırırken vermek: `-e`

```text
docker run --rm -e APP_ENV=production -e PORT=9000 app
```

```text
env: production port: 9000
```

Aynı imaj, `-e` olmadan `env: development port: 8000` yazıyor. İmaj
değişmedi; yalnızca ona verilen ayar değişti.

Birçok değişken için bir dosya (`--env-file`):

```text
# app.env
APP_ENV=staging
DB_HOST=db
```

```text
docker run --rm --env-file app.env app
```

Dosyada her satır `AD=değer`; `#` ile başlayan satır yorum, tırnak
gerekmiyor.

`-e AD` (değersiz) bilgisayarındaki aynı adlı değişkenin değerini aktarıyor.
PowerShell'de önce `$env:APP_ENV = "test"`, sonra `docker run -e APP_ENV app`.

## İmaja varsayılan koymak: `ENV`

```dockerfile
ENV APP_ENV=production
ENV PYTHONUNBUFFERED=1
```

`ENV` imaja bir **varsayılan** yazıyor; o imajdan çalışan her konteynerde
var. `-e` ile verilen değer `ENV`'i **eziyor**:

```text
docker run --rm app                          # env=production (ENV'den)
docker run --rm -e APP_ENV=development app   # env=development (-e kazanır)
```

<figure class="fig">
  <div class="flow">
    <span class="node">Programın varsayılanı<br><small>os.environ.get(..., "development")</small></span><span class="arrow">←</span>
    <span class="node acc">İmajdaki ENV<br><small>APP_ENV=production</small></span><span class="arrow">←</span>
    <span class="node ok">Çalıştırırken -e<br><small>-e APP_ENV=staging</small></span>
  </div>
  <figcaption>Sağdaki soldakini eziyor: <code>-e</code> varsa o, yoksa imajdaki <code>ENV</code>, o da yoksa programın kendi varsayılanı.</figcaption>
</figure>

Python imajlarında sık görülen iki `ENV`:

| Değişken | Ne yapar? |
|---|---|
| `PYTHONUNBUFFERED=1` | `print` çıktısını bekletmeden yazar; `docker logs` hemen görür. |
| `PYTHONDONTWRITEBYTECODE=1` | `__pycache__` / `.pyc` dosyası oluşturmaz. |

## Yalnızca derlemede: `ARG`

`ARG` **yalnızca `docker build` sırasında** geçerli bir değişken:

```dockerfile
FROM alpine:3.22
ARG VERSION=1.0
RUN echo "building $VERSION" > /version.txt
```

```text
docker build --build-arg VERSION=2.1 -t app .
```

`RUN` satırı `2.1`'i görüyor; ama **konteyner çalışırken `VERSION` yok**:

```text
docker run --rm app sh -c 'echo version=$VERSION'
version=
```

Çalışırken de gerekiyorsa `ENV`'e aktarılır: `ENV APP_VERSION=$VERSION`.

| | `ARG` | `ENV` |
|---|---|---|
| Ne zaman geçerli? | Yalnızca derlemede | Derlemede ve çalışırken |
| Nasıl değiştirilir? | `--build-arg AD=değer` | `-e AD=değer` |
| İmajda görünür mü? | `docker history`'de evet | `docker image inspect`'te evet |

## Sırlar ne ENV'e ne ARG'a

Şifre ya da API anahtarını imaja koymanın iki "kolay" yolu var; ikisi de
yanlış. Bir `ARG` ile derleme yapıp imajın geçmişine bakalım:

```text
docker build --build-arg TOKEN=s3cret -t app .
docker history app --format "{{.CreatedBy}}"
```

```text
RUN |2 TOKEN=s3cret VERSION=2.1 /bin/sh -c echo "building $VERSION" ...
```

Sır **açıkça** imajın geçmişinde duruyor. `ENV` ile koysaydık
`docker image inspect` onu gösterirdi. İmajı alan herkes okuyabilir.

Doğru yol: **sırrı imaja koyma, çalıştırırken ver.**

- `docker run --env-file secrets.env app` (dosya `.dockerignore`'da ve
  `.gitignore`'da olmalı),
- Compose'da `env_file:` (Compose bölümü),
- büyük sistemlerde sır yöneticileri (Docker secrets, bulut sağlayıcının sır
  kasası).

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>İmajın içinde</h4><p><code>ENV API_KEY=...</code> → <code>docker image inspect</code> gösterir</p><p><code>ARG TOKEN=...</code> → <code>docker history</code> gösterir</p><p>İmajı alan herkes okur</p></div>
    <div class="ok"><h4>Çalıştırırken</h4><p><code>docker run --env-file secrets.env app</code></p><p>Dosya <code>.gitignore</code> ve <code>.dockerignore</code>'da</p><p>İmaj paylaşılsa da sır gitmez</p></div>
  </div>
  <figcaption>Kural: sır imajın hiçbir katmanına yazılmaz.</figcaption>
</figure>

## Neyi nereye koymalı?

| Ayar | Yeri |
|---|---|
| Programın her yerde aynı varsayılanı (`PYTHONUNBUFFERED`) | `ENV` |
| Ortama göre değişen (`APP_ENV`, `DB_HOST`, `PORT`) | Çalıştırırken `-e` / `--env-file` |
| Yalnızca derlemeyi etkileyen (sürüm etiketi) | `ARG` |
| Sırlar (şifre, anahtar, jeton) | Yalnızca çalıştırırken; asla imajda |

## Özet

- Ortam değişkenleri programa dışarıdan ayar veriyor; Python'da
  `os.environ.get("AD", "varsayılan")`, değerler metin.
- `-e AD=değer` ve `--env-file dosya` çalıştırırken verir; `-e` imajdaki
  `ENV`'i ezer.
- `ENV` imaja varsayılan yazar (çalışırken de geçerli); `ARG` yalnızca
  derlemede (`--build-arg`).
- **Sır imaja girmez:** `ARG` değeri `docker history`'de, `ENV` değeri
  `docker image inspect`'te görünür. Sırlar çalıştırırken verilir.
