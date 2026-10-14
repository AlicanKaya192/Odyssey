**Questions to ask when designing a pipeline**

1. **Which jobs are independent of each other?** Let the independent
   ones run at the same time: lint, tests, building the docs.
2. **What needs to wait for what?** Write `needs` only where it is really
   needed. Unnecessary `needs` makes the pipeline longer.
3. **Which one is the critical path?** It sets the pipeline's time;
   speeding up starts there.
4. **What should happen only on `main`?** Deployment, versioning,
   releasing → `if`.
5. **Who hears about it when something fails?** A notification with
   `if: failure()`.

**The quick ones first**

Make short checks (lint, formatting) a separate job, and let the long
jobs wait for them or run next to them. You do not need to wait six
minutes of tests for a typo; lint tells you in one minute.

**Common mistakes**

| Written | Result | Correct |
|---|---|---|
| `needs: tests` (job named `test`) | The file is invalid | Write the job's name exactly |
| `a` → `b`, `b` → `a` | A cycle, the file is invalid | Remove one arrow |
| `if: github.ref == "refs/heads/main"` | Double quotes give an error in an expression | Single quotes: `'refs/heads/main'` |
| No `if: failure()` on `notify` | When something fails it does not run (it is skipped) | `if: failure()` |
| No `if` on the deployment | Deployment is attempted on PRs too | `github.event_name == 'push' && github.ref == 'refs/heads/main'` |
| Looking in one job for another job's file | The file is not there: a separate machine | Artifacts (the eighth section) |

**Waves and time** (the lesson's example)

| Wave | Jobs | Finishes |
|---|---|---|
| 1 | `lint` (1), `test` (6), `docs` (2) | minute 6 |
| 2 | `build` (3) | minute 9 |
| 3 | `deploy` (2) | minute 11 |

One by one it would take 14 minutes.
