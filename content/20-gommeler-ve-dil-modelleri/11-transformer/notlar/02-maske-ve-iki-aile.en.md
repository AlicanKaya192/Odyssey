Let us test that the mask really prevents leaks: change the last word and
see whether the output of the first four words changes.

```python
X2 = (X + Pe).copy()
X2[4] = E[vocab.index("dog")] + Pe[4]
full = np.ones((5, 5), dtype=bool)
print(np.allclose(block(X + Pe, mask)[:4], block(X2, mask)[:4]))
print(np.allclose(block(X + Pe, full)[:4], block(X2, full)[:4]))
```

```text
True
False
```

- With the mask, the output of the first four words is not affected by the
  last word (`True`). So the "next word" loss for all positions of a sentence
  can be found with a single forward pass: position 4 has not seen word 5
  while predicting it. In an RNN the same work had to be done word by word,
  in turn.
- In attention without a mask every word sees every word (`False`).

These two options separate the two big families of transformers:

- **Encoder** models have no mask; every word sees both sides. They are
  trained by hiding some words of the sentence and having them predicted (a
  masked language model). They are used for **understanding** tasks such as
  classification, search and tagging.
- **Decoder** models have the causal mask; they are trained by predicting the
  next word and they **generate** text. The large language models that chat
  today belong to this family.
- The first transformer used both together: the encoder read the source
  sentence, and the decoder produced the translation word by word.
