Paket PyPI'a da yüklensin, ama saklanan bir anahtar olmadan (güvenilir yayıncı). Bir `publish` işi ekle:

- `build` bitince başlasın, makine `ubuntu-latest`.
- `pypi` ortamına bağlansın (`environment: pypi`).
- Yalnızca `id-token: write` iznini alsın.
- `dist` artifact'ini `dist` klasörüne indirsin.
- `pypa/gh-action-pypi-publish@release/v1` eylemini çalıştırsın.
