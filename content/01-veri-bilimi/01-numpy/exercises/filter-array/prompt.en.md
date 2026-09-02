You have the scores of seven students. You will separate the ones who
passed and find their average — **without a loop and without `if`.**

**What you need to do:**

1. The `scores` array is ready in the starter code.
2. Take the scores that are **60 or above** into an array called `passed`.
3. Take the scores **between 60 and 85** (60 included, 85 not) into an array
   called `middle`.
4. Print, in order: `passed`, how many passed, the average of those who
   passed (rounded to two places), and `middle`.

**Expected output:**

```
[82 91 60 74 88]
5
79.0
[82 60 74]
```

**Trap:** `and` **does not work** when combining two conditions; you use `&`
and put each condition in parentheses. Writing `and` gives you a
`ValueError`.
