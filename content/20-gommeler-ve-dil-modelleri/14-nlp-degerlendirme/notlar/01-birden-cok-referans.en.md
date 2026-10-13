In the lesson the candidate carrying the same meaning got 0.001 BLEU because
there was a single reference. Since a sentence can be said in many right
ways, BLEU was designed from the start for **several references**: each
word group is counted up to the largest number of times it appears in any
one reference; the brevity penalty uses the reference closest in length.

```python
def bleu_multi(candidate, references, max_n=4):
    c = candidate.split()
    refs = [r.split() for r in references]
    logs = []
    for n in range(1, max_n + 1):
        cand = ngrams(c, n)
        best = Counter()
        for r in refs:
            best |= ngrams(r, n)
        clipped = sum(min(k, best[g]) for g, k in cand.items())
        logs.append(math.log(max(clipped, 1e-9) / max(sum(cand.values()), 1)))
    closest = min((abs(len(r) - len(c)), len(r)) for r in refs)[1]
    brevity = min(1.0, math.exp(1 - closest / len(c)))
    return round(brevity * math.exp(sum(logs) / max_n), 3)


second = ("the package is coming on monday and you will get "
          "a tracking number by email")
for cand in candidates[1:3]:
    print(bleu(cand, reference), bleu_multi(cand, [reference, second]))
```

```text
0.702 0.717
0.001 0.714
```

- With a second reference added, the synonymous candidate rises from 0.001
  to 0.714; the first candidate stays almost in place (0.702 → 0.717).
- The `|` operation of `Counter`s takes the largest count of each group: if
  a group appears once in the first reference and twice in the second, it
  is counted up to 2.
- This is why translation test sets are often built with 2–4 human
  translations per sentence. But writing references is expensive, and no set
  of references covers all the right answers.
