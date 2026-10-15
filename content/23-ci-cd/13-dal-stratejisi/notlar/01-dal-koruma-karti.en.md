**Three branch strategies**

| | Trunk-based | GitHub flow | GitFlow |
|---|---|---|---|
| Branch lifetime | Hours, a day or two | Days | Can be weeks |
| Long-lived branches | Only `main` | Only `main` | `main` + `develop` |
| Release | Continuous | From `main`, when wanted | From a release branch |
| What it needs | Very strong tests | PRs and CI | More manual work |

**Rules for `main` (Settings › Rules)**

| Rule | What it prevents |
|---|---|
| Require a PR | Direct pushes to `main` |
| Require approval | Unreviewed code getting in |
| Required checks | Code that fails the tests getting in |
| Branch must be up to date | Two PRs that pass separately breaking things together |
| Block force pushes and deletion | History being rewritten |
| Merge queue | The "update, test again" fatigue |

**A required check's name**

- The **job's** name, not the workflow's: `lint`, `test`.
- If `name:` is given, that name.
- In a matrix every copy is separate: `test (3.12)`, `test (3.13)`.
- If the name changes and the rule is not updated, the PR waits forever.

**Situations that keep a PR waiting**

| Situation | Why |
|---|---|
| The job's name changed | No result comes with the name in the rule |
| A path filter did not start the workflow | A workflow that does not start reports no result |
| `[skip ci]` | The same: no run, no result |
| Stuck in the queue | The workflow does not listen to `merge_group` |

**A skipped job**

A job skipped by `if:` counts as **successful** for a required check.
This is why the gate job must carry `if: always()`.
