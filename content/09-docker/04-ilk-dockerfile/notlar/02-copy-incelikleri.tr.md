`COPY` en çok kullanılan talimat ve küçük ayrıntıları sonucu değiştiriyor.
Bunlar en sık karşılaşılanlar.

## Hedefin sonundaki `/`

```dockerfile
WORKDIR /app
COPY app.py .              # /app/app.py
COPY app.py main.py        # /app/main.py (adı değişti)
COPY app.py src/           # /app/src/app.py (src klasörü oluşturuldu)
```

Hedef `/` ile bitiyorsa **klasör** sayılıyor ve dosya onun içine
kopyalanıyor. Bitmiyorsa dosyanın **yeni adı** sayılıyor.

## Birden çok dosya

```dockerfile
COPY app.py utils.py ./    # ikisi de /app'e
COPY *.py ./               # bütün .py dosyaları
```

Birden çok kaynak varsa hedef bir klasör olmalı ve `/` ile bitmeli.

## Klasör kopyalamak

```dockerfile
COPY src/ ./src/
```

Bir klasör kopyalanınca **içindekiler** kopyalanıyor. `COPY src/ .` yazarsan
`src`'nin içindekiler doğrudan `/app`'e dökülür; klasörün kendisi gelmez.
Klasörü korumak için hedefe de adını yaz: `./src/`.

## `COPY . .` her şeyi alır

`.` derleme bağlamının tamamı: `.git` klasörü, `__pycache__`, sanal ortam
(`.venv`), `.env` dosyası, büyük veri dosyaları... Hepsi imaja giriyor.
İstemediklerini dışarıda bırakmanın yolu `.dockerignore` dosyası; bir
sonraki bölümde.

## `COPY` mi, `ADD` mi?

`ADD` `COPY`'nin yaptığı her şeyi yapıyor, artı:

- `.tar.gz` gibi sıkıştırılmış dosyaları kopyalarken açıyor,
- bir internet adresinden dosya indirebiliyor.

Bu "ekstra" davranışlar sürpriz yaratıyor (dosyayı açmasını istemediğin
hâlde açabiliyor). Kural: **her zaman `COPY`**; yalnızca bir arşivi açman
gerekiyorsa `ADD`.

## Kaynak bağlamın dışına çıkamaz

```dockerfile
COPY ../shared/config.json .    # olmaz
```

Derleme bağlamı (`docker build`'e verilen klasör) dışındaki hiçbir dosya
görünmüyor; `..` ile yukarı çıkılamıyor. Gerekiyorsa bağlamı bir üst klasör
yapıp Dockerfile'ı `-f` ile göster:

```text
docker build -f greeter/Dockerfile -t greeter .
```
