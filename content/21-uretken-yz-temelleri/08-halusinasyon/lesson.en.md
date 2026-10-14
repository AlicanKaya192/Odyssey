# Hallucination and Reliability

In section 06, asked for the capital of a country it had never seen, the toy
model said "the capital of canada is ottawa": confident, grammatically perfect
and wrong. A language model producing content without basis in a fluent way is
called **hallucination**. This section deals with two questions: why it
happens and how a program can **catch** it.

## Why does it happen?

- **The goal is fluency, not truth.** In training the model learns to predict
  the next token. "A continuation that resembles text" and "a correct
  continuation" are often the same, but not always.
- **Gaps in knowledge.** On a topic missing or rare in its data, the model
  still produces something; saying "I don't know" is also a behaviour that has
  to be learnt.
- **Unfaithfulness to the given text.** While summarising a document placed in
  front of it or answering from it, the model can add a detail that is not in
  the document. This is also called **unfaithfulness**.

There is no setting that prevents hallucination completely; but on the
program's side three things can be done: **measure** that the model is not
sure, **check** the answer against a source, and **not answer** where certainty
cannot be reached.

## Measuring with consistency

The toy model from section 06 is in the file `tiny_chat.py` for use in the
exercises. Let us ask the same question 20 times at temperature 1 and look at
the share of the most common answer:

```python
from collections import Counter
from tiny_chat import ask, CAPITALS


def consistency(country, n=20):
    answers = Counter(ask(country, temperature=1.0, seed=s)[0]
                      for s in range(n))
    answer, count = answers.most_common(1)[0]
    return answer, count / n


for c in ["france", "peru", "turkey", "chile"]:
    answer, share = consistency(c)
    print(c, share, answer)
```

```text
france 1.0 the capital of france is paris .
peru 1.0 the capital of peru is lima .
turkey 0.35 the capital of canada is ottawa .
chile 0.35 the capital of canada is ottawa .
```

For the countries it knows, 20 of 20 answers are the same. For the countries
it does not know, even the most common answer is only 35% of the
tries: the model says something different every time. This is called a
**self-consistency** check: on a topic a model knows, its answers agree; on a
topic it does not know, they scatter.

## If you are not sure, do not answer

Let us turn consistency into a gate: if the share of the most common answer is
below 0.6, say "I am not sure". Let us try all twelve countries in the
dictionary and compare the answers with the real capital:

```python
def gated(country, threshold=0.6):
    answer, share = consistency(country)
    return answer if share >= threshold else None


correct = wrong = abstained = 0
for country, capital in CAPITALS.items():
    answer = gated(country)
    if answer is None:
        abstained += 1
    elif answer.split()[5] == capital:
        correct += 1
    else:
        wrong += 1
print("correct", correct, "wrong", wrong, "abstained", abstained)
print("without the gate, wrong:",
      sum(ask(c)[0].split()[5] != cap for c, cap in CAPITALS.items()))
```

```text
correct 10 wrong 0 abstained 2
without the gate, wrong: 2
```

Without the gate the model gave a wrong answer to two of the twelve questions;
with the gate no wrong answer is left and those two questions get "I am not
sure". The price is the number of calls: 20 calls for every question. The
separation is this sharp in the toy model because it knows everything it knows
in a single form; in real models the answers vary a little even on topics they
know, the threshold is tuned on data, and there can be consistent but wrong
answers too. Consistency is a **sign**, not a proof.

## Checking the answer against a source

When the model is given a document and asked to answer from it, a stronger
check is possible: do the details in the answer appear in the document? Let us
take a shop's return policy as the source. The twelve answers below are
**examples**: we wrote them by hand and know which are faithful to the policy
(`True` faithful, `False` containing a made-up detail).

```python
import re

POLICY = ("Orders over 50 euros ship for free. Standard delivery takes "
          "3 to 5 working days. Returns are accepted within 30 days of "
          "delivery. Refunds are paid to the original card within 7 days. "
          "Customer service is open Monday to Friday, 9:00 to 17:00.")

EXAMPLES = [
    ("Shipping is free for orders over 50 euros.", True),
    ("Standard delivery takes 3 to 5 working days.", True),
    ("Standard delivery takes 1 to 2 working days.", False),
    ("Yes, within 30 days of delivery.", True),
    ("Yes, within 60 days of delivery.", False),
    ("The refund is paid to your original card within 7 days.", True),
    ("The refund is paid as store credit within 7 days.", False),
    ("Monday to Friday, from 9:00 to 17:00.", True),
    ("Every day from 9:00 to 17:00, including Sunday.", False),
    ("Yes, we ship to Canada in 10 days.", False),
    ("Yes, if your order is over 50 euros.", True),
    ("The policy does not say; please ask customer service.", True),
]
DETAIL = re.compile(r"\d+(?::\d+)?|[A-Z][a-z]+")


def details(text):
    found = DETAIL.findall(text)
    first = text.split()[0].strip(",.")
    return [d for d in found if d != first]


def unsupported(answer, source):
    known = set(DETAIL.findall(source))
    return [d for d in details(answer) if d not in known]


for answer, faithful in EXAMPLES[:3] + EXAMPLES[8:10]:
    print(faithful, unsupported(answer, POLICY))
```

```text
True []
True []
False ['1', '2']
False ['Sunday']
False ['Canada', '10']
```

`details` collects the numbers, times and capitalised names in the answer
(except the sentence's first word, which always starts with a capital).
`unsupported` lists the ones that do not appear in the source. A made-up
duration ("1 to 2"), a day ("Sunday") or a country ("Canada") is caught.

## How good is the checker?

Let us measure the checker like a classifier that marks every example in whose
answer it finds an unsupported detail as "made up":

```python
tp = fp = fn = tn = 0
for answer, faithful in EXAMPLES:
    flagged = bool(unsupported(answer, POLICY))
    if flagged and not faithful:
        tp += 1
    elif flagged:
        fp += 1
    elif not faithful:
        fn += 1
        print("missed:", answer)
    else:
        tn += 1
print("tp", tp, "fp", fp, "fn", fn, "tn", tn)
```

```text
missed: The refund is paid as store credit within 7 days.
tp 4 fp 0 fn 1 tn 7
```

Four of the five made-up answers were caught and none of the faithful answers
was marked by mistake. The missed answer is instructive: "store credit" is not
in the policy, but it is neither a number nor a capitalised name; it is outside
what the checker looks at. Simple rules catch the most common inventions
(numbers, dates, names) cheaply but do not check the meaning. These examples
are twelve sentences we wrote; in a real application the checker is measured
on a labelled sample of real answers.

## In practice

- **Give a source:** giving the model the document to base its answer on (RAG,
  the next sections) closes the knowledge gap and makes checking possible.
- **Show the source:** having the answer state which chunk every claim comes
  from (a source number) makes checking easier; that the number really points
  to that chunk is checked separately.
- **Be able to abstain:** say "if it is not in the source, say you don't know"
  in the system message, and do not show an answer the program cannot be sure
  of.
- **Measure:** the hallucination rate is a number measured on labelled
  examples; it is measured again when a setting changes.

## Summary

- Hallucination: producing content without basis in a fluent way. The goal
  being fluency rather than truth, and gaps in knowledge, are the main causes.
- Self-consistency: asking the same question a few times and looking at how
  much the answers agree. In the toy model the share was 1.0 on topics it
  knows and 35% on topics it does not.
- Abstaining with a threshold brought the wrong answers to zero in the toy
  model; the price was 20 calls per question.
- Source check: do the numbers and names in the answer appear in the source?
  In twelve examples four of five inventions were caught; an answer whose
  meaning changed but which had no such detail slipped through.
- No single check is enough; checkers are measured too.
