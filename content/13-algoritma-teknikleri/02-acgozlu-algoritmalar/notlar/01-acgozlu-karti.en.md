## When is it right?

Two properties are needed together:

- **The greedy choice property:** there is always a best solution that makes
  the choice that looks best right now.
- **Optimal substructure:** after the first choice, what is left is a smaller
  problem of the same kind, and its best is part of the best of the whole.

The way to show it is the **exchange argument**: take any best solution, swap
its first choice for the greedy choice, and show the solution does not get
worse.

## Does it work?

| Problem | Greedy rule | Gives the best? |
|---|---|---|
| Choosing meetings | earliest end first | yes |
| Fractional knapsack | value per kilo | yes |
| Whole (0/1) knapsack | value per kilo | no → dynamic programming |
| Change (canonical system: 1, 5, 10, 25, 50) | largest coin | yes |
| Change (like `[1, 3, 4]`) | largest coin | no → dynamic programming |
| Huffman coding | merge the two rarest groups | yes |
| Shortest path (no negative edges) | the closest unopened node (Dijkstra) | yes |
| Minimum spanning tree | the lightest edge (Kruskal) | yes |
| Travelling salesman | go to the nearest neighbour | no, only approximate |

The last three rows are in the graph sections of ALG 2.

## Practical tips

- When a greedy idea comes to mind, first look for a **small
  counterexample**: try inputs of 3–4 elements by hand, or compare with a
  solution that tries every possibility on small inputs.
- Most greedy algorithms have the form "sort by a criterion, look in order"
  or "take the best from a heap"; the cost is usually `O(n log n)`.
- Even when the greedy result is not the best, it is fast and often a good
  **starting point** or bound (in branch and bound methods).

## Common mistakes

- Thinking it is right because it worked on one example.
- Choosing the wrong sort criterion (by start or by length for meetings).
- Trusting value per kilo in the whole knapsack.
