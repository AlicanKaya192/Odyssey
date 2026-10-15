**Jobs and dependencies**

| Job | Depends on | When it runs | What it guarantees |
|---|---|---|---|
| `lint` | – | On every run | Format and lint are clean |
| `test` (×2) | `lint` | On every run | Tests on two versions, coverage ≥ 90% |
| `build` | `test` | On every run | The package builds, `dist` is kept |
| `ci-ok` | all | Always (`always()`) | One required check |
| `release` | `ci-ok` | Only on a `v*` tag | Consistent version, a release page |

**What happens on which event?**

| Event | lint | test | build | ci-ok | release |
|---|---|---|---|---|---|
| PR opened / new commit | ✓ | ✓ | ✓ | ✓ | – |
| Merge queue | ✓ | ✓ | ✓ | ✓ | – |
| Push to `main` | ✓ | ✓ | ✓ | ✓ | – |
| A `v0.3.0` tag | ✓ | ✓ | ✓ | ✓ | ✓ |

**Permissions**

| Where | Permission |
|---|---|
| The top of the file | `contents: read` |
| The `release` job | `contents: write` |
| Nowhere | `write-all` |

**Cancelling and time**

- The `concurrency` group is workflow + ref; cancelling only in PRs.
- `timeout-minutes`: lint 10, test 15.
- `cache: pip` in the tests.

**Repository settings**

- The `main` rule: PR, one approval, required check `ci-ok`, no force
  pushes.
- Workflow permissions "read only" by default.
- Only maintainers create `v*` tags.
