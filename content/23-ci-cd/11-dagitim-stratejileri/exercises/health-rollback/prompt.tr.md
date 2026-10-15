`deploy-staging` işi dağıtıyor ama uygulamanın çalıştığına bakmıyor. Dağıtım adımından sonra iki adım ekle:

- `python scripts/check_health.py "$APP_URL"`; `APP_URL` ortam değişkeni `${{ vars.STAGING_URL }}` olsun.
- `python scripts/deploy.py staging --rollback`; **yalnızca önceki bir adım düştüyse** çalışsın.
