## Measures

| Measure | Formula | Reading |
|---|---|---|
| Support | `support(A ∪ B)` | how often the rule holds |
| Confidence | `support(A ∪ B) / support(A)` | share of `B` when `A` is present |
| Lift | `confidence / support(B)` | `> 1` raises, `≈ 1` unrelated, `< 1` lowers |

Lift is symmetric: `A → B` and `B → A` have the same lift (beer ↔ chips both
2.86 in the lesson); confidence is not (0.527 and 0.607).

## Apriori

- **Downward closure:** every subset of a frequent set is frequent.
- Level by level: `k + 1`-item candidates from frequent `k`-item sets; a
  candidate with a rare subset is dropped without counting.
- The data is scanned once per level; on large data methods like
  **FP-Growth** reduce scanning by keeping the data in a compressed tree.

## In practice

- In Python the `mlxtend` package (`apriori`, `association_rules`) is common;
  baskets must be turned into a true/false table (one column per item).
- Filter sets first with a support threshold, then rules with a confidence or
  lift threshold.

## Common mistakes

- Sorting rules only by confidence: popular items are everywhere.
- Taking association for causation: not "beer raises chips" but "they are
  seen together".
- Choosing a very low threshold and producing thousands of rules.
- Ignoring rules with lift below 1: they are information too (items that
  replace each other).
