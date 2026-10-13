In the lesson the nearest neighbours of "refund" were typos. How common is
that? When the data generator makes a typo it swaps two adjacent letters; so
the misspelled word is made of **the same letters** as the right one. With
the lesson's `E`, let us count them among the first five neighbours of a few
words:

```python
for word in ["parcel", "refund", "password", "invoice", "account", "tracking"]:
    sims = E @ E[index[word]]
    top = [vocab[i] for i in np.argsort(-sims)[1:6]]
    typos = [t for t in top if sorted(t) == sorted(word)]
    print(f"{word:<9} {len(typos)} {typos}")
```

```text
parcel    3 ['pracel', 'parecl', 'pacrel']
refund    3 ['rfeund', 'refnud', 'reufnd']
password  3 ['paswsord', 'psasword', 'passwrod']
invoice   4 ['invocie', 'ivnoice', 'invioce', 'inovice']
account   3 ['acconut', 'accuont', 'acocunt']
tracking  4 ['tracikng', 'tracknig', 'trcaking', 'trakcing']
```

- For many words most of the first five neighbours are their own typos. The
  vectors learned this not by looking at letters but **by looking at
  context**: "rfeund" and "refund" appear in the same sentence patterns.
- For this the misspelled form had to be seen a few times in training (we
  kept words appearing at least 3 times). A typo never seen has no vector.
- For unseen typos the word has to be built **from letter pieces**: methods
  such as fastText learn a word's vector as the sum of the vectors of its
  character n-grams; "pracel" and "parcel" share many pieces. The BPE of the
  next section is another form of the same idea.
