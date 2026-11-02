Why run an experiment when there is already data? Because in observational
data it is very hard to say that one of two things "moving together"
causes the other.

| | Observational data | Randomised experiment |
|---|---|---|
| Who sees what? | people choose, or the system decides by a rule | chance decides |
| Confounders | can differ between the groups | equal on average |
| Where does the difference come from? | the change, the selection or both | the change or chance |
| Conclusion | association | cause and effect |

## Examples of confounders

- Those who turn on a new feature are already more frequent visitors.
- Those who use a discount code already intended to shop.
- Those who move to the app's new version have newer phones.

In each, the conclusion "the feature / code / version raises sales" can be
wrong.

## When an experiment is not possible

Sometimes an experiment is not possible (changing prices for everyone,
legal limits). Then methods that measure confounders and account for them
(matching, regression, difference in differences) are used. All of them
rest on the assumption "there is no unmeasured confounder"; a randomised
experiment does not need that assumption.
