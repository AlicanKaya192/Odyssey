You do not have to write edit distance yourself every time you want to find
similar texts. The `difflib` module in Python's standard library measures how
similar two texts are and finds the closest matches.

```python
import difflib

words = ["pandas", "numpy", "python", "matplotlib", "seaborn", "sklearn"]
print(difflib.get_close_matches("pyhton", words))
print(difflib.get_close_matches("matplot", words, n=1))
print(round(difflib.SequenceMatcher(None, "kitten", "sitting").ratio(), 3))

old = ["import pandas", "df = pandas.read_csv('a.csv')", "print(df.head())"]
new = ["import pandas as pd", "df = pd.read_csv('a.csv')", "print(df.head())"]
for line in difflib.unified_diff(old, new, lineterm="", n=0):
    print(line)
```

```text
['python']
['matplotlib']
0.615
--- 
+++ 
@@ -1,2 +1,2 @@
-import pandas
-df = pandas.read_csv('a.csv')
+import pandas as pd
+df = pd.read_csv('a.csv')
```

- `get_close_matches(word, list)` gives the ones with a similarity above 0.6,
  most similar first; ready for "did you mean?".
- `SequenceMatcher(...).ratio()` is a similarity ratio between 0 and 1:
  `2 × matched / total length`.
- `unified_diff` writes the difference of two lists of lines in `git diff`
  format.

`difflib` does not use edit distance but another method that looks for the
longest matching pieces (Ratcliff–Obershelp); the results are often similar
but not exactly the same. For matching records with spelling differences in
large data sets there are also third-party packages written in C, such as
`rapidfuzz`.
