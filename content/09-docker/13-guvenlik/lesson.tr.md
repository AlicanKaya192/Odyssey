# Güvenlik ve İyi Alışkanlıklar

Konteyner programı bilgisayarın geri kalanından ayırıyor ama bu ayrılık
mutlak değil: çekirdek ortak, bazı ayarlar ayrılığı gevşetiyor ve imajın
içine yanlışlıkla koyduğun şey imajla birlikte herkese gidiyor. Bu bölümde
en önemli alışkanlıkları topluyoruz; çoğunu önceki bölümlerde gördün,
şimdi bir arada ve nedenleriyle.

## Konteyner varsayılan olarak root

```text
docker run --rm python:3.13-slim id
uid=0(root) gid=0(root) groups=0(root)
```

Konteynerin içindeki program **root** (yönetici, kullanıcı numarası 0)
olarak çalışıyor. Program ele geçirilirse saldırgan konteynerin içinde her
şeyi yapabiliyor; bağlı bir klasöre root olarak yazabiliyor; çekirdekte bir
açık varsa dışarı çıkma ihtimali artıyor.

Kural: **programı root olmayan bir kullanıcıyla çalıştır.**

## `USER`: kullanıcıya geçmek

```dockerfile
FROM python:3.13-slim
RUN useradd --create-home --uid 1000 app
WORKDIR /app
COPY . .
USER app
CMD ["python", "app.py"]
```

- `useradd --create-home --uid 1000 app`: `app` adında, ev klasörü olan,
  numarası 1000 olan bir kullanıcı oluştur (Debian tabanlı imajlarda;
  Alpine'da `adduser -D app`).
- `USER app`: bu satırdan sonraki talimatlar **ve konteynerin kendisi** bu
  kullanıcıyla çalışır.

```text
docker run --rm app id
uid=1000(app) gid=1000(app) groups=1000(app)
```

`USER`'ı paket kurulumlarından **sonra** yaz: `pip install` ve `apt-get`
root ister.

## İzin tuzağı

`WORKDIR /app` klasörü root olarak oluşturuyor. `USER app`'ten sonra
program oraya yazmaya kalkınca:

```text
touch: cannot touch '/app/x': Permission denied
```

Okumak serbest, yazmak yasak. Program bir klasöre yazacaksa o klasörün
sahibini kullanıcı yap:

```dockerfile
RUN useradd --create-home --uid 1000 app
WORKDIR /app
RUN chown app:app /app
USER app
```

Kopyalanan dosyaların sahibi de varsayılan olarak root; gerekiyorsa
`COPY --chown=app:app . .`. Veri volume'a yazılıyorsa (Volume bölümü),
volume'un bağlandığı klasör (`/data`) de aynı şekilde kullanıcıya verilir.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>root olarak (varsayılan)</h4><p>uid=0</p><p>Ele geçirilirse konteynerde her şey serbest</p><p>Bağlı klasörlere root olarak yazar</p></div>
    <div class="ok"><h4>USER app</h4><p>uid=1000</p><p>Yalnızca kendi klasörüne yazabilir</p><p>Zarar sınırlı kalır</p></div>
  </div>
  <figcaption>Paketleri root olarak kur, programı kullanıcıyla çalıştır: <code>USER</code> paket kurulumundan sonra gelir.</figcaption>
</figure>

## Çalıştırırken yetkiyi azaltmak

| Seçenek | Ne yapar? |
|---|---|
| `--read-only` | Konteynerin dosya sistemini salt okunur yapar; yazılacak yerler volume ile verilir. |
| `--cap-drop ALL` | Root'un özel yetkilerini (ağ ayarı, dosya sahipliği değiştirme...) kaldırır. |
| `--memory 512m --cpus 1` | Bellek ve işlemci sınırı; kaçak bir program bilgisayarı kilitlemez. |
| `--user 1000` | İmajda `USER` yoksa bile kullanıcıyla çalıştırır. |

```text
docker run --rm --read-only alpine:3.22 sh -c "touch /x"
touch: /x: Read-only file system
```

**Asla** yapılmayanlar:

- `--privileged`: konteynere bilgisayarın neredeyse bütün yetkilerini
  veriyor; ayrılık fiilen kalkıyor.
- Docker'ın kendi soketini (`/var/run/docker.sock`) konteynere bağlamak:
  konteyner bilgisayarda istediği konteyneri çalıştırabilir hâle geliyor.
- `--network host` (gerekmedikçe): ağ ayrılığı kalkıyor.

Odyssey bu yüzden compose alıştırmalarında `privileged`, `network_mode:
host` ve çalışma klasörü dışına bağlamayı reddediyor.

## İmajın içindekiler

- **Sır yok** (Ortam Değişkenleri bölümü): `ENV` / `ARG` ile şifre yazılmaz;
  `.env` `.dockerignore`'da.
- **Gereksiz program yok** (İmajı Küçültmek bölümü): derleme araçları ayrı
  aşamada; her fazla program olası bir açık.
- **Bilinen taban**: resmî ya da doğrulanmış yayıncının imajı, sürüm
  sabitli.

## Güncel kalmak

Taban imajlardaki açıklar zamanla bulunup kapatılıyor; yamalar yeni
imajlarla geliyor. Sürümü `3.13-slim` gibi sabitlemek yamaların gelmesine
izin veriyor; ama **senin imajın ancak yeniden kurulunca** onları alıyor:

```text
docker build --pull -t app .
```

`--pull` taban imajın yenisini indirip öyle kuruyor. Docker Desktop'taki
**Docker Scout** bir imajdaki bilinen açıkları listeleyebiliyor (Images ›
imaj › Vulnerabilities).

## Kontrol listesi

1. Sürüm sabitli, güvenilir taban imaj (`python:3.13-slim`).
2. `.dockerignore` (`.env`, `.git`); imajda sır yok.
3. Paketler `USER`'dan önce; sonra `USER app`.
4. Yazılan klasörler `chown` ile kullanıcıya.
5. Çok aşamalı derleme; son imajda yalnızca gereken.
6. Çalıştırırken: `--privileged` yok, soket yok; gerekiyorsa `--read-only`,
   bellek sınırı.
7. Düzenli `docker build --pull`.

## Özet

- Konteyner varsayılan olarak root; `RUN useradd ...` + `USER app` ile
  kullanıcıya geç.
- `USER`'dan sonra root'un oluşturduğu klasörlere yazılamaz:
  `chown app:app` ya da `COPY --chown`.
- Çalıştırırken yetkiyi azalt: `--read-only`, `--cap-drop ALL`, bellek
  sınırı; `--privileged` ve Docker soketini bağlamak yok.
- İmajda sır ve gereksiz program yok; taban imajı `--pull` ile güncel tut.
