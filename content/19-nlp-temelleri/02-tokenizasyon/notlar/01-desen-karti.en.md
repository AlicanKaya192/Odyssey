The regular expression pieces used most often when writing a tokeniser.

## Building blocks

| Piece | Meaning | Example match |
|---|---|---|
| `\w` | letter, digit, underscore (Unicode) | `a`, `ş`, `7`, `_` |
| `\d` | digit | `4` |
| `\s` | any kind of space | space, tab, line end |
| `[^\w\s]` | neither letter nor space: punctuation | `!`, `,`, `$` |
| `+` / `*` / `?` | one or more / zero or more / optional | `\w+`, `\d*`, `s?` |
| <code>a&#124;b</code> | either a or b; tried from left to right | <code>\$\d+&#124;\w+</code> |
| `(?:...)` | a non-capturing group | `\w+(?:'\w+)?` |
| `(?<=x)` | a position preceded by x (lookbehind) | `(?<=[.!?])\s+` |
| `\b` | a word boundary | `\bcat\b` |
| `re.VERBOSE` | spaces and `#` comments inside a pattern | long patterns |

## Functions

| Function | What it returns |
|---|---|
| `re.findall(pattern, text)` | A list of every matching piece (a token list) |
| `re.split(pattern, text)` | The pieces split at the pattern (sentence splitting) |
| `re.sub(pattern, new, text)` | `new` in place of every match (cleaning, placeholders) |
| `re.compile(pattern)` | A pattern object to use again and again |

## Giving scikit-learn your own pattern

The default pattern dropped single letters and the "n't". A pattern that
keeps words with apostrophes and single letters:

```python
from sklearn.feature_extraction.text import CountVectorizer

keep = CountVectorizer(token_pattern=r"(?u)\b\w+(?:'\w+)?\b").build_analyzer()
print(keep("I can't wait: it's a 5-star deal!"))
```

```text
['i', "can't", 'wait', "it's", 'a', '5', 'star', 'deal']
```

"can't", "it's", "i", "a" and "5" are kept now. Punctuation is still gone:
`token_pattern` only takes the pieces that match.

## Common patterns

| Pattern | Regular expression (roughly) |
|---|---|
| Email | `[\w.+-]+@\w+\.\w+` |
| Address (URL) | `https?://\S+` |
| Hashtag and user | `[#@]\w+` |
| Money | `\$\d+(?:[.,]\d+)*` |
| Date (dd.mm.yyyy) | `\d{2}\.\d{2}\.\d{4}` |
| Hyphenated word | `\w+(?:-\w+)+` |

These are "rough": the real rules for emails and addresses are far more
complex. For text data this much is usually enough; always try your pattern
on your own data.
