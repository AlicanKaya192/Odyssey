## Three families

| Family | What it does | Example |
|---|---|---|
| Constructive | builds the solution step by step | nearest neighbour, greedy knapsack |
| Local search | improves the solution at hand with small changes | 2-opt, hill climbing |
| Metaheuristic | adds rules to escape local optima | simulated annealing, genetic algorithm, tabu search |

A common pattern: **construct first, then improve** (nearest neighbour +
2-opt).

## Settings of simulated annealing

| Setting | Effect |
|---|---|
| Starting temperature | if high, almost every step is accepted at first |
| Cooling rate | `0.99`–`0.999`; slower cooling is better, and longer |
| Step size | large enough to cross the distance between dips |
| Number of steps | until the temperature nears zero |

With the lesson's annealing and the other settings unchanged, a step size of
`±1` finds the best from only 6 of 20 starts; with `±3`, from all 20. The
setting depends on the problem's scale.

## Common mistakes

- Calling what a heuristic found "the best": it is only "the best found".
- Trusting a single random run: try a few seeds, keep the best and look at the
  spread.
- Forgetting to save the best known solution: since annealing accepts bad
  steps, the final state may not be the best state (`best` is kept separately).
- Making evaluation expensive: in 2-opt, computing only the two changed edges
  is much faster than measuring the whole tour again at each step.
