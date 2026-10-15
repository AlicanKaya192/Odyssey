The pipeline builds the package and keeps it as `dist`. Add a `deploy-staging` job:

- It should start when `build` finishes; the machine is `ubuntu-latest`.
- It should be tied to the `staging` environment.
- It should get the code and download the `dist` artifact into the `dist` folder.
- It should run `python scripts/deploy.py staging`.
