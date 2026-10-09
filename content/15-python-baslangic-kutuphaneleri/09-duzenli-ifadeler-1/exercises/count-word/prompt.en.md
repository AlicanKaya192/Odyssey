Write the function `count_word(text, word)`: count how many times `word`
appears in the text as a **whole word**, ignoring case (`cat` inside `concat`
does not count). `word` may contain special characters (`a+b`): `re.escape`
it before putting it in the pattern. The word boundary is `\b`.

**Expected output:**

```
2
2
```
