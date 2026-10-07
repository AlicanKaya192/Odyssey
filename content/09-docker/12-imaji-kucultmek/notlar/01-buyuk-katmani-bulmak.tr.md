İmajın neden büyük olduğunu bulmanın yolları.

## `docker history`

```text
docker history app --format "{{.Size}}\t{{.CreatedBy}}"
```

Her katmanın boyutu ve onu oluşturan talimat. En büyük sayılara bak:

| Görürsen | Büyük ihtimalle |
|---|---|
| `COPY . .` yüzlerce MB | `.dockerignore` eksik (`.git`, `.venv`, veri) |
| `RUN pip install` çok büyük | `--no-cache-dir` yok ya da gereksiz paketler var |
| Silme satırı 0 B ama önceki büyük | Silme ayrı `RUN`'da; aynı satıra taşı |
| `apt-get install` büyük | `--no-install-recommends` yok, liste temizlenmemiş |

## İmajın içine bakmak

```text
docker run --rm app du -sh /app /usr/local/lib/python3.13/site-packages
```

`du -sh` bir klasörün kapladığı yeri yazıyor. Beklemediğin büyük bir klasör
genellikle yanlışlıkla kopyalanmış bir şey.

## Boyutu bir sayıyla görmek

```text
docker image inspect app --format "{{.Size}}"
```

Bayt cinsinden. Odyssey'nin `max_size_mb` kontrolü bu sayıya bakıyor.

## Paylaşılan katmanlar

`docker images`'taki boyutlar katmanları paylaşımlı saymıyor: aynı
`python:3.13-slim`'den kurulan beş imajın her biri 180 MB'ın üstünde
görünür, ama diskte Python katmanları bir kez durur. Gerçek kullanım için
`docker system df`.

## Daha görsel bir araç

`dive` adlı açık kaynak araç bir imajı katman katman açıp her katmanda hangi
dosyaların eklendiğini gösteriyor. Bu patikada kurmuyoruz ama büyük
projelerde işe yarar.
