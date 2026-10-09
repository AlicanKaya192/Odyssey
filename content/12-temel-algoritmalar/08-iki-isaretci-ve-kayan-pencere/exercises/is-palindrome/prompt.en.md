Write the function `is_palindrome(text)` **with two pointers**: it returns
`True` if the text reads the same backwards. An empty string and a single
letter are palindromes.

Compare the letters at the two ends; if equal, move the pointers inwards,
otherwise `False` at once. Do not use `reversed` or `[::-1]`.

**Expected output:**

```
True
False
True
```
