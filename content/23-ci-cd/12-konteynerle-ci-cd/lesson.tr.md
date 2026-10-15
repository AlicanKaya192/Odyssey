# Konteynerle CI/CD

On birinci bölümde dağıtılan şey bir Python paketiydi: sunucuda doğru
Python sürümü, doğru kütüphaneler kurulu olmalıydı. **Konteyner**
(container) bu sorunu ortadan kaldırıyor: uygulama, çalışması için
gereken her şeyle birlikte tek bir **imaja** (image) konuyor ve o imaj
her makinede aynı çalışıyor. Bu bölümde hattın imajı derlemesini, imajın
içinde testleri çalıştırmasını ve imajı bir **imaj deposuna** (registry)
göndermesini kuruyoruz.

## Kısa hatırlatma: imaj, konteyner, depo

Docker patikasını okumadıysan dört kelime yeter:

<figure class="fig anat">
  <div class="anat-row"><span>Dockerfile</span><span>İmajın tarifi: hangi tabandan başlanacak, hangi dosyalar kopyalanacak, hangi komut çalışacak.</span></div>
  <div class="anat-row"><span>İmaj</span><span>Tariften derlenen, değişmeyen paket. Uygulama + Python + kütüphaneler.</span></div>
  <div class="anat-row"><span>Konteyner</span><span>İmajın çalışan bir kopyası.</span></div>
  <div class="anat-row"><span>İmaj deposu</span><span>İmajların saklandığı ve indirildiği yer. GitHub'ınki <code>ghcr.io</code>.</span></div>
</figure>

Hatta bunun anlamı şu: sekizinci bölümdeki "bir kez derle" kuralının
paketi artık bir imaj. Hat imajı bir kez derler, **o imajı** test eder,
**o imajı** depoya gönderir; sunucu da aynı imajı çalıştırır.

<figure class="fig">
  <div class="flow">
    <span class="node">derle</span>
    <span class="arrow">→</span>
    <span class="node">imajda test</span>
    <span class="arrow">→</span>
    <span class="node">depoya gönder</span>
    <span class="arrow">→</span>
    <span class="node acc">dağıt</span>
  </div>
</figure>

## İmajı derlemek ve içinde test etmek

GitHub'ın `ubuntu-latest` makinesinde Docker kurulu gelir. İmaj
derlemek için Docker'ın kendi eylemleri kullanılır:

```yaml
  image:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: greeter:test
      - run: docker run --rm greeter:test python -m pytest -q
```

- `setup-buildx-action` derleyiciyi (Buildx) hazırlar; önbellek gibi
  özellikler onunla gelir.
- `build-push-action` imajı `Dockerfile`'dan derler. `context: .` derleme
  için deponun köküne bakılacağını söyler.
- `load: true` derlenen imajı makinenin kendi Docker'ına yükler; yoksa
  imaj derleyicinin içinde kalır ve `docker run` onu bulamaz.
- Son adım testleri **imajın içinde** çalıştırır. Testler geçerse
  bildiğimiz şey artık "kod çalışıyor" değil, "bu imaj çalışıyor".

Testlerin imajın içinde koşması için test dosyaları ve `pytest` imajda
olmalı. Bunu istemeyen ekipler ayrı bir test aşaması (multi-stage) kurar;
temel fikir aynı: denenen imaj ile gönderilen imaj aynı tariften.

## İmaja ad vermek: etiketler

Bir imaj deposunda aynı imajın birçok adı (etiketi) olabilir. Hangi
etiketin ne zaman verileceği bir kuraldır. Yaygın kural:

- Her derlemede **commit kimliği** (SHA): her imaj tek, geri izlenebilir.
- `main`'e gönderimde `latest`: "son hâl".
- `v1.4.2` etiketinde sürüm numarası ve kısa hâli `1.4`.

```python
def image_tags(image, ref, sha):
    tags = [f"{image}:{sha[:7]}"]
    if ref == "refs/heads/main":
        tags.append(f"{image}:latest")
    if ref.startswith("refs/tags/v"):
        version = ref.removeprefix("refs/tags/v")
        major, minor, _ = version.split(".")
        tags.append(f"{image}:{version}")
        tags.append(f"{image}:{major}.{minor}")
    return tags


image = "ghcr.io/ada/greeter"
sha = "4f2a9c81d0e5b7a3c6e1f09d8b2a4c7e5f3d1b09"
for ref in ["refs/heads/main", "refs/heads/login", "refs/tags/v1.4.2"]:
    print(ref)
    for tag in image_tags(image, ref, sha):
        print("  " + tag)
```

```text
refs/heads/main
  ghcr.io/ada/greeter:4f2a9c8
  ghcr.io/ada/greeter:latest
refs/heads/login
  ghcr.io/ada/greeter:4f2a9c8
refs/tags/v1.4.2
  ghcr.io/ada/greeter:4f2a9c8
  ghcr.io/ada/greeter:1.4.2
  ghcr.io/ada/greeter:1.4
```

Dal derlemesi (`login`) yalnızca SHA etiketini alıyor; `latest`'i bir
özellik dalının üstüne yazmak, "son hâl"i yanlış imaja çevirirdi.

**`latest` ile dağıtma.** `latest` her `main` gönderiminde başka bir
imajı gösterir. Sunucu `latest`'i çalıştırıyorsa, iki hafta sonra geri
dönmek istediğinde "önceki" diye bir ad yoktur. Dağıtımda değişmeyen bir
etiket (SHA ya da sürüm) kullanılır; on birinci bölümdeki geri alma da
ancak böyle mümkün.

## İmajı depoya göndermek

İmaj `ghcr.io`'ya gönderilecek. Giriş için ayrı bir şifre gerekmez:
dokuzuncu bölümdeki `GITHUB_TOKEN` yeter, yeter ki iş `packages: write`
izni istesin.

```yaml
  publish:
    needs: image
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/ada/greeter:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

- `if: github.event_name == 'push'`: PR'da imaj derlenir ve sınanır ama
  **gönderilmez**. Fork'tan gelen bir PR'ın depoya imaj koyması
  istenmez; zaten orada gizli değerler boş gelir.
- `docker/login-action` depoya girer; şifre yerine çalışmanın geçici
  anahtarı.
- `push: true` imajı depoya gönderir.
- Depodaki imaj adı **küçük harf** olmalı. Kullanıcı ya da depo adında
  büyük harf varsa adı elle küçük harfle yaz.

## Katman önbelleği

Bir imaj katmanlardan oluşur: Dockerfile'daki her adım bir katman.
Docker bir adımı, o adım ve öncesi değişmediyse yeniden çalıştırmaz,
önbellekteki katmanı kullanır. Bir adım değişince **o adım ve ondan
sonraki her adım** yeniden çalışır.

Kendi bilgisayarında bu önbellek hep oradadır. Hattın makinesi ise her
çalışmada **sıfırdan** açılır: önbellek yoksa her derleme her adımı baştan
çalıştırır. Bunu küçük bir modelle görelim (basitleştirilmiş model:
her adımın hangi dosyalara baktığı elle yazılmış):

```python
steps = [
    ("FROM python:3.13-slim", []),
    ("COPY requirements.txt .", ["requirements.txt"]),
    ("RUN pip install -r requirements.txt", []),
    ("COPY . .", ["app.py", "requirements.txt"]),
    ("CMD python app.py", []),
]


def rebuilt(steps, changed, cache):
    out = []
    for instruction, files in steps:
        if not cache or out or set(files) & set(changed):
            out.append(instruction)
    return out


for changed, cache in [(["app.py"], True), (["requirements.txt"], True),
                       (["app.py"], False)]:
    print(f"changed {changed[0]}, cache {cache}")
    for instruction in rebuilt(steps, changed, cache):
        print("  " + instruction)
```

```text
changed app.py, cache True
  COPY . .
  CMD python app.py
changed requirements.txt, cache True
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD python app.py
changed app.py, cache False
  FROM python:3.13-slim
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD python app.py
```

- Yalnızca `app.py` değişince önbellekle iki adım çalışıyor; kütüphane
  kurulumu (genelde en uzun adım) atlanıyor.
- `requirements.txt` değişince kurulum da yeniden çalışıyor; bu doğru.
- Önbellek yoksa her şey baştan: `app.py`'deki tek satır için bütün
  kütüphaneler yeniden kuruluyor.

Hatta önbelleği `cache-from` / `cache-to` verir. `type=gha` katmanları
GitHub'ın önbellek alanında saklar (yedinci bölümdeki önbellekle aynı
yer); `mode=max` ara katmanları da saklar. Dockerfile'da önce
`requirements.txt`'yi kopyalayıp kurmak, sonra kodun geri kalanını
kopyalamak bu yüzden önemli: sık değişen dosya en sona.

## Testin yanında bir veritabanı: servisler

Bazı testler gerçek bir veritabanı ister. GitHub Actions bir işin
yanında konteyner açabilir: bunlara **servis** (service) denir. Servis,
iş başlamadan açılır ve iş bitince silinir.

```yaml
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_PASSWORD: test
        ports:
          - "5432:5432"
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 5s
          --health-retries 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/postgres
```

- `ports` servisin portunu makineye açar; testler `localhost:5432`'ye
  bağlanır.
- `options` içindeki sağlık denetimi (health check) önemli: veritabanı
  konteyneri açılır açılmaz bağlantı kabul etmez. Denetim olmadan
  testler, veritabanı hazır olmadan başlayıp rastgele düşebilir.
- Buradaki şifre gizli değil: veritabanı yalnızca bu iş boyunca var ve
  dışarıdan erişilemiyor.
- Port satırı tırnak içinde: eski YAML kurallarıyla okuyan araçlar
  (örneğin Python'un PyYAML'ı) `22:22` gibi değerleri **altmışlık sayı**
  sanıp `1342`'ye çeviriyor. Tırnak bu tuzağı her araçta kapatır.

## Sırada

On üçüncü bölümde birden çok kişinin aynı depoda çalıştığı duruma
geçiyoruz: dal stratejisi, PR kontrolleri ve `main`'i koruma kuralları.

## Özet

- Konteynerle "bir kez derle" kuralının paketi imaj: derle, imajın
  içinde test et, aynı imajı gönder, aynı imajı dağıt.
- `docker/setup-buildx-action` + `docker/build-push-action`; imajı
  makinede çalıştırmak için `load: true`.
- Etiketler: her derlemede SHA, `main`'de `latest`, sürüm etiketinde
  sürüm numarası. Dağıtımda değişmeyen etiket kullanılır.
- `ghcr.io`'ya `docker/login-action` ve `GITHUB_TOKEN` ile girilir; iş
  `packages: write` ister. PR'da imaj gönderilmez.
- Hattın makinesi her seferinde sıfırdan; katman önbelleği
  `cache-from` / `cache-to: type=gha`.
- `services:` işin yanında veritabanı gibi konteyner açar; sağlık
  denetimi olmadan testler hazır olmayan servise bağlanabilir.
