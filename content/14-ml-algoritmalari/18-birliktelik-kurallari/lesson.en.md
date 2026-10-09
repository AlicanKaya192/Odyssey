# Association Rules

Sentences like "those who buy bread also buy butter" are **association
rules**. Market basket analysis extracts them from thousands of purchases:
which products are often seen together, and how much does one raise the
chance of the other? In this section we see three measures (support,
confidence, lift), the **Apriori** algorithm that finds frequent itemsets, and
why confidence can mislead.

## Baskets and support

Let us have 2000 baskets. We make the data with a generator whose rules we
know: butter is more likely when bread is there, sugar when coffee is, chips
when beer is; tea, however, is **less** likely when coffee is there (one
replaces the other). Milk is frequent in everyone's basket but depends on
nothing.

The **support** of an itemset is the share of baskets containing it.

```python
import numpy as np
from itertools import combinations

# (item, probability) or (item, item it depends on, if present, if absent)
RULES = [("milk", 0.6), ("bread", 0.4), ("butter", "bread", 0.6, 0.1),
         ("coffee", 0.35), ("sugar", "coffee", 0.55, 0.1),
         ("tea", "coffee", 0.15, 0.4), ("beer", 0.2),
         ("chips", "beer", 0.5, 0.08), ("eggs", 0.3), ("apples", 0.25)]


def make_basket(r):
    b = set()
    for u, rule in zip(r, RULES):
        p = rule[1] if len(rule) == 2 else (rule[2] if rule[1] in b else rule[3])
        if u < p:
            b.add(rule[0])
    return frozenset(b)


rng = np.random.default_rng(18)
baskets = [make_basket(rng.random(10)) for _ in range(2000)]


def support(items):
    items = frozenset(items)
    return sum(1 for b in baskets if items <= b) / len(baskets)


print(sum(len(b) for b in baskets) / len(baskets))
for s in (["milk"], ["bread"], ["bread", "butter"], ["beer", "chips"]):
    print(s, round(support(s), 3))
```

```text
3.1575
['milk'] 0.585
['bread'] 0.404
['bread', 'butter'] 0.236
['beer', 'chips'] 0.112
```

A basket holds 3.16 items on average. Milk's support is 0.585: in more than
half of the baskets. Bread and butter are together in 23.6% of the baskets.

## Apriori: frequent itemsets

10 items have `2^10 − 1 = 1023` non-empty subsets; with 100 items the number is
astronomical. **Apriori** rests on one observation: if a set is frequent, all
of its subsets are frequent too. The other way round: if a set is rare, no set
containing it can be frequent. So sets are grown **level by level**:

1. Count the support of single items, drop those below the threshold.
2. From the remaining `k`-item sets build `k + 1`-item candidates; drop,
   without counting, any candidate whose `k`-item subsets are not **all**
   frequent (pruning).
3. Count the candidates' support, drop those below the threshold; until no
   candidates remain.

<figure class="fig">
<svg viewBox="0 0 520 270" width="520" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="13.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="13.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="72.5" y="34" font-size="11" text-anchor="middle">milk 0.58</text><rect class="box" x="138.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="138.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="197.5" y="34" font-size="11" text-anchor="middle">bread 0.40</text><rect class="box" x="263.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="263.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="322.5" y="34" font-size="11" text-anchor="middle">butter 0.30</text><rect class="box" x="388.5" y="16" width="118" height="28" rx="6"/><rect class="curve" x="388.5" y="16" width="118" height="28" rx="6"/><text class="ink" x="447.5" y="34" font-size="11" text-anchor="middle">chips 0.18</text><rect class="box" x="11.7" y="111" width="80" height="28" rx="6"/><rect class="curve" x="11.7" y="111" width="80" height="28" rx="6"/><text class="ink" x="51.7" y="129" font-size="11" text-anchor="middle">mi br 0.23</text><rect class="box" x="95.0" y="111" width="80" height="28" rx="6"/><rect class="curve" x="95.0" y="111" width="80" height="28" rx="6"/><text class="ink" x="135.0" y="129" font-size="11" text-anchor="middle">mi bu 0.17</text><rect class="box" x="178.3" y="111" width="80" height="28" rx="6"/><text class="dim" x="218.3" y="129" font-size="11" text-anchor="middle">mi ch 0.11</text><rect class="box" x="261.7" y="111" width="80" height="28" rx="6"/><rect class="curve" x="261.7" y="111" width="80" height="28" rx="6"/><text class="ink" x="301.7" y="129" font-size="11" text-anchor="middle">br bu 0.24</text><rect class="box" x="345.0" y="111" width="80" height="28" rx="6"/><text class="dim" x="385.0" y="129" font-size="11" text-anchor="middle">br ch 0.07</text><rect class="box" x="428.3" y="111" width="80" height="28" rx="6"/><text class="dim" x="468.3" y="129" font-size="11" text-anchor="middle">bu ch 0.05</text><rect class="box" x="14.5" y="206" width="116" height="28" rx="6"/><text class="dim" x="72.5" y="224" font-size="11" text-anchor="middle">mi br bu 0.13</text><rect class="box" x="139.5" y="206" width="116" height="28" rx="6" stroke-dasharray="4 3"/><text class="dim" x="197.5" y="224" font-size="11" text-anchor="middle">mi br ch ✕</text><rect class="box" x="264.5" y="206" width="116" height="28" rx="6" stroke-dasharray="4 3"/><text class="dim" x="322.5" y="224" font-size="11" text-anchor="middle">mi bu ch ✕</text><rect class="box" x="389.5" y="206" width="116" height="28" rx="6" stroke-dasharray="4 3"/><text class="dim" x="447.5" y="224" font-size="11" text-anchor="middle">br bu ch ✕</text></svg>
<figcaption>Apriori with four items (threshold 0.15; names by first two letters: mi milk, br bread, bu butter, ch chips). Purple frame: frequent; grey: rare; dashed with ✕: pruned, its support was never counted because one of its subsets is rare.</figcaption>
</figure>

```python
def apriori(baskets, min_support):
    n = len(baskets)
    level = [frozenset([i]) for i in sorted({i for b in baskets for i in b})]
    frequent, counted, k = {}, 0, 1
    while level:
        counted += len(level)                      # candidates counted
        counts = {c: sum(1 for b in baskets if c <= b) for c in level}
        kept = {c: v / n for c, v in counts.items() if v / n >= min_support}
        frequent.update(kept)
        k += 1
        cands = set()
        for a, b in combinations(list(kept), 2):
            u = a | b
            if len(u) == k and all(frozenset(s) in kept
                                   for s in combinations(u, k - 1)):
                cands.add(u)
        level = sorted(cands, key=sorted)
    return frequent, counted


freq, counted = apriori(baskets, 0.05)
sizes = {}
for f in freq:
    sizes[len(f)] = sizes.get(len(f), 0) + 1
print(sizes, counted)
items = sorted({i for b in baskets for i in b})
brute = {frozenset(c) for k in range(1, len(items) + 1)
         for c in combinations(items, k) if support(c) >= 0.05}
print(brute == set(freq))
```

```text
{1: 10, 2: 44, 3: 22, 4: 1} 171
True
```

With a support threshold of 0.05 there are 77 frequent sets: 10 single items,
44 pairs, 22 triples, 1 quadruple. To find them Apriori counted the support
of only 171 candidates; brute force, counting all 1023 subsets one by one,
found the same sets. As the number of items grows, the gap grows
exponentially.

## Rules: confidence and lift

A frequent set yields a rule `A → B` (`A` and `B` split the set in two):

- **Confidence:** `support(A ∪ B) / support(A)`, the share of baskets with
  `A` that also have `B`.
- **Lift:** `confidence / support(B)`. Above 1, `A` **raises** `B`; around 1
  there is no relation; below 1 it lowers it.

```python
def make_rules(freq, min_conf):
    rules = []
    for f, s in freq.items():
        for r in range(1, len(f)):
            for a in combinations(sorted(f), r):
                A, B = frozenset(a), f - frozenset(a)
                conf = s / freq[A]
                if conf >= min_conf:
                    lift = conf / freq[B]
                    rules.append((sorted(A), sorted(B),
                                  round(conf, 3), round(lift, 2)))
    return sorted(rules, key=lambda x: -x[3])


rules = make_rules(freq, 0.5)
print(len(rules))
for A, B, conf, lift in rules[:4]:
    print(A, "->", B, conf, lift)
for A, B, conf, lift in rules:
    if (A, B) in ((["bread"], ["butter"]), (["tea"], ["milk"])):
        print(A, "->", B, conf, lift)
```

```text
55
['beer'] -> ['chips'] 0.527 2.86
['chips'] -> ['beer'] 0.607 2.86
['beer', 'milk'] -> ['chips'] 0.525 2.85
['chips', 'milk'] -> ['beer'] 0.578 2.72
['bread'] -> ['butter'] 0.585 1.93
['tea'] -> ['milk'] 0.615 1.05
```

By lift the strongest rule is between beer and chips (2.86): 60.7% of those
who bought chips also bought beer, while only 21% of all baskets have beer.
Bread → butter is strong too (lift 1.93).

The real lesson is in the last line: the rule **tea → milk** has confidence
0.615, higher than bread → butter's (0.585). But its lift is 1.05: milk is
already in 58.5% of the baskets, and tea hardly changes that. Someone looking
only at confidence would produce a meaningless rule, "recommend milk to tea
buyers". A popular item shows up on the right of every rule with high
confidence; lift corrects this.

## The support threshold

```python
for ms in (0.2, 0.1, 0.05, 0.02, 0.01):
    f, c = apriori(baskets, ms)
    print(ms, len(f), c, max(len(x) for x in f))
```

```text
0.2 13 46 2
0.1 30 67 3
0.05 77 171 4
0.02 177 264 5
0.01 318 434 5
```

As the threshold falls from 0.2 to 0.01, the number of frequent sets rises
from 13 to 318 and the largest set grows from 2 items to 5. A low threshold
catches rare but interesting associations; in return far more candidates are
counted and the rule list grows too long to read. Since a real store has
thousands of items, the threshold is chosen very carefully.

## Summary

- Support: the share of baskets containing the set. Confidence: the share of
  `B` when `A` is present. Lift: confidence divided by `B`'s overall share.
- Apriori: every subset of a frequent set is frequent; candidates are built
  and pruned level by level.
- Sort rules by lift (or both), not by confidence: popular items mislead with
  high confidence.
- As the support threshold drops, the number of sets and rules grows fast.
