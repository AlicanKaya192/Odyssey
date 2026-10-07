# Portlar: Konteynere Dışarıdan Ulaşmak

Şimdiye kadarki konteynerler bir şey yazıp bitiyordu. Gerçek hayatta
konteynerlerin çoğu **sunucu**: bir web sitesi, bir API, bir veritabanı.
Hiç bitmiyorlar ve dışarıdan gelecek istekleri bekliyorlar. Bu bölümde bir
konteynerdeki sunucuya bilgisayarından nasıl ulaşılacağını öğreneceğiz.

## Port nedir?

Bir bilgisayarda aynı anda birçok program ağı dinleyebiliyor. Gelen bir
isteğin hangi programa gideceğini **port numarası** söylüyor: bir apartmanın
adresi aynı, daire numarası farklı.

- `localhost:8000` → bu bilgisayarın 8000 numaralı kapısı.
- Web siteleri genelde 80 (http) ve 443 (https); geliştirme sırasında 8000,
  8080, 5000 gibi numaralar kullanılıyor.

API patikasında `api.odyssey.test` adresine istek atmıştın; o da bir
bilgisayardaki bir porta gidiyordu.

## Konteynerin kendi ağı var

Python'un hazır web sunucusunu bir konteynerde çalıştıralım:

```dockerfile
FROM python:3.13-slim
WORKDIR /srv
COPY index.html .
CMD ["python", "-m", "http.server", "8000"]
```

`python -m http.server 8000` bulunduğu klasördeki dosyaları 8000 portundan
sunuyor. Kur ve çalıştır, sonra tarayıcıda `localhost:8000`'i aç:

```text
docker run -d --name web site
curl localhost:8000
```

```text
curl: (7) Failed to connect to localhost:8000 after 2225 ms: Could not connect to server
```

Sunucu çalışıyor ama ulaşılamıyor. Sebep: konteynerin **kendi ağı** var.
İçindeki 8000 numaralı port, bilgisayarının 8000 numaralı portu değil.
Konteyner dışarıya kapalı bir oda gibi.

## Port yayınlamak: `-p`

Odaya dışarıdan bir kapı açmak için `-p` (publish, yayınla):

```text
docker run -d --name web -p 8080:8000 site
curl localhost:8080
```

```text
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.16
...
```

`-p 8080:8000` şunu söylüyor: **bilgisayarın 8080'ine gelen istekleri
konteynerin 8000'ine aktar.** Sıra her zaman `ana makine:konteyner`.

<figure class="fig">
  <div class="flow">
    <span class="node">Tarayıcı<br><small>localhost:8080</small></span><span class="arrow">→</span>
    <span class="node acc">Bilgisayarın 8080'i<br><small>-p 8080:8000</small></span><span class="arrow">→</span>
    <span class="node ok">Konteynerin 8000'i<br><small>python -m http.server</small></span>
  </div>
  <figcaption>Soldaki numara bilgisayarın kapısı, sağdaki konteynerin içindeki. <code>-p</code> yoksa ilk ok hiç yok.</figcaption>
</figure>

Tarayıcıda `http://localhost:8080` açınca sayfa geliyor. Konteynerin
günlüğünde isteğin geldiği de görünüyor:

```text
docker logs web
172.17.0.1 - - [06/Oct/2026 19:43:26] "GET / HTTP/1.1" 200 -
```

`172.17.0.1` Docker'ın ağındaki "dış dünya"nın adresi; istek bilgisayarından
o kapıdan girdi.

## Seçenekler

| Yazım | Anlamı |
|---|---|
| `-p 8080:8000` | Bilgisayarın 8080'i → konteynerin 8000'i |
| `-p 8000:8000` | Aynı numara iki tarafta (en yaygını) |
| `-p 127.0.0.1:8080:8000` | Yalnızca bu bilgisayardan ulaşılsın, ağdaki başkaları ulaşamasın |
| `-p 8080:8000 -p 9090:9000` | Birden çok port |
| `-P` | `EXPOSE` edilen her portu rastgele boş bir porta yayınla |

Hangi portun nereye gittiğini `docker port` gösteriyor:

```text
docker run -d --name web2 -P site
docker port web2
8000/tcp -> 0.0.0.0:32768
```

`docker ps`'in PORTS sütunu da aynı şeyi yazıyor: `0.0.0.0:32768->8000/tcp`.

## `EXPOSE` yayınlamaz

```dockerfile
EXPOSE 8000
```

`EXPOSE` yalnızca **belgeliyor**: "bu imajdaki program 8000'i dinliyor".
Kapıyı açmıyor; açan `-p`. Yine de yazılmalı:

- imajı kullanan kişi hangi portu yayınlayacağını görüyor,
- `-P` hangi portları yayınlayacağını buradan öğreniyor.

## En sık hata: 127.0.0.1'i dinlemek

Programın **hangi adresi dinlediği** de önemli. Aynı sunucuyu yalnızca
`127.0.0.1`'i dinleyecek şekilde başlatalım:

```text
docker run -d -p 8081:8000 site python -m http.server 8000 --bind 127.0.0.1
curl localhost:8081
```

```text
curl: (52) Empty reply from server
```

`-p` doğru ama yanıt boş. `127.0.0.1` "yalnızca bu bilgisayarın içinden"
demek ve konteynerin içinde "bu bilgisayar" **konteynerin kendisi**.
Docker'ın dışarıdan aktardığı istek konteynere başka bir adresten geliyor ve
program onu kabul etmiyor.

Çözüm: konteynerin içindeki program **`0.0.0.0`'ı** (bütün adresleri)
dinlemeli. `http.server` varsayılan olarak bunu yapıyor; Flask ve uvicorn gibi
araçlarda ise genellikle açıkça yazmak gerekiyor:

```text
uvicorn main:app --host 0.0.0.0 --port 8000
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>127.0.0.1'i dinliyor</h4><p>Yalnızca konteynerin içinden gelen istekler</p><p>Dışarıdan: <code>Empty reply from server</code></p></div>
    <div class="ok"><h4>0.0.0.0'ı dinliyor</h4><p>Bütün adreslerden gelen istekler</p><p>Dışarıdan: <code>200 OK</code></p></div>
  </div>
  <figcaption>Konteynerin içinde "bu bilgisayar" konteynerin kendisi. Docker'ın aktardığı istek başka bir adresten geliyor.</figcaption>
</figure>

## Aynı port iki kez kullanılamaz

Bilgisayarın bir portunu yalnızca bir program tutabilir. İkinci bir
konteyner aynı portu isterse:

```text
docker: Error response from daemon: ... Bind for 0.0.0.0:8080 failed:
port is already allocated
```

Başka bir ana makine portu seç (`-p 8081:8000`) ya da öncekini durdur. Port
Docker dışındaki bir program tarafından da tutuluyor olabilir.

## Özet

- Konteynerin kendi ağı var; içindeki port dışarıya kendiliğinden açılmaz.
- `-p ana-makine:konteyner` kapıyı açar: `-p 8080:8000`.
  `127.0.0.1:` öneki yalnızca bu bilgisayara açar; `-P` rastgele porta.
- `docker port` ve `docker ps` hangi portun nereye gittiğini gösterir.
- `EXPOSE` yalnızca belgeler; açan `-p`.
- Konteynerdeki program `0.0.0.0`'ı dinlemeli; `127.0.0.1` dinlerse
  `Empty reply from server`.
- Aynı ana makine portu iki kez kullanılamaz: `port is already allocated`.
