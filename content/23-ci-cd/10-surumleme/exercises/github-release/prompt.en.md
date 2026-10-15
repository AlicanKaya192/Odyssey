The pipeline tests, builds the package and keeps it as the `dist` artifact. Add a `release` job that publishes the release:

- It should start when `build` finishes; the machine is `ubuntu-latest`.
- Only this job should get the `contents: write` permission.
- It should download the `dist` artifact into the `dist` folder.
- It should run `gh release create "$GITHUB_REF_NAME" dist/* --repo "$GITHUB_REPOSITORY" --generate-notes`, with the `GH_TOKEN` environment variable set to `${{ secrets.GITHUB_TOKEN }}`.
