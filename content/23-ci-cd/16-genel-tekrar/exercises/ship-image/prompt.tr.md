Etiketle çalışan bu hat imajı derliyor ama gönderemiyor. Düzelt ve dağıtımı ekle:

- `publish` işine izinler: `contents: read`, `packages: write`.
- Derleme adımında `push: true`.
- Yeni `deploy-production` işi: `publish` bitince, `ubuntu-latest`, `environment: production`; `concurrency` grubu `deploy-production`, `cancel-in-progress: false`. Kodu çeksin ve `python scripts/deploy.py "ghcr.io/ada/tempconv:$GITHUB_SHA"` çalıştırsın.
