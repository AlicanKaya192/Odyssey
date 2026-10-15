Add a `deploy-production` job that deploys to production:

- It should start when `deploy-staging` finishes, only on a `v` tag: `if: startsWith(github.ref, 'refs/tags/v')`. The machine is `ubuntu-latest`.
- Write the environment as a dictionary: `name: production`, `url: https://app.example.com`.
- Only one production deployment at a time: the `concurrency` group `deploy-production`, `cancel-in-progress: false`.
- It should get the code, download `dist` and run `python scripts/deploy.py production`.
