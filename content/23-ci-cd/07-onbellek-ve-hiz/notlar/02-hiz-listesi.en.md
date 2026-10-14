**Measure first**

On GitHub, each step's duration is written inside the run. Find the
longest step; speeding up starts there. The pipeline's total time is set
by the critical path (the fifth section): speeding up a job that is not
on the critical path does not shorten the pipeline.

**Checklist**

| Question | Way | Section |
|---|---|---|
| Are the dependencies downloaded every time? | `cache: pip` or `actions/cache` | 7 |
| Does a documentation change run the tests? | `paths-ignore` | 4 |
| Are old runs on the same branch still going? | `concurrency` + `cancel-in-progress` | 7 |
| Do the tests run twice on a PR? | Limit `push` to `main` | 4 |
| Are independent jobs one after another? | Remove unnecessary `needs` | 5 |
| Does a quick check wait for the long tests? | Lint as a separate job | 5 |
| Is the matrix bigger than needed? | `exclude`, other systems with one version | 6 |
| Are all tests awaited on a broken PR? | `pytest -x` | 7 |
| Does a stuck job go on for hours? | `timeout-minutes` | 3, 7 |

**Traps**

- No `hashFiles` in the key → old packages come back even when the
  dependencies change.
- No `runner.os` in the key → a Windows package is installed on Linux.
- The cache step after the installation → the restore is useless.
- `cancel-in-progress: true` on a deployment → a deployment left half
  done.
- Deleting or skipping tests for speed → the pipeline is fast but
  catches nothing.
