# Tokens, the Context Window and Cost

At the end of the previous section we saw that chat APIs are stateless and the
history is sent again in every call. This section measures three consequences
of that: the model reads text as **tokens**, there is a **limit** to how many
tokens it can read, and on a paid service every token has a **price**. To
measure these we introduce a small tool that we will also use in the
exercises.

## A client with recorded replies

The program works offline and does not connect to a real model. So we wrote a
client called `llm_client.py` that behaves like a chat API:

- `ChatClient(script)`: answers each call with the **next reply** in the
  `script` list. The replies were written in advance; they were not taken from
  a model, so they are **example replies**, not a measurement of a model.
- `client.chat(messages, max_tokens=...)`: checks the message list, counts
  tokens, rejects a request that exceeds the context window, cuts the answer
  at `max_tokens` and returns a `Reply` (text, finish reason, input and output
  token counts).
- `client.calls`: a record of every call made. From here you can check **what
  your program sent** to the model.

Since what the model answers is known in advance, what is learnt here is not
the model itself but whether **the program that uses it** works correctly:
sending the right messages, respecting the limits, computing the cost.

## Counting tokens

Real models split text into pieces with methods like the BPE we saw in the NLP
path; every model has its own tokenizer and the counts change from model to
model. `llm_client` uses a **simplified** counter: every punctuation mark is
one token, and a word is one token for every started group of four
characters. Real counts differ but their sizes are similar; every calculation
here is done the same way with real counts.

```python
from llm_client import count_tokens, count_message_tokens

for text in ["cat", "capital", "Hello, world!", "internationalization",
             "What is the capital of Peru?",
             "Peru'nun başkenti neresidir?"]:
    print(count_tokens(text), text)
```

```text
1 cat
2 capital
6 Hello, world!
5 internationalization
8 What is the capital of Peru?
9 Peru'nun başkenti neresidir?
```

Long words take more tokens. The same question is written in Turkish with
fewer but longer words and takes 9 tokens in this counter (8 in English).
With real tokenizers too, the token count of the same text changes with the
language.

The token count of a message list adds the role markers of each message to the
contents (`count_message_tokens`; in this counter 4 per message and 2 for the
start of the answer).

## The context window

A model can process a limited number of tokens in one call: the **context
window**. The input messages and the answer to be generated must fit in the
window together. A request that does not fit is rejected:

```python
from llm_client import ChatClient, ContextLengthError

messages = [
    {"role": "system", "content": "You are a helpful travel assistant."},
    {"role": "user", "content": "What is the capital of Peru?"},
]
print("input tokens", count_message_tokens(messages))
client = ChatClient(["The capital of Peru is Lima."], context_window=60)
reply = client.chat(messages, max_tokens=20)
print(reply.text, reply.finish_reason, reply.input_tokens,
      reply.output_tokens)
try:
    client.chat(messages, max_tokens=50)
except ContextLengthError as error:
    print("error:", error)
```

```text
input tokens 29
The capital of Peru is Lima. stop 29 8
error: 29 input + 50 output tokens > window of 60
```

In the first call 29 input + 20 output tokens fit in the window
of 60. In the second call reserving 50 tokens for the answer takes the total
over the window and the request is rejected before the model even runs. Real
models have windows of thousands or even hundreds of thousands of tokens; but
long documents and long conversations may not fit there either.

## As the conversation grows

Let us have an eight-message conversation with a travel assistant. In every
call we send the whole history and record each call's input token count. The
last question asks for the name given in the first message; that reply is a
function that changes depending on whether the name appears in the messages
sent:

```python
QUESTIONS = [
    "My name is Ada and I am planning a trip to Peru.",
    "What is the capital of Peru?",
    "Which currency do they use there?",
    "Is it cold in Lima in July?",
    "What should I pack for a week?",
    "How long is a flight from Madrid to Lima?",
    "Do I need a visa?",
    "What is my name?",
]


def name_reply(messages):
    seen = any("Ada" in m["content"] for m in messages[:-1])
    return "Your name is Ada." if seen else "I do not know your name."


REPLIES = [
    "Nice to meet you, Ada. Peru is a great choice.",
    "The capital of Peru is Lima.",
    "Peru uses the sol.",
    "July is winter in Lima, so it is cool and often cloudy.",
    "Pack layers, a light jacket and comfortable shoes.",
    "A direct flight takes about twelve hours.",
    "It depends on your passport; check the official embassy site.",
    name_reply,
]
SYSTEM = {"role": "system", "content": "You are a helpful travel assistant."}


def run_chat(keep=None):
    client = ChatClient(REPLIES)
    history = [SYSTEM]
    replies = []
    for question in QUESTIONS:
        history.append({"role": "user", "content": question})
        sent = history if keep is None else [SYSTEM] + history[1:][-keep:]
        reply = client.chat(sent, max_tokens=100)
        history.append({"role": "assistant", "content": reply.text})
        replies.append(reply)
    return client, replies


client, replies = run_chat()
inputs = [r.input_tokens for r in replies]
print(inputs)
print("input tokens in total", sum(inputs))
print("last answer:", replies[-1].text)
```

```text
[35, 66, 92, 113, 147, 183, 211, 241]
input tokens in total 1088
last answer: Your name is Ada.
```

Every call's input is larger than the one before: as the history piles up,
the same messages are sent again and again. Even in this conversation of eight
short messages the total number of input tokens is 4.5 times that of
the last call. As the conversation grows the total grows roughly with the
square of the number of messages: in a conversation of $n$ messages, 1, 2,
…, $n$ messages are sent, a total of $n(n+1)/2$.

## Trimming the history

The simplest remedy is to keep the system message and send only the last few
messages. Let us repeat the same conversation with the last 4 messages:

```python
trimmed, short_replies = run_chat(keep=4)
inputs = [r.input_tokens for r in short_replies]
print(inputs)
print("input tokens in total", sum(inputs))
print("last answer:", short_replies[-1].text)
```

```text
[35, 66, 74, 64, 72, 87, 81, 75]
input tokens in total 554
last answer: I do not know your name.
```

The token count now stays at a certain level and the total drops clearly. But
there is a price: the name was given in the first message and is no longer in
the trimmed history; the last question gets an "I do not know" answer.
Trimming means **forgetting**. In practice two approaches are combined:
important facts (the person's name, preferences, decisions made) are kept
separately and added to the system message, or the old part is replaced by a
short summary. Module 2's Conversation History and Memory section covers these
in detail.

## Cost

Paid services usually price input and output tokens separately; output tokens
are often more expensive. The prices below are **examples**: 0.50 units per
million input tokens and 1.50 units per million output tokens. Real prices
change from service to service and over time.

```python
PRICE_IN, PRICE_OUT = 0.50, 1.50


def cost(replies):
    tokens_in = sum(r.input_tokens for r in replies)
    tokens_out = sum(r.output_tokens for r in replies)
    return (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000


full, short = cost(replies), cost(short_replies)
print(f"full history {full:.6f}  trimmed {short:.6f}")
print(f"per 100000 chats: {full * 100_000:.2f} vs {short * 100_000:.2f}")
```

```text
full history 0.000690  trimmed 0.000425
per 100000 chats: 68.95 vs 42.55
```

The price of a single conversation looks small; but an application has
thousands of conversations a day. As the scale grows, the question "what do I
send in every call?" turns directly into a question of cost. A long system
message, needless history or needlessly long answers are paid again
in every call. (`max_tokens` itself is not paid for, it only reserves room in
the window; the price is usually for the tokens generated.)

## Summary

- The model reads text as tokens; the token count changes with word length
  and language. The counter in this section is simplified; real counts differ
  from model to model.
- The sum of input and output tokens must fit in the context window; a request
  that does not fit is rejected.
- Because the conversation history is sent again in every call, the total
  token count grows quickly with the number of messages.
- Trimming the history reduces tokens but also loses information; important
  facts should be kept separately.
- Cost = input tokens × input price + output tokens × output price; every
  needless token is paid again in every call.
