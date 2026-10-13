# n-grams and Zipf's Law

Counting words one by one forgets their order: "not good" and "good not" end
up in the same bag, and the fact that "not" stood next to "good" is lost. An
**n-gram** is a run of n consecutive tokens; word pairs (bigrams) and triples
(trigrams) bring back part of that order. This section covers producing and
counting n-grams, their price (the vocabulary explosion), character n-grams,
words that appear together (collocations) and one of the most surprising
regularities of language, **Zipf's law**.

## Word pairs and triples

```python
tokens = "the fit is not good at all".split()
print(" | ".join(" ".join(b) for b in zip(tokens, tokens[1:])))
print(" | ".join(" ".join(t) for t in zip(tokens, tokens[1:], tokens[2:])))
```

```text
the fit | fit is | is not | not good | good at | at all
the fit is | fit is not | is not good | not good at | good at all
```

- `zip(tokens, tokens[1:])` pairs the list with a shifted copy of itself:
  every token forms a pair with the next one. Triples need two shifts.
- A text of n tokens gives n − 1 bigrams and n − 2 trigrams.
- "not good" is now one piece: the model sees "not good", not "good".

## Counting n-grams

Which word pairs are the most common in positive and negative reviews?

```python
import re
from collections import Counter
from text_data import make_reviews

reviews = make_reviews(2000)
docs = [re.findall(r"[a-z']+", r["text"].lower()) for r in reviews]
labels = [r["label"] for r in reviews]


def bigram_counts(label):
    pairs = Counter()
    for d, y in zip(docs, labels):
        if y == label:
            pairs.update(zip(d, d[1:]))
    return pairs


for label in ["positive", "negative"]:
    print(label)
    for (a, b), n in bigram_counts(label).most_common(4):
        print("  ", a, b, n)
```

```text
positive
   for the 499
   the money 264
   the price 263
   worth the 256
negative
   after days 89
   working after 87
   stopped working 82
   my old 80
```

Positive reviews bring "for the" and "worth the" to the top; negative ones
"stopped working" and "working after". The single words "working" or
"stopped" were ambiguous; as a pair their meaning is clear. "after days"
appeared because we dropped the digits ("after 23 days").

## The price: the vocabulary explosion

Every distinct n-gram is a new column in the model. In scikit-learn
`ngram_range=(1, 2)` produces single words and pairs together:

```python
from sklearn.feature_extraction.text import CountVectorizer

texts = [r["text"] for r in reviews]
for ngrams in [(1, 1), (1, 2), (1, 3)]:
    vectorizer = CountVectorizer(ngram_range=ngrams).fit(texts)
    print(ngrams, len(vectorizer.vocabulary_))
chars = CountVectorizer(analyzer="char_wb", ngram_range=(3, 3)).fit(texts)
print("char 3-gram", len(chars.vocabulary_))
```

```text
(1, 1) 350
(1, 2) 2737
(1, 3) 8960
char 3-gram 1300
```

350 columns with single words, 2737 once pairs are added, 8960 with
triples. The number of words stayed the same while the number of columns
grew 25 times. In real text the growth is much bigger; most pairs and
triples appear once or twice. That is why dropping the rare ones (`min_df`,
in the notes) is almost a must when you use n-grams.

## Character n-grams

n-grams can be built from letters too. `analyzer="char_wb"` splits each word
into letter triples after padding it with spaces at both ends. Let us write
our own version, marking the word border with `<` and `>`:

```python
def char_ngrams(word, n=3):
    padded = "<" + word + ">"
    return {padded[i:i + n] for i in range(len(padded) - n + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b)


print(sorted(char_ngrams("love")))
love = char_ngrams("love")
for w in ["loves", "lvoe", "glove", "hate"]:
    print(w, round(jaccard(love, char_ngrams(w)), 2))
love2, lvoe2 = char_ngrams("love", 2), char_ngrams("lvoe", 2)
print("lvoe n=2", round(jaccard(love2, lvoe2), 2))
```

```text
['<lo', 'lov', 'ove', 've>']
loves 0.5
lvoe 0.0
glove 0.5
hate 0.0
lvoe n=2 0.25
```

- **Jaccard similarity** is the share of two sets' common elements among all
  their elements: 1 is identical, 0 nothing in common.
- "loves" shares half of its pieces with "love": inflected forms stay close
  in character n-grams. That is one way to catch suffix differences partly,
  without stemming.
- But **the similarity with "lvoe" is 0**: swapping two letters broke every
  triple. With letter pairs the similarity rises to 0.25; short pieces cope
  better with typos but tell words apart less well.
- **"glove" is 0.5 too**: similar letters do not mean similar meaning.
  Character n-grams capture spelling, not meaning. For meaning we need the
  embeddings of the second module.

## Words that appear together: PMI

Some pairs, such as "bluetooth connection" or "customer service", appear
together far more often than chance. They are called **collocations**. The
most frequent pairs ("for the") are not collocations; they are just frequent
words standing side by side. The way to tell them apart is **PMI**
(pointwise mutual information): it compares how often the pair really
appears with how often it would appear if the two words were independent.

```python
import math

unigrams = Counter(w for d in docs for w in d)
bigrams = Counter(b for d in docs for b in zip(d, d[1:]))
n_uni, n_bi = sum(unigrams.values()), sum(bigrams.values())


def pmi(pair):
    together = bigrams[pair] / n_bi
    apart = (unigrams[pair[0]] / n_uni) * (unigrams[pair[1]] / n_uni)
    return math.log2(together / apart)


frequent = [b for b, c in bigrams.items() if c >= 20]
for pair in sorted(frequent, key=pmi, reverse=True)[:5]:
    print(" ".join(pair), bigrams[pair], round(pmi(pair), 2))
```

```text
broke on 27 10.2
on day 28 10.2
can't say 57 9.17
bluetooth connection 70 8.82
just perfect 22 8.82
```

- A PMI of 10 means the pair appears 2¹⁰ ≈ 1000 times more often than
  independence would predict.
- "bluetooth connection" and "brewing time" are real collocations. "broke
  on" and "on day" come from the data's template ("broke on day 5"). In real
  data, too, the top of a PMI list often points at a fixed phrase or a
  repeated sentence.
- The `c >= 20` condition matters: rare pairs seen once get an artificially
  high PMI.

## Zipf's law

If you sort the words of a text by frequency, the product of the position
(rank) and the frequency is roughly constant: the second word appears half
as often as the first, the tenth a tenth as often. This is called **Zipf's
law**; it shows up in almost every language and every kind of text. Let us
measure it on real English. We have a real English text offline: the
docstrings of Python's own standard library.

```python
import importlib
import inspect

import matplotlib.pyplot as plt
import numpy as np

MODULES = ["argparse", "collections", "csv", "datetime", "email", "functools",
           "http.client", "json", "logging", "os", "pathlib", "re", "statistics",
           "string", "textwrap", "threading", "typing", "unittest", "zipfile"]
docstrings = []
for name in MODULES:
    module = importlib.import_module(name)
    docstrings.append(module.__doc__ or "")
    for _, obj in sorted(inspect.getmembers(module), key=lambda kv: kv[0]):
        if inspect.isfunction(obj) or inspect.isclass(obj):
            doc = inspect.getdoc(obj)
            if isinstance(doc, str):
                docstrings.append(doc)


def rank_freq(texts):
    counts = Counter(w for t in texts for w in re.findall(r"[a-z']+", t.lower()))
    return np.array(sorted(counts.values(), reverse=True), dtype=float)


fig, ax = plt.subplots(figsize=(6.4, 3.6))
corpora = {"docstrings": docstrings, "reviews": [r["text"] for r in reviews]}
for name, texts in corpora.items():
    freqs = rank_freq(texts)
    ranks = np.arange(1, len(freqs) + 1)
    slope = np.polyfit(np.log(ranks), np.log(freqs), 1)[0]
    print(name, len(freqs), int(freqs.sum()), round(slope, 2))
    ax.loglog(ranks, freqs, label=f"{name} (slope {slope:.2f})")
ax.set_xlabel("rank")
ax.set_ylabel("frequency")
ax.legend()
```

```text
docstrings 2741 28771 -1.22
reviews 331 30741 -2.0
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="410.120781pt" height="246.787125pt" viewBox="0 0 410.120781 246.787125" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 246.787125 
L 410.120781 246.787125 
L 410.120781 0 
L 0 0 
L 0 246.787125 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 45.800781 206.784 
L 402.920781 206.784 
L 402.920781 7.2 
L 45.800781 7.2 
L 45.800781 206.784 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="62.033509" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <g style="fill: currentColor" transform="translate(53.233509 223.184)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">0</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="156.46723" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <g style="fill: currentColor" transform="translate(147.66723 223.084)">
       <text>
        <tspan x="0" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.892187" style="font-size: 7px; font-family:inherit; fill: currentColor">1</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="250.900952" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <g style="fill: currentColor" transform="translate(242.100952 223.184)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">2</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="345.334674" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <g style="fill: currentColor" transform="translate(336.534674 223.184)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">3</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <defs>
       <path id="m4926b1a248" d="M 0 0 
L 0 2 
" style="stroke: currentColor; stroke-width: 0.6"/>
      </defs>
      <g>
       <use xlink:href="#m4926b1a248" x="47.40554" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m4926b1a248" x="52.881935" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m4926b1a248" x="57.712458" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m4926b1a248" x="90.460891" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m4926b1a248" x="107.089844" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m4926b1a248" x="118.888274" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m4926b1a248" x="128.039847" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m4926b1a248" x="135.517227" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_13">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m4926b1a248" x="141.839262" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_14">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m4926b1a248" x="147.315657" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_15">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m4926b1a248" x="152.14618" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_16">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m4926b1a248" x="184.894613" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_17">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m4926b1a248" x="201.523566" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_18">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m4926b1a248" x="213.321996" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_19">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m4926b1a248" x="222.473569" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_20">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m4926b1a248" x="229.950949" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_21">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m4926b1a248" x="236.272984" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_22">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m4926b1a248" x="241.749379" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_23">
     <g id="line2d_23">
      <g>
       <use xlink:href="#m4926b1a248" x="246.579902" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_24">
     <g id="line2d_24">
      <g>
       <use xlink:href="#m4926b1a248" x="279.328335" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_25">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m4926b1a248" x="295.957288" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_26">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m4926b1a248" x="307.755718" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_27">
     <g id="line2d_27">
      <g>
       <use xlink:href="#m4926b1a248" x="316.907291" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_28">
     <g id="line2d_28">
      <g>
       <use xlink:href="#m4926b1a248" x="324.384671" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_29">
     <g id="line2d_29">
      <g>
       <use xlink:href="#m4926b1a248" x="330.706705" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_30">
     <g id="line2d_30">
      <g>
       <use xlink:href="#m4926b1a248" x="336.183101" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_31">
     <g id="line2d_31">
      <g>
       <use xlink:href="#m4926b1a248" x="341.013624" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_32">
     <g id="line2d_32">
      <g>
       <use xlink:href="#m4926b1a248" x="373.762057" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_33">
     <g id="line2d_33">
      <g>
       <use xlink:href="#m4926b1a248" x="390.39101" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="xtick_34">
     <g id="line2d_34">
      <g>
       <use xlink:href="#m4926b1a248" x="402.18944" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="text_5">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="224.360781" y="237.184781" transform="rotate(-0 224.360781 237.184781)">rank</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_35">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="45.800781" y="197.712" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <g style="fill: currentColor" transform="translate(21.200781 202.412)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">0</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_36">
      <g>
       <use xlink:href="#m5c8d5162d3" x="45.800781" y="146.715167" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <g style="fill: currentColor" transform="translate(21.200781 151.365167)">
       <text>
        <tspan x="0" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.892187" style="font-size: 7px; font-family:inherit; fill: currentColor">1</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_37">
      <g>
       <use xlink:href="#m5c8d5162d3" x="45.800781" y="95.718333" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <g style="fill: currentColor" transform="translate(21.200781 100.418333)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">2</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_38">
      <g>
       <use xlink:href="#m5c8d5162d3" x="45.800781" y="44.7215" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <g style="fill: currentColor" transform="translate(21.200781 49.4215)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">3</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_39">
      <defs>
       <path id="m0fd5f78bf4" d="M 0 0 
L -2 0 
" style="stroke: currentColor; stroke-width: 0.6"/>
      </defs>
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="205.611509" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_40">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="202.654104" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_41">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="200.045487" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_42">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="182.360423" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_43">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="173.380327" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_44">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="167.008847" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_45">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="162.066743" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_46">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="158.02875" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_47">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="154.614676" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_48">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="151.65727" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_15">
     <g id="line2d_49">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="149.048654" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_16">
     <g id="line2d_50">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="131.36359" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_17">
     <g id="line2d_51">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="122.383493" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_18">
     <g id="line2d_52">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="116.012013" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_19">
     <g id="line2d_53">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="111.06991" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_20">
     <g id="line2d_54">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="107.031917" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_21">
     <g id="line2d_55">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="103.617842" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_22">
     <g id="line2d_56">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="100.660437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_23">
     <g id="line2d_57">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="98.05182" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_24">
     <g id="line2d_58">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="80.366756" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_25">
     <g id="line2d_59">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="71.38666" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_26">
     <g id="line2d_60">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="65.01518" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_27">
     <g id="line2d_61">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="60.073076" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_28">
     <g id="line2d_62">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="56.035083" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_29">
     <g id="line2d_63">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="52.621009" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_30">
     <g id="line2d_64">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="49.663603" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_31">
     <g id="line2d_65">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="47.054987" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_32">
     <g id="line2d_66">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="29.369923" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_33">
     <g id="line2d_67">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="20.389826" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_34">
     <g id="line2d_68">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="14.018346" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_35">
     <g id="line2d_69">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="45.800781" y="9.076243" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="106.992" transform="rotate(-90 14.798438 106.992)">frequency</text>
    </g>
   </g>
   <g id="line2d_70">
    <path d="M 62.033509 33.403487 
L 90.460891 45.191553 
L 107.089844 54.675027 
L 118.888274 55.924621 
L 128.039847 56.183229 
L 135.517227 62.604311 
L 141.839262 62.803841 
L 152.14618 70.447141 
L 156.46723 72.290771 
L 160.376096 75.336239 
L 163.94461 75.336239 
L 167.227325 75.513421 
L 170.266645 76.144965 
L 173.096183 76.144965 
L 175.74304 77.175273 
L 178.22938 78.458124 
L 180.573563 78.972013 
L 182.79097 81.386521 
L 186.895598 81.502782 
L 188.803479 82.334159 
L 190.626536 83.966168 
L 192.371993 84.228273 
L 194.046186 84.761977 
L 197.202516 86.591075 
L 198.694027 86.591075 
L 200.133194 87.035525 
L 201.523566 87.035525 
L 202.868344 87.336858 
L 204.170423 87.95211 
L 206.656763 88.266266 
L 207.845601 89.236391 
L 209.000946 89.737868 
L 210.124634 90.424672 
L 211.218353 91.68034 
L 212.283661 92.24107 
L 213.321996 92.24107 
L 214.334691 92.43118 
L 215.32298 94.637746 
L 217.230861 95.497957 
L 218.152519 95.497957 
L 219.053919 96.392933 
L 219.935932 98.05182 
L 220.799376 98.549541 
L 221.645015 99.57985 
L 223.285715 100.113554 
L 225.629899 101.796462 
L 226.382435 102.387101 
L 227.12141 102.688434 
L 227.847306 103.617842 
L 230.628849 104.921021 
L 231.295727 104.921021 
L 231.951933 105.259159 
L 232.597806 105.259159 
L 233.233664 105.602541 
L 233.859814 105.602541 
L 234.476548 105.95133 
L 235.084145 105.95133 
L 235.682872 106.305699 
L 236.854724 106.305699 
L 237.428329 106.665832 
L 237.994021 106.665832 
L 238.552017 107.404155 
L 239.102522 107.782756 
L 240.181849 107.782756 
L 240.711044 108.167942 
L 241.233497 108.959014 
L 242.258852 108.959014 
L 243.750363 110.201263 
L 244.715397 110.201263 
L 245.18953 111.06991 
L 245.658244 111.06991 
L 246.121662 111.517352 
L 247.033078 111.517352 
L 247.481302 111.974021 
L 248.363315 111.974021 
L 249.226759 112.916616 
L 250.488767 112.916616 
L 250.900952 113.403397 
L 251.713098 113.403397 
L 252.509474 114.410281 
L 252.901937 114.410281 
L 253.290679 114.931426 
L 254.435276 114.931426 
L 254.809817 115.46513 
L 256.98796 115.46513 
L 257.339997 116.012013 
L 259.056232 116.012013 
L 259.391026 116.572743 
L 260.379316 116.572743 
L 260.703524 117.148039 
L 261.661047 117.148039 
L 262.287197 118.345501 
L 262.903931 118.345501 
L 263.208855 118.969419 
L 265.282107 118.969419 
L 265.569912 119.611425 
L 266.139533 119.611425 
L 266.421404 120.954117 
L 267.529905 120.954117 
L 267.802411 121.657276 
L 269.138427 121.657276 
L 269.400485 122.383493 
L 271.189456 122.383493 
L 271.43877 123.134333 
L 272.903642 123.134333 
L 273.14278 123.911523 
L 274.549045 123.911523 
L 274.778805 124.71698 
L 275.908685 124.71698 
L 276.130973 125.55284 
L 277.867192 125.55284 
L 278.079141 126.421486 
L 279.328335 126.421486 
L 279.532884 127.325597 
L 281.329319 127.325597 
L 281.524151 128.268192 
L 282.674097 128.268192 
L 282.862658 129.252694 
L 285.238185 129.252694 
L 285.415343 130.283003 
L 286.976243 130.283003 
L 287.146066 131.36359 
L 288.479908 131.36359 
L 288.643629 132.499616 
L 290.869635 132.499616 
L 291.024106 133.697077 
L 292.685964 133.697077 
L 292.833755 134.963001 
L 294.140444 134.963001 
L 294.283095 136.305694 
L 296.500502 136.305694 
L 296.635188 137.73507 
L 299.491611 137.73507 
L 299.616839 139.263099 
L 302.745373 139.263099 
L 302.861063 140.904416 
L 304.558356 140.904416 
L 304.779445 142.677174 
L 307.446968 142.677174 
L 307.653059 144.604271 
L 311.664583 144.604271 
L 311.850579 146.715167 
L 314.717216 146.715167 
L 314.889899 149.048654 
L 318.27852 149.048654 
L 318.436867 151.65727 
L 323.346336 151.65727 
L 323.486309 154.614676 
L 327.730433 154.614676 
L 327.856237 158.02875 
L 333.699965 158.02875 
L 333.863035 162.066743 
L 338.475987 162.066743 
L 338.621163 167.008847 
L 347.021989 167.008847 
L 347.139896 173.380327 
L 355.072609 173.380327 
L 355.201781 182.360423 
L 368.097748 182.360423 
L 368.215295 197.712 
L 386.688054 197.712 
L 386.688054 197.712 
" clip-path="url(#p09cc2e088b)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="line2d_71">
    <path d="M 62.033509 16.272 
L 90.460891 32.748958 
L 107.089844 47.005824 
L 118.888274 53.823744 
L 128.039847 55.961381 
L 135.517227 55.998201 
L 141.839262 56.332372 
L 147.315657 60.430304 
L 152.14618 62.406563 
L 156.46723 62.703852 
L 160.376096 64.253269 
L 163.94461 64.904718 
L 167.227325 67.410274 
L 173.096183 68.614591 
L 178.22938 69.141941 
L 180.573563 69.208751 
L 182.79097 69.682154 
L 184.894613 70.660443 
L 186.895598 70.875818 
L 188.803479 72.757054 
L 190.626536 73.233366 
L 195.654708 73.63827 
L 200.133194 75.336239 
L 204.170423 75.602546 
L 205.432431 75.962679 
L 212.283661 76.421238 
L 213.321996 76.795047 
L 214.334691 77.562142 
L 215.32298 78.155418 
L 216.288014 78.155418 
L 217.230861 78.356761 
L 218.152519 78.765024 
L 219.053919 79.712099 
L 219.935932 79.712099 
L 220.799376 80.814199 
L 221.645015 81.270867 
L 222.473569 82.947706 
L 223.285715 83.836269 
L 224.082091 84.228273 
L 224.863296 84.761977 
L 225.629899 85.86959 
L 226.382435 85.86959 
L 227.12141 86.444886 
L 227.847306 86.444886 
L 228.560577 86.886382 
L 229.261655 88.266266 
L 229.950949 88.425031 
L 231.295727 89.569444 
L 231.951933 89.907583 
L 232.597806 91.314255 
L 233.859814 91.68034 
L 234.476548 92.052578 
L 235.084145 92.052578 
L 235.682872 93.0115 
L 236.854724 93.407005 
L 237.428329 94.637746 
L 237.994021 94.849687 
L 238.552017 94.849687 
L 239.102522 95.279752 
L 239.645736 95.497957 
L 240.181849 96.392933 
L 240.711044 96.854359 
L 241.233497 96.854359 
L 241.749379 97.088727 
L 242.762073 97.088727 
L 243.259195 97.325603 
L 244.235719 97.325603 
L 245.18953 97.807092 
L 246.579902 97.807092 
L 247.033078 98.05182 
L 247.92468 98.05182 
L 248.797309 99.058705 
L 249.226759 99.058705 
L 249.651758 99.845094 
L 250.900952 99.845094 
L 251.309036 100.385307 
L 251.713098 100.660437 
L 252.113219 100.660437 
L 252.509474 100.939027 
L 253.675772 100.939027 
L 254.057282 101.221167 
L 254.435276 101.221167 
L 254.809817 101.506947 
L 255.18097 101.506947 
L 255.913347 102.089813 
L 256.274689 102.688434 
L 257.339997 102.688434 
L 257.689038 102.993924 
L 258.035133 102.993924 
L 258.378332 103.617842 
L 259.056232 103.617842 
L 259.391026 103.936519 
L 259.72311 103.936519 
L 260.052525 104.587967 
L 260.703524 104.587967 
L 261.025189 104.921021 
L 261.34435 104.921021 
L 261.661047 105.259159 
L 262.287197 105.259159 
L 262.596724 105.95133 
L 262.903931 106.305699 
L 263.208855 106.305699 
L 263.511528 106.665832 
L 263.811984 106.665832 
L 264.110255 107.031917 
L 264.406372 107.031917 
L 264.700366 108.167942 
L 265.282107 108.167942 
L 265.569912 108.559946 
L 265.855712 108.559946 
L 266.139533 109.365404 
L 266.421404 109.365404 
L 266.9794 110.201263 
L 267.255576 110.201263 
L 267.529905 110.631328 
L 267.802411 110.631328 
L 268.342051 111.517352 
L 268.609232 112.440304 
L 268.874683 116.012013 
L 269.138427 116.012013 
L 269.400485 116.572743 
L 270.432289 123.134333 
L 270.686235 123.134333 
L 270.938617 123.911523 
L 271.189456 123.911523 
L 271.43877 124.71698 
L 271.686578 129.252694 
L 271.932897 129.252694 
L 272.903642 137.73507 
L 273.380532 144.604271 
L 273.616913 144.604271 
L 273.85194 146.715167 
L 274.085627 146.715167 
L 274.317991 151.65727 
L 275.007285 151.65727 
L 275.234499 154.614676 
L 275.908685 154.614676 
L 276.130973 158.02875 
L 276.352063 158.02875 
L 276.571967 162.066743 
L 277.654142 162.066743 
L 277.867192 167.008847 
L 279.12276 167.008847 
L 279.328335 173.380327 
L 280.739208 173.380327 
L 280.936857 182.360423 
L 287.146066 182.360423 
L 287.315188 197.712 
L 299.990244 197.712 
L 299.990244 197.712 
" clip-path="url(#p09cc2e088b)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 45.800781 206.784 
L 45.800781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 402.920781 206.784 
L 402.920781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 45.800781 206.784 
L 402.920781 206.784 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 45.800781 7.2 
L 402.920781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 245.400469 45.201562 
L 395.920781 45.201562 
Q 397.920781 45.201562 397.920781 43.201562 
L 397.920781 14.2 
Q 397.920781 12.2 395.920781 12.2 
L 245.400469 12.2 
Q 243.400469 12.2 243.400469 14.2 
L 243.400469 43.201562 
Q 243.400469 45.201562 245.400469 45.201562 
L 245.400469 45.201562 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_72">
     <path d="M 247.400469 20.298437 
L 257.400469 20.298437 
L 267.400469 20.298437 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_11">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="275.400469" y="23.798437" transform="rotate(-0 275.400469 23.798437)">docstrings (slope -1.22)</text>
    </g>
    <g id="line2d_73">
     <path d="M 247.400469 35.299219 
L 257.400469 35.299219 
L 267.400469 35.299219 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="275.400469" y="38.799219" transform="rotate(-0 275.400469 38.799219)">reviews (slope -2.00)</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p09cc2e088b">
   <rect x="45.800781" y="7.2" width="357.12" height="199.584"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Rank and frequency on a double logarithmic axis. Python's docstrings (real English) form a line with a slope near −1; the generated reviews drop suddenly with their small vocabulary.</figcaption>
</figure>

- `inspect.getdoc` gives the docstring of a function or a class. In total a
  real English text of 28,771 words.
- On a double logarithmic axis (`loglog`) Zipf's law shows up as a **straight
  line**; its slope is about −1. For the docstrings the slope is −1.22.
- The slope of our generated reviews is −2: the vocabulary is small (331
  words) and the tail drops suddenly. In this respect the generated data
  **does not look like** real language: real language has far more rare
  words. In this path we train models on generated data; on real data the
  vocabulary will be much bigger and sparser.

Let us look at the product of rank and frequency:

```python
freqs = rank_freq(docstrings)
for rank in [1, 2, 5, 10, 50, 100, 500, 1000]:
    print(rank, int(freqs[rank - 1]), int(rank * freqs[rank - 1]))
print(int((freqs == 1).sum()), len(freqs))
```

```text
1 1667 1667
2 979 1958
5 596 2980
10 288 2880
50 83 4150
100 45 4500
500 9 4500
1000 4 4000
999 2741
```

- From rank 5 to rank 1000 the product stays between 3000 and 4500:
  frequency is roughly inversely proportional to rank. The first few words
  ("the", "a") stray a little from the law; that is usual in real texts too.
- The last line: **999 of the 2741 distinct words appear only once** (36%).
  They are called **hapax legomena** ("said once"). A third of the
  vocabulary is a single example; a model can learn almost nothing about
  these words.

What Zipf's law means for NLP: a few words make up most of a text, while
most words are rare. When we turn text into numbers (05), most of the table
will be zero, that is, **sparse**.

## Summary

- An n-gram is n consecutive tokens; word pairs bring back order information
  such as "not good". They are produced with `zip(tokens, tokens[1:])`.
- The price is the vocabulary explosion: 350 columns with single words, 2737
  with pairs, 8960 with triples. Rare n-grams have to be dropped.
- Character n-grams catch suffix differences, but swapped letters break the
  triples; similar spelling does not mean similar meaning ("glove").
- PMI finds words that appear together; leave rare pairs out.
- Zipf's law: frequency is inversely proportional to rank. In real text a
  third of the words appear once; our generated data does not look like real
  language in this respect.
