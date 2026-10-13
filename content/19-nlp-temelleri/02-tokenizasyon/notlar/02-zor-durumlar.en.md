The lesson's `TOKEN` pattern worked well on support tickets. What happens
when you take it to another kind of text?

```python
import re

TOKEN = re.compile(r"""
    [\w.+-]+@\w+\.\w+      # an email
  | \$\d+(?:\.\d+)?        # money
  | [A-Z]+-\d+             # an order number
  | \w+(?:'\w+)?           # a word; can't is one piece
  | [^\w\s]                # a single punctuation mark
""", re.VERBOSE)

for text in ["see https://example.com/help", "only $1,299.00", "on 14.03.2026",
             "state-of-the-art", "thanks :)"]:
    print("|".join(TOKEN.findall(text)))
```

```text
see|https|:|/|/|example|.|com|/|help
only|$1|,|299|.|00
on|14|.|03|.|2026
state|-|of|-|the|-|art
thanks|:|)
```

All five fell apart:

| Text | What happened | What can be done |
|---|---|---|
| An address (URL) | Split into 9 pieces | Put an `https?://\S+` rule first |
| `$1,299.00` | Broken at the thousands comma: `$1` | Add `(?:[.,]\d+)*` to the money pattern |
| `14.03.2026` | Five pieces | A date rule, or turning dates into a placeholder |
| `state-of-the-art` | Seven pieces | A hyphenated-word rule; but "e-mail" and "email" still differ |
| `:)` | Two punctuation marks | An emoticon list for sentiment analysis |

## The lesson

A tokeniser is only as good as the data it was written for. When you move to
a new source:

1. Tokenise 20–30 random texts and look at them by hand.
2. Note the patterns that fall apart (addresses, dates, money, emoticons).
3. Add a rule for each **in front of the general rules**.
4. Measure how the vocabulary changes.

In Turkish text, also: the decimal comma ("3,75"), the date format
(14.03.2026) and suffixes after an apostrophe ("Ankara'ya"). Ready-made
tokenisers often come with English rules; always try them on Turkish data.
