Write the function `pair_rules(baskets, min_support, min_conf)`: for every
item pair `{a, b}` with support at least `min_support` try two rules
(`a → b`, `b → a`). Return those with confidence at least `min_conf` as the
text `"a -> b lift"` (lift `round(..., 2)`); from the largest lift down, ties
by text.

**Expected output:**

```
bread -> butter 1.6
butter -> bread 1.6
bread -> milk 0.96
milk -> bread 0.96
butter -> milk 0.8
```
