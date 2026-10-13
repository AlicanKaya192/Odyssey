The basic structure of search engines is the inverted index: word → the
numbers of the documents it appears in. `build_index(docs)` should build the
number list for each word (ascending, no repeats); `search_all(index, query)`
should return, sorted, the numbers of the documents containing **all** the
query's words.

**Expected output:**

```
[0, 1] [0, 2]
[0]
[]
```
