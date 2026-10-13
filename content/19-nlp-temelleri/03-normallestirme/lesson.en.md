# Normalisation and Stemming

After splitting we have a list of tokens, but many different tokens carry
the same meaning: "love", "loves", "loved", "loving". Each of them will be a
separate column for the model, and it will have to learn each of them
separately. **Normalisation** is the job of bringing these different forms
together. This section covers four tools: removing stop words, stemming,
reducing words to their dictionary form (lemmatisation) and turning variable
information into placeholders. Each has a price; half of the section is
about measuring those prices.

## Stop words

Words such as "the", "is" and "at" appear in every text and carry no topic
or feeling on their own. They are called **stop words**. scikit-learn gives
a ready-made English list:

```python
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

print(len(ENGLISH_STOP_WORDS))
print(sorted(ENGLISH_STOP_WORDS)[:8])
print([w for w in ["not", "no", "never", "nor", "very", "too"] if w in ENGLISH_STOP_WORDS])
tokens = "the fit is not good at all".split()
print([t for t in tokens if t not in ENGLISH_STOP_WORDS])
```

```text
318
['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against']
['not', 'no', 'never', 'nor', 'very', 'too']
['fit', 'good']
```

- The list has 318 words: "a", "about", "above"... all frequent words that
  look meaningless on their own.
- But **"not", "no", "never" and "nor"** are on the list, and so are "very"
  and "too". From "the fit is not good at all" only **"fit good"** is left:
  a negative review looks positive.

Let us measure what removing stop words gains on the reviews:

```python
import re
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_data import make_reviews

reviews = make_reviews(2000)
docs = [re.findall(r"[a-z]+", r["text"].lower()) for r in reviews]
words = Counter(w for d in docs for w in d)
kept = Counter(w for d in docs for w in d if w not in ENGLISH_STOP_WORDS)
print(len(words), sum(words.values()))
print(len(kept), sum(kept.values()))
```

```text
332 30798
298 16176
```

The first number is the count of distinct words, the second the total count
of words. Removing stop words cut the vocabulary from 332 to 298, but **half
of all the words** were gone (30,798 → 16,176). Stop words are few but very
frequent. Removing them is good for shortening and speeding things up; but
in sentiment analysis do not use the list without taking the negation and
intensity words out of it. TF-IDF, which we meet in the coming sections,
already lowers the weight of frequent words by itself; often no stop list is
needed at all.

## Stemming

**Stemming** cuts the suffixes off the end of a word by rules: "loves" →
"love", "batteries" → "battery". It uses no dictionary; it only looks at the
letters. Let us write our own simple stemmer:

```python
SUFFIX_RULES = [("ies", "y"), ("ing", ""), ("ed", ""), ("ly", ""), ("s", "")]


def stem(word):
    for suffix, replacement in SUFFIX_RULES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            if suffix == "s" and word.endswith("ss"):
                return word
            return word[: len(word) - len(suffix)] + replacement
    return word


for w in ["loves", "loved", "loving", "batteries", "quickly", "glass",
          "stopped", "news", "university", "universe", "running", "ran"]:
    print(w, "->", stem(w))
```

```text
loves -> love
loved -> lov
loving -> lov
batteries -> battery
quickly -> quick
glass -> glass
stopped -> stopp
news -> new
university -> university
universe -> universe
running -> runn
ran -> ran
```

- The rules are tried in order; the first matching suffix is cut. The
  condition that at least three letters remain protects words such as "is"
  and "as"; the "ss" rule protects "glass".
- **Inconsistent stems:** "loves" → "love" but "loved" and "loving" → "lov".
  Forms of the same word fell into two different stems. "stopped" → "stopp",
  "running" → "runn": the rule does not know about doubled consonants.
- **Over-stemming:** "news" → "new". News and new became the same token.
- **Under-stemming:** "ran" did not join "run"; no suffix rule can catch
  irregular verbs.

Real stemmers (the best known is the **Porter** algorithm, ready in nltk)
use dozens of rules and exceptions, but they have the same limits: they look
at letters, not at meaning. A stemmer's output is not always a real word
("lov", "univers"); that is fine, because what matters to a model is that the
forms of one word fall into the same token.

Its effect on this data:

```python
stems = Counter(stem(w) for d in docs for w in d if w not in ENGLISH_STOP_WORDS)
print(len(stems))
groups = {}
for w in kept:
    groups.setdefault(stem(w), []).append(w)
for s, ws in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:4]:
    print(s, sorted(ws))
```

```text
292
day ['day', 'days']
lvoe ['lvoe', 'lvoes']
love ['love', 'loves']
work ['working', 'works']
```

The vocabulary only went from 298 to 292: the generated reviews have few
inflected forms. In real reviews stemming usually shrinks the vocabulary
noticeably. The groups show what stemming joined; the misspelled "lvoe" and
"lvoes" joined each other, not the correct "love". Stemming does not fix
typos.

## Dictionary form (lemmatisation)

**Lemmatisation** reduces a word to its base form in the dictionary: "was" →
"be", "better" → "good", "mice" → "mouse". This is done not by rules but by a
**dictionary** and grammar:

```python
LEMMAS = {"was": "be", "were": "be", "is": "be", "better": "good", "best": "good",
          "ran": "run", "running": "run", "batteries": "battery", "mice": "mouse"}

for w in ["was", "better", "ran", "mice", "loves"]:
    print(w, "->", LEMMAS.get(w, w))
```

```text
was -> be
better -> good
ran -> run
mice -> mouse
loves -> loves
```

This small dictionary shows the idea; "loves", which is not in it, stayed as
it was. Real tools (spaCy, nltk's WordNet) use dictionaries of hundreds of
thousands of words and the word's role in the sentence (noun or verb): "saw"
is "see" as a verb and "saw" as a noun. Lemmatisation is more accurate than
stemming but slower, and it needs a resource for each language.

## Turkish: an agglutinative language

In Turkish many suffixes are added to a word one after another. An English
stemmer is no use for Turkish; the suffixes have to be cut again and again:

```python
SUFFIXES = ["imizden", "lerden", "lardan", "ler", "lar", "den", "dan", "de", "da"]


def turkish_root(word):
    changed = True
    while changed:
        changed = False
        for suffix in SUFFIXES:
            if word.endswith(suffix) and len(word) > len(suffix) + 1:
                word = word[: -len(suffix)]
                changed = True
                break
    return word


for w in ["evlerimizden", "kitaplardan", "okulda", "kalemler", "dede", "adalar"]:
    print(w, "->", turkish_root(w))
```

```text
evlerimizden -> ev
kitaplardan -> kitap
okulda -> okul
kalemler -> kalem
dede -> de
adalar -> ada
```

- "evlerimizden" ("from our houses") became "evler" by cutting "imizden",
  then "ev" (house) by cutting "ler": the loop runs until no suffix is left.
- **"dede" (grandfather) → "de"**: it was taken for the locative suffix
  "-de". When a word itself seems to end in a suffix, the rule goes wrong.
  "adalar" (islands) is right: "ada".
- Real tools for Turkish use **morphological analysers** that list every
  possible analysis of a word; the best known is Zemberek. The Snowball
  stemmers also have a Turkish version.

## Turning variable information into placeholders

In the support tickets every order number, amount and email was a separate
token (section 02). What matters to a model is the fact that "there is an
order number here", not the number itself. Let us replace the variable
information with a **placeholder**:

```python
import re
from text_data import make_tickets

RULES = [
    (r"[\w.+-]+@\w+\.\w+", "<email>"),
    (r"\$\d+(?:\.\d+)?", "<money>"),
    (r"[A-Z]+-\d+", "<order>"),
    (r"\d+", "<num>"),
]


def mask(text):
    for pattern, placeholder in RULES:
        text = re.sub(pattern, placeholder, text)
    return text


tickets = [t["text"] for t in make_tickets(2000)]
print(mask("Refund $12.50 for ORD-48213, mail ana12@example.com by 2026-03-14."))
before_ = {w for t in tickets for w in t.lower().split()}
after = {w for t in tickets for w in mask(t).lower().split()}
print(len(before_), len(after))
```

```text
Refund <money> for <order>, mail <email> by <num>-<num>-<num>.
1718 384
```

- The rules are applied **in order**: the digit rule comes last, otherwise
  the digits inside the amount and the order number would become `<num>`
  first and the pattern would no longer match.
- The date turned into three `<num>`s; if the date matters on its own, it
  gets a rule (and a `<date>`) too.
- The vocabulary fell **from 1718 to 384**. More than three quarters of the
  ticket "words" were numbers, amounts and addresses, each appearing in a
  single ticket.

## When not to normalise

Normalisation throws information away. The rule: **ask which differences
your task cares about.**

- In sentiment analysis "not", "never" and "very" matter; take them off the
  stop list.
- In topic discovery "running" and "run" are the same topic; stemming helps.
- In information extraction you need the order number itself; do not use a
  placeholder.
- Subword tokenisation (BPE) and the language models we meet in the second
  module do not need stemming; they learn suffixes and forms by themselves.

## Summary

- Normalisation joins different forms of the same meaning and shrinks the
  vocabulary.
- Ready-made stop lists also remove "not", "no" and "never"; in sentiment
  analysis that destroys negation.
- Stemming cuts suffixes by rules: fast, but it makes inconsistent stems,
  over-stemming and under-stemming mistakes.
- Lemmatisation finds the base form with a dictionary and grammar: more
  accurate, more expensive.
- In Turkish suffixes come one after another; a simple cutter turns "dede"
  into "de", and the real solution is a morphological analyser.
- Placeholders reduce variable information to a single token: the ticket
  vocabulary fell from 1718 to 384.
