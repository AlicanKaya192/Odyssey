**Hattın akışı**

Derle → imajın içinde test et → aynı imajı depoya gönder → aynı imajı
dağıt.

**Eylemler**

| Eylem | Ne yapar |
|---|---|
| `docker/setup-buildx-action@v3` | Derleyiciyi (Buildx) hazırlar |
| `docker/build-push-action@v6` | İmajı derler; `push: true` ile gönderir |
| `docker/login-action@v3` | İmaj deposuna girer |

**`build-push-action` ayarları**

| Ayar | Anlamı |
|---|---|
| `context: .` | Derleme deponun kökünden |
| `tags:` | İmajın adı ve etiketi |
| `load: true` | İmajı makinenin Docker'ına yükle (`docker run` için) |
| `push: true` | İmajı depoya gönder |
| `cache-from: type=gha` | Katmanları GitHub önbelleğinden al |
| `cache-to: type=gha,mode=max` | Katmanları önbelleğe yaz (ara katmanlar dahil) |

**Derle ve imajda test et**

```yaml
      - uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: greeter:test
      - run: docker run --rm greeter:test python -m pytest -q
```

**`ghcr.io`'ya gönder**

```yaml
    permissions:
      contents: read
      packages: write
    steps:
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
```

- PR'da derle ve sına, **gönderme**: `if: github.event_name == 'push'`.
- İmaj adı küçük harf.

**İşin kendisi bir konteynerde**

```yaml
  lint:
    runs-on: ubuntu-latest
    container: python:3.13-slim
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install ruff
      - run: python -m ruff check .
```

`container:` işin bütün adımlarını o imajın içinde çalıştırır; `services:`
ise işin **yanında** ayrı konteyner açar.
