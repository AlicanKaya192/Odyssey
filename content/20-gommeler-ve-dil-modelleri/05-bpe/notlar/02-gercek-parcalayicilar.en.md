The tokenisers of real models are relatives of the BPE in this lesson:

| Method | Difference |
|---|---|
| WordPiece | Picks the pair not by frequency but by how much merging raises the likelihood; pieces inside a word are marked with `##` |
| SentencePiece | Does not split text into words first; counts the space as a symbol too (`▁`), works the same in every language |
| Byte-level BPE | Starts from 256 bytes instead of letters; no character, emoji included, is ever unknown |

## Why does the number of pieces matter?

Language models process text piece by piece: how much text they can take in
(the context length) and the cost of computing are measured **in pieces**. A
tokeniser trained for one language splits other languages into more pieces.
With the `merges` learned from the lesson's English tickets, let us split the
Turkish words of the first note:

```python
english = [w for w in test for _ in range(test[w])]
turkish_words = ["evlerimizden", "okullardan", "kitaplarda", "kalemler",
                 "evlerde", "okuldan"]
for name, sample in [("english", english), ("turkish", turkish_words)]:
    pieces = sum(len(encode(w, merges)) for w in sample)
    print(name, round(pieces / len(sample), 2))
```

```text
english 1.34
turkish 6.67
```

- English tickets take 1.34 pieces per word, the Turkish words 6.67: almost
  letter by letter. The tokeniser never saw Turkish roots or suffixes.
- At scale this is a real inequality: text carrying the same meaning takes
  far more pieces in some languages; the model's context fills faster and
  processing costs more. That is why multilingual models train their
  tokenisers on text gathered from many languages.
