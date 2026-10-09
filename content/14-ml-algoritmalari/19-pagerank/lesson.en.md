# PageRank

How important is a web page? The first idea is to count how many pages link to
it. **PageRank** asks a subtler question: a link from an important page is
worth more. This idea, at the heart of Google's first search engine, is used
today to find influential people in social networks, important papers in
citation networks and critical junctions in road networks. In this section we
write PageRank from scratch with **power iteration** and compare it with the
exact solution of a linear equation.

## The random surfer

Picture a surfer: at every step they click one of the current page's links at
random. Now and then (with probability `1 − d`) they get bored and jump to a
random page. After surfing for a long time, what is the probability of being
on each page? That probability is the page's **PageRank**. `d` is called the
**damping** factor; its classic value is 0.85.

We write this with a matrix: `M[i, j]` is the probability of moving from page
`j` to page `i` (an equal share for each of `j`'s links). In one step the
probabilities are updated as `r → d · M r + (1 − d) / n`; repeating this until
the change stops is **power iteration**.

```python
import numpy as np

pages = ["A", "B", "C", "D", "E", "F"]
links = {"A": ["B", "C"], "B": ["C"], "C": ["A"],
         "D": ["C", "E"], "E": ["C", "F"], "F": ["C"]}
n = len(pages)
idx = {p: i for i, p in enumerate(pages)}


def transition(links):
    M = np.zeros((n, n))                 # M[i, j]: probability j -> i
    for p, outs in links.items():
        for q in outs:
            M[idx[q], idx[p]] = 1 / len(outs)
    return M


def pagerank(M, d=0.85, tol=1e-10):
    r = np.full(n, 1 / n)                # everyone starts equal
    for it in range(1, 1000):
        new = d * M @ r + (1 - d) / n
        if np.abs(new - r).sum() < tol:
            return new, it
        r = new
    return r, it


def show(r):
    return " ".join(f"{p}={v:.3f}" for p, v in zip(pages, r))


M = transition(links)
r, it = pagerank(M)
print(show(r))
print(it, round(r.sum(), 6))
exact = np.linalg.solve(np.eye(n) - 0.85 * M, np.full(n, 0.15 / n))
print(np.abs(exact - r).max() < 1e-9)
print({p: sum(p in outs for outs in links.values()) for p in pages})
```

```text
A=0.347 B=0.173 C=0.379 D=0.025 E=0.036 F=0.040
46 1.0
True
{'A': 1, 'B': 1, 'C': 5, 'D': 0, 'E': 1, 'F': 1}
```

The iteration stopped after 46 steps and the probabilities sum to 1. The same
result comes from the exact solution of the linear equation
`(I − d M) r = (1 − d) / n`. C, which receives the most links (5), is first
with 0.379. The interesting one is A: it has only **one** link but is second
with 0.347. That single link comes from C, and C gives all of its value to A
alone. B, E and F also receive one link each, but from unimportant pages.
PageRank does not count links, it **weighs** them.

<figure class="fig">
<svg viewBox="0 0 520 330" width="520" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arr19" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dim" d="M0 0L10 5L0 10z"/></marker></defs><line class="line" x1="174.5" y1="68.3" x2="352.1" y2="61.5" marker-end="url(#arr19)"/><line class="line" x1="164.8" y1="98.4" x2="215.1" y2="129.4" marker-end="url(#arr19)"/><line class="line" x1="361.2" y1="79.9" x2="300.3" y2="122.1" marker-end="url(#arr19)"/><line class="line" x1="224.0" y1="120.8" x2="173.6" y2="89.8" marker-end="url(#arr19)"/><line class="line" x1="107.9" y1="239.5" x2="217.8" y2="174.8" marker-end="url(#arr19)"/><line class="line" x1="110.4" y1="253.6" x2="234.9" y2="275.6" marker-end="url(#arr19)"/><line class="line" x1="260.0" y1="257.5" x2="260.0" y2="199.0" marker-end="url(#arr19)"/><line class="line" x1="281.8" y1="274.5" x2="394.7" y2="246.3" marker-end="url(#arr19)"/><line class="line" x1="399.9" y1="228.7" x2="302.7" y2="174.0" marker-end="url(#arr19)"/><circle class="box" cx="130" cy="70" r="44.5"/><circle class="curve" cx="130" cy="70" r="44.5"/><text class="ink" x="130" y="69" font-size="14" text-anchor="middle">A</text><text class="dim" x="130" y="83" font-size="10" text-anchor="middle">0.347</text><circle class="box" cx="390" cy="60" r="35.0"/><circle class="curve" cx="390" cy="60" r="35.0"/><text class="ink" x="390" y="59" font-size="14" text-anchor="middle">B</text><text class="dim" x="390" y="73" font-size="10" text-anchor="middle">0.173</text><circle class="box" cx="260" cy="150" r="46.0"/><circle class="curve" cx="260" cy="150" r="46.0"/><text class="ink" x="260" y="149" font-size="14" text-anchor="middle">C</text><text class="dim" x="260" y="163" font-size="10" text-anchor="middle">0.379</text><circle class="box" cx="90" cy="250" r="20.7"/><circle class="curve" cx="90" cy="250" r="20.7"/><text class="ink" x="90" y="249" font-size="14" text-anchor="middle">D</text><text class="dim" x="90" y="263" font-size="10" text-anchor="middle">0.025</text><circle class="box" cx="260" cy="280" r="22.5"/><circle class="curve" cx="260" cy="280" r="22.5"/><text class="ink" x="260" y="279" font-size="14" text-anchor="middle">E</text><text class="dim" x="260" y="293" font-size="10" text-anchor="middle">0.036</text><circle class="box" cx="420" cy="240" r="23.0"/><circle class="curve" cx="420" cy="240" r="23.0"/><text class="ink" x="420" y="239" font-size="14" text-anchor="middle">F</text><text class="dim" x="420" y="253" font-size="10" text-anchor="middle">0.040</text></svg>
<figcaption>The six-page network; arrows are links, circle size is PageRank. Only one arrow reaches A, but it comes from C, which gives all of its value to A.</figcaption>
</figure>

## A page with no way out

A page linking nowhere (a **dangling node**) swallows the surfer: that column
of `M` is zero and probability leaks away at every step. Let us delete F's
link:

```python
links2 = dict(links, F=[])
M2 = transition(links2)
r2, _ = pagerank(M2)
print(show(r2), round(r2.sum(), 3))
M2[:, idx["F"]] = 1 / n                  # from the dead end to every page
r3, _ = pagerank(M2)
print(show(r3), round(r3.sum(), 3))
```

```text
A=0.260 B=0.135 C=0.276 D=0.025 E=0.036 F=0.040 0.773
A=0.336 B=0.175 C=0.358 D=0.032 E=0.046 F=0.052 1.0
```

Before the fix the total is 0.773: more than a fifth of the probability was
lost at F. The common remedy is to act as if the dangling page linked to every
page equally; the total is 1 again.

## The damping factor

```python
for d in (0.5, 0.85, 0.99):
    rd, steps = pagerank(M, d)
    print(d, show(rd), steps)
```

```text
0.5 A=0.242 B=0.144 C=0.317 D=0.083 E=0.104 F=0.109 23
0.85 A=0.347 B=0.173 C=0.379 D=0.025 E=0.036 F=0.040 46
0.99 A=0.396 B=0.198 C=0.399 D=0.002 E=0.002 F=0.003 65
```

With a small `d` the surfer jumps randomly often: the ranks move closer (even
D gets 0.083) and the iteration is fast (23 steps). As `d` approaches 1 the
links become decisive: A, B and C form a closed loop among themselves (no link
leads out of it) and at 0.99 collect almost all of the probability; D, E, F
drop to zero and the iteration takes 65 steps. 0.85 is a balance between the
two extremes.

## Convergence on a large network

On a random network of 1000 pages (each with 1–10 links), let us look at how
the error shrinks:

```python
rng = np.random.default_rng(19)
N = 1000
Mb = np.zeros((N, N))
for j in range(N):
    k = rng.integers(1, 11)
    Mb[rng.choice(N, k, replace=False), j] = 1 / k
exact_b = np.linalg.solve(np.eye(N) - 0.85 * Mb, np.full(N, 0.15 / N))
rb = np.full(N, 1 / N)
for it in range(1, 41):
    rb = 0.85 * Mb @ rb + 0.15 / N
    if it % 10 == 0:
        print(it, f"{np.abs(rb - exact_b).sum():.1e}")
```

```text
10 1.1e-04
20 7.3e-08
30 6.8e-11
40 6.6e-14
```

The error shrinks about a thousandfold every 10 steps; after 40 steps it is
6.6 × 10⁻¹⁴. The theoretical guarantee is looser: the error falls at least by
a factor of `d` per step (over 10 steps `0.85¹⁰ ≈ 0.197`). The real web has
billions of pages, so the exact solution (a matrix inverse) is impossible;
power iteration needs only matrix products and a few dozen steps.

## Summary

- PageRank is the long-run probability that a random surfer is on a page.
- `r ← d M r + (1 − d)/n`; repeat until the change stops (power iteration).
  It equals the exact solution of `(I − d M) r = (1 − d)/n`.
- Links are not counted but weighed: a link from an important page is
  valuable.
- Dangling pages leak probability; they are assumed to move to every page
  equally.
- A small `d` flattens the ranks; close to 1, closed loops collect
  everything.
