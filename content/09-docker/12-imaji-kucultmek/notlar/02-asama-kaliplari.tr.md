Çok aşamalı derleme yalnızca küçültmek için değil; bir Dockerfile'da
birden çok amaç için de kullanılıyor.

## Test aşaması

```dockerfile
FROM python:3.13-slim AS base
WORKDIR /app
COPY . .

FROM base AS test
RUN python -m unittest

FROM base AS runtime
CMD ["python", "main.py"]
```

- `FROM base`: başka bir aşamadan başlamak; ortak adımlar bir kez yazılıyor.
- `docker build --target test .` testleri çalıştırır; düşerse derleme düşer.
- `docker build .` son aşamayı (`runtime`) kurar; testler imaja girmez.

## Geliştirme ve yayın

```dockerfile
FROM python:3.13-slim AS runtime
...
CMD ["python", "main.py"]

FROM runtime AS dev
ENV DEBUG=true
CMD ["python", "main.py", "--reload"]
```

Compose'da hangisinin kurulacağı:

```yaml
services:
  web:
    build:
      context: .
      target: dev
```

## Hazır bir imajdan dosya almak

`COPY --from` yalnızca aşama adı değil, bir imaj adı da alabiliyor:

```dockerfile
COPY --from=alpine:3.22 /bin/busybox /usr/local/bin/busybox
```

Bir aracı bütün imajı taşımadan almak için. Dikkat: alınan dosyanın
çalışması için ihtiyaç duyduğu kütüphaneler de yeni imajda olmalı.

## Aşama sırası ve önbellek

Her aşamanın kendi önbelleği var. Son aşamanın ihtiyaç duymadığı bir aşama
`docker build` sırasında **atlanıyor** (BuildKit): test aşaması varsayılan
derlemede çalışmıyor; ancak `--target test` ile.
