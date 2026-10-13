Attention compares every word with every word. When all the words of a
sentence attend to each other (self-attention, the next section), n words
need n × n scores. An RNN takes n steps.

```python
for n in [10, 100, 1000, 10000]:
    scores = n * n
    memory_mb = scores * 4 / 1e6
    print(f"{n:>6} {scores:>12,} {memory_mb:>10.1f} MB")
```

```text
    10          100        0.0 MB
   100       10,000        0.0 MB
  1000    1,000,000        4.0 MB
 10000  100,000,000      400.0 MB
```

- A text of 1000 words needs a million scores, 10,000 words a hundred
  million; if each score is a 4-byte number, a single attention table is 400
  MB. In real models this table is computed again in every layer and every
  "head" (the next section).
- This quadratic growth is one of the main reasons that limit how much text a
  language model can read at once (the context window). For long texts,
  sparse attention, sliding windows and methods that compute the table piece
  by piece were developed.
- On the other hand, attention is **parallel**: all n × n scores can be
  computed at once. In an RNN each step must wait for the previous one. This
  parallelism is the main reason large models are built with attention.
