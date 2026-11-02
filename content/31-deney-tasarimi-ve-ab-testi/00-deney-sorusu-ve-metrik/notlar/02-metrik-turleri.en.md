| Kind | Example | Per-user value | Test |
|---|---|---|---|
| Proportion | buying rate | 0 or 1 | two-proportion z-test |
| Mean | revenue per user | a continuous number | Welch's t-test |
| Count | visits per user | 0, 1, 2, ... | Welch's t-test |
| Ratio metric | revenue per order | the ratio of two totals | delta method or bootstrap |

## Relative and absolute change

- **Absolute:** B − A. If buying rose from 11.7% to 12.2%, +0.5 points.
- **Relative:** (B − A) / A. The same change is about +4%.

Both are written; reporting only the relative change makes a small
difference look big (Effect Size section).

## A rough rule for sensitivity

The larger the coefficient of variation (deviation / mean), the more people
are needed to see the same relative difference: roughly with its square.
That is why long-tailed metrics like revenue are expensive. Options:

- a more sensitive intermediate metric (buying rate) as primary, revenue as
  secondary;
- capping the extremes, e.g. pulling the top 1% down to a fixed ceiling;
  the rule is written in advance;
- variance reduction (the CUPED section).

## Short and long term

Some metrics change at once (clicks), some late (retention). A short-term
metric not tied to the long-term goal can mislead; this is covered in the
Novelty Effects and Long-Term Impact section.
