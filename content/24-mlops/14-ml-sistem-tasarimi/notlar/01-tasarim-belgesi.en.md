A short design document is written before writing code. This example is
filled in for the module's churn model.

## Goal

- Business goal: reduce churn by offering a discount to customers who
  would churn.
- Business measure: profit = the expected value of customers saved − the
  cost of the offers.
- Assumptions: an offer costs 5 units; a customer who would churn accepts
  with 30%, and a customer who stays is worth 60 units.

## Data

- Source: the customer table, pulled as of a date every night.
- Label: `churned`, known a month later (label delay).
- Validation: schema and range checks, a 5% quarantine threshold.

## Model

- Baseline: the rule `support_calls >= 2`.
- Model: scaled logistic regression; the threshold is chosen by profit.
- Gate: on a current, labelled set it must beat the baseline and the live
  model.

## Serving

- Batch prediction, every night; the result is written to a table.
- Fallback: if the model or the table is missing, the rule runs.

## Monitoring and retraining

- Monitoring: PSI, the calibration gap, monthly profit.
- Retraining: once a month + on a quality alert; the last window is chosen
  by measuring.

## Don't

- Don't write the goal as "accuracy must be above 80%"; write the business
  measure.
- Don't choose a threshold without writing the assumptions into the
  document.
