Data mistakes that are common in real projects, and the check that
catches each one:

| What happened | How it looks in the data | Caught by |
|---|---|---|
| The unit changed | A fee of 2990 instead of 29.90 | Range |
| The spelling changed | `"PRO"` or `"Pro "` instead of `"pro"` | Allowed values |
| A new category was added | A `"gold"` plan | Allowed values |
| A column was renamed | No `tenure`, but a `tenure_months` | Missing value (in every row) |
| A number came as text | `"29.90"` | Type |
| A field came empty | `None` | Missing value |
| The source system broke | Every support call count is `0` | Profile |
| The data came in partly | 120 rows instead of 1000 | Row count |
| The same row came twice | The same `id` twice | Uniqueness |

The checks in the last two rows are not in this section's code, but they
are written with the same idea: is the batch's row count in the expected
range, are there repeats in the `id` column
(`len(ids) == len(set(ids))`).

## No error doesn't mean sound data

In the lesson's measurement, none of the three broken batches raised an
error:

| Damage | Error | Result |
|---|---|---|
| Fee in cents | None | The accuracy fell |
| Plan name in capitals | None | Every customer was counted as `basic` |
| Usage hours empty | None | scikit-learn's trees handled the empty value themselves |

## Checklist

- Is there a written rule for every column?
- Were the rules reviewed together with the team that sends the data?
- Was a margin left on the ranges inferred from reference data?
- Does validation run **before** training, as a separate step of the
  pipeline?
- Is there a limit for the share of bad rows? Does the pipeline stop
  when it is exceeded?
- Are the quarantined rows stored somewhere and inspected?
- Are the same rules applied at prediction time too?

## Don't

- Don't silently delete bad rows and carry on: how many rows went and
  why must be known.
- Don't pin the rules to the exact smallest and largest values of the
  reference data; real but slightly different customers get rejected.
- Don't use a profile warning as an automatic rejection; let a person
  look first.
