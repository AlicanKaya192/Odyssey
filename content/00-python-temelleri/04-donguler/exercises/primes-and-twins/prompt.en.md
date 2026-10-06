A **prime number** is greater than 1 and divisible only by 1 and itself:
2, 3, 5, 7, 11… Two primes that differ by 2 are called **twin primes**:
(3, 5), (5, 7), (11, 13)…

From `2` to `100` (100 included):

1. Count how many primes there are in the variable `prime_count`.
2. Find the **largest** twin prime pair in this range in the variables
   `twin_a` and `twin_b`.

```
Primes up to 100 : 25
Largest twin pair: 71 73
```

In this exercise two loops run one inside the other:

- **The outer loop** takes every number from 2 to 100, one by one.
- **The inner loop** checks whether that number is prime: starting from 2,
  it tries dividing by the numbers smaller than it. If one divides it
  exactly, the number is not prime; you can stop looking with `break`.

For the twin pairs, keep **the previous prime** in a variable. When you
find a new prime and the difference is 2, you have found a twin pair.
Because the numbers go from small to large, the last pair you find is the
largest.

> Watch out: to tell whether a number is prime, set up a flag that starts
> as "prime" (`is_prime = True`) and make it `False` when you find a
> divisor. Do not forget to set this flag back to `True` for **every** new
> number.
