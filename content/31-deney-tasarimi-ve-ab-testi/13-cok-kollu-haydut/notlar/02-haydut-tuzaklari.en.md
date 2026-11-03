A bandit breaks some of the things an A/B test assumes and brings its own
traps.

## Rates that change over time

If weekdays and weekends, or campaign days, differ, the bandit piles onto
the arm that looked good in the first days and is slow to come back when
conditions change. The fix: forgetting old data over time (counting only
the last weeks) or always splitting a small share of the traffic equally.

## Delayed outcomes

If buying happens days after the visit, updates are made with missing
data: an arm that got traffic recently looks unfairly bad. Updates are made
with users whose outcome is really known.

## The novelty effect

The temporary rise from the Novelty Effects and Long-Term Impact section
fools the bandit too: a new arm looks good in the first days and collects
the traffic.

## Measurement

- The estimates of rarely chosen arms are biased (measured in this
  section); an ordinary confidence interval is not used in the result
  report.
- Guardrail metrics are not the bandit's target: a bandit can raise sales
  while breaking refunds. Guardrail metrics are watched separately.

## A short rule

If the size of a decision will be reported and it will last, an A/B test
first. For short-lived, frequently changing choices, a bandit.
