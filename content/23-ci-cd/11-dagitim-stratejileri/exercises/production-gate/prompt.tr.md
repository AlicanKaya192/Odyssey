Canlıya dağıtan bir `deploy-production` işi ekle:

- `deploy-staging` bitince başlasın, yalnızca `v` etiketinde: `if: startsWith(github.ref, 'refs/tags/v')`. Makine `ubuntu-latest`.
- Ortamı sözlük olarak yaz: `name: production`, `url: https://app.example.com`.
- Aynı anda tek canlı dağıtım olsun: `concurrency` grubu `deploy-production`, `cancel-in-progress: false`.
- Kodu çeksin, `dist`'i indirsin, `python scripts/deploy.py production` çalıştırsın.
