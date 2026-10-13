When rules are not enough, information extraction is turned into a
**sequence labelling** problem: each token gets a label and a model learns
the labels. The most common label format is **BIO**:

| Label | Meaning |
|---|---|
| `B-TYPE` | The first token of an entity (begin) |
| `I-TYPE` | A continuation of the same entity (inside) |
| `O` | Not part of any entity (outside) |

Let us turn the pieces we found with rules into BIO labels. Texts labelled
like this become data for training a model:

```python
import re

PATTERNS = {"AMOUNT": r"\$\d+\.\d{2}", "ORDER": r"\bORD-\d{5}\b",
            "DATE": r"\b\d{1,2} [A-Z][a-z]+ \d{4}\b"}


def bio(text):
    tokens = list(re.finditer(r"\S+", text))
    tags = ["O"] * len(tokens)
    for kind, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            inside = [i for i, t in enumerate(tokens)
                      if t.start() < match.end() and t.end() > match.start()]
            for n, i in enumerate(inside):
                tags[i] = ("B-" if n == 0 else "I-") + kind
    return [(t.group(), tag) for t, tag in zip(tokens, tags)]


for token, tag in bio("Refund $12.49 for ORD-12345 sent on 13 October 2026."):
    print(f"{token:<10} {tag}")
```

```text
Refund     O
$12.49     B-AMOUNT
for        O
ORD-12345  B-ORDER
sent       O
on         O
13         B-DATE
October    I-DATE
2026.      I-DATE
```

- A token belongs to an entity if it **overlaps** a match: "2026." is one
  token together with the final full stop, but it is part of the date.
- The three-token date is `B-DATE I-DATE I-DATE`. Without `I-`, two separate
  entities next to each other could not be told apart from one long entity.
- A model learning these labels looks at each token and its **neighbours**
  (does it start with "$", is the previous token "refund", is the previous
  label `B-`). Because labels depend on each other, methods that solve the
  whole sequence together are used instead of classifying tokens one by one.
  In the Embeddings and Language Models module we will do exactly that with
  HMMs and the Viterbi algorithm.
