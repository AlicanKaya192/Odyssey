# İmajı Küçültmek: Çok Aşamalı Derleme

Bir imaj ne kadar büyükse o kadar yavaş iniyor, o kadar çok yer kaplıyor ve
içinde o kadar çok gereksiz program duruyor (her biri olası bir güvenlik
açığı). Bu bölümde imajın neden büyüdüğünü ölçecek ve en güçlü küçültme
yöntemini, **çok aşamalı derlemeyi**, öğreneceğiz.

## Boyut nereden geliyor?

`docker images` her imajın boyutunu gösteriyor:

```text
IMAGE              DISK USAGE
python:3.13-slim        178MB
alpine:3.22            12.8MB
```

Kendi imajının boyutu = taban imaj + senin eklediğin katmanlar. Hangi
katmanın ne kadar tuttuğunu `docker history` söylüyor; büyük bir sayı
görürsen oraya bak.

## Silmek katmanı küçültmez

Bir dosyayı oluşturup sonraki satırda silelim:

```dockerfile
FROM alpine:3.22
RUN head -c 30000000 /dev/urandom > /big.bin
RUN rm /big.bin
```

Dosya imajda yok, ama:

```text
docker history odyssey-a
4.1kB   RUN /bin/sh -c rm /big.bin
30MB    RUN /bin/sh -c head -c 30000000 /dev/urandom…
```

İmaj **72,8 MB**. Her `RUN` bir katman ve katmanlar üst üste duruyor: ikinci
katman dosyayı yalnızca "silindi" diye **işaretliyor**; birinci katmandaki
30 MB yerinde. (İmajın boyutu ayrıca katmanların sıkıştırılmamış hâlini de
sayıyor.)

Aynı iş **tek** `RUN`'da:

```dockerfile
RUN head -c 30000000 /dev/urandom > /big.bin && rm /big.bin
```

İmaj **12,8 MB**: Alpine'ın kendisi kadar. Dosya aynı katmanda oluşup
silindiği için katmana hiç girmedi.

Kural: **geçici dosyayı oluşturduğun `RUN`'da sil.** Paket kurarken
önbelleği aynı satırda temizlemek (`pip install --no-cache-dir`, `apt-get
... && rm -rf /var/lib/apt/lists/*`) bu yüzden.

## Çok aşamalı derleme

Çoğu zaman bir şeyi **üretmek** için gereken araçlar, onu **çalıştırmak**
için gerekmiyor: derleyiciler, test araçları, kaynak dosyalar. Çok aşamalı
derlemede bir Dockerfile'da **birden çok `FROM`** var; her `FROM` yeni bir
aşama başlatıyor ve son imaja yalnızca **son aşama** giriyor.

Örnek: Python'la bir HTML raporu üretiyoruz, ama raporu taşımak için
Python'a gerek yok.

```dockerfile
FROM python:3.13-slim AS build
WORKDIR /src
COPY build_report.py .
RUN python build_report.py

FROM alpine:3.22
COPY --from=build /out /report
CMD ["cat", "/report/index.html"]
```

- `AS build`: aşamaya ad veriyor.
- İlk aşamada Python raporu üretip `/out`'a yazıyor.
- İkinci `FROM` sıfırdan, temiz bir Alpine'la başlıyor.
- `COPY --from=build /out /report`: başka bir aşamadan **yalnızca** gereken
  dosyaları al.

<figure class="fig">
  <div class="flow">
    <span class="node">Aşama 1: build<br><small>python:3.13-slim · 176 MB</small></span><span class="arrow">→ COPY --from=build /out →</span>
    <span class="node ok">Aşama 2 (son imaj)<br><small>alpine:3.22 · 12,8 MB</small></span>
  </div>
  <figcaption>İlk aşama üretiyor ve atılıyor; son imaja yalnızca son aşama ve oraya kopyalanan sonuç giriyor.</figcaption>
</figure>

Sonuç:

```text
IMAGE           DISK USAGE
report          12.8MB
report:build    176MB
```

Son imaj 12,8 MB ve içinde Python **yok**: üretim araçları ilk aşamada kaldı.

## Bir aşamayı tek başına kurmak: `--target`

```text
docker build --target build -t report:build .
```

Derleme `build` aşamasında duruyor; ara sonucu incelemek ya da testleri
çalıştırmak için kullanışlı (176 MB'lık imaj buydu).

## Python uygulamalarında

Saf Python bir uygulama `python:3.13-slim` üzerinde kalıyor (çalışmak için
Python lazım); ama çok aşamalı derleme yine işe yarıyor:

```dockerfile
FROM python:3.13 AS build
WORKDIR /src
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.13-slim
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . /app
CMD ["python", "/app/main.py"]
```

Derlenmesi gereken paketler (C eklentili kütüphaneler) **büyük** imajda
derleme araçlarıyla hazırlanıyor; son imaja yalnızca hazır paketler giriyor.
(Bu örnek internetten paket indirdiği için bu patikada çalıştırılmıyor.)

## Küçültme kontrol listesi

1. Doğru taban: `-slim` (ya da uygunsa `alpine`), tam imaj değil.
2. `.dockerignore`: `.git`, `.venv`, veri dışarıda.
3. `pip install --no-cache-dir`; geçici dosyalar aynı `RUN`'da silinir.
4. Üretim araçları ayrı bir aşamada; son aşamaya yalnızca sonuç.
5. `docker history` ile en büyük katmanı bul.

## Özet

- İmaj boyutu = taban + katmanlar; büyük katmanı `docker history` gösterir.
- Sonraki `RUN`'da silmek imajı küçültmez (72,8 MB); aynı `RUN`'da silmek
  küçültür (12,8 MB).
- Çok aşamalı derleme: birden çok `FROM`, `AS ad`, `COPY --from=ad`; son
  imaja yalnızca son aşama girer (176 MB → 12,8 MB).
- `--target ad` derlemeyi o aşamada durdurur.
