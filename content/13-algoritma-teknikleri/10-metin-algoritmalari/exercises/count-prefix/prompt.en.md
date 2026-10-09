Write the function `count_prefix(words, prefixes)` with a **trie**: for each
prefix it returns the number of words starting with that prefix, as a list in
the same order as the prefixes. The empty prefix counts all words.

At each node write the number of words passing through it under the key
`"#"`; for a query go down to the prefix's node and read the count. No
`startswith`.

**Expected output:**

```
[4, 5, 3, 0, 8]
```
