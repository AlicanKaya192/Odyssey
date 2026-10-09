## Formulas

| What | Formula |
|---|---|
| Transition matrix | `M[i, j] = 1 / outdegree(j)` if there is a link `j → i` |
| One step | `r ← d · M r + (1 − d) / n` |
| Exact solution | `(I − d M) r = (1 − d) / n · 1` |
| Stopping | `Σ abs(r_new − r) < tol` |
| Error bound | falls at least by a factor of `d` per step (in the L1 norm) |

## Special cases

| Case | Problem | Remedy |
|---|---|---|
| Dangling page | probability leaks, total < 1 | set that column to `1 / n` |
| Closed loop (spider trap) | collects the probability | damping (`d < 1`) |
| Disconnected parts | there may be no single solution | random jumps (`1 − d`) connect them |

## Where is it used?

- Search engines: one of the signals in page ranking.
- Social networks: influential accounts; citation networks: important papers.
- Recommendation: personalised PageRank finds what is "close to this node and
  important".
- Word and sentence graphs: TextRank for keywords and summaries.

## Common mistakes

- Building the matrix the wrong way round: `M[i, j]` is from `j` to `i`; each
  column must sum to 1.
- Forgetting dangling pages: the order is not wrong, but the total is not 1
  and comparisons break.
- Taking the number of links (in-degree) for PageRank.
- Trying the exact solution on a large network: the matrix is `n × n` and its
  dense form does not fit in memory; a sparse matrix and power iteration are
  used.
