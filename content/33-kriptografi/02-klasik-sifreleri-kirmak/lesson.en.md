# Breaking Classical Ciphers

In the Classical Ciphers section we said every cipher has a weakness. In
this section we actually break them all. The aim is not to learn attacks
but **to see by measurement why a cipher is not enough**: how easily does
someone who does not know the key get from ciphertext to plaintext? The
answers to this question shaped how modern ciphers are designed.

We separate two situations for the attacker:

- **Ciphertext-only:** they only have the ciphertext. Every attack in this
  section is like this.
- **Known-plaintext:** they know some plaintext–ciphertext pairs. We will
  see this in the XOR and the One-Time Pad section.

The text in the examples is in the file `cipher_data.py`: an English
paragraph of 704 letters (`SAMPLE`) and the approximate percentages of
letters in English (`ENGLISH_FREQ`).

## Caesar: try every key

With 26 keys, trying them all is the easiest way. But how do we know which
one is right? A computer does not see "meaningful text"; it needs a
**measure**. The simplest: count common words in the decrypted text.

```python
def caesar(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


COMMON = {"the", "is", "and", "of", "in", "to"}
secret = "wkh vhfuhw lv lq wkh jdughq"
scores = []
for shift in range(26):
    words = caesar(secret, -shift).split()
    hits = sum(word in COMMON for word in words)
    scores.append((hits, shift))
best = max(scores)
print(len(scores), "keys tried")
print("best shift:", best[1], "->", caesar(secret, -best[1]))
```

```text
26 keys tried
best shift: 3 -> the secret is in the garden
```

26 tries took no time at all, and the right key gave itself away with
common words. Every cipher with a small key space falls like this.

## Letter frequency

Letters are not used equally often in any language. In English `e` is the
most common letter, followed by `t`, `a`, `o`. Let us count in our sample
text:

```python
from collections import Counter

from cipher_data import SAMPLE

letters = [ch for ch in SAMPLE.lower() if ch.isalpha()]
counts = Counter(letters)
for letter, n in counts.most_common(5):
    print(letter, f"{100 * n / len(letters):.1f}%")
```

```text
e 12.6%
t 10.7%
h 8.8%
a 8.5%
o 6.8%
```

This distribution is a **fingerprint**. The Caesar and substitution ciphers
change letters but not the distribution: whatever letter the plaintext `e`
became, that letter is the most common one in the ciphertext.

## The best shift with chi-squared

A sturdier measure than a word list, using every letter, is the
**chi-squared** distance: for each letter, the square of the difference
between the expected and the observed count, divided by the expected count,
summed. The more the text looks like English, the **smaller** the result.
Let us encrypt the sample with a shift we pretend not to know and score
every shift:

```python
from cipher_data import SAMPLE, ENGLISH_FREQ


def chi_squared(text):
    letters = [ch for ch in text.lower() if ch.isalpha()]
    total = len(letters)
    score = 0
    for letter, percent in ENGLISH_FREQ.items():
        expected = total * percent / 100
        observed = letters.count(letter)
        score += (observed - expected) ** 2 / expected
    return score


secret = caesar(SAMPLE, 7)
ranked = sorted((chi_squared(caesar(secret, -s)), s) for s in range(26))
for score, shift in ranked[:3]:
    print(f"shift {shift:>2}: {score:8.1f}")
```

```text
shift  7:     41.3
shift 13:   2620.1
shift 18:   3026.5
```

The right shift (7) scored more than sixty times lower than the second
best. No word list was needed; the statistics of the language were enough.

## A first step against substitution

The substitution cipher has 26! keys, so brute force is useless. But letter
frequency works here too: sort the ciphertext letters by frequency and match
them with the English order (`etaoinshr…`).

```python
import string
from collections import Counter

from cipher_data import SAMPLE

key = "qwertyuiopasdfghjklzxcvbnm"
table = str.maketrans(string.ascii_lowercase, key)
secret = SAMPLE.lower().translate(table)

order = [ch for ch, _ in Counter(c for c in secret if c.isalpha()).most_common()]
guess = dict(zip(order, "etaoinshrdlcumwfgypbvkjxqz"))
real = dict(zip(key, string.ascii_lowercase))
right = sum(guess[ch] == real[ch] for ch in order)
print("letters in text:", len(order))
print("right at first try:", right)
print("most common:", order[0], "->", guess[order[0]])
```

```text
letters in text: 22
right at first try: 5
most common: t -> e
```

Only a few letters were right at the first try: in a text of 704 letters
the frequencies do not match the English average exactly. But the most
common letter was correctly matched to `e`, and that is a start. A real
solution goes on from here: the most common three-letter word is probably
`the`, one-letter words are `a` or `i`, double letters (`ll`, `ee`, `ss`)…
Every right guess makes the next one easier. By hand this takes a few
minutes, with a program a second.

## Vigenère: find the key length

Because Vigenère turns the same letter into different letters in different
places, the letter distribution of the ciphertext **flattens**. The number
that measures this is the **index of coincidence** (IoC): the probability
that two letters picked at random from the text are the same. About 0.066
in English text, 1/26 ≈ 0.038 in random text with evenly spread letters.

If we guess a key length `L` and split the text into `L` columns (each
column holds the letters shifted by the same key letter), then for the
right `L` every column is a plain Caesar cipher and its IoC rises to the
value of English:

```python
from collections import Counter

from cipher_data import SAMPLE


def vigenere(text, key):
    result, i = "", 0
    for ch in text.lower():
        if ch.isalpha():
            result += chr((ord(ch) - 97 + ord(key[i % len(key)]) - 97) % 26 + 97)
            i += 1
    return result


def ioc(letters):
    n = len(letters)
    return sum(v * (v - 1) for v in Counter(letters).values()) / (n * (n - 1))


secret = vigenere(SAMPLE, "lemon")
print("plain IoC: ", round(ioc([c for c in SAMPLE.lower() if c.isalpha()]), 4))
print("cipher IoC:", round(ioc(secret), 4))
for length in range(1, 8):
    columns = [secret[i::length] for i in range(length)]
    average = sum(ioc(col) for col in columns) / length
    print(length, round(average, 4))
```

```text
plain IoC:  0.0682
cipher IoC: 0.0416
1 0.0416
2 0.0412
3 0.0414
4 0.0414
5 0.0684
6 0.0404
7 0.0408
```

The ciphertext's IoC dropped to 0.042: the distribution flattened. But at
length 5 the column average suddenly rose to 0.068; the key `lemon` has
five letters. Once the length is known, each column is solved as a separate
Caesar cipher with chi-squared and the key's letters appear one by one.
Charles Babbage and Friedrich Kasiski did this by hand (with a different
method) in the 19th century.

## The lesson of this section

| Cipher | How it breaks | What was needed? |
|---|---|---|
| Caesar | Brute force | 26 tries |
| Substitution | Letter frequency + word patterns | A few hundred letters |
| Vigenère | Length with IoC, then chi-squared column by column | A few hundred letters |
| Rail fence | Trying row counts | A few tries |

What they all share: the ciphertext carries the **statistics** of the
plaintext. What we expect from a modern cipher is that, for someone who
does not know the key, the ciphertext is **indistinguishable from random**.
The first method to achieve this perfectly, the one-time pad, comes in the
next section.

## Summary

- **Brute force** is enough for a small key space; recognising the right
  key needs a measure (common words, chi-squared).
- **Letter frequency** is a language's fingerprint; Caesar and substitution
  do not change it.
- The shift with the lowest **chi-squared** is the right shift.
- The **index of coincidence** gives Vigenère's key length; then each
  column is a separate Caesar.
- The goal of a modern cipher: ciphertext indistinguishable from random.
