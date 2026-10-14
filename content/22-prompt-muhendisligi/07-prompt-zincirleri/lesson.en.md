# Chaining Prompts

Answering a support message is really several jobs: finding the
message's topic, extracting the order number in it, finding the relevant
rule and writing an answer to the customer. You can ask for all of them
with one long prompt; but when something goes wrong you cannot see **at
which step** it went wrong. Another way is to split the job into small
steps, do each step with a separate call and give one step's output to
the next: a **prompt chain**. In this section we build a chain, validate
each step's output and stop the chain on an error, and compare the
chain's token price with a single prompt.

## A three-step chain

<figure class="fig">
  <div class="flow">
    <span class="node">Classify</span>
    <span class="arrow">→</span>
    <span class="node">Extract order no</span>
    <span class="arrow">→</span>
    <span class="node acc">Answer with the relevant rule</span>
  </div>
  <figcaption>Each step's output is validated; a step that cannot be validated stops the chain.</figcaption>
</figure>

The first two steps return JSON and are validated. The third step puts
into the prompt the help-centre article from the previous module
(`doc_data.py`) that matches the category the first step found. We write
each step's result and input tokens into a log:

```python
import json

from doc_data import DOCS
from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
POLICY = {doc["id"]: doc["text"] for doc in DOCS}


def ask(client, instruction, text, max_tokens=60):
    messages = [{"role": "system", "content": instruction},
                {"role": "user", "content": text}]
    reply = client.chat(messages, max_tokens=max_tokens)
    return reply.text, reply.input_tokens


def parse(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def run_chain(client, message):
    log = []
    text, used = ask(client, 'Give the category as JSON: {"category": ...}',
                     message)
    data = parse(text)
    ok = isinstance(data, dict) and data.get("category") in LABELS
    log.append(("classify", ok, used))
    if not ok:
        return log, None
    category = data["category"]
    text, used = ask(client, 'Give the order number as JSON: '
                     '{"order_id": "ORD-12345" or null}', message)
    data = parse(text)
    ok = isinstance(data, dict) and "order_id" in data
    log.append(("extract", ok, used))
    if not ok:
        return log, None
    instruction = ("Answer in at most 3 sentences, using only this "
                   "policy:\n" + POLICY[category])
    text, used = ask(client, instruction, message, max_tokens=120)
    log.append(("reply", True, used))
    return log, text


client = ChatClient([
    '{"category": "shipping"}', '{"order_id": "ORD-48213"}',
    "Delivery takes 3 to 5 working days; ORD-48213 is on its way.",
    "refunds",
])
for message in ["Where is my order ORD-48213?",
                "I still have no money back for my return."]:
    log, answer = run_chain(client, message)
    print(log)
    print("answer:", answer)
```

```text
[('classify', True, 38), ('extract', True, 45), ('reply', True, 132)]
answer: Delivery takes 3 to 5 working days; ORD-48213 is on its way.
[('classify', False, 40)]
answer: None
```

For the second message the first step's answer is not JSON (`refunds` as
plain text); the chain stops there and the log tells **where** it
stopped. In one long prompt the same error would have surfaced somewhere
in the answer sent to the customer, and its cause would be invisible.
This is the chain's real benefit: each step's input and output can be
checked and improved separately.

The program decides what happens on a stop: asking that step again with
an error message (the repair from the Structured Output section),
switching to a default path or sending the message to a person.

## The chain's token price

The chain sends the message again in every step; a single prompt sends
it once. But a single prompt does not know which rule is needed, so it
must carry **all the rules**. Let us measure both:

```python
from llm_client import count_message_tokens

single = [{"role": "system", "content":
           "Classify the message, find the order number and answer "
           "in at most 3 sentences using the right policy:\n"
           + "\n".join(POLICY[label] for label in LABELS)},
          {"role": "user", "content": "Where is my order ORD-48213?"}]
fresh = ChatClient(['{"category": "shipping"}',
                    '{"order_id": "ORD-48213"}', "On its way."])
log, _ = run_chain(fresh, "Where is my order ORD-48213?")
chain_total = sum(used for _, _, used in log)
print("single prompt:", count_message_tokens(single))
print("chain, 3 calls:", chain_total)
```

```text
single prompt: 412
chain, 3 calls: 215
```

In this example the chain is cheaper: the single prompt takes 412 tokens
because it carries all five rules, the chain's three calls 215 in total.
But this result depends on the size of the context. If the rules were
short or few, the chain sending the message again in every step and each
step producing its own answer could turn the picture around. Do not guess
which one is cheaper; measure it with your own data.

## Skip the step that is not needed

Not every message needs every step. Payment questions often need no
order number; if we skip the extraction step for payment and warranty
messages, the number of calls falls. Let us count on the test messages of
the earlier sections:

```python
from shop_data import TICKETS

NEEDS_ORDER = {"shipping", "returns", "refunds"}
test = [t for t in TICKETS if t["id"] % 4 == 0]
fixed = 3 * len(test)
conditional = sum(3 if t["label"] in NEEDS_ORDER else 2 for t in test)
print("calls, every step:", fixed)
print("calls, skipping extract:", conditional)
```

```text
calls, every step: 30
calls, skipping extract: 26
```

The decision to skip rests on the first step's output; if the first step
is wrong, the skip is wrong too. That is why the first steps of a chain
are the most checked.

## When a chain, when a single prompt?

| Chain | Single prompt |
|---|---|
| Steps can be checked and improved separately | One call, less waiting |
| Each step gets only the context it needs | All context goes in every call |
| It is clear at which step an error happened | The error gets lost inside the answer |
| More calls, the input is sent again | Intermediate results cannot be checked |

The rule: build a chain if the job consists of different sub-jobs and
an error in one sub-job spoils the following ones. Splitting a single,
simple job into a chain only raises the number of calls.

## Summary

- A prompt chain splits a job into steps; each step's output is the next
  one's input.
- Validate every step's output; stop the chain at a step that cannot be
  validated and log where it stopped.
- A chain can send each step only the context it needs; but it sends the
  input again in every step. Measure the price.
- Skipping an unneeded step lowers the number of calls; the decision to
  skip depends on the earlier step being right.
- Do not split a single, simple job into a chain.
