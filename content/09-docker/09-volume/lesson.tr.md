# Veriyi Saklamak: Volume ve Bind Mount

İlk Konteynerler bölümünde kural koymuştuk: konteynerin içine önemli bir şey
yazma, konteyner silinince gider. Peki bir veritabanı, bir not uygulaması,
yüklenen dosyalar? Veri bir yerde kalmalı. Docker'da bu yerin iki biçimi var:
**volume** ve **bind mount**.

## Sorun: yazılabilir katman geçici

Konteynerin içinde yazdığın her şey onun ince, yazılabilir katmanına
gidiyor. Konteyner silinince katman da gidiyor. Yeni bir sürüm çıkardığında
eski konteyneri silip yenisini çalıştırıyorsun; veri konteynerin içindeyse
her güncellemede kayboluyor.

Çözüm: veriyi konteynerin **dışında** bir yerde tutup konteynerin içindeki
bir klasöre **bağlamak**.

<figure class="fig">
  <div class="flow">
    <span class="node">Konteyner 1<br><small>/data/n.txt yazar</small></span><span class="arrow">→</span>
    <span class="node acc">Volume: notes<br><small>konteynerin dışında</small></span><span class="arrow">→</span>
    <span class="node ok">Konteyner 2<br><small>/data/n.txt okur</small></span>
  </div>
  <figcaption>İki konteyner de silindi; veri volume'da kaldı. Konteynerin <code>/data</code> klasörü aslında volume'un kendisi.</figcaption>
</figure>

## Volume: Docker'ın yönettiği depo

**Volume**, Docker'ın senin için oluşturup yönettiği adlandırılmış bir veri
alanı. Oluştur ve bir konteynere bağla:

```text
docker volume create notes
docker run --rm -v notes:/data alpine:3.22 sh -c "echo first > /data/n.txt"
docker run --rm -v notes:/data alpine:3.22 cat /data/n.txt
```

```text
first
```

İki **ayrı** konteyner; ikisi de `--rm` ile çalışıp silindi. Ama ikincisi
birincinin yazdığı dosyayı okudu, çünkü dosya konteynerde değil `notes`
volume'unda.

`-v notes:/data` şunu söylüyor: **`notes` volume'unu konteynerin `/data`
klasörüne bağla.** Konteynerdeki program `/data`'ya yazdığını sıradan bir
klasöre yazıyor sanıyor.

Volume yoksa `-v` onu kendiliğinden oluşturuyor; `volume create` yazmak
şart değil ama ne yaptığını açık gösteriyor.

## Volume komutları

```text
docker volume ls                  # bütün volume'lar
docker volume inspect notes       # ayrıntılar
docker volume rm notes            # sil (kullanan konteyner yoksa)
docker volume prune               # hiçbir konteynerin kullanmadığı volume'lar
```

```text
docker volume ls
DRIVER    VOLUME NAME
local     notes
```

`docker volume inspect` volume'un nerede durduğunu söylüyor:
`/var/lib/docker/volumes/notes/_data`. Bu yol Docker'ın Linux'unun (WSL 2)
içinde; Windows'un dosya gezgininde doğrudan görünmüyor. Volume'a
konteynerler üzerinden ulaşıyorsun.

**Dikkat:** `docker volume rm` ve `docker volume prune` veriyi **geri
dönüşsüz** siliyor. Konteyneri silmek volume'a dokunmuyor; volume'u silmek
veriyi götürüyor.

## Dockerfile'da `VOLUME`

```dockerfile
VOLUME /data
```

İmajı kullanan kişiye "bu programın verisi `/data`'da; onu bir volume'a
bağla" diye **belgeliyor**. `-v` verilmezse Docker o klasör için adsız bir
volume oluşturuyor; veri yine konteynerin yazılabilir katmanında kalmamış
oluyor ama adı rastgele olduğu için bulmak zor. Kendi adlı volume'unu `-v`
ile vermek her zaman daha iyi.

## Bind mount: bilgisayarındaki bir klasör

**Bind mount**, bilgisayarındaki **belirli bir klasörü** konteynerin içine
bağlıyor. Konteyner o klasörün kendisini görüyor; birinde yaptığın
değişiklik anında ötekinde.

PowerShell'de bulunduğun klasörü bağlamak:

```text
docker run --rm -v ${PWD}:/app -w /app python:3.13-slim python app.py
```

- `${PWD}`: PowerShell'de "şu anki klasör".
- `-w /app`: konteynerin çalışma klasörü (`WORKDIR` gibi).

Bu, imaj kurmadan, bilgisayarındaki `app.py`'yi konteynerdeki Python 3.13 ile
çalıştırıyor. Kodu düzenleyip komutu yeniden çalıştırınca yeni hâli
çalışıyor. **Geliştirirken** çok kullanışlı.

Konteynerin bir klasörü yalnızca **okuyabilmesini** istiyorsan sona `:ro`
(read-only):

```text
docker run --rm -v ${PWD}/config:/config:ro app
```

## Hangisi ne zaman?

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Volume</h4><pre><code class="language-text">-v notes:/data</code></pre><p>Docker yönetir</p><p>Veritabanı, yüklenen dosyalar</p></div>
    <div><h4>Bind mount</h4><pre><code class="language-text">-v ${PWD}:/app</code></pre><p>Bilgisayarındaki klasör</p><p>Geliştirirken kod, ayar</p></div>
  </div>
  <figcaption>İki nokta üst üstenin solunda ad varsa volume, yol varsa bind mount.</figcaption>
</figure>

| | Volume | Bind mount |
|---|---|---|
| Yazımı | `-v notes:/data` (ad) | `-v ${PWD}:/app` (yol) |
| Nerede durur? | Docker'ın içinde | Bilgisayarındaki klasörde |
| Kim yönetir? | Docker | Sen |
| Tipik kullanım | Veritabanı verisi, yüklenen dosyalar | Geliştirirken kod, ayar dosyası |
| Başka bilgisayara taşınır mı? | Komutla (yedekleyerek) | Klasör zaten senin |

Kural: **verinin kendisi volume'da, geliştirdiğin kod bind mount'ta.**
Yayındaki bir imaja kod bind mount ile verilmez; kod imajın içinde
(`COPY`) olmalı.

## Volume'u yedeklemek

Volume'un içeriğini bir dosyaya almak için küçük bir konteyner kullanılıyor:
hem volume'u hem bilgisayarındaki klasörü bağlayıp `tar` ile arşivliyor.

```text
docker run --rm -v notes:/data -v ${PWD}:/backup alpine:3.22 `
  tar czf /backup/notes.tgz -C /data .
```

Satır sonundaki `` ` `` PowerShell'de "komut alt satırda sürüyor" demek (bash'te `\`). Bu tek komutta bu bölümün iki bağlama biçimi birlikte var.

## Özet

- Konteynerin yazılabilir katmanı geçici; kalıcı veri dışarıda tutulup
  konteynere **bağlanır**.
- **Volume:** `-v ad:/klasör`; Docker yönetir, konteyner silinse de kalır.
  `docker volume ls / inspect / rm / prune`. `rm` ve `prune` veriyi siler.
- `VOLUME /data` verinin yerini belgeler; `-v` ile ad vermek daha iyi.
- **Bind mount:** `-v ${PWD}:/app`; bilgisayarındaki klasörün kendisi.
  Geliştirirken kod için; `:ro` salt okunur.
- Veri volume'da, geliştirilen kod bind mount'ta, yayındaki kod imajın
  içinde.
