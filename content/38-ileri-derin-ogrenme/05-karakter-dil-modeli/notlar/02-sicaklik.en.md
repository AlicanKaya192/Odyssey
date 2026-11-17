Greedy choice always produces the same text. For variety we **sample**
according to the probabilities; the **temperature** sets how peaked those
probabilities are: the logits are divided by the temperature before the
softmax. It was written with NumPy in the text generation section of the
Embeddings and Language Models module; in PyTorch the same thing is:

```python
import torch

logits = torch.tensor([2.0, 1.0, 0.1])
for temp in (0.5, 1.0, 2.0):
    probs = torch.softmax(logits / temp, dim=0)
    print(temp, [round(p, 2) for p in probs.tolist()])

gen = torch.Generator().manual_seed(0)
probs = torch.softmax(logits, dim=0)
sample = torch.multinomial(probs, num_samples=5, replacement=True, generator=gen)
print(sample.shape, sample.dtype)
```

```text
0.5 [0.86, 0.12, 0.02]
1.0 [0.66, 0.24, 0.1]
2.0 [0.5, 0.3, 0.19]
torch.Size([5]) torch.int64
```

- A low temperature (0.5) enlarges the most likely option: the behaviour
  gets close to greedy choice. A high temperature (2) evens the
  probabilities out: the text becomes more varied but makes more mistakes.
- `torch.multinomial` draws ids by probability; we gave it its own
  `Generator` so that it is repeatable. The returned ids are `int64`, so they
  can go straight into an `nn.Embedding`.

| Method | Output | When |
|---|---|---|
| Greedy (`argmax`) | Always the same, can fall into repetition | Short tasks with one right answer |
| Sampling, temperature < 1 | A little varied, mostly right | General text generation |
| Sampling, temperature > 1 | Very varied, often wrong | Brainstorming, experiments |
