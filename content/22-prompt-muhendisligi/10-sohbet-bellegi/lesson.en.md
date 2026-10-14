# Conversation History and Memory

A chat API is stateless: the model does not remember earlier messages,
the program sends the history again in every call. In the previous module
(Tokens, the Context Window and Cost) we measured the price of this: the
total tokens grow fast with the number of messages, and when the history
is trimmed the model forgets the name from the first message. In this
section we look at ways to shorten without forgetting: **summarizing**
old messages and keeping important facts in a separate **memory**. We
measure both on the same conversation and see the new responsibility
memory brings: personal data.

## Three ways, one conversation

A ten-message support conversation. The customer gives her name in the
first message and the order number in the second; in the last message
she asks where the order is. We try three ways:

- **full:** the whole history in every call.
- **last4:** only the last four messages.
- **memory:** the last four messages and a list of facts added to the
  system message. The program extracts the name and order number from
  every user message with regular expressions and keeps them in memory.

```python
import re

from llm_client import count_message_tokens

SYSTEM = "You are the support assistant of an outdoor gear shop."
USER = [
    "Hi, my name is Ada.",
    "My order ORD-48213 has not arrived.",
    "It was supposed to come on Monday.",
    "Can you check where it is?",
    "I need the backpack for a trip.",
    "The trip starts on Friday.",
    "Is express delivery possible next time?",
    "How much does express delivery cost?",
    "Do you ship to Norway?",
    "So where is my order now?",
]
REPLY = "Thanks, I am looking into it."
FACTS = {"name": re.compile(r"my name is (\w+)", re.I),
         "order": re.compile(r"\bORD-\d{5}\b")}


def remember(memory, text):
    for key, pattern in FACTS.items():
        found = pattern.search(text)
        if found:
            memory[key] = found.group(found.lastindex or 0)


def conversation(strategy, keep=4):
    history, memory, sizes = [], {}, []
    for text in USER:
        remember(memory, text)
        history.append({"role": "user", "content": text})
        system = SYSTEM
        if strategy == "memory" and memory:
            facts = "; ".join(f"{k}={v}" for k, v in memory.items())
            system += " Known facts: " + facts
        recent = history if strategy == "full" else history[-keep:]
        sent = [{"role": "system", "content": system}] + recent
        sizes.append(count_message_tokens(sent))
        history.append({"role": "assistant", "content": REPLY})
    return sizes, sent


for strategy in ["full", "last4", "memory"]:
    sizes, sent = conversation(strategy)
    knows = "ORD-48213" in " ".join(m["content"] for m in sent)
    print(f"{strategy:6} total {sum(sizes):4} last {sizes[-1]:3} "
          f"knows the order: {knows}")
```

```text
full   total 1565 last 277 knows the order: True
last4  total  695 last  73 knows the order: False
memory total  847 last  89 knows the order: True
```

The whole history knows the order number but spends 1565 tokens over ten
calls; the last call alone is 277. The last four messages bring the
total down to 695, but at the last question the order number is in none
of the messages sent: the model has to ask "which order?" or guess. The
memory way keeps the number and spends 847 tokens, a little more than
half of the whole history; its price is a few words added to the system
message in every call.

## A summary: short but lossy

An alternative to memory is to summarize old messages into one sentence
with a model call and put it into the system message. The summary below
is an **example reply**; it will replace the first four messages:

```python
from llm_client import ChatClient

client = ChatClient(["The customer Ada says her order is late "
                     "and asks where it is."])
old = [{"role": "user", "content": text} for text in USER[:4]]
instruction = {"role": "system",
               "content": "Summarize this support chat in one sentence."}
summary = client.chat([instruction] + old, max_tokens=40).text
print(summary)
print("order number kept:", "ORD-48213" in summary)
print(count_message_tokens(old), "tokens ->",
      count_message_tokens([{"role": "system", "content": summary}]))
```

```text
The customer Ada says her order is late and asks where it is.
order number kept: False
56 tokens -> 23
```

The summary shortened the messages but dropped the order number. A
summary is a text a model writes: it decides what to keep and may drop an
important detail. A summary also has its own call and price. That is why
the two ways are often used together: **exact facts** (name, order
number, the chosen product) in a structured memory, **the flow of the
conversation** in the summary.

You can also extract the facts with a model instead of regular
expressions (as JSON, as in the Structured Output section); then you still
validate the value that comes out.

## Memory holds personal data

A memory is a record about the customer. You need to mind what it keeps:
information such as passwords and card numbers must never be stored, the
needed facts are kept only as long as needed and can be deleted. A filter
before storing:

```python
SECRET = re.compile(r"password|passcode|\b\d{4} \d{4} \d{4} \d{4}\b", re.I)


def remember_safely(memory, text):
    if SECRET.search(text):
        return "not stored"
    remember(memory, text)
    return "stored"


memory = {}
for text in ["My name is Ada.",
             "My password is hunter2, can you reset it?",
             "My card is 1234 5678 9012 3456.",
             "Please check ORD-10077."]:
    print(remember_safely(memory, text), "|", text)
print(memory)
```

```text
stored | My name is Ada.
not stored | My password is hunter2, can you reset it?
not stored | My card is 1234 5678 9012 3456.
stored | Please check ORD-10077.
{'name': 'Ada', 'order': 'ORD-10077'}
```

Nothing from the messages with a password or a card number went into
memory. This filter is simple: it can miss another spelling ("pass
word", a card number with dashes); as we saw in the masking lesson of the
previous module, regular expressions stay incomplete. The rule is clear
anyway: **memory keeps what the job needs, not everything the customer
says.**

Long-term memory (remembering in the next conversation too) needs even
more care:

- Memory is kept **per user**; one customer's memory never gets into
  another customer's conversation.
- The customer should be able to see and delete their memory.
- Records have a **lifetime**; old facts are deleted on their own.

## Summary

- Sending the whole history is expensive; keeping the last messages loses
  information.
- Keep exact facts (name, order number) in a structured memory and add
  them to the system message; it prevents forgetting with few tokens.
- A summary shortens the flow of the conversation but is a text a model
  writes; it may drop an important detail.
- Filter what goes into memory: information such as passwords and card
  numbers is never stored.
- Long-term memory should be per user, visible, deletable and timed.
