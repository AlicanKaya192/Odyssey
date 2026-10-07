Do Section 12's word count in Spark syntax.

**What to do:**

1. The lines are in the starter code; `lines = sc.parallelize(text, 2)`.
2. Split into words with `flatMap`, make `(word, 1)` with `map`, add up with
   `reduceByKey`.
3. Sort the result by count from largest to smallest and, for equal counts,
   by word: `sortBy(lambda kv: (-kv[1], kv[0]))`.
4. Print the first four items (`take(4)`) with the word and count on each
   line.
5. Print how many different words there are (`count()`).

**Expected output:**

```
data 3
spark 3
in 2
memory 2
13
```
