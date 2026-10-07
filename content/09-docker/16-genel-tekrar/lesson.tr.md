# Genel Tekrar

Docker patikasının sonuna geldin. "Bende çalışıyordu" sorunuyla başladın;
şimdi bir Python programını her bilgisayarda aynı çalışan, verisini
koruyan, root olmayan ve sağlığını bildiren bir servise dönüştürebiliyorsun.
Bu bölüm yolu baştan sona bir kez daha yürüyor: her durakta en önemli fikir
ve en çok kullanacağın komut.

<figure class="fig">
  <div class="flow">
    <span class="node">Temeller<br><small>00–03</small></span><span class="arrow">→</span>
    <span class="node">Dockerfile<br><small>04–06</small></span><span class="arrow">→</span>
    <span class="node">Veri, Compose<br><small>07–11</small></span><span class="arrow">→</span>
    <span class="node">Güvenli<br><small>12–14</small></span><span class="arrow">→</span>
    <span class="node acc">API<br><small>15</small></span>
  </div>
  <figcaption>Docker patikasının yolu: tek bir konteynerden, her bilgisayarda aynı çalışan bir servise.</figcaption>
</figure>

## 1. Konteyner ve imaj (Bölüm 00–03)

**İmaj** bir programın ve ihtiyaç duyduğu her şeyin donmuş paketi;
**konteyner** o imajdan açılmış, çalışan bir kopya. Bir imajdan istediğin
kadar konteyner açılır. Konteyner sanal makine değil: kendi işletim
sistemini başlatmıyor, bilgisayarın çekirdeğini paylaşıyor; bu yüzden
saniyede açılıyor.

```text
docker run --rm python:3.13-slim python -c "print(42)"
docker run -d --name web python:3.13-slim sleep 300
docker ps -a / docker logs web / docker exec -it web sh
docker stop web / docker rm web
```

İmaj **katmanlardan** oluşuyor; aynı taban imajı kullanan imajlar o
katmanları paylaşıyor. Etiketsiz ad `latest` demek; sürümü her zaman yaz
(`python:3.13-slim`).

## 2. Dockerfile (Bölüm 04–06)

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

- Her talimat bir katman; değişen talimattan **sonrası** önbellekten
  gelmiyor. Bu yüzden önce paketler, en sonda sık değişen kod.
- `.dockerignore` bağlama girmeyecekleri ayıklıyor: `.git`, `.venv`,
  `**/__pycache__`, `.env`.
- `CMD` varsayılan komut, `docker run app ...` ile ezilir. `ENTRYPOINT`
  sabit komut, `CMD` ona argüman olur.
- **Exec biçimi** (`["python", "app.py"]`): SIGTERM programa ulaşıyor.
  Kabuk biçiminde `docker stop` 10 saniye bekleyip öldürüyor (`137`).

## 3. Dışarıyla bağlantı (Bölüm 07–09)

| Konu | Kural |
|---|---|
| Port | `-p 8080:8000`: bilgisayarın 8080'i → konteynerin 8000'i. Program `0.0.0.0`'da dinlemeli. |
| Ortam | `-e KEY=value`, `--env-file .env`; Dockerfile'da `ENV` varsayılan. Sır imaja girmez. |
| Volume | `-v notes:/data`: veri konteynerin dışında, konteyner silinse de kalır. |
| Bind mount | `-v ${PWD}:/app`: bilgisayarındaki klasör konteynerde; geliştirirken. |

Konteynerin içindeki dosya sistemi geçici: konteyner silinince içine
yazılan her şey gidiyor. Kalması gereken her şey volume'a.

## 4. Compose (Bölüm 10–11)

```yaml
services:
  web:
    build: ./web
    ports: ["8095:8000"]
    env_file: .env
    depends_on:
      api:
        condition: service_healthy
  api:
    build: ./api
    volumes: [api-data:/data]
    healthcheck:
      test: ["CMD", "python", "healthcheck.py"]
volumes:
  api-data:
```

Compose bütün `docker run` ayarlarını bir dosyada topluyor:
`docker compose up -d --build`, `ps`, `logs -f`, `down` (`-v` volume'ları
da siler). Servisler aynı ağda, birbirine **servis adıyla** ulaşıyor
(`http://api:8000`); konteynerin içinde `localhost` kendisi.
`depends_on` yalnızca başlama sırası; "hazır olana kadar bekle" için
sağlık denetimi + `condition: service_healthy`.

## 5. Üretime hazır imaj (Bölüm 12–13)

- **Çok aşamalı derleme:** derleme araçları ilk aşamada kalıyor, son imaja
  yalnızca sonuç kopyalanıyor (`COPY --from=build`). Ölçtüğümüz örnekte
  176 MB → 12,8 MB.
- Bir dosyayı sonraki bir `RUN`'da silmek imajı küçültmüyor: dosya önceki
  katmanda duruyor. Aynı `RUN`'da indir, kullan, sil.
- **Root olma:** `RUN useradd ... app` + `USER app`; yazılan klasörleri
  `chown` ile kullanıcıya ver.
- Sır imaja girmez (`ARG` değerleri bile `docker history`'de görünüyor);
  `--privileged` ve Docker soketini bağlamak yok.

## 6. Sorun çıkınca (Bölüm 14)

Önce hangi aşamada olduğuna karar ver:

| İmaj kurulamıyor | Konteyner çalışmıyor |
|---|---|
| Çıktının **son satırları** | `docker ps -a` → çıkış kodu |
| Düşen adım `[3/5] RUN ...` | `docker logs` → son sözler |
| `--progress=plain --no-cache` | `--entrypoint sh` ile içine bak |

Çıkış kodları: `0` iş bitti (sunucu değilse doğal), `1` programın hatası,
`127` komut bulunamadı, `137` öldürüldü (SIGTERM duyulmadı ya da bellek).

## Bütün parçalar bir arada (Bölüm 15)

Patikanın son projesindeki Dockerfile neredeyse bütün bölümleri
kullanıyor:

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

Sürümü sabit taban (03), önbellek sırası (05), ortamdan ayarlar (08), veri
klasörü (09), root olmayan kullanıcı (13), sağlık denetimi (11, 15), exec
biçimi (06). Her satırın neden orada olduğunu söyleyebiliyorsan, bu
patikanın amacına ulaştın.

## Sırada ne var?

Docker bir programı **paketlemeyi** ve **çalıştırmayı** öğretti. Sıradaki
adım, yazdığın API'yi (API 2 patikası) ya da bir makine öğrenmesi modelini
bu paketle bir sunucuya taşımak: aynı imaj, aynı `compose.yaml`, yalnızca
farklı bir `.env`.
