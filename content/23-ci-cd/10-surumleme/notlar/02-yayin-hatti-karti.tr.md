**Etiket komutları**

```text
git tag -a v1.2.0 -m "Release 1.2.0"   # açıklamalı etiket
git push origin v1.2.0                 # etiketi adıyla gönder
git tag --list "v1.*"                  # etiketleri listele
git show v1.2.0                        # etiket hangi commit'i gösteriyor
```

- Etiket `git push` ile kendiliğinden gitmez.
- Yayınlanmış etiket taşınmaz, silinip yeniden konmaz; hata varsa yeni
  sürüm.

**Etiketle başlayan hat**

```yaml
on:
  push:
    tags: ["v*"]
```

| Nerede | Etiketin adı |
|---|---|
| Kabukta (`run:`) | `$GITHUB_REF_NAME` |
| İş akışı ifadesinde | `${{ github.ref_name }}` |
| Deponun adı (`sahip/depo`) | `$GITHUB_REPOSITORY` |

**Sıra**

1. Test.
2. Etiket `pyproject.toml`'daki numarayla aynı mı (`v` + sürüm)?
3. Bir kez derle, artifact olarak sakla.
4. GitHub sürümü (`contents: write`) ve/veya PyPI (`id-token: write`).

**GitHub sürümü**

```yaml
      - run: |
          gh release create "$GITHUB_REF_NAME" dist/* \
            --repo "$GITHUB_REPOSITORY" --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- Kod çekilmeyen işte `--repo` şart; yoksa `gh` depoyu bulamaz.
- `--generate-notes`: son sürümden bu yana birleştirilen PR'lardan not.

**PyPI (güvenilir yayıncı)**

```yaml
  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - uses: pypa/gh-action-pypi-publish@release/v1
```

- Saklanan bir anahtar yok; PyPI'da depo ve iş akışı bir kez tanımlanır.
- Yüklenen numara bir daha kullanılamaz. Denemeler için TestPyPI.
