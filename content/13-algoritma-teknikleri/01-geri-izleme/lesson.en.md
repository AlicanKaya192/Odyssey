# Backtracking

You are looking for the exit of a maze. At a junction you pick one of the
paths; if you walk into a dead end, you **go back to the last junction** and
try another path. **Backtracking** is exactly this: build a solution step by
step, make a choice at each step, and if a choice leads nowhere, undo it and
try the next one.

It is used for problems where every possibility has to be tried: all subsets
of a set, all orderings of a list, placements that follow rules (sudoku,
chess puzzles), selections whose sum hits a target. Its real strength is
**pruning**: as soon as it is clear a choice will not work, throwing away all
the possibilities below it without trying them.

## The skeleton: choose, explore, undo

```python
def backtrack(path):
    if IS_COMPLETE(path):
        ADD_TO_RESULT(path)
        return
    for choice in CHOICES(path):
        path.append(choice)        # choose
        backtrack(path)            # continue with this choice
        path.pop()                 # undo
```

Every backtracking algorithm is a variation of these three lines. The key
is the `pop`: if you do not undo the choice, the next attempt starts with the
leftovers of the previous one.

## All subsets

The subsets of `[1, 2, 3]`: each element is either in or out. At each step we
ask "which of the next elements should I add?":

```python
def subsets(items):
    result, path = [], []
    def backtrack(start):
        result.append(path[:])            # every node is a subset
        for i in range(start, len(items)):
            path.append(items[i])
            backtrack(i + 1)              # continue with the next elements
            path.pop()
    backtrack(0)
    return result

print(subsets([1, 2, 3]))
print(len(subsets(list(range(20)))))
```

```text
[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
1048576
```

<figure class="fig">
<svg viewBox="0 0 317 222" width="317" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="47.9" y1="140.0" x2="47.9" y2="200.0"/>
<line class="line" x1="84.9" y1="80.0" x2="47.9" y2="140.0"/>
<line class="line" x1="84.9" y1="80.0" x2="121.9" y2="140.0"/>
<line class="line" x1="183.6" y1="20.0" x2="84.9" y2="80.0"/>
<line class="line" x1="195.9" y1="80.0" x2="195.9" y2="140.0"/>
<line class="line" x1="183.6" y1="20.0" x2="195.9" y2="80.0"/>
<line class="line" x1="183.6" y1="20.0" x2="269.9" y2="80.0"/>
<rect class="box" x="164.3" y="6.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="183.6" y="24.6" font-size="13" text-anchor="middle">[ ]</text>
<rect class="box" x="65.6" y="66.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="84.9" y="84.5" font-size="13" text-anchor="middle">[1]</text>
<rect class="box" x="17.3" y="126.0" width="61.2" height="28" rx="7"/>
<text class="ink" x="47.9" y="144.6" font-size="13" text-anchor="middle">[1, 2]</text>
<rect class="box" x="6.0" y="186.0" width="83.9" height="28" rx="7"/>
<text class="ink" x="47.9" y="204.6" font-size="13" text-anchor="middle">[1, 2, 3]</text>
<rect class="box" x="91.3" y="126.0" width="61.2" height="28" rx="7"/>
<text class="ink" x="121.9" y="144.6" font-size="13" text-anchor="middle">[1, 3]</text>
<rect class="box" x="176.6" y="66.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="195.9" y="84.5" font-size="13" text-anchor="middle">[2]</text>
<rect class="box" x="165.3" y="126.0" width="61.2" height="28" rx="7"/>
<text class="ink" x="195.9" y="144.6" font-size="13" text-anchor="middle">[2, 3]</text>
<rect class="box" x="250.6" y="66.0" width="38.6" height="28" rx="7"/>
<text class="ink" x="269.9" y="84.5" font-size="13" text-anchor="middle">[3]</text>
</svg>
<figcaption>Every node is a subset. Backtracking walks the tree depth-first from left to right; the order in the output is the order of this walk.</figcaption>
</figure>

We add a copy with `path[:]`; if we added `path` itself, all of them would
point to the same list and end up empty. `n` elements have `2ⁿ` subsets:
with 20 elements it passed a million. Each element doubles it; backtracking
is not a fast method, it is a **complete** one.

## All orderings (permutations)

This time at each step we ask "which of the elements not used yet?". We keep
the used ones in a list of flags:

```python
def permutations(items):
    result, path, used = [], [], [False] * len(items)
    def backtrack():
        if len(path) == len(items):
            result.append("".join(path))
            return
        for i, x in enumerate(items):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            backtrack()
            path.pop()
            used[i] = False           # clear the flag when undoing too
    backtrack()
    return result

print(permutations("abc"))
```

```text
['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
```

`n` elements have `n!` orderings: 3,628,800 with 10 elements. The ready-made
ones are `itertools.permutations`, `itertools.combinations` and
`itertools.product`; use them in real code, but when you need to add your own
rule (pruning) you write the skeleton yourself.

## Pruning: never open a branch that cannot work

Let us look for the subsets whose sum is exactly 50. If the values are
positive and sorted there is a rule: as soon as the sum passes 50, **no
choice below that branch** can work, only bigger numbers would be added. We
cut that branch off:

```python
def subset_sum(values, target, prune):
    values = sorted(values)
    found, path, nodes = [], [], [0]
    def backtrack(start, total):
        nodes[0] += 1
        if total == target:
            found.append(path[:])
        for i in range(start, len(values)):
            if prune and total + values[i] > target:
                break                     # the next ones are even bigger
            path.append(values[i])
            backtrack(i + 1, total + values[i])
            path.pop()
    backtrack(0, 0)
    return len(found), nodes[0]
```

On 20 different numbers chosen between 1 and 59, the number of nodes visited
without and with pruning:

```text
without pruning : 11 solutions, 1048576 nodes
with pruning    : 11 solutions, 215 nodes
```

The same 11 solutions; without pruning it walks all `2²⁰` subsets, with
pruning it visits only a few hundred nodes. The whole art of backtracking is
this: a good pruning rule.

## Eight queens

How can eight queens be placed on a chessboard so that none attacks another?
We put one queen in each row; if a column or a diagonal is taken, we never
try that square.

```python
def queens(n):
    cols, diag1, diag2 = set(), set(), set()
    solutions, nodes = [0], [0]
    def place(row):
        nodes[0] += 1
        if row == n:
            solutions[0] += 1
            return
        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue                  # under attack: pruning
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            place(row + 1)
            cols.remove(col); diag1.remove(row - col); diag2.remove(row + col)
    place(0)
    return solutions[0], nodes[0]

print(queens(8))
```

```text
(92, 2057)
```

<figure class="fig">
<svg viewBox="0 0 274 274" width="274" xmlns="http://www.w3.org/2000/svg">
<rect class="box" x="35" y="1" width="34" height="34"/>
<rect class="box" x="103" y="1" width="34" height="34"/>
<rect class="box" x="171" y="1" width="34" height="34"/>
<rect class="box" x="239" y="1" width="34" height="34"/>
<rect class="box" x="1" y="35" width="34" height="34"/>
<rect class="box" x="69" y="35" width="34" height="34"/>
<rect class="box" x="137" y="35" width="34" height="34"/>
<rect class="box" x="205" y="35" width="34" height="34"/>
<rect class="box" x="35" y="69" width="34" height="34"/>
<rect class="box" x="103" y="69" width="34" height="34"/>
<rect class="box" x="171" y="69" width="34" height="34"/>
<rect class="box" x="239" y="69" width="34" height="34"/>
<rect class="box" x="1" y="103" width="34" height="34"/>
<rect class="box" x="69" y="103" width="34" height="34"/>
<rect class="box" x="137" y="103" width="34" height="34"/>
<rect class="box" x="205" y="103" width="34" height="34"/>
<rect class="box" x="35" y="137" width="34" height="34"/>
<rect class="box" x="103" y="137" width="34" height="34"/>
<rect class="box" x="171" y="137" width="34" height="34"/>
<rect class="box" x="239" y="137" width="34" height="34"/>
<rect class="box" x="1" y="171" width="34" height="34"/>
<rect class="box" x="69" y="171" width="34" height="34"/>
<rect class="box" x="137" y="171" width="34" height="34"/>
<rect class="box" x="205" y="171" width="34" height="34"/>
<rect class="box" x="35" y="205" width="34" height="34"/>
<rect class="box" x="103" y="205" width="34" height="34"/>
<rect class="box" x="171" y="205" width="34" height="34"/>
<rect class="box" x="239" y="205" width="34" height="34"/>
<rect class="box" x="1" y="239" width="34" height="34"/>
<rect class="box" x="69" y="239" width="34" height="34"/>
<rect class="box" x="137" y="239" width="34" height="34"/>
<rect class="box" x="205" y="239" width="34" height="34"/>
<rect class="line" x="1" y="1" width="272" height="272"/>
<circle class="dot" cx="18.0" cy="18.0" r="10.9"/>
<circle class="dot" cx="154.0" cy="52.0" r="10.9"/>
<circle class="dot" cx="256.0" cy="86.0" r="10.9"/>
<circle class="dot" cx="188.0" cy="120.0" r="10.9"/>
<circle class="dot" cx="86.0" cy="154.0" r="10.9"/>
<circle class="dot" cx="222.0" cy="188.0" r="10.9"/>
<circle class="dot" cx="52.0" cy="222.0" r="10.9"/>
<circle class="dot" cx="120.0" cy="256.0" r="10.9"/>
</svg>
<figcaption>The first solution found: one queen in every row, every column and every diagonal.</figcaption>
</figure>

92 solutions, only 2057 nodes. There are `8⁸ = 16,777,216` ways to put one
queen per row anywhere on its row; even the permutations that put one in
each row and column number `8! = 40,320`. Sets bring the attack check down to
`O(1)`: on the squares of one diagonal `row − col` or `row + col` is constant.

## In data science: why "try everything" does not scale

- **Feature selection:** finding the best subset of 30 features by trying
  every subset means training `2³⁰` = 1,073,741,824 models. That is why in
  practice greedy methods (the next section: forward selection) or
  regularisation (Lasso) are used.
- **Hyperparameter grid search:** scikit-learn's `GridSearchCV` tries every
  combination, like `itertools.product`; 4 parameters × 5 values = 625
  combinations, 3125 trainings with 5-fold cross-validation. There is no pruning; that is why random search or smarter
  methods are preferred for large searches.

Backtracking gives exact answers on small problems; as they grow you either
need a good pruning rule or methods that give up the exact answer (greedy,
heuristic).

## Summary

- Backtracking: choose, continue, undo; it tries every possibility
  completely.
- `path.append` / recursion / `path.pop`; add `path[:]` (a copy) to the
  result.
- Subsets `2ⁿ`, orderings `n!`: they explode quickly.
- Pruning: cut a branch as soon as it is clear it cannot work; the same
  answer, far fewer nodes.
- The ready-made ones are `itertools.combinations`, `permutations`,
  `product`.
