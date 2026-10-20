With a small sample, luck can make anything appear; measure the noise first.

## The canary at 1% (8 customers), ten days

| | Lowest | Highest |
|---|---|---|
| Healthy model | 0.500 | 1.000 |
| Broken model | 0.000 | 0.750 |

On day 7 the two models got the same score (0.750).

## The A/A test (the same model in two groups, 200 repeats)

| Customers per group | 95% of the gaps below |
|---|---|
| 100 | 0.130 |
| 400 | 0.062 |
| 1600 | 0.034 |

When the group grows four times, the noise drops to about half.

## Checklist

- Was the minimum number of customers written down for every canary stage?
- Was the noise measured with an A/A test before the A/B test?
- Was the test's duration (or number of customers) decided in advance?
- Is the measure compared the one that really matters (a business measure)?

## Don't

- Don't stop the test as soon as a difference appears; luck is at its
  largest then.
- Don't say "the new model is bad" or "good" with eight customers.
- Don't record a difference below the noise as a gain.
