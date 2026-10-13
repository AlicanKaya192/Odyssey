# Introduction to NLP

Most of the data you have worked with so far was a table: each row an
example, each column a number or a category. Yet most of the world's data is
**text**: product reviews, support tickets, emails, news, contracts, chat
logs. **Natural Language Processing** (**NLP**) is the name for the methods
that let a computer work with that text. This section shows why text is hard
data, which questions NLP answers and the data we will use throughout the
path; at the end we measure how badly a simple rule of our own works and see
why this path exists.

## Why is text hard data?

In a table the "price" column is a number; comparing 49.99 with 59.99 is
easy. Text has no such ready-made columns. Whether a review is positive or
negative is not written in any column; it is buried in the words. On top of
that:

- **Same meaning, different spelling.** "Great", "really good" and "loved
  it" say the same thing but share almost no letters.
- **Same spelling, different meaning.** *Bank* is a financial institution
  and the side of a river. The **context** (the words around it) decides.
- **Negation.** "Not bad" is a positive sentence, yet it contains "bad".
- **Sarcasm.** "Great, it broke on day two." A positive word says something
  negative.
- **Typos and formatting.** "graet", "GREAT!!!" and "great." should all be
  the same word, but for a computer they are three different strings.
- **The language itself.** Turkish is **agglutinative**: "evlerimizden" is
  one word that holds "house", the plural, "our" and "from". English needs
  four words for it ("from our houses").

A computer, though, can only calculate with numbers. So the core job of NLP
is this: **turn text into numbers while keeping as much of its meaning as
possible**, and make decisions with those numbers.

<figure class="fig">
  <div class="flow">
    <span class="node acc">Text<br><code>"Not bad!"</code></span>
    <span class="arrow">→</span>
    <span class="node">Clean</span>
    <span class="arrow">→</span>
    <span class="node">Split</span>
    <span class="arrow">→</span>
    <span class="node">To numbers</span>
    <span class="arrow">→</span>
    <span class="node ok">Model<br><b>positive</b></span>
  </div>
  <figcaption>Almost every NLP system goes through these steps; the path covers each of them in turn.</figcaption>
</figure>

## Which questions does NLP answer?

| Task | Question | Example | In this path |
|---|---|---|---|
| Classification | Which group does this text belong to? | Is the review positive, which team should get the ticket? | NLP Fundamentals 08–11 |
| Search | Which document is closest to this question? | Searching help articles | NLP Fundamentals 07 |
| Information extraction | Which date, amount or order is in the text? | Finding the number "ORD-48213" | NLP Fundamentals 14 |
| Topic discovery | What are these thousands of texts about? | The main themes of tickets | NLP Fundamentals 12–13 |
| Tagging | What role does each word play? | Noun or verb? | Embeddings and Language Models 07 |
| Language modelling | What could the next word be? | Autocomplete | Embeddings and Language Models 06, 13 |

Tasks like translation, summarisation and question answering are built on
these foundations; at the end of the second module we look conceptually at
how large language models do them.

## Two approaches: rules and learning

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>RULE-BASED</h5>
<pre><code>if "refund" in text:
    team = "refunds"</code></pre>
      <p>Written by an expert. Easy to read, but every new phrase needs a new rule.</p>
    </div>
    <div class="ok">
      <h5>LEARNING</h5>
<pre><code>model.fit(texts, labels)
model.predict(new_texts)</code></pre>
      <p>Learns from labelled examples. Needs data, catches similar phrases by itself.</p>
    </div>
  </div>
  <figcaption>The two are not rivals: rules for information with an exact format, a learning model for meaning and tone.</figcaption>
</figure>

The first NLP systems were **rule-based**: an expert wrote rules by hand,
such as "a ticket containing *refund* goes to the refunds team". Rules are
easy to understand and fast, but language is so varied that the list of
rules never ends. Most systems today **learn**: instead of writing rules by
hand we train a model on **labelled examples** (a text plus the correct
answer). In this path we write both; at the end of this section we see in
numbers why rules are not enough.

## Our data set

The texts we use throughout the path come from the file `text_data.py`. It
downloads nothing from the internet; it generates product reviews and
support tickets from a **fixed seed**. So the same texts come out on your
computer and on mine, and the numbers in the lessons match yours exactly.
The texts are in English: in real projects most data is English too, and
the exercise code then needs no special characters. Problems specific to
Turkish get their own headings.

```python
from collections import Counter
from text_data import make_reviews

reviews = make_reviews(2000)
print(len(reviews))
for key, value in reviews[0].items():
    print(key, "=", value)
print(Counter(r["label"] for r in reviews))
```

```text
2000
id = 1
product = sports watch
text = Not bad for the price. The weight is not fragile at all.
rating = 5
label = positive
Counter({'positive': 1318, 'negative': 393, 'neutral': 289})
```

- `make_reviews(2000)` gives 2000 reviews; each is a dictionary: `id`,
  `product`, `text` (the review itself), `rating` (1–5 stars) and `label`.
- The label comes from the stars: 4–5 stars `positive`, 3 stars `neutral`,
  1–2 stars `negative`.
- The distribution is **imbalanced**: 1318 reviews are positive, only 289
  neutral. In real shops, too, people mostly write reviews when they are
  happy.
- Look at the first review: "Not bad for the price". It contains *bad*, yet
  its label is positive. We come back to this sentence shortly.

`make_tickets` generates support tickets the same way; we use them in later
sections.

## A first look: lengths and words

Looking at the data before any model is always the first job. Two simple
questions: how long are the reviews and which words are the most common?

```python
from collections import Counter
from text_data import make_reviews

reviews = make_reviews(2000)
for label in ["positive", "neutral", "negative"]:
    lengths = [len(r["text"].split()) for r in reviews if r["label"] == label]
    print(label, round(sum(lengths) / len(lengths), 1), min(lengths), max(lengths))

words = Counter()
for r in reviews:
    for w in r["text"].lower().split():
        words[w.strip(".,!?")] += 1
print(len(words))
print(" ".join(f"{w}:{c}" for w, c in words.most_common(8)))
```

```text
positive 15.4 4 40
neutral 15.9 4 34
negative 16.1 3 38
360
the:3613 is:1717 i:902 for:663 it:602 not:601 my:592 but:492
```

- `text.split()` splits the text at spaces; each piece is roughly a word.
  This job is called **tokenisation**; in section 02 we see why `split` is
  not enough.
- Reviews average 15–16 words; the length does not give the label away.
- `lower()` lowercases the text and `strip(".,!?")` removes punctuation at
  the start and end of a word. Without them "Great", "great" and "great!"
  would count as three different words.
- The most common words are "the", "is", "i", "for": words that carry no
  meaning and appear in every text. They are called **stop words**; the
  topic of section 03.
- "not" appears 601 times. Negation is very common in this data; every
  method based on counting words will have to deal with it.

## A first classifier: hand-written rules

Now let us write the simplest program that predicts a review's label: count
the positive words and the negative words, and whichever is larger wins.

```python
from text_data import make_reviews

GOOD = {"good", "great", "excellent", "perfect",
        "love", "worth", "fantastic", "comfortable"}
BAD = {"bad", "terrible", "awful", "broke",
       "hate", "waste", "poor", "useless"}


def predict(text):
    words = [w.strip(".,!?") for w in text.lower().split()]
    score = sum(w in GOOD for w in words) - sum(w in BAD for w in words)
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


reviews = make_reviews(2000)
hits = sum(predict(r["text"]) == r["label"] for r in reviews)
print(hits, len(reviews), round(hits / len(reviews), 3))
print(round(sum(r["label"] == "positive" for r in reviews) / len(reviews), 3))
```

```text
898 2000 0.449
0.659
```

- `sum(w in GOOD for w in words)` gives `True`/`False` for each word; `sum`
  counts each `True` as 1. That is how many positive words appear.
- The rule is right on 898 of the 2000 reviews: an **accuracy** of 44.9%.
- The second line is more striking: calling **every review "positive"**
  without looking at it gives 65.9% accuracy. Our hand-written rule is
  worse than this prediction that does nothing.

This lazy prediction that always says the most frequent class is called a
**baseline**. The first way to tell whether a model is any good is to
compare it with the baseline. On imbalanced data the baseline can be
surprisingly high; a model that does not beat 65.9% has learned nothing.

## Where do the rules go wrong?

```python
import textwrap

wrong = [r for r in reviews if predict(r["text"]) != r["label"]]
print(len(wrong))
for r in wrong[:5]:
    print(r["label"], "->", predict(r["text"]))
    print(textwrap.fill(r["text"], 60, initial_indent="  ", subsequent_indent="  "))
```

```text
1102
positive -> negative
  Not bad for the price. The weight is not fragile at all.
positive -> neutral
  It does the job. Much better tahn my old office chair.
negative -> neutral
  i would not buy this sports watch again.
positive -> neutral
  I lvoe the armrests. Much better than my old office chair.
  Exactly what I needed. My daughter loves it too. Exactly
  what I needed.
positive -> neutral
  Not flimsy for the price.
```

`textwrap.fill` breaks the long text into lines of 60 characters, indented
by two spaces; only to make it readable. Each of the five mistakes shows a
different problem:

1. **Negation:** "Not bad" and "not fragile" are positive, but the rule saw
   *bad* and said negative.
2. **A word not on the list:** "It does the job" and "Much better" are
   positive phrases, but they are not on our list; the score stayed at 0
   and the rule said neutral.
3. **Negation in a verb:** "would not buy" is negative, but it contains no
   word from the lists.
4. **Typos and inflection:** "lvoe" and "loves" did not match "love" on the
   list.
5. **An incomplete list:** "Not flimsy" is positive, but "flimsy" is not
   even on the list.

You can fix some of these by adding words to the lists, but every added word
brings a new exception (add "not" and you catch "not worth" but miss "not
bad"). The rest of this path is made of answers to this problem: cleaning
and splitting text properly, turning words into numbers systematically and
**learning from data** instead of writing rules by hand. In section 09 you
will see a learning model reach about 90% on the same reviews.

## The map of this path

- **NLP Fundamentals** (this module): cleaning, splitting and turning text
  into numbers (bag of words, TF-IDF), search, classification, sentiment
  analysis, topic modelling, information extraction and finally a support
  ticket classifier built end to end. Tools: Python, NumPy, scikit-learn.
- **Embeddings and Language Models**: vectors that capture the meaning of
  words, subword tokenisation, language models that predict the next word,
  attention and the transformer. We write all of them from scratch with
  NumPy, on small examples.

## Summary

- NLP turns text into numbers while keeping its meaning, and makes decisions
  with them.
- Text is hard: the same meaning is spelled differently, the same spelling
  means different things, negation and sarcasm fool word counting.
- Always compare a model with a **baseline** first. On imbalanced data even
  always saying the majority gives high accuracy.
- Hand-written rules are easy to understand but cannot keep up with the
  variety of language; on this data they stayed at 44.9%, below the baseline
  (65.9%).
