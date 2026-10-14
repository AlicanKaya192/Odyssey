# The Anatomy of a Prompt

The text you send to a language model is called a **prompt**. In the
previous module we saw that a chat API takes a list of messages, counts
tokens and that every call has a price. This module is about the inside
of that list: how to write what you want from the model and how to use
the answer that comes back. In this section we take a prompt apart, look
at what each part does and how many tokens it takes, and see that the
answer does not always come in the form you expect.

## How we will work in this module

The program is offline and does not connect to a real model. We keep
using the recorded-reply client from the previous module (`llm_client.py`):
`ChatClient(script)` answers each call with the next reply in the list.
These replies were written in advance; they were not taken from a model,
so they are **example replies**. That is why the lesson has no measurement
such as "this prompt gave better answers", and it cannot have one.

We will learn two things here:

- **The principles of writing prompts.** These are habits that help with
  many models, but you can only learn how much a principle changes your
  model by measuring it on your own model with your own examples. The
  section on evaluating prompts shows how.
- **The program around the model.** The code that builds the prompt,
  parses the answer, validates it, retries on errors and keeps track of
  the cost. This part does not depend on the model, and here it is really
  run and measured.

<figure class="fig">
  <div class="flow">
    <span class="node">Build the prompt</span>
    <span class="arrow">→</span>
    <span class="node acc">Test the program with example replies</span>
    <span class="arrow">→</span>
    <span class="node">Measure on your model</span>
  </div>
  <figcaption>The program is tested here; the prompt's effect is measured on your model, with your evaluation set.</figcaption>
</figure>

## A prompt is a list of messages

In a chat API a prompt is not a single text but a list of messages with
roles:

- `system`: the model's role and the rules it follows. Written once at
  the start of the conversation and sent again in every call.
- `user`: the user's message or the job the program gives the model.
- `assistant`: the model's earlier answers (as history or as examples).

## The parts of a prompt

A good prompt usually has these parts. Not every prompt needs all of
them, but the model fills a missing part with its own guess:

<figure class="fig anat">
  <div class="anat-row"><span>Role</span><span>Who the model acts as: "you are a shop's support assistant"</span></div>
  <div class="anat-row"><span>Task</span><span>What to do: "put the message into a category"</span></div>
  <div class="anat-row"><span>Context</span><span>Information the job needs: the list of categories, rules, documents</span></div>
  <div class="anat-row"><span>Format</span><span>What the answer looks like: "the category name only, in lower case"</span></div>
  <div class="anat-row"><span>Input</span><span>The data processed in this call: the customer's message</span></div>
</figure>

In later sections we will add two more parts: **examples** (few-shot
prompts) and **constraints** (length, tone, things not to do). Let us
build a prompt that classifies the support messages of an outdoor shop.
The fixed parts go into the system message, the changing input into the
user message:

```python
from llm_client import count_tokens, count_message_tokens

PARTS = {
    "role": "You are a support assistant for an outdoor gear shop.",
    "task": "Put the customer message into one category.",
    "labels": "Categories: shipping, returns, refunds, warranty, payment.",
    "format": "Answer with the category name only, in lower case.",
    "input": "My parcel should have arrived on Monday. Where is it?",
}


def build_messages(parts):
    system = " ".join(parts[k] for k in ["role", "task", "labels", "format"])
    return [{"role": "system", "content": system},
            {"role": "user", "content": parts["input"]}]


messages = build_messages(PARTS)
for name, text in PARTS.items():
    print(f"{name:7} {count_tokens(text):2} tokens")
print("message list", count_message_tokens(messages), "tokens")
```

```text
role    15 tokens
task    11 tokens
labels  19 tokens
format  14 tokens
input   17 tokens
message list 86 tokens
```

Building the prompt from parts instead of writing one long text by hand
has two benefits: you see how much room each part takes, and you can
change one part and try it without touching the others. When we improve
prompts systematically (towards the end of this module) this is exactly
what we will do.

## Sending and checking the answer

We send the message list to the client. This time the answer is a single
word, so we keep `max_tokens` small:

```python
from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
client = ChatClient(["shipping"])
reply = client.chat(messages, max_tokens=5, temperature=0.0)
print(repr(reply.text), reply.finish_reason, reply.text in LABELS)

sent = client.calls[0]
print([m["role"] for m in sent["messages"]], sent["max_tokens"])
```

```text
'shipping' stop True
['system', 'user'] 5
```

The last line matters: `client.calls` shows what your program **actually
sent** to the model. A faulty prompt often comes not from a badly written
instruction but from the program sending the wrong message: a wrong role,
a missing input, a system message that was never added. In a real
application too, logging the outgoing request is the first debugging tool.

For classification we wrote `temperature=0.0`: we want the same answer to
the same message every time. Even at temperature zero there is no
guarantee that real models always give exactly the same answer; but
where we do not want creative text, a low temperature is the natural
choice.

## The answer may not come in the form you expect

We said "the category name only", but a model does not always follow
that instruction: it starts with a capital letter, adds a full stop,
writes a sentence or hesitates between two categories. The six replies
below are **example replies** that stand for such cases. Let us compare
two parsers: one only cleans the answer and looks it up in the list
(strict), the other looks for the first category name anywhere in the
text (lenient):

```python
EXAMPLE_REPLIES = ["shipping", "Shipping.", " refunds\n",
                   "The category is returns.",
                   "warranty, maybe payment", "I would say shipping."]


def strict(text):
    label = text.strip().lower().rstrip(".!")
    return label if label in LABELS else "needs_review"


def lenient(text):
    found = [label for label in LABELS if label in text.lower()]
    return found[0] if found else "needs_review"


for text in EXAMPLE_REPLIES:
    print(f"{text!r:27} {strict(text):13} {lenient(text)}")
```

```text
'shipping'                  shipping      shipping
'Shipping.'                 shipping      shipping
' refunds\n'                refunds       refunds
'The category is returns.'  needs_review  returns
'warranty, maybe payment'   needs_review  warranty
'I would say shipping.'     needs_review  shipping
```

The strict parser rescues the first three replies; spaces, a capital
letter and a final full stop are harmless differences. It sets the other
three apart as `needs_review`. The lenient parser gives every reply a
category; it finds a sensible one in the two replies that are sentences,
but for `"warranty, maybe payment"` it picks `warranty` **although it is
not sure**. The model hesitated between two categories and that
information is lost; the lenient parser can no longer tell which answer
is doubtful.

The lesson: you must ask for the answer's format clearly in the prompt,
but that is not enough; the program must **validate** the answer that
comes back. Setting aside an answer that cannot be validated, or asking
again with an error message (in the Structured Output section), is safer
than fixing it with a guess.

## The fixed part is paid in every call

If the classifier processes thousands of messages, the system message is
sent again in every call. Only the input changes:

```python
INPUTS = ["Where is my parcel?",
          "The zip of my tent broke after one year.",
          "Can I pay in three instalments?"]
fixed = count_tokens(messages[0]["content"])
for text in INPUTS:
    total = count_message_tokens(build_messages({**PARTS, "input": text}))
    print(f"{total:3} tokens, system part {fixed} ({fixed / total:.0%})")
print("system tokens for 10000 messages:", fixed * 10000)
```

```text
 76 tokens, system part 59 (78%)
 81 tokens, system part 59 (73%)
 79 tokens, system part 59 (75%)
system tokens for 10000 messages: 590000
```

For short messages 73–78% of the tokens sent are the fixed part.
That is a reason to keep the system message short; but not a reason to
drop an instruction or context that is needed. First write a prompt that
works, then remove unneeded words by measuring.

## Summary

- A prompt is a list of messages with roles: `system`, `user`,
  `assistant`.
- The parts of a good prompt are role, task, context, format and input;
  the model fills a missing part with a guess.
- Building the prompt from parts makes it easy to measure and change the
  parts one by one.
- Look at what the program actually sends with a log such as
  `client.calls`.
- Asking for a format is not enough; validate the answer and set aside
  what cannot be validated.
- The replies in this module are example replies; you measure a
  principle's effect on your own model.
