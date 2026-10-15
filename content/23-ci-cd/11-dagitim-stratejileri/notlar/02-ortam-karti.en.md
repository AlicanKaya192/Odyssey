**A GitHub environment (Settings › Environments)**

| Rule | What it does |
|---|---|
| Required reviewers | The job waits until approval comes |
| Wait timer | The job waits for a set time before starting |
| Branch and tag rule | Deploys only from an allowed branch/tag |
| Environment secrets | Visible only to jobs tied to that environment |
| Environment variables | `${{ vars.NAME }}`, only in that environment |

**Tying a job to an environment**

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

- `url`: a link to the live address on the run page.
- `cancel-in-progress: false` for deployments: a deployment cut in half
  leaves the server between two versions.

**After deploying**

```yaml
      - run: python scripts/deploy.py staging
      - run: python scripts/check_health.py "$APP_URL"
        env:
          APP_URL: ${{ vars.STAGING_URL }}
      - run: python scripts/deploy.py staging --rollback
        if: failure()
```

**Checklist**

- Staging first, then production; production only with a tag.
- The production environment has reviewers.
- The deployed package is the same file `build` produced.
- A health check after deploying, a rollback if it fails.
- Only one production deployment at a time (`concurrency`).
