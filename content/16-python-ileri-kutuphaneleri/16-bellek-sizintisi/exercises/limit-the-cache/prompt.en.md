`price(product_id)` keeps its results in its own dictionary and the
dictionary never shrinks. Remove the dictionary and add
`@lru_cache(maxsize=256)` to the function. The expected output:

```
256 22
```

**Expected output:**

```
256 22
```
