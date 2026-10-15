**Release day, step by step**

1. Is `main` green? `ci-ok` must have passed in the last run.
2. Raise the version in `pyproject.toml` (`0.3.0` → `0.4.0`, by the rule
   from the tenth section).
3. Write the new version's section in `CHANGELOG.md`: `## [0.4.0]`.
4. Bring these two into `main` with a PR.
5. Put a tag on that commit of `main` and push it:

```text
git tag v0.4.0
git push origin v0.4.0
```

6. Watch the tag's run: the `release` job opens the release page.
7. Check the `dist` files and the notes on the release page.

**If something goes wrong**

| Situation | What to do |
|---|---|
| `check_version.py` failed (tag ≠ version) | No release happened. Delete the tag, fix the version, tag again |
| Tests failed on the tag | No release happened. Bring the fix into `main`, tag with a **new** version number |
| The release came out but the package is broken | Do not pull the release back; a new small version with the fix (`0.4.1`) |

```text
git tag -d v0.4.0
git push origin --delete v0.4.0
```

**What not to do**

- Moving a released tag to another commit: everyone who downloaded that
  version sees different code.
- Releasing by hand, skipping the pipeline: the tested package and the
  released package drift apart.
- Putting the tag on a branch other than `main`.

**Taking the release notes from a file**

`--generate-notes` makes notes from PR titles. If hand-written notes are
wanted, the `## [0.4.0]` section of `CHANGELOG.md` is extracted into a
file and given with `gh release create ... --notes-file notes.md`.
