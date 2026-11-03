## What do I use at which step?

| Step | Tool |
|---|---|
| How many people are needed? | `proportion_effectsize` + `NormalIndPower().solve_power` |
| Assignment | a salted hash: `hashlib.md5(f"{salt}:{user_id}".encode())` → bucket |
| SRM | `stats.chisquare(n)`; stop if p < 0.001 |
| Two rates | `proportions_ztest`, `confint_proportions_2indep` |
| A statistic without a formula | the bootstrap: `rng.choice(x, len(x))`, percentile interval |
| An assumption-free test | permutation: `rng.permutation(labels)` |
| Looking every day | Bonferroni α / looks, or a threshold calibrated by simulation |
| Many metrics | `multipletests(p, method="holm")` or `"fdr_bh"` |
| A noisy metric | CUPED: Y − θ(X − X̄), θ = cov(X, Y) / var(X) |
| A ratio metric | the delta method (user-level variance and covariance) |
| A changing assignment ratio | a stratified estimate |
| A shared resource | cluster assignment, analysis at the cluster level |
| A quick choice | Thompson sampling: `rng.beta(1 + k, 1 + n - k)` |
| An inconclusive result | P(B > A) and the expected loss |

## Numbers

- At least one false alarm in 20 independent tests: about 64%.
- The variance left after CUPED: 1 − ρ².
- The design effect in a cluster: 1 + (m − 1) · ICC.
- The SRM threshold: 0.001.

## Four decisions

| Interval | Decision |
|---|---|
| entirely above the threshold | launch |
| entirely below zero | harmful |
| contains zero and the threshold | inconclusive |
| above zero, below the threshold | not worth it |

## Red flags

- Writing the plan after the test; changing the threshold, the metric or
  the duration according to the result.
- Reading a result while there is SRM.
- Looking every day and stopping when significant.
- Highlighting the most striking segment or metric.
- Taking the first week's effect as lasting.
- Counting views as independent.
