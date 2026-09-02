You have the scores of two exams, but **the students are in a different
order**. You will add them up — and see why pandas gets this right.

`first` is in the order Ada, Kerem, Mina; `second` is in the order Mina, Ada,
Kerem.

**What you need to do:**

1. Add the two Series together into a Series called `total`.
2. Print `total` and **the name with the highest total**.
3. The `extra` Series carries only the label `Efe`. Put `total + extra` into a
   Series called `with_extra` and print how many `NaN` it contains.

**Expected output:**

```
Ada       65
Kerem    115
Mina     100
dtype: int64
Kerem
4
```

**You are seeing two things at once:**

- **Alignment:** the orders did not match, yet the totals are right. pandas
  added `Ada` to `Ada`. NumPy would have gone by position and given a
  silently wrong answer.
- **A label that does not match:** the last line gives four `NaN`. `Efe` is
  not in the first Series and the other three are not in `extra` — rather
  than making something up, pandas says "unknown".
