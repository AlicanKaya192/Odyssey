The `deploy-staging` job deploys but does not check that the application works. After the deploy step, add two steps:

- `python scripts/check_health.py "$APP_URL"`; the `APP_URL` environment variable should be `${{ vars.STAGING_URL }}`.
- `python scripts/deploy.py staging --rollback`; it should run **only if an earlier step failed**.
