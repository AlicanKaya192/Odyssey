How similar are two texts? The first step in finding copied or repeated
documents is splitting the text into **pieces (shingles)**: `k` consecutive
words. The **Jaccard similarity** of two texts' piece sets = common pieces /
all distinct pieces.

```python
def shingles(text, k=3):
    words = text.lower().split()
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}


a = "the model was trained on a large text corpus"
b = "the model was trained on a small text corpus"
sa, sb = shingles(a), shingles(b)
print(len(sa), len(sb), len(sa & sb))
print(round(len(sa & sb) / len(sa | sb), 2))
```

```text
7 7 4
0.4
```

Only one word changed, but all three pieces containing that word changed too;
the similarity is 0.4. If `k` is small, unrelated texts also find common
pieces; if it is large, a small change lowers the similarity a lot.

When the pieces go into a Python set they are already hashed behind the
scenes; Rabin-Karp's rolling hash is the way to do this fast at the letter
level. Comparing every pair among millions of documents, however, is not
possible: **MinHash** in section 13 reduces each set to a signature of a few
numbers and estimates the Jaccard similarity.
