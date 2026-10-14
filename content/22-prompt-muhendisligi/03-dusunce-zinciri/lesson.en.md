# Step-by-Step Reasoning

A customer asks: "I bought a tent for 189.90 euros and two pairs of socks
at 12.50 euros each, and used a 10% discount code on the whole order;
what do I pay?" Answering this in one step is hard; you first need the
socks' price, then the total, then the discount. Asking the model to
write the steps before the answer is called **chain-of-thought**
prompting. In this section we see how a program uses such an answer:
parsing the final answer, checking the steps and, most importantly,
**not leaving to the model something code can compute**.

## When does it help?

Research has shown that large models give the right answer more often on
multi-step arithmetic and logic questions when they write the
intermediate steps before the answer. There are two ways to do it: add
"write the steps first, then give the answer" to the instruction, or
write the example answers of a few-shot prompt together with their
steps.

Three warnings:

- **Not every job needs it.** In one-step jobs such as putting a message
  into a category it may make no difference; but the token price is
  always paid.
- **Some models already reason step by step.** For models trained to
  produce a long chain of reasoning before the answer on their own, this
  instruction may be unnecessary.
- **The written steps need not be right.** Steps make the answer easier
  to check, but they can themselves be wrong.

## Parsing the final answer

For a program to use a stepwise answer, the final answer must sit in a
fixed place. We write in the instruction "the last line is
`Answer: <number>`". The four **example replies** below stand for
answers this question could get: a correct chain of reasoning, one that
forgets a pair, one that slips in a multiplication and an answer that
forgets the last line.

```python
import re

REPLIES = [
    "Socks: 2 * 12.50 = 25.00\nTotal: 189.90 + 25.00 = 214.90\n"
    "Discount: 214.90 * 0.10 = 21.49\n"
    "To pay: 214.90 - 21.49 = 193.41\nAnswer: 193.41",
    "Total: 189.90 + 12.50 = 202.40\n"
    "Discount: 202.40 * 0.10 = 20.24\n"
    "To pay: 202.40 - 20.24 = 182.16\nAnswer: 182.16",
    "Socks: 2 * 12.50 = 25.00\nTotal: 189.90 + 25.00 = 214.90\n"
    "Discount: 214.90 * 0.10 = 21.94\n"
    "To pay: 214.90 - 21.94 = 192.96\nAnswer: 192.96",
    "The tent and the socks cost 214.90 euros, so with the "
    "discount you pay about 193 euros.",
]


def final_answer(text):
    found = re.search(r"^Answer:\s*(\d+(?:\.\d+)?)\s*$", text, flags=re.M)
    return float(found.group(1)) if found else None


for reply in REPLIES:
    print(final_answer(reply))
```

```text
193.41
182.16
192.96
None
```

The fourth answer is probably close to the right result, but the
program cannot use it: "about 193" is a guess, not a number. If the last
line is missing, the answer is marked `None` and asked again or sent to a
person.

## Checking the steps

Because the steps are written down, we can check them with code. Let us
find every operation of the form `a + b = c` and compute it again:

```python
STEP = re.compile(r"(\d+(?:\.\d+)?) ([-+*]) (\d+(?:\.\d+)?) = (\d+(?:\.\d+)?)")
OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
       "*": lambda a, b: a * b}


def wrong_steps(text):
    wrong = []
    for a, op, b, c in STEP.findall(text):
        if abs(OPS[op](float(a), float(b)) - float(c)) > 0.005:
            wrong.append(f"{a} {op} {b} = {c}")
    return wrong


for reply in REPLIES:
    print(wrong_steps(reply))
```

```text
[]
[]
['214.90 * 0.10 = 21.94']
[]
```

The multiplication error in the third answer (`21.94` instead of
`21.49`) was caught. But the second answer came out clean, although its
result is wrong: the operation `189.90 + 12.50 = 202.40` is **computed
correctly**, it is just the wrong step; the second pair of socks was
forgotten. The step checker finds calculation errors, not reasoning
errors.

## Let code compute what can be computed

The answer to this question can in fact be computed: if the prices,
counts and discount are known, the program finds the right amount
itself. The model's job is then not to calculate but to **extract the
numbers** from the customer's message (in the Structured Output and Tool
Calling sections). Let us find the right amount with code and compare the
answers with it:

```python
def order_total(items, discount):
    subtotal = sum(price * count for price, count in items)
    return round(subtotal * (1 - discount), 2)


expected = order_total([(189.90, 1), (12.50, 2)], 0.10)
print("expected", expected)
for reply in REPLIES:
    answer = final_answer(reply)
    print(answer, "ok" if answer == expected else "wrong or missing")
```

```text
expected 193.41
193.41 ok
182.16 wrong or missing
192.96 wrong or missing
None wrong or missing
```

Only one of the four answers gives the right amount, and the code sets
all three problems apart: the forgotten step, the calculation error and
the missing last line. The rule: **do not leave exact calculations such as
money, dates and unit conversions to the model.** Let the model do the
language side (finding the numbers, writing the answer) and the code do
the calculation.

## Several answers, a majority vote

For questions that cannot be computed but have one right answer, another
way is to ask the same question several times at a temperature above
zero and take a **majority vote** on the final answers (the consistency
idea from the previous module). The five values below are example final
answers of five separate attempts:

```python
from collections import Counter

from llm_client import count_tokens

samples = [193.41, 193.41, 182.16, 193.41, None]
votes = Counter(a for a in samples if a is not None)
answer, count = votes.most_common(1)[0]
print(answer, count, "of", len(samples))
print("tokens: steps", count_tokens(REPLIES[0]),
      "direct", count_tokens("Answer: 193.41"))
```

```text
193.41 3 of 5
tokens: steps 60 direct 6
```

The majority is at 193.41, with three of five attempts. This way raises
reliability when errors are scattered; but with a model that makes the
same error again and again, the majority is wrong too. The price is also
large: five attempts are five calls, and a stepwise answer takes
10 times the tokens of a direct answer. Step-by-step reasoning
and majority votes are worth it only if an error costs more than these
tokens.

## Whom do you show the steps?

The steps are for the program to check; the customer is usually shown
only the final answer. The steps may contain a wrong intermediate result,
an internal rule or information that should not be written to a
customer. That is another benefit of parsing the last line separately.

## Summary

- Step-by-step reasoning can help with multi-step questions; not every
  job needs it and the token price is large.
- Have the final answer put on a fixed line (`Answer: ...`) and parse only
  that; if the line is missing, do not use the answer.
- Recomputing the operations in the steps with code finds calculation
  errors, not reasoning errors.
- Let code do exact calculations (money, dates, units); let the model
  extract the numbers.
- A majority vote reduces scattered errors but multiplies the number of
  calls.
