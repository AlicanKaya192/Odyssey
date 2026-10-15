Son parça: bir `release` işi ekle.

- `ci-ok` bitince, yalnızca `v` etiketinde: `if: startsWith(github.ref, 'refs/tags/v')`. Makine `ubuntu-latest`.
- Yalnızca bu işe yazma izni: `permissions: contents: write`.
- Adımlar: kodu çek; `python scripts/check_version.py "$GITHUB_REF_NAME"`; `dist`'i `dist` klasörüne indir.
- Son adım `run: |` ile iki satır: önce `gh release create "$GITHUB_REF_NAME" dist/* \`, altında `--repo "$GITHUB_REPOSITORY" --generate-notes`. `GH_TOKEN` ortam değişkeni `${{ secrets.GITHUB_TOKEN }}`.
