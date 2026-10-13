# Tokenisation

Before a model can work with text, the text has to be split into pieces.
These pieces are called **tokens**, and the job of splitting is called
**tokenisation**. So far we have used `split()`; this section shows where
`split()` falls short, how to write our own tokeniser with regular
expressions, what scikit-learn's default tokeniser silently drops and why
splitting text into sentences is not as easy as it looks.

## Why is split() not enough?

A sentence as it might appear in a support ticket:

```python
text = "I can't wait: $49.99 for ORD-48213?! Mail ana12@example.com."
print("|".join(text.split()))
```

```text
I|can't|wait:|$49.99|for|ORD-48213?!|Mail|ana12@example.com.
```

`split()` only splits at spaces; the `|` sign shows the borders between the
pieces. The problems:

- **Punctuation sticks to words:** "wait:" and "ORD-48213?!" are single
  tokens. If "wait" appears as "wait", "wait:" and "wait." it becomes three
  different tokens.
- **The email keeps its full stop:** the dot at the end of
  "ana12@example.com." belongs to the sentence, not to the address.

## Splitting with a regular expression

A first try: make every run of letters and digits (`\w+`) and every single
non-space sign (`[^\w\s]`) a separate token.

```python
import re

print("|".join(re.findall(r"\w+|[^\w\s]", text)))
```

```text
I|can|'|t|wait|:|$|49|.|99|for|ORD|-|48213|?|!|Mail|ana12|@|example|.|com|.
```

- `\w` is a letter, digit or underscore; `\s` is any kind of space.
  `[^\w\s]` is neither, which means punctuation.
- `re.findall` returns every piece that matches the pattern, in order. In a
  pattern `|` means "either this or that".
- Punctuation is now separate, but this time things were split too much:
  "can't" is three tokens (`can`, `'`, `t`), "$49.99" four tokens, the order
  number and the email fell apart. The amount of 49.99 dollars is no longer
  in any token.

## Writing your own pattern

The fix: put the important patterns first and the general rule last.
`re.findall` tries the alternatives from left to right and takes the first
that matches.

```python
import re

TOKEN = re.compile(r"""
    [\w.+-]+@\w+\.\w+      # an email
  | \$\d+(?:\.\d+)?        # money
  | [A-Z]+-\d+             # an order number
  | \w+(?:'\w+)?           # a word; can't is one piece
  | [^\w\s]                # a single punctuation mark
""", re.VERBOSE)

print("|".join(TOKEN.findall(text)))
```

```text
I|can't|wait|:|$49.99|for|ORD-48213|?|!|Mail|ana12@example.com|.
```

- `re.VERBOSE` lets you write spaces and `#` comments inside the pattern;
  long patterns become readable this way.
- `(?:...)` groups without capturing; it is needed so that `findall` returns
  the whole match.
- `\w+(?:'\w+)?` takes a word together with its apostrophe part, if any:
  "can't", "it's" and "I'm" are single tokens.
- **Order matters:** if the word rule came first, "ana12" would be caught
  before the email rule and the email would fall apart again.

Every task needs its own pattern. In support tickets order numbers and
amounts matter; in tweets `#hashtags` and `@users`; in code `snake_case` and
`a.b()`.

## scikit-learn's default tokeniser

Later we use `CountVectorizer` and `TfidfVectorizer` to turn text into
numbers. Both have a tokeniser inside, and it **silently** drops some things:

```python
from sklearn.feature_extraction.text import CountVectorizer

analyze = CountVectorizer().build_analyzer()
print(analyze("I can't wait: it's a 5-star deal!"))
```

```text
['can', 'wait', 'it', 'star', 'deal']
```

- `build_analyzer()` shows how the vectoriser splits text: it lowercases
  first, then splits with `token_pattern`.
- The default pattern is `r"(?u)\b\w\w+\b"`: words of **at least two
  characters**. "I", "a" and "5" were dropped; "can't" became "can" and the
  "t" was lost; "it's" became "it".
- So the trace of negation ("n't") is gone: "can" and "can't" are the same
  token. In sentiment analysis that is a serious loss. You can pass your own
  tokeniser with `CountVectorizer(token_pattern=...)` or `tokenizer=`.

## How many tokens does each tokeniser give?

Let us compare four tokenisers on 2000 support tickets. They all work on
lowercase text, so any difference comes from the splitting alone.

```python
import re
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
analyze = CountVectorizer().build_analyzer()
tokenizers = {
    "split": lambda t: t.lower().split(),
    "regex": lambda t: re.findall(r"\w+|[^\w\s]", t.lower()),
    "pattern": lambda t: [tok.lower() for tok in TOKEN.findall(t)],
    "sklearn": analyze,
}
for name, tokenize in tokenizers.items():
    tokens = [tok for t in texts for tok in tokenize(t)]
    print(name, len(tokens), len(set(tokens)))
```

```text
split 36829 1718
regex 47205 1497
pattern 43840 1572
sklearn 35699 1479
```

The first number is the total number of tokens, the second the number of
distinct tokens (the vocabulary).

- **split** gives the biggest vocabulary: because punctuation sticks,
  "order", "order." and "order?" count separately.
- **regex** produces the most tokens (every punctuation mark separate, the
  order number in three pieces) but a small vocabulary; the pieces of digits
  are shared.
- **pattern** keeps emails, amounts and order numbers whole, so its
  vocabulary is bigger than regex's: "ana12@example.com" and "$49.99" are
  each a separate "word". These tokens usually appear in a single ticket and
  are useless to a model. The fix is to turn them into placeholders such as
  `<email>` and `<money>`; in sections 03 and 14.
- **sklearn** produces the fewest tokens: no punctuation and no single
  letters.

There is no correct tokeniser; there is one that fits your task. What
matters is **knowing** what gets dropped.

## Splitting into sentences

Tasks such as summarising or translating split the text into sentences
first. The first idea: split at the space after a full stop, exclamation
mark or question mark.

```python
import re


def sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)


for s in sentences("Dr. Lee paid $4.50 today. Great service! Would buy again."):
    print(repr(s))
```

```text
'Dr.'
'Lee paid $4.50 today.'
'Great service!'
'Would buy again.'
```

- `(?<=[.!?])` is a "lookbehind": the previous character is a full stop,
  exclamation mark or question mark. So the punctuation stays in the
  sentence and only the space is removed.
- "$4.50" stayed intact (no space after its dot), but **"Dr."** was taken
  for a sentence of its own. "Mr.", "e.g." and "U.S." fall into the same
  trap.
- Real sentence splitters (nltk, spaCy) use lists of abbreviations or
  trained models. In the exercise you fix this with an abbreviation list.

## The apostrophe in Turkish

```python
import re

print(re.findall(r"\w+", "İstanbul'da 3 gün kaldım."))
```

```text
['İstanbul', 'da', '3', 'gün', 'kaldım']
```

In Python 3, `\w` knows Unicode: "ü" and "ı" are part of the word. The
apostrophe separates a proper name from its suffix: "İstanbul" and "da" are
separate tokens ("in Istanbul"). That is usually what you want: "İstanbul'da",
"İstanbul'a" and "İstanbul'un" share the same root. But for suffixes without
an apostrophe, as in "evlerimizden" ("from our houses"), the tokeniser does
not help; that is the topic of section 03.

## Summary

- Tokenisation splits text into the pieces a model will count; every later
  step builds on that decision.
- `split()` glues punctuation to words; `re.findall(r"\w+|[^\w\s]", ...)`
  separates it but breaks up "can't", amounts and numbers.
- When writing your own pattern, put special patterns first and the general
  rule last; explain it with `re.VERBOSE`.
- scikit-learn's default pattern drops single letters and the "n't"; know
  this in sentiment analysis and pass a `token_pattern` if needed.
- Splitting into sentences is hard because of abbreviations; cases such as
  "Dr." need a list or a model.
