# RAG: Retrieval-Augmented Generation

In the previous section we learnt to find the chunks most relevant to a
question. **RAG** (retrieval-augmented generation) gives these chunks to the
model and asks it to **base** its answer on them. The setup has four steps:

<figure class="fig">
  <div class="flow">
    <span class="node">Question</span>
    <span class="arrow">→</span>
    <span class="node acc">Search</span>
    <span class="arrow">→</span>
    <span class="node">Chunks + question</span>
    <span class="arrow">→</span>
    <span class="node acc">Model</span>
    <span class="arrow">→</span>
    <span class="node ok">Answer + source</span>
  </div>
  <figcaption>The chunks most relevant to the question are found, numbered and given to the model with the question; the model bases its answer on these chunks and writes the source number.</figcaption>
</figure>

Our documents speak instead of the model's general knowledge: the information
can be kept up to date, sources can be shown and the answer can be checked
against the document (08).

## Building the prompt

The chunking and search code from 09 is in the file `retrieval.py`. We split
the chunks sentence by sentence. We number the chunks found and put them in
the user message; the system message tells the model its rules: answer only
from the sources, write the source number, and say so if there is no answer.

```python
import re
from retrieval import Index, by_sentence, QUESTIONS
from llm_client import ChatClient

index = Index(by_sentence())
NOT_FOUND = "I could not find this in the sources."
SYSTEM = ("Answer only from the numbered sources. Cite the source number "
          "like [2]. If the sources do not contain the answer, reply: "
          + NOT_FOUND)


def build_messages(question, found):
    sources = "\n".join(f"[{i}] {text}"
                        for i, ((_, text), _) in enumerate(found, 1))
    user = f"Sources:\n{sources}\n\nQuestion: {question}"
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": user}]


question = "Do gift cards expire?"
messages = build_messages(question, index.search(question, 3))
print(messages[1]["content"])
```

```text
Sources:
[1] Gift cards are available for 25, 50 and 100 euros and are valid for 3 years.
[2] Purchases paid with a gift card are refunded as a new gift card.
[3] Points expire if you make no purchase for 12 months.

Question: Do gift cards expire?
```

## An example reader instead of a model

A real model would read this message and write an answer in its own words.
Since the program is offline, we give `ChatClient` an **example reader**
function as the reply: from the sentences in the sources it picks the one that
shares the most words with the question and returns it with its number; if the
number of shared words is below a threshold it says "not found". It is far
cruder than a real model; its purpose is not to replace the model but to
**run and measure** the rest of the setup (search, prompt, sources,
abstaining).

```python
import textwrap

STOP = {"the", "a", "an", "is", "are", "do", "does", "i", "my", "you",
        "to", "of", "in", "for", "can", "how", "what", "when", "it", "on",
        "and", "or", "will", "if", "be", "me", "we", "your", "with", "at",
        "much", "long", "many"}


def words(text):
    found = re.findall(r"[a-z0-9]+(?:[.:][0-9]+)?", text.lower())
    return {w for w in found if w not in STOP}


def make_reader(min_overlap):
    def reader(messages):
        user = messages[-1]["content"]
        question = user.split("Question: ")[-1]
        best, best_overlap = NOT_FOUND, 0
        for n, source in re.findall(r"\[(\d+)\] (.+)", user):
            overlap = len(words(question) & words(source))
            if overlap > best_overlap:
                best, best_overlap = f"{source} [{n}]", overlap
        return best if best_overlap >= min_overlap else NOT_FOUND
    return reader


def rag(question, k=3, min_overlap=2):
    found = index.search(question, k) if k else []
    client = ChatClient([make_reader(min_overlap)])
    return client.chat(build_messages(question, found), max_tokens=100)


def show(question, answer):
    print(question)
    print(textwrap.fill(answer, 66, initial_indent="    ",
                        subsequent_indent="    "))


for q in ["Do gift cards expire?", "Is the store open on Sunday?",
          "Do you sell bicycles?"]:
    show(q, rag(q).text)
```

```text
Do gift cards expire?
    Gift cards are available for 25, 50 and 100 euros and are
    valid for 3 years. [1]
Is the store open on Sunday?
    Our store is open Monday to Saturday, 10:00 to 19:00, and
    closed on Sundays and public holidays. [1]
Do you sell bicycles?
    I could not find this in the sources.
```

The answers come from the sources with their numbers; for the bicycle
question, which is not in the documents, the system says "not found".

## Without and with sources

Let us ask all 27 questions in three ways: without any source (`k=0`) and
with 3 sources at two different thresholds. We put every answer into one of
four groups: **correct** (the answer phrase is there), **abstain ok** ("not
found" for a question with no answer), **wrong** (it answered but the phrase is
missing, or it answered a question with no answer), **missed** ("not found" for
a question that has an answer).

```python
def evaluate(k, min_overlap):
    counts = {"correct": 0, "abstain ok": 0, "wrong": 0, "missed": 0}
    tokens = 0
    for q in QUESTIONS:
        reply = rag(q["q"], k, min_overlap)
        tokens += reply.input_tokens
        if q["key"] is None:
            group = "abstain ok" if reply.text == NOT_FOUND else "wrong"
        elif reply.text == NOT_FOUND:
            group = "missed"
        else:
            group = "correct" if q["key"] in reply.text else "wrong"
        counts[group] += 1
    return counts, round(tokens / len(QUESTIONS))


for k, min_overlap in [(0, 2), (3, 2), (3, 1)]:
    print(f"k={k} overlap>={min_overlap}", *evaluate(k, min_overlap))
```

```text
k=0 overlap>=2 {'correct': 0, 'abstain ok': 3, 'wrong': 0, 'missed': 24} 74
k=3 overlap>=2 {'correct': 15, 'abstain ok': 3, 'wrong': 2, 'missed': 7} 132
k=3 overlap>=1 {'correct': 17, 'abstain ok': 1, 'wrong': 7, 'missed': 2} 132
```

Without sources the setup misses all 24 questions: the reader has no text to
rest on. (A real model would write some answer without sources too, but from
its general knowledge; it could not know this shop's rules.) With 3 sources
and threshold 2, 15 of the 24 questions are correct, all three questions with
no answer get "not found" and only 2 answers are wrong; but 7 questions are
missed. Lowering the threshold to 1 raises the correct answers to 17 and
brings the missed ones down to 2; in exchange the wrong answers rise to 7 and
two of the questions with no answer get an answer too. Which is better depends
on the application: where a wrong answer is costly (money, health, law) the
higher threshold is chosen. The sources add 58 tokens to every call on average
(74 → 132).

## What goes wrong?

```python
for q in QUESTIONS:
    reply = rag(q["q"], 3, 1)
    if q["key"] is None or q["key"] not in reply.text:
        show(q["q"], reply.text)
```

```text
How much does shipping cost for a 30 euro order?
    Shipping costs are refunded only if you return the whole
    order. [1]
Can I return boots I wore on a hike?
    Brush off dried mud after every hike. [1]
How long do I have to send something back?
    To make a claim, send a photo of the damage and your order
    number. [1]
When will I get my money back?
    I could not find this in the sources.
How long is the warranty on a tent zipper?
    Store the tent loosely, not tightly packed. [1]
How much does it cost to fix a broken zip after the warranty?
    We repair broken zips for free while the product is under
    warranty. [1]
Do you deliver to Canada?
    I could not find this in the sources.
Do you sell bicycles?
    I could not find this in the sources.
In which year was the shop founded?
    Wash down sleeping bags at most twice a year at 30 degrees
    with a special down detergent. [1]
Can I pick up my order in the store?
    Shipping costs are refunded only if you return the whole
    order. [1]
```

The errors are of two kinds. **Wrong retrieval:** the search does not find the
right sentence; "send something back" and "money back" run into the word
mismatch we saw in 09. **Misusing what was retrieved:** the reader is fooled
by a single shared word; "In which year was the shop founded?" is tied to the
sleeping-bag washing sentence because of the word "year", and "Can I pick up
my order in the store?" to the sentence about refunding shipping costs because
of "order". A real model is not as crude as this reader; but these two kinds of
error are also seen in real RAG systems. The next section measures them
separately.

## In real RAG systems

- **Search quality comes first.** The model cannot use information in a chunk
  it was not given. Measure the search first (09), then the answer.
- **The system message** explicitly asks to tie the answer to the sources, to
  cite them and to say "not found"; but it is not assumed that the model will
  always follow it, the answer is checked (08).
- **The number of sources** is a trade-off: many chunks bring tokens and cost,
  and unrelated chunks can mislead the model; few chunks can miss the
  information.
- **Freshness:** when a document changes only that document's chunks are
  turned into vectors again; the model does not need retraining.

## Summary

- RAG: find the chunks relevant to the question, number them and put them in
  the prompt, ask the model to answer based only on them and to cite them,
  and check the answer.
- The setup without sources could not answer any question; the setup with
  sources did.
- The abstain threshold is a trade-off: a low threshold gives more correct but
  also more wrong answers, a high one fewer wrong answers but more misses.
- The reader in this section is a crude example standing in for a real model;
  the numbers show how the setup behaves, not how good a model is.
