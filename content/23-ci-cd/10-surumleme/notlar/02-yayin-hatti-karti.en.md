**Tag commands**

```text
git tag -a v1.2.0 -m "Release 1.2.0"   # annotated tag
git push origin v1.2.0                 # send the tag by name
git tag --list "v1.*"                  # list tags
git show v1.2.0                        # which commit the tag points at
```

- A tag is not sent by `git push` by itself.
- A published tag is not moved, nor deleted and added again; if there is
  a bug, release a new version.

**A pipeline that starts with a tag**

```yaml
on:
  push:
    tags: ["v*"]
```

| Where | The tag's name |
|---|---|
| In the shell (`run:`) | `$GITHUB_REF_NAME` |
| In a workflow expression | `${{ github.ref_name }}` |
| The repository's name (`owner/repo`) | `$GITHUB_REPOSITORY` |

**Order**

1. Test.
2. Is the tag the same number as in `pyproject.toml` (`v` + version)?
3. Build once, keep it as an artifact.
4. GitHub release (`contents: write`) and/or PyPI (`id-token: write`).

**GitHub release**

```yaml
      - run: |
          gh release create "$GITHUB_REF_NAME" dist/* \
            --repo "$GITHUB_REPOSITORY" --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- In a job that did not get the code `--repo` is required; otherwise `gh`
  cannot find the repository.
- `--generate-notes`: notes from the PRs merged since the last release.

**PyPI (trusted publishing)**

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

- No key is kept; the repository and workflow are stated once on PyPI.
- An uploaded number can never be used again. TestPyPI for trials.
