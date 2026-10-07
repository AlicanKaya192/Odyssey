Build MapReduce's classic example yourself: counting words.

**What to do:**

1. Write `mapper(line)`: it produces `(word, 1)` for every word in the line
   (`yield`).
2. Shuffle: gather each word's values with `defaultdict(list)`.
3. Write `reducer(key, values)`: it returns `(word, total)`.
4. Print the words that appear at least twice, sorted by count from largest
   to smallest and, for equal counts, alphabetically, with the word and the
   count on each line.

**Expected output:**

```
shuffle 3
data 2
machines 2
many 2
needs 2
reduce 2
the 2
then 2
```
