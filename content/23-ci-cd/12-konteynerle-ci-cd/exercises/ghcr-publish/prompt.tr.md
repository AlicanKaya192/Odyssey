`image` işi imajı derleyip sınıyor. İmajı `ghcr.io`'ya gönderen bir `publish` işi ekle:

- `image` bitince başlasın, yalnızca gönderimde: `if: github.event_name == 'push'`. Makine `ubuntu-latest`.
- İş izinleri: `contents: read`, `packages: write`.
- Adımlar: kodu çek, `docker/setup-buildx-action@v3`, `docker/login-action@v3` (`registry: ghcr.io`, `username: ${{ github.actor }}`, `password: ${{ secrets.GITHUB_TOKEN }}`).
- Son adım `docker/build-push-action@v6`: `context: .`, `push: true`, `tags: ghcr.io/ada/greeter:${{ github.sha }}`, `cache-from: type=gha`, `cache-to: type=gha,mode=max`.
