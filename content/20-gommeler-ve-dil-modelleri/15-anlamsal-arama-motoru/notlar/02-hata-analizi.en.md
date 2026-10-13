The first step to improving a system is to look at **where the errors
gather**. Which categories does hybrid search confuse in its first result?

```python
import textwrap

best = categories[engine.scores(queries).argmax(axis=1)]
wrong = best != labels
pairs = Counter(zip(labels[wrong], best[wrong]))
print(int(wrong.sum()))
for (truth, guess), n in pairs.most_common(4):
    print(truth, "->", guess, n)
(truth, guess), _ = pairs.most_common(1)[0]
i = next(i for i in range(len(queries))
         if labels[i] == truth and best[i] == guess)
print(textwrap.fill(queries[i], 76))
```

```text
322
shipping -> billing 63
shipping -> refund 38
technical -> account 36
shipping -> technical 26
Dear support, Where is my order ORD-96253? It has not arrived yet. This is
the second time this happens.
```

- The first result is wrong for 322 of the 2000 tickets. The most common
  error is parcel tickets going to a billing article (63), then parcel going
  to refund (38).
- The example ticket is clearly a parcel question: "Where is my order ...?
  It has not arrived yet." But the word "order" also appears in the billing
  articles, and the rest of the ticket ("dear support", "the second time
  this happens") says nothing. In the average vector, the two words carrying
  the topic melt among words unrelated to the topic.
- Improvement ideas that follow: dropping greeting and closing sentences,
  averaging words with TF-IDF weights (the SIF of 04), or writing more
  articles per category. Which one works has to be seen by measuring again:
  error analysis gives ideas, not proof.
