# Bir Python API'sini Paketlemek

Bu bölümde patikada öğrendiğin her şeyi tek bir gerçek projede
birleştiriyoruz: küçük bir not API'sini (programların HTTP ile konuştuğu
bir sunucu) baştan sona Docker'a hazırlıyoruz. Sonunda elinde başka bir
bilgisayarda tek komutla açılan, verisini kaybetmeyen, root olmayan ve
sağlığını kendisi bildiren bir servis olacak.

## Proje

```text
notes-api/
├── app.py            # API'nin kendisi
├── healthcheck.py    # "sağlıklı mıyım?" denetimi
├── requirements.txt  # Python paketleri
├── Dockerfile
├── .dockerignore
├── compose.yaml
└── .env              # ortama göre değişen ayarlar
```

API üç adres sunuyor:

| İstek | Ne yapar? |
|---|---|
| `GET /health` | `{"status": "ok"}`: program ayakta mı? |
| `GET /notes` / `POST /notes` | Notları listeler / yeni not ekler. |
| `GET /stats` | Not sayısı ve programın kaç kez başladığı. |

Notlar bir SQLite veritabanında (tek dosyalık veritabanı) duruyor.
Program yalnızca Python'un standart kütüphanesini kullanıyor; bu yüzden
`requirements.txt` şimdilik boş, ama yapı paket eklendiği gün de aynı
kalacak.

<figure class="fig">
  <div class="flow">
    <span class="node">curl<br><small>localhost:8095</small></span><span class="arrow">→</span>
    <span class="node">ports<br><small>8095 → 8000</small></span><span class="arrow">→</span>
    <span class="node ok">app.py<br><small>0.0.0.0:8000, USER app</small></span><span class="arrow">→</span>
    <span class="node acc">notes-data<br><small>/data/notes.db</small></span>
  </div>
  <figcaption>Bir isteğin yolu: bilgisayarın portundan konteynere, programdan volume'daki veritabanına. Konteyner silinse de veritabanı volume'da kalıyor.</figcaption>
</figure>

## Program Docker'a hazır mı?

Dockerfile yazmadan önce programın kendisi dört kurala uymalı. Hepsini
önceki bölümlerde gördün; burada `app.py`'de nasıl göründüklerine
bakıyoruz.

**1. Her adresten dinle.** `localhost` yalnızca konteynerin kendisi
demek; dışarıdan gelen istek ulaşamaz (Portlar bölümü).

```python
ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
```

**2. Ayarları ortamdan oku.** Veritabanının yeri ve port koda yazılmıyor;
varsayılanı var, ortam değişkeni varsa o geçerli (Ortam Değişkenleri
bölümü).

```python
DB_PATH = os.environ.get("DB_PATH", "notes.db")
PORT = int(os.environ.get("PORT", "8000"))
```

**3. Günlüğü ekrana yaz.** Dosyaya değil, standart çıktıya:
`docker logs` onu topluyor. `flush=True` (ya da imajda
`PYTHONUNBUFFERED=1`) satırın beklemeden çıkmasını sağlıyor.

**4. SIGTERM'de düzgün kapan.** `docker stop` önce SIGTERM gönderiyor,
10 saniye sonra öldürüyor (CMD ve ENTRYPOINT bölümü). Sinyali yakalayan
program hemen ve temiz kapanıyor:

```python
def stop(signum, frame):
    print("shutting down", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, stop)
```

Ölçtük: bu programda `docker compose stop` **0,9 saniyede** bitti ve
çıkış kodu 0 oldu.

## Dockerfile, satır satır

```dockerfile
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/notes.db \
    PORT=8000

RUN useradd --create-home --uid 1000 app \
 && mkdir /data \
 && chown app:app /data

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py healthcheck.py ./

USER app
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD ["python", "healthcheck.py"]
CMD ["python", "app.py"]
```

| Satır | Neden? |
|---|---|
| `FROM python:3.13-slim` | Sürümü sabit, küçük taban imaj. |
| `PYTHONDONTWRITEBYTECODE=1` | Python `__pycache__` dosyaları yazmasın; konteynerde işe yaramıyorlar. |
| `PYTHONUNBUFFERED=1` | Çıktı beklemeden `docker logs`'a düşsün. |
| `DB_PATH`, `PORT` | Varsayılan ayarlar; çalıştırırken değiştirilebilir. |
| `useradd ... && mkdir /data && chown` | Kullanıcıyı ve veri klasörünü **tek katmanda** hazırla; klasörün sahibi kullanıcı. |
| `COPY requirements.txt` → `RUN pip install` | Önce paketler: kod değişince bu katmanlar önbellekten gelir. |
| `COPY app.py healthcheck.py ./` | Sık değişen kod en sonda. Birden çok dosyada hedef `./` ile biter. |
| `USER app` | Program root olmadan çalışsın; paket kurulumundan **sonra**. |
| `EXPOSE 8000` | Belge: program bu portu dinliyor. |
| `HEALTHCHECK` | Docker programın sağlığını kendisi denetlesin. |
| `CMD [...]` | Exec biçimi: SIGTERM doğrudan Python'a ulaşır. |

Kurulan imaj diskte **176 MB** (indirilen sıkıştırılmış hâli 43 MB); bunun
neredeyse tamamı taban imaj. Bizim eklediğimiz katmanlar toplam 115 KB
kadar (`docker history` ile ölçtük).

## `HEALTHCHECK`: Docker'ın kendi denetimi

Compose bölümünde sağlık denetimini `compose.yaml`'a yazmıştık.
`HEALTHCHECK` talimatı aynı şeyi **imajın içine** koyuyor: imajı kim, nasıl
çalıştırırsa çalıştırsın denetim yanında geliyor.

```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD ["python", "healthcheck.py"]
```

- `--interval=5s`: her 5 saniyede bir denetle (varsayılan 30 saniye).
- `--timeout=3s`: 3 saniyede cevap gelmezse başarısız say.
- `--retries=3`: üst üste 3 başarısızlıkta "sağlıksız" (unhealthy) de.
- `CMD`: denetim komutu. Çıkış kodu 0 → sağlıklı, 1 → sağlıksız.

Denetim komutu konteynerin **içinde** çalışıyor. `python:3.13-slim`'de
`curl` yok; bu yüzden denetimi Python ile ayrı bir dosyada yazdık:

```python
PORT = os.environ.get("PORT", "8000")

try:
    urllib.request.urlopen(f"http://localhost:{PORT}/health", timeout=2)
except OSError:
    sys.exit(1)
```

Port ortamdan okunuyor: biri `PORT`'u değiştirirse denetim de onunla
değişiyor. Denetim dosyasının imaja kopyalanması gerektiğini unutma.

```text
docker compose ps
NAME             STATUS
notesapi-web-1   Up 2 seconds (health: starting)
notesapi-web-1   Up 6 seconds (healthy)
```

İlk denetim geçene kadar durum `health: starting`, sonra `healthy`.
Denetimi bilerek yanlış porta (9000) yönelttiğimizde konteyner çalışmaya
devam etti ama yaklaşık 15 saniye sonra `(unhealthy)` oldu: 5 saniyelik
aralıkla üst üste 3 başarısızlık.

## `.dockerignore`

```text
.git
.env
**/__pycache__
*.db
```

- `.env` imaja girmesin: içindeki ayarlar (ileride parolalar) imajla
  birlikte herkese gitmesin.
- `*.db`: bilgisayarında denerken oluşan veritabanı imaja kopyalanmasın;
  veri volume'da yaşıyor.

## `compose.yaml`

```yaml
services:
  web:
    build: .
    ports:
      - "8095:8000"
    env_file: .env
    volumes:
      - notes-data:/data
    restart: unless-stopped

volumes:
  notes-data:
```

| Ayar | Ne yapar? |
|---|---|
| `build: .` | İmajı bu klasördeki Dockerfile'dan kur. |
| `ports` | Bilgisayarın 8095'i konteynerin 8000'ine. |
| `env_file: .env` | Ortam değişkenlerini dosyadan al; Dockerfile'daki `ENV`'in üstüne yazar. |
| `notes-data:/data` | Adlı volume: veritabanı konteyner silinse de kalır. |
| `restart: unless-stopped` | Program çökerse yeniden başlat; sen durdurduysan başlatma. |

`.env`:

```text
DB_PATH=/data/notes.db
PORT=8000
```

Dockerfile'daki `ENV` **varsayılan**, `.env` o ortamın ayarı. Aynı imaj
geliştirme bilgisayarında ve sunucuda farklı `.env` ile çalışabilir.

## Çalıştırıp denemek

```text
docker compose up -d --build
curl localhost:8095/health
{"status": "ok"}
```

Not eklemek için gövdeyi bir dosyaya yaz (`note.json`: `{"text": "buy milk"}`)
ve `-d @dosya` ile gönder; tırnakları kabukta kaçırmakla uğraşmazsın.
PowerShell'de `curl` başka bir komutun takma adı, orada `curl.exe` yaz.

```text
curl -X POST localhost:8095/notes -d @note.json
{"id": 1, "text": "buy milk"}
curl localhost:8095/notes
[{"id": 1, "text": "buy milk"}]
```

Boş not gönderince program `400` ile reddediyor:
`{"error": "text is required"}`. Günlük:

```text
docker compose logs web
web-1  | listening on port 8000, database /data/notes.db
web-1  | POST /notes 201
web-1  | POST /notes 400
web-1  | GET /notes 200
```

Sağlık denetimi her 5 saniyede bir `/health`'e istek atıyor; günlüğü
doldurmasın diye program o adresi yazmıyor.

## Veri kalıcı mı?

```text
docker compose down
docker compose up -d
curl localhost:8095/stats
{"notes": 1, "starts": 2}
```

`down` konteyneri sildi, `up` yenisini kurdu; not yerinde duruyor ve
program ikinci kez başladığını biliyor, çünkü veritabanı volume'da.
`docker compose down -v` ise volume'u da siliyor: veri gider.

Konteynerin içinden bakınca dosyanın sahibi kullanıcı (1000):

```text
docker compose exec web ls -ln /data
-rw-r--r-- 1 1000 1000 12288 Oct  6 20:34 notes.db
```

## Sık yapılan hatalar

**Veri klasörü kullanıcıya verilmemiş.** `mkdir /data && chown app:app
/data` satırı olmadan program açılır açılmaz düşüyor:

```text
sqlite3.OperationalError: unable to open database file
```

Boş bir adlı volume, bağlandığı klasörün imajdaki sahibini alıyor. Klasör
imajda hiç yoksa Docker onu root'a ait oluşturuyor ve `app` kullanıcısı
oraya yazamıyor.

**Sağlık denetimi kopyalanmamış ya da yanlış porta bakıyor.** Program
çalışır, ama durum bir süre sonra `unhealthy` olur. Sebebi
`docker inspect web --format "{{json .State.Health}}"` çıktısında,
denetimin son çıktılarında yazıyor.

**`localhost`'ta dinlemek.** Port açık görünür ama istek cevapsız kalır
(`Empty reply from server`); program `0.0.0.0`'da dinlemeli.

**Kodu değiştirip yeniden kurmamak.** `docker compose up -d` imajı
yeniden kurmuyor; kod değiştiyse `--build`.

## Yayından önce kontrol listesi

1. Program `0.0.0.0`'da dinliyor, ayarları ortamdan okuyor, günlüğü
   ekrana yazıyor, SIGTERM'de kapanıyor.
2. Taban imajın sürümü sabit (`python:3.13-slim`).
3. Önce `requirements.txt` ve `pip install`, sonra kod.
4. `.dockerignore` var; `.env` ve yerel veritabanı imaja girmiyor.
5. Kullanıcı `USER app`; yazılan klasörler ona ait.
6. `EXPOSE`, `HEALTHCHECK` ve exec biçiminde `CMD`.
7. Veri adlı volume'da; `restart: unless-stopped`.
8. `docker compose up -d --build` → `healthy` → istekler cevap veriyor →
   `down` / `up` sonrası veri yerinde.

## Özet

- Önce program hazır olmalı: `0.0.0.0`, ortam değişkenleri, ekrana günlük,
  SIGTERM.
- Dockerfile'da sıralama önbellek için (paketler önce, kod sonra), güvenlik
  için (`USER` paketlerden sonra) ve kapanış için (exec biçimi) önemli.
- `HEALTHCHECK` sağlık denetimini imajın içine koyuyor; denetim
  konteynerin içinde çalışıyor, çıkış kodu 0 = sağlıklı.
- Compose servisi tek komutla kuruyor; veri adlı volume'da, ayarlar
  `.env`'de.
