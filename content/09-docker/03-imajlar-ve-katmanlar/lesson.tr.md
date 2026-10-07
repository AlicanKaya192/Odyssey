# İmajlar, Etiketler ve Katmanlar

Şimdiye kadar `alpine:3.22` ve `python:3.13-slim` imajlarını kullandın. Bu
bölümde imajın kendisine yakından bakacağız: adı nasıl okunur, sürümü
nereden anlaşılır, içi neden üst üste dilimlerden oluşur ve bilgisayarda
nasıl yönetilir.

## Bir imajın adını okumak

`python:3.13-slim` aslında kısaltılmış bir ad. Tam hâli şu:

<figure class="fig">
  <div class="anat">
    <div class="sig"><code>docker.io / library / python : 3.13-slim</code></div>
    <div class="anat-row"><span>docker.io</span><span><b>Kayıt</b>: imajın indirildiği yer (Docker Hub). Yazılmazsa bu.</span></div>
    <div class="anat-row"><span>library</span><span><b>Ad alanı</b>: yayıncı. Resmî imajlarda <code>library</code>; yazılmazsa bu.</span></div>
    <div class="anat-row"><span>python</span><span><b>Depo</b>: imajın adı.</span></div>
    <div class="anat-row"><span>3.13-slim</span><span><b>Etiket</b>: sürüm ve çeşit. Yazılmazsa <code>latest</code>.</span></div>
  </div>
  <figcaption><code>python:3.13-slim</code> yazdığında Docker baştaki iki parçayı kendisi ekliyor.</figcaption>
</figure>

- **Kayıt** (registry): imajın indirildiği yer. Yazılmazsa Docker Hub
  (`docker.io`).
- **Ad alanı** (namespace): imajı yayınlayan. Docker'ın resmî imajlarında
  `library`; yazılmazsa o varsayılıyor. Bir kişinin imajı `ada/myapp`
  gibi.
- **Depo** (repository): imajın adı, `python`.
- **Etiket** (tag): `:`'dan sonrası, genellikle sürüm. `3.13-slim`.

Yani `docker pull python:3.13-slim` yazdığında Docker
`docker.io/library/python:3.13-slim` imajını indiriyor. `docker pull`
çıktısının son satırı da bu tam adı yazıyor.

## Etiketler: aynı imajın sürümleri

Bir deponun onlarca etiketi olabiliyor. `python` deposundan birkaçı:

| Etiket | Ne? | Yaklaşık boyut |
|---|---|---|
| `3.13` | Python 3.13, geniş bir Debian üzerinde (derleme araçları dahil) | ~1 GB |
| `3.13-slim` | Python 3.13, küçültülmüş Debian | ~180 MB |
| `3.13-alpine` | Python 3.13, Alpine üzerinde | ~50 MB |
| `3.13.16-slim` | Tam olarak 3.13.16 | ~180 MB |
| `latest` | Etiket yazılmazsa kullanılan | değişir |

Etiketin içinde iki bilgi var: **Python'un sürümü** (`3.13`) ve **altındaki
Linux** (`slim`, `alpine`; bazen Debian'ın sürüm adı: `trixie`, `bookworm`).

## `latest` en yeni demek değil

Etiket yazmazsan Docker `latest` etiketini kullanıyor:

```text
docker pull python          # = docker pull python:latest
```

`latest` sihirli bir kelime değil; yayıncının "varsayılan" diye seçtiği
etiket. Bugün Python 3.13'ü gösterirken yarın 3.14'ü gösterebilir. Aynı
Dockerfile bugün çalışıp bir ay sonra bozulabilir.

Bu yüzden kural: **imajın sürümünü her zaman yaz** (sürümü "sabitlemek",
pinning). `FROM python:latest` ya da yalnızca `FROM python` yerine
`FROM python:3.13-slim`.

Daha da kesin olmak istersen imajın **özetini** (digest) yazabilirsin: bir
imajın içeriğinden hesaplanan ve asla değişmeyen kimlik.

```text
docker pull alpine:3.22
...
Digest: sha256:5291449c3df73caf6ed85e649dec1b9e818b39a5d8c871e97afc13e9cd5e8fa8
```

`FROM alpine@sha256:5291449c...` yazılırsa her zaman tam olarak o imaj
iniyor. Etiket bir yer imi gibi taşınabiliyor; özet taşınamıyor.

## Katmanlar

İmaj tek parça bir dosya değil, **üst üste dilimlerden** (katman, layer)
oluşuyor. Her dilim bir öncekine göre neyin eklendiğini ya da değiştiğini
tutuyor.

`docker history` bir imajın katmanlarını gösteriyor:

```text
docker history alpine:3.22
```

```text
IMAGE          CREATED       CREATED BY                                      SIZE
5291449c3df7   2 weeks ago   CMD ["/bin/sh"]                                 0B
<missing>      2 weeks ago   ADD alpine-minirootfs-3.22.6-x86_64.tar.gz /…   8.97MB
```

Alttan üste okunuyor: önce Alpine'ın dosyaları eklenmiş (8,97 MB), sonra
varsayılan komut `/bin/sh` olarak ayarlanmış (0 B; yalnızca bir ayar, dosya
eklemiyor).

`python:3.13-slim` biraz daha kalabalık:

```text
CREATED BY                                   SIZE
CMD ["python3"]                              0B
RUN /bin/sh -c set -eux; for src in idle3…   16.4kB
RUN /bin/sh -c set -eux; savedAptMark=…      40.4MB
ENV PYTHON_VERSION=3.13.16                   0B
RUN /bin/sh -c set -eux; apt-get update; …   4.94MB
ENV PATH=/usr/local/bin:…                    0B
# debian.sh --arch 'amd64' out/ 'trixie' …   87.7MB
```

En altta Debian "trixie"nin dosyaları (87,7 MB), üstünde birkaç sistem
paketi, sonra Python'un kendisi (40,4 MB), en üstte varsayılan komut.
Dosya ekleyen talimatlar (`RUN`, `COPY`, `ADD`) boyut tutuyor; ayar
talimatları (`ENV`, `CMD`) 0 B.

<figure class="fig">
<svg viewBox="0 0 620 212" width="620" xmlns="http://www.w3.org/2000/svg">
  <rect class="box" x="30" y="4" width="380" height="30" rx="6" stroke-dasharray="5 4"/>
  <text class="ink" x="44" y="24" font-size="13">Konteynerin yazılabilir katmanı</text>
  <rect class="box" x="30" y="40" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="63" font-size="13">CMD ["python3"]</text>
  <text class="dim" x="396" y="63" font-size="12" text-anchor="end">0 B</text>
  <rect class="box" x="30" y="82" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="105" font-size="13">Python 3.13.16</text>
  <text class="dim" x="396" y="105" font-size="12" text-anchor="end">40.4 MB</text>
  <rect class="box" x="30" y="124" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="147" font-size="13">Sistem paketleri</text>
  <text class="dim" x="396" y="147" font-size="12" text-anchor="end">4.9 MB</text>
  <rect class="box" x="30" y="166" width="380" height="36" rx="6"/>
  <text class="ink" x="44" y="189" font-size="13">Debian trixie dosyaları</text>
  <text class="dim" x="396" y="189" font-size="12" text-anchor="end">87.7 MB</text>
  <line class="line" x1="428" y1="40" x2="428" y2="202"/>
  <line class="line" x1="420" y1="40" x2="428" y2="40"/>
  <line class="line" x1="420" y1="202" x2="428" y2="202"/>
  <text class="ink" x="440" y="118" font-size="13" font-weight="600">python:3.13-slim</text>
  <text class="dim" x="440" y="136" font-size="12">salt okunur, paylaşılır</text>
  <text class="dim" x="440" y="24" font-size="12">← konteyner silinince gider</text>
</svg>
  <figcaption>İmaj alttan üste dizilmiş katmanlar. Konteyner en üste kendi ince katmanını ekliyor; imajın katmanlarına hiç dokunmuyor.</figcaption>
</figure>

## Katmanlar neden önemli?

**1. Paylaşılıyor.** İki imaj aynı alt katmanlara sahipse o katmanlar
diskte **bir kez** duruyor. Python'dan başlayan on imaj kurarsan Python'un
katmanları on kez değil bir kez yer kaplıyor; yalnızca senin eklediğin üst
katmanlar ayrı.

**2. Bir kez iniyor.** `docker pull` yalnızca bilgisayarında olmayan
katmanları indiriyor. Yeni bir sürüm çıktığında çoğu zaman yalnızca üstteki
birkaç katman iniyor.

**3. Derleme önbelleği bunun üstüne kurulu.** Kendi imajını kurarken
değişmeyen katmanlar yeniden oluşturulmuyor; derleme saniyelere iniyor.
Bunu Önbellek bölümünde ayrıntısıyla göreceğiz.

**4. Konteynerin yazılabilir katmanı.** İmajın katmanları salt okunur.
Konteyner çalışınca en üste **ince, yazılabilir bir katman** ekleniyor;
konteynerin içinde yaptığın her değişiklik oraya gidiyor. Konteyner
silinince o katman da gidiyor; bir önceki bölümde kaybolan dosyanın sebebi
buydu.

## İmajı incelemek

`docker image inspect` bir imajın bütün ayarlarını JSON olarak veriyor.
Uzun bir çıktı; belli bir alanı `--format` ile seçebilirsin:

```text
docker image inspect python:3.13-slim --format "{{.Config.Cmd}}"
```

```text
[python3]
```

Bu imajdan komut vermeden bir konteyner çalıştırırsan `python3` açılıyor.
Başka işe yarar alanlar: `{{.Config.Env}}` (ortam değişkenleri),
`{{.Os}}/{{.Architecture}}` (hangi sistem için: `linux/amd64`).

## Kendi adını vermek: `docker tag`

`docker tag` var olan bir imaja **ikinci bir ad** veriyor. İmaj
kopyalanmıyor; aynı imaja yeni bir etiket yapıştırılıyor:

```text
docker tag alpine:3.22 mybase:1.0
docker images
```

```text
IMAGE              ID             DISK USAGE   CONTENT SIZE
alpine:3.22        5291449c3df7       12.8MB         3.88MB
mybase:1.0         5291449c3df7       12.8MB         3.88MB
```

İki satırın **ID'si aynı**: tek bir imaj, iki ad. Kendi imajlarını
yayınlarken `myapp:1.0`, `myapp:1.1` gibi etiketler verip eskilere de
ulaşabiliyorsun.

## Silmek ve temizlemek

```text
docker rmi mybase:1.0           # bir adı (etiketi) sil
docker image rm alpine:3.22     # aynı iş, uzun yazımı
docker image prune              # adsız (dangling) imajları sil
docker system prune             # durmuşlar, adsızlar, boştaki ağlar, önbellek
```

- Bir imajın birden çok adı varsa `docker rmi` yalnızca o adı siliyor
  (`Untagged: mybase:1.0`); imaj, son adı da silinince gidiyor.
- Bir konteyner (durmuş olsa bile) bir imajı kullanıyorsa o imaj
  silinemiyor; önce konteyneri sil.
- **Adsız imaj** (dangling): aynı adla yeni bir imaj kurunca eskisi adını
  kaybedip `<none>` olarak kalıyor. `docker image prune` bunları
  temizliyor.
- `prune` komutları ne sileceklerini söyleyip onay istiyor.

## Docker Hub'da imaj seçmek

Docker Hub'da herkes imaj yayınlayabiliyor. Güvenmek için bakılacak
işaretler:

- **Docker Official Image**: Docker'ın ve yazılımın sahiplerinin birlikte
  bakımını yaptığı imajlar (`python`, `alpine`, `postgres`, `nginx`).
  Adında ad alanı yok.
- **Verified Publisher**: kimliği doğrulanmış şirketlerin imajları.
- Uzun süredir güncellenmemiş, kimin yayınladığı belli olmayan imajlardan
  uzak dur: içinde ne olduğunu bilmiyorsun.

## Özet

- Tam ad: `kayıt/ad-alanı/depo:etiket`; `python:3.13-slim` =
  `docker.io/library/python:3.13-slim`.
- Etiket sürümü ve altındaki Linux'u söylüyor. `latest` en yeni demek
  değil; **sürümü her zaman sabitle**. En kesini özet (`@sha256:...`).
- İmaj üst üste **katmanlardan** oluşuyor (`docker history`); katmanlar
  paylaşılıyor, bir kez iniyor ve derleme önbelleğinin temeli.
- Konteyner en üste kendi yazılabilir katmanını ekliyor.
- `docker image inspect` ayarları, `docker tag` yeni bir ad, `docker rmi`
  silme, `docker image prune` adsızları temizleme.
