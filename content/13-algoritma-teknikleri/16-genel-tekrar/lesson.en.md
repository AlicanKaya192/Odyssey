# Overall Review

You have reached the end of ALG 2. In ALG 1 you learned to measure cost and
the basic structures; here you learned **problem-solving techniques**:
splitting a problem, trying cleverly, storing repeated work, seeing relations
as a graph and settling for a good estimate when the exact answer is
expensive. This section gathers the essence of each technique and the most
important numbers we measured.

<figure class="fig">
  <div class="flow">
    <span class="node">Techniques<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Graphs<br><small>05–09</small></span><span class="arrow">→</span>
    <span class="node">Text, numbers<br><small>10–11</small></span><span class="arrow">→</span>
    <span class="node">Randomness<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Heuristics, patterns<br><small>14–15</small></span>
  </div>
  <figcaption>The path of ALG 2: general techniques first, then graphs, then special fields and approximate methods.</figcaption>
</figure>

## 1. Divide and conquer (Section 0)

Split the problem into smaller parts of the same kind, solve the parts, combine
the results. The **recursion tree** gives the cost: each level's work × the
number of levels. In merge sort each level is `n` and there are `log n` levels
→ `O(n log n)`. Karatsuba does three half-size multiplications instead of four
and brings `n²` down to `n^1.58`. If the parts overlap, divide and conquer
repeats work; DP is needed there.

## 2. Backtracking (Section 1)

Choose, explore, undo. It generates all subsets and orders; its power comes
from **pruning**: never opening a branch that clearly cannot work. The 92
solutions of eight queens were found by visiting only 2057 nodes.

## 3. Greedy algorithms (Section 2)

At each step choose what looks best right now and never go back. Fast, but
**not always right**: in meeting selection "ends earliest" is right, "shortest"
is wrong; right for the fractional knapsack, wrong for the whole one. Its
correctness is shown with an **exchange** argument. Huffman coding is greedy
too.

## 4. Dynamic programming (Sections 3–4)

Solve overlapping subproblems **once** and store them. In `fib(30)`, 2,692,537
calls dropped to 59 with memory. The recipe: define the state, write the
transition, set the starting values, fix the order, read the answer.

| Problem | State | Cost |
|---|---|---|
| Fewest coins | `dp[amount]` | `O(amount × coins)` |
| 0/1 knapsack | `dp[capacity]` (walk backwards) | `O(n × capacity)` |
| LCS, edit distance | `dp[i][j]` | `O(n × m)` |
| LIS | `tails` + `bisect` | `O(n log n)` |
| Kadane | the best ending here | `O(n)` |

## 5. Graphs (Sections 5–9)

Nodes and edges; in Python mostly an **adjacency list** (a dictionary).

| Question | Algorithm | Cost |
|---|---|---|
| Fewest steps (unweighted) | BFS | `O(n + m)` |
| Connected components, cycles | DFS / BFS | `O(n + m)` |
| Shortest path (no negatives) | Dijkstra (heap) | `O(m log n)` |
| Negative edges | Bellman-Ford | `O(n · m)` |
| All pairs | Floyd–Warshall | `O(n³)` |
| A known goal | A* (estimate + cost) | often fewer nodes than Dijkstra |
| Dependency order | Kahn / DFS | `O(n + m)` |
| Cheapest connection | Kruskal / Prim | `O(m log m)` |
| In the same group? | union-find | constant in practice |

In the data pipeline 19 hours of work finished in 18 hours thanks to the jobs
that can run in parallel: the **critical path**. Stopping Kruskal at `k` groups
gave single-linkage clustering and found the same groups as scikit-learn.

## 6. String and number algorithms (Sections 10–11)

- **KMP** searches without going back in the text using the prefix table: in
  the worst case naive search made more than half a million comparisons, KMP
  about twenty thousand.
- **Rabin-Karp** compares a window as a single number with a rolling hash;
  strong for many patterns and finding copies. A **trie** brings a prefix
  search down to as many steps as the prefix is long.
- **Euclid** `gcd(a, b) = gcd(b, a % b)`; the **sieve** finds the primes up to
  100,000 with about 14 times less work than trial division; **fast
  exponentiation** computes a million-sized exponent with 27 multiplications.

## 7. Randomness and probabilistic structures (Sections 12–13)

- **Quickselect** is `O(n)` on average; a random pivot makes the worst case
  unlikely. **Fisher-Yates** shuffles without bias with `randint(0, i)`.
  **Reservoir sampling** takes an equal-probability sample from a stream with
  memory for `k` items. The Monte Carlo error shrinks like `1/√n`.
- A **Bloom filter** says "definitely not / probably yes" (0.73% false
  positives in the lesson), **Count-Min** only overestimates, **HyperLogLog**
  estimated the distinct count with 1024 counters with an error below 4%, and
  **MinHash** estimates the Jaccard similarity with small signatures.

## 8. Heuristics and patterns (Sections 14–15)

- Brute force is possible when small and impossible when large: an 80-digit
  number of tours for 60 cities. Nearest neighbour + 2-opt brought a random
  tour's 3155 down to 690. Simulated annealing escapes the dip by accepting bad
  steps with a decreasing probability.
- Budget first: `n` ~20 → `2ⁿ`, ~1000 → `n²`, ~10⁶ → `n log n`. Binary search
  on the answer, a monotonic stack, BFS in a state space, meet in the middle.
  Test the fast solution against brute force with random inputs.

## Which technique for which question?

| If the problem has | Technique |
|---|---|
| Independent parts, cheap combining | divide and conquer |
| All options needed, early elimination possible | backtracking + pruning |
| A local best choice that is safe (provable) | greedy |
| "The best / how many ways" + overlapping subproblems | dynamic programming |
| Relations, networks, dependencies | graph algorithms |
| Very big data, an approximate answer is enough | probabilistic structures, sampling |
| The exact solution is expensive, a good one is enough | heuristic methods |

## Summary

Each technique in ALG 2 is a different answer to the same question: **how do I
drop repeated or needless work?** By splitting, pruning, storing, using the
graph's structure or giving up a little exactness. In ALG 3 these tools will
show up again inside machine learning algorithms.
