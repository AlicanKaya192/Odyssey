`entropy(text)` should return the text's Shannon entropy per character,
rounded to 2 places: for each character's share `p`,
`-sum(p * math.log2(p))`. For empty text it should return `0.0`.

**Expected output:**

```
'aaaaaaaa' 0.0
'password' 2.75
'q8Zr2LxP0vT7mWk9' 4.0
'' 0.0
```
