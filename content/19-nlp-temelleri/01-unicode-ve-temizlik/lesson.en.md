# Unicode and Cleaning Text

In the previous section we used `lower()` and `strip()` to count "Great",
"great" and "great!" as one word. Real text is much messier than that: a
review copied from a web page can hold spaces you cannot see, curly quotes,
HTML leftovers and letters that look the same but are encoded differently.
The computer treats each of them as something different. This section shows
how text is stored in a computer, **Unicode normalisation**, the Turkish case
trap and finally a **cleaning pipeline** that tidies up messy reviews.

## How does a computer store a letter?

A computer can only store numbers. Every character gets a number; the world
standard for that numbering is **Unicode**. A character's number in Unicode
is called its **code point**. When text is written to a file or sent over a
network, these numbers are turned into bytes; the most common way is
**UTF-8**.

```python
for ch in ["A", "a", "ş", "é", "€"]:
    print(ch, ord(ch), len(ch.encode("utf-8")))
print(chr(351), "ş" == chr(351))
```

```text
A 65 1
a 97 1
ş 351 2
é 233 2
€ 8364 3
ş True
```

- `ord` gives a character's code point, `chr` does the reverse: 351 is "ş".
- `encode("utf-8")` turns text into bytes. English letters take 1 byte, "ş"
  and "é" 2 bytes, "€" 3 bytes. That is UTF-8's great advantage: English
  text is byte for byte the same as old ASCII, and every other language fits
  too.
- In Python a `str` is always made of code points; `len("ş")` is 1. You deal
  with bytes only when reading and writing files: `open(...,
  encoding="utf-8")`.

## Strings that look the same but differ

"é" can be written in two ways: as one ready-made character, or as "e"
followed by a **combining mark**. Both look the same on screen.

```python
import unicodedata

a = "caf" + chr(0xE9)      # é: one character
b = "cafe" + chr(0x301)    # e + a combining accent
print(a, b, a == b, len(a), len(b))
print(unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b))
print([unicodedata.name(c) for c in b[-2:]])
```

```text
café café False 4 5
True
['LATIN SMALL LETTER E', 'COMBINING ACUTE ACCENT']
```

- The two "café"s look the same but are different strings to Python: one has
  4 characters, the other 5. If one reached the search box and the other the
  database this way, the search would find nothing.
- `unicodedata.normalize("NFC", ...)` brings text into a **standard form**:
  it combines the letter and the mark into one character. After
  normalisation the two are equal.
- `unicodedata.name` gives a character's official name; very useful when
  hunting an invisible character.

**NFC** (compose) and **NFD** (decompose) are the two standard forms.
Converting text to NFC before comparing or storing it is a good habit.

## Compatibility normalisation: NFKC

Some characters are just a **visual variant** of another: the ligature "ﬁ"
is really "f" and "i", "ＡＢＣ" are full-width letters (they come from East
Asian keyboards) and "…" is a single-character ellipsis. **NFKC** turns these
into their plain forms too.

```python
import unicodedata

samples = [chr(0xFB01) + "ne", "ＡＢＣ１２３", "wow" + chr(0xFF01),
           "x" + chr(0xB2), "wait" + chr(0x2026)]
for s in samples:
    print(s, "->", unicodedata.normalize("NFKC", s))
```

```text
ﬁne -> fine
ＡＢＣ１２３ -> ABC123
wow！ -> wow!
x² -> x2
wait… -> wait...
```

Careful: after NFKC "x²" became "x2", so "x squared" turned into "x two". In
reviews that does not matter, but in a maths or chemistry text NFKC breaks
the meaning. Normalisation is always chosen **for the task**.

## The Turkish case trap

Turkish has four i's: I/ı and İ/i. Python's `lower()` and `upper()` know
nothing about the language; they apply the English rule.

```python
word = "İSTANBUL"
low = word.lower()
print(low, len(word), len(low))
print("ILIK".lower(), "ılık".upper())

TR_LOWER = str.maketrans({"I": "ı", "İ": "i"})


def turkish_lower(text):
    return text.translate(TR_LOWER).lower()


print(turkish_lower("İSTANBUL"), turkish_lower("ILIK"))
```

```text
i̇stanbul 8 9
ilik ILIK
istanbul ılık
```

- `"İSTANBUL".lower()` turns an 8-letter word into a **9-character** string.
  Python makes "İ" into "i" plus a combining dot (U+0307). It looks like
  "istanbul" on screen but is not equal to "istanbul".
- `"ILIK".lower()` gives "ilik"; in Turkish the right answer is "ılık"
  (lukewarm). The two words mean completely different things.
- The fix: convert the two Turkish-specific letters by hand before
  lowercasing. `str.maketrans` builds a letter mapping table and `translate`
  applies it.

`casefold()` has the same problem. Every program that works with Turkish text
has to do this conversion itself.

## Removing accents

We want someone who types "cafe" in a search to find "café" too. For that
the accents are removed: the text is split into letters and marks with NFD,
then the marks are dropped.

```python
import unicodedata


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


for w in ["café", "naïve", "Ångström", "şeker", "ılık", "İzmir"]:
    print(w, "->", strip_accents(w))
```

```text
café -> cafe
naïve -> naive
Ångström -> Angstrom
şeker -> seker
ılık -> ılık
İzmir -> Izmir
```

- `unicodedata.combining(c)` gives a non-zero number for combining marks; we
  drop those.
- "ş" became "s" and "İ" became "I", but **"ı" stayed as it was**: in Unicode
  "ı" is not an accented "i" but a separate letter. There is nothing to
  decompose.
- In Turkish, removing accents is risky: "aşk" (love) and "ask" (ask), "yaşa"
  (live) and "yasa" (law) turn into the same word. Acceptable for search,
  usually a loss of information for classification.

## Messy text from the web

`messy_reviews` in `text_data.py` gives the same reviews as if they had been
copied from a web page: the no-break space, the zero-width space, curly
quotes, HTML tags such as `<br>` and HTML entities such as `&amp;`. `ascii()`
shows invisible characters as codes.

```python
from text_data import messy_reviews

reviews = messy_reviews(2000)
print(ascii(reviews[3]["text"][:44]))
```

```text
'It\xa0does the\xa0job.<br>Much better\xa0tahn my old '
```

`\xa0` is the no-break space: it looks like a space on screen but
`split(" ")` does not count it as one, so "It\xa0does" stays a single word.
How many reviews carry which trace?

```python
from collections import Counter

SIGNS = {"no-break space": chr(0xA0), "zero-width space": chr(0x200B),
         "curly quote": chr(0x2019), "html tag": "<", "entity": "&amp;"}
found = Counter()
for r in reviews:
    for name, sign in SIGNS.items():
        found[name] += sign in r["text"]
for name, count in found.items():
    print(name, count)
```

```text
no-break space 1130
zero-width space 715
curly quote 43
html tag 585
entity 66
```

1130 of the 2000 reviews have a no-break space and 715 a zero-width space.
They are very common in real data too: copy and paste, word processors and
web editors add them.

## A cleaning pipeline

Let us write a function that fixes all of it in order:

```python
import html
import re
import unicodedata

QUOTES = str.maketrans({chr(0x2018): "'", chr(0x2019): "'",
                        chr(0x201C): '"', chr(0x201D): '"'})


def clean(text):
    text = html.unescape(text)                  # &amp; -> &
    text = re.sub(r"<[^>]+>", " ", text)        # <br>, <p> -> a space
    text = unicodedata.normalize("NFKC", text)  # ！ -> !, … -> ...
    text = text.translate(QUOTES)               # curly quote -> straight
    text = text.replace(chr(0x200B), "")        # invisible space
    return " ".join(text.split())               # every kind of space -> one space


raw = [r["text"] for r in reviews]
print(ascii(clean(raw[3])[:44]))


def vocabulary(texts):
    return {w.strip(".,!?" + chr(34)).lower() for t in texts for w in t.split(" ")}


print(len(vocabulary(raw)), len(vocabulary(clean(t) for t in raw)))
```

```text
'It does the job. Much better tahn my old off'
2225 362
```

- `html.unescape` turns HTML entities into real characters.
- `re.sub(r"<[^>]+>", " ", text)` removes everything between `<` and `>`;
  you know regular expressions from the Core Libraries path.
- `text.split()` (without an argument) splits at every kind of space,
  including the no-break space, tabs and line ends; `" ".join(...)` joins
  them back with single spaces.
- **The result:** the messy text had 2225 distinct "words"; after cleaning
  362 are left. The clean data has 360; the only difference is the `&` sign
  and an empty string left over from punctuation. Without cleaning,
  five sixths of the vocabulary would be rubbish: made-up words such as
  "the\xa0job" and "job.<br>Much".

**Order matters.** In this pipeline HTML entities are decoded before tags are
removed, and that has a price: an escaped phrase such as `&lt;b&gt;` in the
text first becomes `<b>` and is then removed as a tag. The reviews have no
such phrase; if they did, removing tags first would be necessary. Know why
each step of a cleaning pipeline sits where it does.

## What not to clean

Cleaning can remove information too. In sentiment analysis "GREAT!!!" and
"great" are not the same: the capitals and the exclamation marks carry the
strength of the feeling. In a programming question "C++" and "C" differ;
removing punctuation merges them. Numbers, dates and order numbers are
needed for information extraction. The rule: **the task decides the
cleaning.** First measure what is messy, as in this section, then remove
only the noise.

## Summary

- Unicode gives each character a number (a code point); UTF-8 turns those
  numbers into bytes. Always open files with `encoding="utf-8"`.
- Text that looks the same can be encoded differently: before comparing,
  `unicodedata.normalize("NFC", ...)`; to simplify visual variants too, NFKC
  (but watch characters that carry meaning, such as "x²").
- Python's `lower()` does not know Turkish: "İ" → "i̇", "I" → "i". Convert
  the Turkish letters with `translate` first.
- Removing accents helps search but can merge words in Turkish; "ı" cannot
  be decomposed at all.
- Web text is full of invisible characters. The cleaning pipeline cut the
  vocabulary from 2225 to 362. Choose cleaning for the task; do not remove
  traces that carry feeling, such as capitals and exclamation marks, for no
  reason.
