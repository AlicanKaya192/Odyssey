**GitHub ortamı (Settings › Environments)**

| Kural | Ne yapar |
|---|---|
| Onaylayıcılar | İş, onay gelene kadar bekler |
| Bekleme süresi | İş başlamadan önce belirli bir süre bekler |
| Dal ve etiket kuralı | Yalnızca izin verilen dal/etiketten dağıtılır |
| Ortam gizli değerleri | Yalnızca o ortama bağlı işlerde görünür |
| Ortam değişkenleri | `${{ vars.AD }}`, yalnızca o ortamda |

**İşi ortama bağlamak**

```yaml
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
```

```yaml
  deploy-production:
    needs: deploy-staging
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    concurrency:
      group: deploy-production
      cancel-in-progress: false
```

- `url`: çalışma sayfasında canlı adresin bağlantısı.
- Dağıtımda `cancel-in-progress: false`: yarıda kesilen dağıtım sunucuyu
  iki sürümün arasında bırakır.

**Dağıtımdan sonra**

```yaml
      - run: python scripts/deploy.py staging
      - run: python scripts/check_health.py "$APP_URL"
        env:
          APP_URL: ${{ vars.STAGING_URL }}
      - run: python scripts/deploy.py staging --rollback
        if: failure()
```

**Kontrol listesi**

- Önce staging, sonra production; canlıya yalnızca etiketle.
- Canlı ortamında onaylayıcı var.
- Dağıtılan paket `build`'in ürettiği aynı dosya.
- Dağıtımdan sonra sağlık denetimi, düşerse geri alma.
- Aynı anda tek canlı dağıtımı (`concurrency`).
