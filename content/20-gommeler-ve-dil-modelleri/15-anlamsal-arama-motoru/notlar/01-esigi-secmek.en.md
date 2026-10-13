The threshold is a trade-off: as it rises, more unrelated text is rejected,
but more real tickets are left unanswered too. Let us put three rates side
by side for a few thresholds:

```python
inside = engine.scores(queries).max(axis=1)
outside = [engine.scores(texts).max(axis=1) for texts in [reviews, world]]
for t in [0.3, 0.35, 0.4, 0.45, 0.5]:
    rejected = [round(float((top < t).mean()), 3) for top in outside]
    print(t, round(float((inside >= t).mean()), 3), *rejected)
```

```text
0.3 1.0 0.41 0.952
0.35 0.995 0.424 0.952
0.4 0.96 0.55 0.952
0.45 0.898 0.676 0.952
0.5 0.769 0.732 0.952
```

The columns: the threshold, real tickets answered, reviews rejected,
small-world sentences rejected.

- As the threshold goes from 0.3 to 0.5, rejected reviews rise from 41% to
  73.2%; but answered real tickets fall from 100% to 76.9%. One customer in
  four is left without an answer.
- For small-world sentences the rate is always 95.2%. The 4.8% that pass are
  sentences like "the bus is slow" and "the taxi stopped at the depot":
  "slow" and "stopped" appear in tickets too ("the website is very slow",
  "stopped working"), and these sentences get high scores; no threshold in
  this range separates them.
- The threshold should be chosen on a **separate** validation set, not by
  looking at the test set; otherwise the measured rates come out optimistic.
  Here we accepted losing 5% of real tickets; that rate is a product
  decision, not a model decision.
- For better separation other signals are used besides the score: the share
  of the query's words in the vocabulary, the gap between the first two
  results, or a separate classifier trained on "off-topic" examples.
