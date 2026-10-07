# İlk Dockerfile

Şimdiye kadarki Dockerfile'lar iki üç satırdı. Bu bölümde gerçek bir Python
projesini paketleyen, her satırının nedenini bildiğin bir Dockerfile
yazacağız. Patikanın geri kalanı bu iskeletin üstüne kurulacak.

## Proje

Klasörde üç dosya var:

```text
greeter/
├── app.py
├── requirements.txt
└── Dockerfile
```

`app.py` programın kendisi, `requirements.txt` ihtiyaç duyduğu paketlerin
listesi (şimdilik boş), `Dockerfile` da tarif:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Altı satır, beş farklı talimat. Tek tek bakalım.

## `FROM`: nereden başlıyoruz?

```dockerfile
FROM python:3.13-slim
```

Her Dockerfile `FROM` ile başlıyor: imajın üstüne kurulacağı **taban
imaj**. Python kurmakla uğraşmıyoruz; Python'u kurulu hazır bir imajdan
başlıyoruz. Sürüm sabitlenmiş (`3.13-slim`, `latest` değil).

## `WORKDIR`: çalışma klasörü

```dockerfile
WORKDIR /app
```

İmajın içinde `/app` klasörünü oluşturup **içine giriyor**; sonraki bütün
talimatlar orada çalışıyor. Terminaldeki `cd` gibi, ama klasör yoksa onu da
oluşturuyor.

Neden gerekli? `WORKDIR` yazmazsan her şey imajın kök klasörüne (`/`)
gidiyor; senin dosyaların Linux'un `bin`, `etc`, `usr` klasörleriyle karışıyor.
Kendi klasörün düzenli ve tahmin edilebilir.

## `COPY`: dosyaları imaja almak

```dockerfile
COPY requirements.txt .
COPY . .
```

`COPY kaynak hedef`:

- **kaynak**: bilgisayarındaki dosya, Dockerfile'ın bulunduğu klasöre göre.
- **hedef**: imajın içindeki yer. `.` "çalışma klasörü" demek, yani `/app`.

`COPY . .` "buradaki her şeyi `/app`'e kopyala" demek. Peki neden önce yalnızca
`requirements.txt`'yi kopyalayıp sonra hepsini kopyalıyoruz? Cevabı bir
sonraki bölümde, derleme önbelleğinde. Şimdilik sıra böyle olsun.

## `RUN`: derleme sırasında komut çalıştırmak

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

`RUN` imaj **kurulurken** bir komut çalıştırıyor ve sonucunu imaja yeni bir
katman olarak kaydediyor. Burada `requirements.txt`'deki paketleri
kuruyoruz; kurulan paketler imajın içinde kalıyor.

`--no-cache-dir` pip'e indirdiği dosyaların kopyasını saklamamasını
söylüyor. Bilgisayarında işe yarayan bu önbellek imajda yalnızca yer
kaplıyor.

## `CMD`: konteyner çalışınca

```dockerfile
CMD ["python", "app.py"]
```

Konteyner **çalıştırıldığında** çalışacak komut. Dockerfile'da tek bir `CMD`
etkili oluyor; birden fazla yazarsan sonuncusu geçerli.

## En önemli ayrım: `RUN` ve `CMD`

<figure class="fig">
  <div class="versus">
    <div><h4>RUN</h4><p><b>Ne zaman:</b> imaj kurulurken (<code>docker build</code>)</p><p><b>Kaç kez:</b> her derlemede bir kez</p><p><b>Sonucu:</b> imaja yeni katman olarak girer</p><p><b>Kaç tane:</b> istediğin kadar</p><p><b>Örnek:</b> paket kurmak</p></div>
    <div class="ok"><h4>CMD</h4><p><b>Ne zaman:</b> konteyner çalışınca (<code>docker run</code>)</p><p><b>Kaç kez:</b> her konteynerde bir kez</p><p><b>Sonucu:</b> programın çıktısı</p><p><b>Kaç tane:</b> yalnızca sonuncusu geçerli</p><p><b>Örnek:</b> programı başlatmak</p></div>
  </div>
  <figcaption><code>RUN</code> imajı hazırlıyor, <code>CMD</code> konteynere ne yapacağını söylüyor.</figcaption>
</figure>

Sık yapılan hata: programı `RUN python app.py` ile çalıştırmaya çalışmak.
O satır programı **imaj kurulurken bir kez** çalıştırır, konteyner açılınca
değil.

## Kurmak ve çalıştırmak

Klasörün içindeyken:

```text
docker build -t greeter .
```

Çıktı (biraz kısaltılmış):

```text
#5 [1/5] FROM docker.io/library/python:3.13-slim@sha256:bf44cdfc...
#6 [2/5] WORKDIR /app
#7 [3/5] COPY requirements.txt .
#8 [4/5] RUN pip install --no-cache-dir -r requirements.txt
#8 1.466 WARNING: Running pip as the 'root' user can result in broken permissions...
#9 [5/5] COPY . .
#10 naming to docker.io/library/greeter:latest done
```

- Her `[n/5]` satırı Dockerfile'daki bir talimat (FROM dahil beş adım).
- pip'in "root" uyarısı burada zararsız: konteynerin içinde başka bir şey
  bozulmuyor. Güvenlik bölümünde imajı root olmayan bir kullanıcıyla
  çalıştırmayı öğreneceğiz.
- Son satır: imaj `greeter:latest` adıyla kaydedildi (`-t greeter` etiket
  yazmadığın için `latest` eklendi).

Çalıştır:

```text
docker run --rm greeter
```

```text
Hello from the greeter
```

## Derleme bağlamı

Komuttaki son `.` **derleme bağlamı** (build context): Docker'a gönderilen
klasör. Derleme başlarken bu klasörün tamamı motora aktarılıyor
(`transferring context` satırı) ve `COPY` yalnızca bu klasörün **içinden**
dosya alabiliyor.

Bağlamın dışından bir dosya istersen ya da adı yanlış yazarsan:

```text
COPY app.pyy .
```

```text
ERROR: failed to build: failed to solve: failed to compute cache key:
failed to calculate checksum of ref ...: "/app.pyy": not found
```

Hatanın sonu önemli: `"/app.pyy": not found` → bağlamda böyle bir dosya yok.

## Dockerfile yazım kuralları

- Talimatlar **büyük harfle** yazılır (`FROM`, `COPY`). Küçük harf de
  çalışıyor ama alışkanlık büyük harf.
- Her satır bir talimat. Uzun bir satırı bölmek için satır sonuna `\`
  konuyor.
- `#` ile başlayan satır yorum.
- Dosyanın adı `Dockerfile` (uzantısız, D büyük). Başka bir adla yazdıysan
  `docker build -f Dockerfile.dev .` ile gösterilir.

## Özet

- İskelet: `FROM` → `WORKDIR` → `COPY requirements.txt` → `RUN pip install`
  → `COPY . .` → `CMD`.
- `WORKDIR` kendi klasörünü oluşturup içine girer; dosyalar `/`'e dağılmaz.
- `COPY kaynak hedef`; kaynak derleme bağlamının içinden, hedef imajın
  içinde (`.` = çalışma klasörü).
- **`RUN` derleme sırasında, `CMD` konteyner çalışınca.**
- `docker build -t ad .` kurar (`.` derleme bağlamı), `docker run --rm ad`
  çalıştırır.
- `"...": not found` hatası: dosya bağlamda yok ya da adı yanlış.
