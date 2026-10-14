# How a Large Language Model Generates

So far we have seen models that generate images and points. The rest of the
module is about **large language models** (**LLMs**) that generate text. In
the NLP path's Embeddings and Language Models module we built the
foundations: the transformer, pre-training and decoding (greedy choice,
temperature, top-k, nucleus sampling). This section connects those pieces to a
**chat model**: how a list of messages turns into a single text, where the
model ends its answer and why it gives a fluent answer to a question it does
not know.

## The model only continues

A language model's only ability is to predict the **next token** of a given
text. Asking a question, getting an answer, playing a role; all of it is built
on top of this single job. Chat models continue a question "as if answering"
because their training data is made of dialogues written in a certain **chat
template**.

Let us see this with a small toy model. We write 30 dialogues that ask for the
capitals of ten countries in three different question forms. Each message is
added to a single token sequence with a marker showing its role (`<user>`,
`<assistant>`), and the answer ends with an `<end>` marker:

```python
import numpy as np
from collections import Counter

CAPITALS = {"france": "paris", "germany": "berlin", "italy": "rome",
            "spain": "madrid", "japan": "tokyo", "egypt": "cairo",
            "canada": "ottawa", "kenya": "nairobi", "peru": "lima",
            "norway": "oslo", "turkey": "ankara", "chile": "santiago"}
KNOWN = list(CAPITALS)[:10]
QUESTIONS = ["what is the capital of {c} ?",
             "which city is the capital of {c} ?",
             "tell me the capital of {c} ."]


def render_chat(messages):
    tokens = []
    for m in messages:
        tokens += ["<" + m["role"] + ">"] + m["content"].split()
    return tokens + ["<assistant>"]


dialogues = []
for c in KNOWN:
    for q in QUESTIONS:
        msgs = [{"role": "user", "content": q.format(c=c)}]
        answer = f"the capital of {c} is {CAPITALS[c]} . <end>"
        dialogues.append(render_chat(msgs) + answer.split())
print(len(dialogues))
print(" ".join(dialogues[0]))
```

```text
30
<user> what is the capital of france ? <assistant> the capital of france is paris . <end>
```

`render_chat` is a small version of what a chat API does behind the scenes:
it turns the message list into a single sequence with role markers and adds
`<assistant>` at the end to say "now it is the assistant's turn". Real models
use different markers, but the idea is the same. Turkey and Chile are in the
dictionary but **not** in the training dialogues: the model will never see
these two countries.

## The toy model: the longest matching context

In a real LLM a transformer predicts the next token. We build a model that
predicts by counting: at every position we take the previous 1–7 tokens as the
context and count the token that follows. When predicting we use the
**longest** familiar context; if it is not familiar we shorten it by one and
try again (a backed-off, variable-length version of the n-gram model from the
NLP path).

```python
ORDER = 8
tables = [dict() for _ in range(ORDER)]
for d in dialogues:
    for i in range(1, len(d)):
        for n in range(1, min(i, ORDER - 1) + 1):
            context = tuple(d[i - n:i])
            tables[n].setdefault(context, Counter())[d[i]] += 1


def next_probs(context):
    for n in range(ORDER - 1, 0, -1):
        counts = tables[n].get(tuple(context[-n:]))
        if counts:
            break
    words = sorted(counts)
    p = np.array([counts[w] for w in words], dtype=float)
    return words, p / p.sum()


words, p = next_probs("capital of france is".split())
print(words, p)
words, p = next_probs(["of"])
print(len(words), "choices after 'of'")
```

```text
['paris'] [1.]
10 choices after 'of'
```

After the context "capital of france is" there is a single option: `paris`.
After "of" alone all ten countries are possible; only a longer context says
which one comes next.

## The generation loop and the finish reason

The answer is produced token by token: take the distribution, choose a token,
append it to the sequence, repeat. Two things stop the loop:

- The model produces the **stop marker** (`<end>`): the answer is finished.
  The finish reason is `stop`.
- The number of generated tokens reaches the **`max_tokens`** limit: the
  answer is cut off. The finish reason is `length`.

Chat APIs return this information with the answer. A program that sees
`length` must know the answer is incomplete.

```python
def generate(messages, max_tokens=20, temperature=0.0, seed=0):
    rng = np.random.default_rng(seed)
    tokens = render_chat(messages)
    out = []
    while len(out) < max_tokens:
        words, p = next_probs(tokens + out)
        if temperature == 0:
            w = words[int(np.argmax(p))]
        else:
            q = p ** (1 / temperature)
            w = words[rng.choice(len(words), p=q / q.sum())]
        if w == "<end>":
            return " ".join(out), "stop"
        out.append(w)
    return " ".join(out), "length"


def ask(country, **kwargs):
    msg = {"role": "user", "content": f"what is the capital of {country} ?"}
    return generate([msg], **kwargs)


for c in ["france", "japan"]:
    print(ask(c))
print(ask("france", max_tokens=3))
```

```text
('the capital of france is paris .', 'stop')
('the capital of japan is tokyo .', 'stop')
('the capital of', 'length')
```

At temperature 0 the most likely token is chosen at every step (greedy
choice); that is why the answer is the same on every run. With
`max_tokens=3` the answer was cut at the third token and the finish reason is
`length`.

## Why does the template matter?

What does the model do if we give only the user's question, without the
`<assistant>` marker?

```python
user_only = ["<user>"] + "what is the capital of france ?".split()
print(next_probs(user_only))
```

```text
(['<assistant>'], array([1.]))
```

The model wants to write the `<assistant>` marker itself as the next token:
that is not an answer, it is the continuation of the dialogue. The model does
not "answer the question"; it produces a continuation that **resembles the
text** in its training data. That is why building the template correctly
matters; chat APIs build the template for you, you only give the message list.

## It answers what it does not know, too

Now let us ask about the two countries that are not in the training
dialogues:

```python
for c in ["turkey", "chile"]:
    print(c, ask(c))
answers = Counter(ask("chile", temperature=1.0, seed=s)[0]
                  for s in range(200))
print(len(answers), "different answers in 200 tries")
for text, n in answers.most_common(3):
    print(n, text)
```

```text
turkey ('the capital of canada is ottawa .', 'stop')
chile ('the capital of canada is ottawa .', 'stop')
10 different answers in 200 tries
26 the capital of germany is berlin .
26 the capital of kenya is nairobi .
24 the capital of france is paris .
```

The model does not say "I don't know"; it builds a grammatically perfect,
confident sentence that is **the answer to another question**. At temperature
1, 200 tries give 10 different answers and none of them is the
capital of Chile: the model can only combine sentence pieces it has seen.
Real LLMs are far larger and "know" far more, but the principle is the same:
a model produces fluent text even for a question its data gives no basis for.
This behaviour is called **hallucination**, and it will be the topic of the
section after next.

## When does temperature change anything?

Let us ask the same question 50 times with different temperatures and count
how many different answers come out; once for a country it knows and once for
one it does not:

```python
for country in ["france", "chile"]:
    for t in [0.0, 0.7, 1.5]:
        outs = {ask(country, temperature=t, seed=s)[0] for s in range(50)}
        print(country, "temperature", t, "->", len(outs), "answers")
```

```text
france temperature 0.0 -> 1 answers
france temperature 0.7 -> 1 answers
france temperature 1.5 -> 1 answers
chile temperature 0.0 -> 1 answers
chile temperature 0.7 -> 10 answers
chile temperature 1.5 -> 10 answers
```

For the question it knows, temperature changes nothing: the distribution has
a single option. For the question it does not know, temperature 0 gives a
single, stable answer (but a wrong one); as the temperature rises, 50 tries
give 10 different answers. It is the same with real models: asking the same
question a few times and checking whether the answers agree is a hint about
how much basis the model has on the topic. Setting the temperature to 0 makes
the answer repeatable, not **correct**.

## The model does not remember

Chat APIs are **stateless**: the model does not remember earlier calls. For it
to answer "what did you just say?", all earlier messages must be sent again in
every call. The "memory" of chat applications is really the message list kept
by the program and sent from the start every time. This has a price: as the
list grows, more tokens are processed in every call. That is the next
section's topic.

## Summary

- An LLM's only job is to predict the next token; chat is a template built on
  top of this job.
- The message list is turned into a single sequence with role markers; the
  assistant marker added at the end says "your turn".
- Generation ends with the stop marker (`stop`) or the `max_tokens` limit
  (`length`); `length` says the answer is incomplete.
- The model produces a fluent answer to a question it does not know, too (in
  the toy model not one correct answer in 200 tries).
- Temperature 0 makes the answer repeatable, not correct; inconsistent answers
  are a sign of weak grounding.
- The API is stateless: the history is sent again in every call.
