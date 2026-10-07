compose.yaml'da en sık kullanılan anahtarlar ve `docker run` karşılıkları.

## Servis anahtarları

| Anahtar | Örnek | `docker run` karşılığı |
|---|---|---|
| `image` | `image: python:3.13-slim` | `docker run python:3.13-slim` |
| `build` | `build: .` | `docker build .` |
| `container_name` | `container_name: web` | `--name web` |
| `command` | `command: ["python", "app.py"]` | imajdan sonra yazılan komut (CMD'yi ezer) |
| `entrypoint` | `entrypoint: ["python"]` | `--entrypoint` |
| `ports` | `- "8080:8000"` | `-p 8080:8000` |
| `expose` | `- "8000"` | (yalnızca diğer servislere) |
| `environment` | `APP_ENV: production` | `-e APP_ENV=production` |
| `env_file` | `env_file: .env` | `--env-file .env` |
| `volumes` | `- appdata:/data` | `-v appdata:/data` |
| `working_dir` | `working_dir: /app` | `-w /app` |
| `user` | `user: "1000"` | `--user 1000` |
| `restart` | `restart: unless-stopped` | `--restart unless-stopped` |
| `init` | `init: true` | `--init` |
| `depends_on` | `- db` | (önce db başlasın) |
| `healthcheck` | `test: [...]` | `--health-cmd` |

## `build` uzun biçimi

```yaml
build:
  context: .
  dockerfile: Dockerfile.dev
  args:
    VERSION: "2.1"
  target: runtime
```

`args` → `--build-arg`, `target` → çok aşamalı derlemede aşama (İmajı
Küçültmek bölümü).

## `environment` iki biçimde yazılabiliyor

```yaml
environment:
  APP_ENV: production
  DEBUG: "false"
```

```yaml
environment:
  - APP_ENV=production
  - DEBUG=false
```

İkisi aynı. Birinci biçimde `true`, `false`, `yes`, `no` gibi değerleri
tırnağa al; YAML onları metin değil mantıksal değer sanabiliyor.

## `restart` seçenekleri

| Değer | Ne zaman yeniden başlatır? |
|---|---|
| `no` (varsayılan) | Hiçbir zaman |
| `on-failure` | Program hatayla (0 dışı kodla) bitince |
| `always` | Her durduğunda (Docker yeniden başlayınca da) |
| `unless-stopped` | `always` gibi; ama sen durdurduysan değil |

## En alttaki bölümler

```yaml
volumes:
  appdata:

networks:
  backend:
```

Servislerde kullanılan **adlı** volume'lar ve özel ağlar burada
tanımlanıyor. Tanımlanmamış adlı bir volume kullanırsan Compose hata veriyor:
`service "web" refers to undefined volume appdata`.

## Dosyanın adı

Compose şu adları sırayla arıyor: `compose.yaml`, `compose.yml`,
`docker-compose.yaml`, `docker-compose.yml`. Yeni projelerde `compose.yaml`.
Başka bir ad için `docker compose -f dosya.yaml up`.
