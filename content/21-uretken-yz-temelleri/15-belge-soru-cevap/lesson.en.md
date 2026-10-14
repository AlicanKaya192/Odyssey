# Capstone: A Document Q&A System

In this section we put the pieces of the module's LLM part together in a
single system: a **document Q&A** system that answers questions from the
shop's help articles. Every step rests on a technique we saw separately
before:

<figure class="fig">
  <div class="flow">
    <span class="node">Mask</span>
    <span class="arrow">→</span>
    <span class="node acc">Two-stage search</span>
    <span class="arrow">→</span>
    <span class="node">Prompt + budget</span>
    <span class="arrow">→</span>
    <span class="node acc">Reader</span>
    <span class="arrow">→</span>
    <span class="node">Verify + log</span>
  </div>
  <figcaption>The question is masked first; the sentences of the most relevant article go into the prompt as far as the budget allows; the answer is verified against the source and logged with its cost.</figcaption>
</figure>

We will build the system first and then compare it with the basic setup from 10
on the same 27 questions. Instead of a model, the **example reader** from 10 is
working again; what we measure is the system around it.

## The pieces

The function that masks personal data (14) and a **two-stage search**: first we
find the question's most relevant article (article-level search was 100%
accurate within the first three in 09), then we give only that article's
sentences as sources. The sources do not exceed a token budget (07).

```python
import re
import textwrap
from retrieval import Index, by_article, by_sentence, QUESTIONS
from rag_tools import build_messages, make_reader, NOT_FOUND, rag
from llm_client import ChatClient, count_tokens

PATTERNS = {"EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
            "PHONE": r"\+?\(?\d[\d\s()-]{8,}\d",
            "ORDER": r"ORD-\d{5}"}


def mask(text):
    for label, pattern in PATTERNS.items():
        text = re.sub(pattern, f"[{label}]", text)
    return text


articles = Index(by_article())
SENTENCES = by_sentence()


def find_sources(question, budget=150):
    (doc, _), score = articles.search(question, 1)[0]
    sources, used = [], 0
    for d, sentence in SENTENCES:
        cost = count_tokens(sentence)
        if d == doc and used + cost <= budget:
            sources.append(((d, sentence), score))
            used += cost
    return sources


for (doc, text), _ in find_sources("Do gift cards expire?"):
    print(text)
```

```text
Gift cards are available for 25, 50 and 100 euros and are valid for 3 years.
They cannot be exchanged for cash.
You can use one gift card and one discount code per order.
```

## Verification

After the model writes the answer we check two things (08): does the source
number in the answer really exist, and do the answer's numbers appear in that
source?

```python
def verify(answer, sources):
    if answer == NOT_FOUND:
        return True
    cite = re.search(r"\[(\d+)\]", answer)
    if not cite or not 1 <= int(cite.group(1)) <= len(sources):
        return False
    source = sources[int(cite.group(1)) - 1][0][1]
    claims = re.findall(r"\d+", answer.replace(cite.group(0), ""))
    return all(c in re.findall(r"\d+", source) for c in claims)
```

## The system

```python
class DocQA:
    PRICE_IN, PRICE_OUT = 0.50, 1.50

    def __init__(self, min_overlap=2):
        self.min_overlap = min_overlap
        self.log = []

    def answer(self, question, reply=None):
        question = mask(question)
        sources = find_sources(question)
        client = ChatClient([reply or make_reader(self.min_overlap)])
        result = client.chat(build_messages(question, sources),
                             max_tokens=100)
        ok = verify(result.text, sources)
        text = result.text if ok else NOT_FOUND
        cost = (result.input_tokens * self.PRICE_IN
                + result.output_tokens * self.PRICE_OUT) / 1_000_000
        self.log.append({"question": question, "verified": ok,
                         "tokens": result.input_tokens, "cost": cost})
        return text


qa = DocQA()
for q in ["Do gift cards expire?",
          "I am ana@example.com, can I return worn boots?",
          "Do you sell bicycles?"]:
    print(textwrap.fill(qa.answer(q), 70))
print(qa.log[1]["question"])
```

```text
Gift cards are available for 25, 50 and 100 euros and are valid for 3
years. [1]
Boots that have been worn outdoors cannot be returned, so please try
them on indoors first. [5]
I could not find this in the sources.
I am [EMAIL], can I return worn boots?
```

In the second question the email address was masked before the search and the
log; the log shows `[EMAIL]`.

## Does verification work?

The example reader copies the sentence as it is, so it never writes a wrong
number. To test the verification, instead of the reader we give a **recorded
reply** containing a wrong number (the kind of error a model can make):

```python
wrong = "Gift cards are valid for 5 years. [1]"
print(qa.answer("Do gift cards expire?", reply=wrong))
print("verified:", qa.log[-1]["verified"])
```

```text
I could not find this in the sources.
verified: False
```

The source says "3 years"; "5" is not there. The verification rejected the
answer, and instead of a made-up period the user got "not found".

## Comparison with the basic setup

Let us measure the setup from 10 (`rag`: sentence-level search, 3 sources) and
the capstone system on the same 27 questions:

```python
def evaluate(ask):
    counts = {"correct": 0, "abstain ok": 0, "wrong": 0, "missed": 0}
    for q in QUESTIONS:
        text = ask(q["q"])
        if q["key"] is None:
            group = "abstain ok" if text == NOT_FOUND else "wrong"
        elif text == NOT_FOUND:
            group = "missed"
        else:
            group = "correct" if q["key"] in text else "wrong"
        counts[group] += 1
    return counts


print("baseline", evaluate(lambda q: rag(q, 3, 2).text))
qa = DocQA()
print("capstone", evaluate(qa.answer))
tokens = sum(e["tokens"] for e in qa.log) / len(qa.log)
cost = sum(e["cost"] for e in qa.log)
print(f"capstone tokens per question {tokens:.0f}, cost {cost:.6f}")
```

```text
baseline {'correct': 15, 'abstain ok': 3, 'wrong': 2, 'missed': 7}
capstone {'correct': 15, 'abstain ok': 3, 'wrong': 0, 'missed': 9}
capstone tokens per question 154, cost 0.002820
```

The capstone system gave the same number of correct answers (15) but **no
wrong answer at all**; the basic setup had 2 wrong. The price is 2 more misses
(7 → 9) and more tokens per question (154; 132 in the basic setup), because the
sentences of a whole article are sent. All three questions with no answer got
"not found". Which to prefer depends on the application: in a customer support
system a wrong answer costs more than saying "not found" and passing the person
to a human. On 27 questions a difference of two questions is small (11); a
decision needs a larger evaluation set.

## What next

This system's weak points are clear, and each points to a method we saw in the
module:

- **The missed questions** mostly come from word mismatch: embedding or hybrid
  search (09).
- When the **reader** is replaced by a real model, the answers become free text:
  evaluation moves from phrase matching to human and model-based evaluation
  (11), and verification becomes even more important (08).
- **The set is small:** with 27 questions small differences between two systems
  cannot be trusted (11); a large set of real questions is needed.
- **Behaviour tuning:** if the "say so if it is not in the source" behaviour
  cannot be had with the prompt, fine-tuning or LoRA (12, 13).

## Summary

- A document Q&A system: mask → search → fit to the budget → build the prompt →
  get the answer → verify → log → measure.
- Two-stage search (first the article, then its sentences) brought the wrong
  answers to zero on this corpus; the price was a few misses and more tokens.
- Verification caught an answer containing a number that is not in the source
  and turned it into "not found".
- Every component can be measured separately; the system is improved through
  the measurements of its components.
