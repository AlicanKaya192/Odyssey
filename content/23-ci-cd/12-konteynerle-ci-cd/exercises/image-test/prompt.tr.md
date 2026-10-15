`image` işi yalnızca kodu çekiyor. Arkasına şu adımları ekle:

- `docker/setup-buildx-action@v3`.
- `docker/build-push-action@v6`: `context: .`, `load: true`, `tags: greeter:test`.
- Testleri imajın içinde çalıştır: `docker run --rm greeter:test python -m pytest -q`.
