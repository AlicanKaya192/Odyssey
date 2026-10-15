This pipeline runs on tags and builds the image but cannot send it. Fix it and add the deployment:

- Permissions on the `publish` job: `contents: read`, `packages: write`.
- `push: true` on the build step.
- A new `deploy-production` job: when `publish` finishes, `ubuntu-latest`, `environment: production`; the `concurrency` group `deploy-production`, `cancel-in-progress: false`. It should get the code and run `python scripts/deploy.py "ghcr.io/ada/tempconv:$GITHUB_SHA"`.
