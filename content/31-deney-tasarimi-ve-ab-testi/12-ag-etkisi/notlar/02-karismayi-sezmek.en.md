Interference does not announce itself: the test looks clean, there is no
SRM, the p-value is small. That is why it is asked about while writing the
plan.

## Questions for the planning stage

- Does a B user's behaviour reduce **something an A user could use**?
  (drivers, stock, a queue, a budget)
- Does someone in B **send** something to someone in A? (messages,
  invitations, shares)
- Does the change affect the other side of the market (sellers, drivers,
  writers)?

If one of the answers is "yes", a user-level test can enlarge or shrink the
effect.

## Design options

| Design | What is done | Its cost |
|---|---|---|
| Cluster (city, region) | everyone in the cluster is in the same group | few clusters, much noise |
| Friend cluster | tightly connected groups in the network are assigned together | finding the clusters is hard |
| Switchback | the whole market is A and B in turns (e.g. hour by hour) | effects that change over time, switch moments |

## Symptoms

- The control group's metric **fell** compared with its period before the
  test (B took from A).
- The test's effect came out much smaller than expected after the change
  was opened to everyone.
- The effect shrinks as B's share grows (the holdout from the Novelty
  Effects and Long-Term Impact section can show this too).
