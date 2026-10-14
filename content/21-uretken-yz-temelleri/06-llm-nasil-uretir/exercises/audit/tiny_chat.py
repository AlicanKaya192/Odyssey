"""The toy chat model from the lesson (read-only)."""
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
