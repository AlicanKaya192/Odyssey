The checks passed before looking at an experiment's result. If one fails,
the result is not read.

| Check | What is tested | Tool |
|---|---|---|
| SRM | do the group sizes match the design | chi-square goodness of fit |
| Balance table | are traits the change cannot affect equal | group averages |
| A/A history | is the system's false alarm rate about 5% | many A/A tests |
| Duration | as in the plan, full weeks | the plan |
| Guardrail metrics | is anything getting worse | secondary tests |
| Log completeness | are event counts reasonable day to day | a daily count chart |

## Why so much care?

A broken experiment produces a fake result that looks "clean": in this
section's example B did nothing, yet its buying rate came out significantly
higher. If a fake win is shipped, later experiments are built on a wrong
baseline.

## Don't

- Wave SRM through as "a small difference, not important".
- "Fill in" lost users by hand, or delete random people from one group to
  equalise: if the loss is not random, the contents are still damaged.
- Conclude the system is broken because a single A/A test came out
  significant.
