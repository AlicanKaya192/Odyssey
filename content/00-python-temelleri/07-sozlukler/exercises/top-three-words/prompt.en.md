The words of a text are given as a list:

```python
words = ["the", "cat", "and", "the", "dog", "and", "the", "bird", "sat", "on", "the", "mat"]
```

1. Count how many times each word appears in the dictionary `counts`
   (`{"the": 4, "cat": 1, ...}`).
2. Print the **three** most common words with their counts.

```
the 4
and 2
bird 1
```

Ordering rule: the larger count first. **If the counts are equal**, the
words go in alphabetical order (`bird` comes before `cat`).

The second step is the hard part. Sorting by a rule with `sorted` needs
something you have not learned yet; instead, run a "find the best" loop
**three times**: on each round, find the best among the words not chosen
yet, print it and add it to the chosen ones.

> Watch out: "best" has two conditions: a larger count **or** the same
> count but earlier in the alphabet. Texts can be compared too:
> `"bird" < "cat"` is `True`.
