Hat test edip paketi derliyor ve `dist` artifact'i olarak saklıyor. Sürümü yayınlayan bir `release` işi ekle:

- `build` bitince başlasın, makine `ubuntu-latest`.
- Yalnızca bu iş `contents: write` iznini alsın.
- `dist` artifact'ini `dist` klasörüne indirsin.
- `gh release create "$GITHUB_REF_NAME" dist/* --repo "$GITHUB_REPOSITORY" --generate-notes` çalıştırsın; `GH_TOKEN` ortam değişkeni `${{ secrets.GITHUB_TOKEN }}` olsun.
