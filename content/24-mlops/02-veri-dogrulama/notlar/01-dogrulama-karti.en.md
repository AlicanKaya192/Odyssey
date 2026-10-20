Before data reaches training, it goes through two kinds of checks:

| Check | Looks at | Catches | Example |
|---|---|---|---|
| Missing value | A single value | An empty or absent column | `usage_hours: missing` |
| Allowed values | A single value | Spelling differences, a new category | `plan: 'PRO' is not allowed` |
| Type | A single value | Text instead of a number | `monthly_fee: '29.90' is not a number` |
| Range | A single value | A change of unit, an impossible value | `tenure: -3 is out of range` |
| Profile comparison | The whole column | Every value valid but the distribution wrong | `support_calls 0.68 CHECK` |

## The order of the checks

`check_row` asks these four questions of every column in this order and
stops at the first one that fails:

1. Is there a value? (`None`, or no such column)
2. Is it one of the allowed values? (in a column with an `allowed` rule)
3. Is it a number? (`isinstance(value, (int, float))`)
4. Is it in range? (`min <= value <= max`)

The order matters: trying to compare an empty value with a range raises
an error, and so does comparing text with a number.

## Quarantine or reject?

| Situation | Decision | Why |
|---|---|---|
| A few bad rows | Quarantine | Rows entered wrongly now and then; carry on with the sound rows |
| The share of bad rows is over the limit | Reject | A systematic break; there may be errors the rules can't see |
| Rules clean, profile says "CHECK" | A person looks | The customers may really have changed |

Rejecting means raising an error (`raise`): the training script ends
with an error code and the pipeline turns red.

## The profile

- From the training data, take the **mean** and the **standard
  deviation** of every numeric column.
- Shift = `|new mean - old mean| / old standard deviation`. Written in
  standard deviations, all the columns are on the same scale.
- The limit (0.5 in this section) is a warning threshold, not a final
  verdict.

## Terms

- **Data validation:** checking data against rules before training or
  prediction.
- **Schema**, **data contract:** the rules of every column; an agreement
  between whoever sends the data and whoever receives it.
- **Batch:** data that arrives at once, such as one month's customers.
- **Quarantine:** setting bad rows aside to inspect them.
- **Gate:** a step that stops the pipeline if it is not passed.
- **Profile:** the summary statistics of a column.
