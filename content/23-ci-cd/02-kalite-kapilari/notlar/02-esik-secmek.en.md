Whether a gate is useful depends on choosing the right threshold. A
threshold that is too loose catches nothing; one that is too strict pushes
the team to turn the gate off or to do meaningless work.

**Lint and format: zero tolerance**

For these gates the threshold is usually "no errors at all". If a rule is
really wrong, the rule is turned off (in a settings file); the error is
not ignored. When added to a large existing project for the first time,
it can first be applied to new code only.

**Coverage: reasonable and never falling**

- 70–90% is common. Chasing 100% often leads to meaningless tests.
- The real question: are the important branches (error paths, edges,
  money calculations) tested?
- Put the threshold a little below today's value and raise it over time;
  do not let coverage fall (a "ratchet").

**What to do when a gate closes**

1. Read the message first: which file, which line, which rule.
2. Run the same command on your own computer and see the same result.
3. Fix it and push again. Turning the gate off or lowering the threshold
   is the last resort and should be a conscious decision.

**Common mistakes**

| Mistake | Result |
|---|---|
| Running the formatter in the pipeline without `--check` | The files are fixed on the machine but never reach the repository; the gate never closes. |
| Putting lint after the tests | You wait minutes of tests for a typo. |
| Raising coverage with tests that have no `assert` | The gate passes but nothing is checked. |
| Lowering the threshold every time it closes | After a while the gate means nothing. |
