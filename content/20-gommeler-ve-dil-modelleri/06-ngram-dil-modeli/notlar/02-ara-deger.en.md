Add-k gives every unseen n-gram the same small probability. A smarter way is
**interpolation**: mixing the trigram probability with the bigram
probability. If the trigram was never seen, the bigram steps in.

`P(c | a, b) = λ · P_tri(c | a, b) + (1 − λ) · P_bi(c | b)`

Let us try it with the lesson's counts (the trigram part from counts, the
bigram part add-0.01):

```python
def p_interp(s, i, lam):
    bigram = p_bigram(s[i - 1], s[i], 0.01)
    if i == 1 or pairs[s[i - 2], s[i - 1]] == 0:
        return (1 - lam) * bigram
    a, b, c = s[i - 2], s[i - 1], s[i]
    return lam * trigrams[a, b, c] / pairs[a, b] + (1 - lam) * bigram


for lam in [0.3, 0.5, 0.7, 0.9]:
    print(lam, perplexity(lambda s, i: p_interp(s, i, lam)))
```

```text
0.3 2.85
0.5 2.6
0.7 2.45
0.9 2.42
```

- As λ grows, perplexity falls up to 0.9; but in the lesson the add-0.001
  trigram reached 2.15. On this small, patterned data simple add-k is good
  enough.
- In this simple version, when the trigram context was never seen, only
  `(1 − λ)` of the probability remains; so the total does not add up to 1.
  In real applications λ is tuned by how often the context was seen.
- For many years the best n-gram method was **Kneser-Ney** smoothing: it
  looks at in how many **different** contexts a word appears ("francisco" is
  frequent but always after "san"; it is not expected in a new context).
  Until neural language models arrived, speech recognition and machine
  translation ran on these models.
