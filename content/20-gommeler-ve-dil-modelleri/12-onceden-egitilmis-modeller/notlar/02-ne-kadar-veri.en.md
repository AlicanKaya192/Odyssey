How much unlabelled text does pretraining need? Let us learn the vectors
from 200, 1000, 5000 and 20,000 tickets and try them with 20 and 50 labels:

```python
for size in [200, 1000, 5000, 20000]:
    index, E = pretrain(unlabelled[:size])
    D = np.array([embed(t) for t in texts])
    print(size, len(index), curve_point(20)[1], curve_point(50)[1])
```

```text
200 171 0.735 0.841
1000 204 0.725 0.842
5000 323 0.728 0.857
20000 440 0.748 0.866
```

The columns: the number of unlabelled tickets, the vocabulary, and accuracy
with 20 and 50 labels.

- Even 200 tickets give 84.1% with 50 labels; 20,000 tickets 86.6%. The
  vocabulary grows from 171 words to 440: rare words (typos, city names) only
  enter the vocabulary when they are seen at least 3 times in a lot of text.
- The gain is small in this small world, because the language of the tickets
  is narrow and regular: a few hundred tickets show most of the words. A real
  language has hundreds of thousands of words and countless patterns; a good
  vector for a rare word needs millions of sentences.
- This is why large language models are trained on billions of words: to see
  the long tail of language (rare words, rare structures). The previous note
  showed that quantity alone is not enough: the text must come from the
  right domain.
