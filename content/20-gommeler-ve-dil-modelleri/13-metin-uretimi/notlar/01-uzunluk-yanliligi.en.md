A sentence's log probability is the sum of its words' log probabilities, and
every word takes the sum a little further negative. So beam search favours
short sentences: a sentence like "hey there , the app ." is almost always
more likely than a long, informative ticket. The cure is **length
normalization**: dividing the score by `length ** alpha` when sorting the
paths. The lesson's `beam_search` does this with `alpha`; `alpha = 0` means
no normalization, `alpha = 1` the average per word.

```python
pad = "    "
for alpha in [0.0, 0.5, 1.0]:
    score, text = beam_search(50, alpha)
    print(alpha, len(text.split()), score)
    print(textwrap.fill(text, 76, initial_indent=pad, subsequent_indent=pad))
```

```text
0.0 12 -7.27
    hello , the parcel arrived damaged and the box was open .
0.5 17 -7.92
    good morning , the parcel arrived damaged and the box was open . this is
    urgent !
1.0 28 -10.16
    i get error e# when i log in on the app crashes every time i open the
    order page . i have been a customer for # years
```

- As normalization grows, the beam picks longer sentences; the total log
  probability falls, but the probability per word rises (−7.27 / 13 ≈ −0.56,
  −10.16 / 29 ≈ −0.35).
- `alpha = 1` goes too far: the sentence grew up to the 30-word limit and was
  cut off (it ends with "for # years"). Rewarding length completely is a bias
  too.
- Which `alpha` is good depends on the task: in machine translation values
  between 0.6 and 1 are common, so that the translation does not come out
  much shorter than the source.
- The lesson: "the most likely sentence" is often not the sentence we want.
  The decoding method tries to close the gap between the model's probability
  and the text we really want.
