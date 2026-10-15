The last piece: add a `release` job.

- When `ci-ok` finishes, only on a `v` tag: `if: startsWith(github.ref, 'refs/tags/v')`. The machine is `ubuntu-latest`.
- Write permission only for this job: `permissions: contents: write`.
- Steps: get the code; `python scripts/check_version.py "$GITHUB_REF_NAME"`; download `dist` into the `dist` folder.
- The last step has two lines with `run: |`: first `gh release create "$GITHUB_REF_NAME" dist/* \`, under it `--repo "$GITHUB_REPOSITORY" --generate-notes`. The `GH_TOKEN` environment variable is `${{ secrets.GITHUB_TOKEN }}`.
