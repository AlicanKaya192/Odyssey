`per_class_hits(ngrams)` should build a `CountVectorizer` with the given
`ngram_range` and a `MultinomialNB`, and return, in a dictionary from class
name to share, how many of **each class's** test examples were found right (3
places), classes in alphabetical order. `ngrams` may come as a list;
pass `tuple(ngrams)`. Which class is hardest, which one do
word pairs help?

**Expected output:**

```
(1, 1)
   account 0.942
   billing 0.924
   refund 0.87
   shipping 0.932
   technical 0.935
(1, 2)
   account 0.951
   billing 0.962
   refund 0.87
   shipping 0.939
   technical 0.952
```
