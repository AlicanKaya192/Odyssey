Patikanın bütün komutları ve kuralları tek sayfada.

## Konteyner

```text
docker run --rm -it python:3.13-slim sh      # aç, içine gir, bitince sil
docker run -d --name web -p 8080:8000 app    # arka planda, port açık
docker ps -a                                 # hepsi, çıkış kodlarıyla
docker logs -f --tail 50 web                 # günlük (canlı)
docker exec -it web sh                       # çalışan konteynerin içi
docker stop web && docker rm web             # durdur, sil
docker cp web:/app/log.txt .                 # dosyayı dışarı al
```

## İmaj

```text
docker build -t app .                        # bu klasörden kur
docker build --no-cache --progress=plain -t app .
docker images                                # imajlar ve boyutları
docker history app                           # katmanlar
docker image prune                           # etiketsiz imajları sil
```

## Dockerfile

| Talimat | Not |
|---|---|
| `FROM python:3.13-slim` | Sürüm sabit; `AS build` ile aşama adı |
| `WORKDIR /app` | Klasörü oluşturur ve oraya geçer |
| `COPY requirements.txt .` | Önce bağımlılıklar |
| `RUN pip install --no-cache-dir -r ...` | Komutları `&&` ile tek katmanda |
| `COPY . .` | Kod en sonda; `.dockerignore` ile |
| `ENV KEY=value` | Varsayılan ayar; sır değil |
| `USER app` | Paketlerden sonra |
| `EXPOSE 8000` | Belge |
| `HEALTHCHECK CMD [...]` | 0 sağlıklı, 1 sağlıksız |
| `CMD ["python", "app.py"]` | Exec biçimi |
| `COPY --from=build ...` | Çok aşamalı derleme |

## Veri ve ayar

```text
docker run -v notes:/data app                # adlı volume
docker run -v ${PWD}:/app app                # bind mount (PowerShell)
docker run -e DEBUG=1 --env-file .env app    # ortam değişkenleri
docker volume ls / docker volume rm notes
```

## Compose

```text
docker compose up -d --build                 # kur ve başlat
docker compose ps                            # durum, (healthy)
docker compose logs -f web                   # bir servisin günlüğü
docker compose exec web sh                   # servisin içi
docker compose down                          # sil (volume kalır)
docker compose down -v                       # volume'larla birlikte
```

## Çıkış kodları

| Kod | Anlamı |
|---|---|
| `0` | Program işini bitirdi |
| `1` | Programın kendi hatası (`docker logs`) |
| `127` | Komut bulunamadı (`CMD` yazımı) |
| `137` | Öldürüldü: SIGTERM duyulmadı ya da bellek |
| `143` | SIGTERM ile düzgün kapandı (`--init` ile) |

## Akılda kalsın

> Dockerfile tarif, imaj sınıf, konteyner nesne. Önce paketler, sonra kod.
> Veri volume'da, ayar ortamda, sır hiçbir yerde. Program `0.0.0.0`'da, root
> olmadan, exec biçiminde.
