The parts of a feature store:

<figure class="fig">
  <div class="versus">
    <div><h4>Offline store</h4>The dated history of every feature. Training data is pulled as of the label date. Can be big and slow.</div>
    <div><h4>Online store</h4>Every customer's latest values. Read by ID at serving time. Small, within milliseconds.</div>
  </div>
  <figcaption>Both are fed from the same definitions and the same writes.</figcaption>
</figure>

## The definition of a feature

| Field | Example |
|---|---|
| Name | `support_calls_30d` |
| Entity (whom it belongs to) | The customer ID |
| Computation | The number of support calls in the last 30 days |
| Type | Integer |
| Freshness | Once a day |
| Owner | The customer data team |

## The "as of" join

Every row of the training table has a customer and a **label date**. For
every feature, the last value **before or on** that date is taken; later
values are ignored.

| Customer | Label date | Call history | Value used |
|---|---|---|---|
| C7 | 2026-02-15 | 01-01: 0, 02-01: 1, 03-01: 4 | 1 |
| C7 | 2026-03-10 | the same | 4 |
| C7 | 2025-12-31 | the same | none (`None`) |

## Checklist

- Do the training and serving features come from the same definition?
- Does every training row have a label date? Are the features pulled as
  of that date?
- Is the feature vector at serving time recorded?
- Are the dates in `YYYY-MM-DD` form and in the same time zone?

## Don't

- Don't rewrite the feature code for serving.
- Don't pull training data from "today's" table and attach it to past
  labels; you'll have seen the future.
- Don't build the test with the same wrong feature as training and trust
  its result.
