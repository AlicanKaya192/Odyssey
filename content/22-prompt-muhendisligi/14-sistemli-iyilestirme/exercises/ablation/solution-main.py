import re

from shop_data import TICKETS


def render(definitions):
    lines = [f"- {label}: {', '.join(words)}"
             for label, words in definitions.items()]
    return "Classify the message into one category.\n" + "\n".join(lines)


def toy_model(prompt, text):
    words = set(re.findall(r"[a-z]+", text.lower()))
    best, best_hits = "unknown", 0
    for label, listed in re.findall(r"^- (\w+): (.+)$", prompt, re.M):
        hits = sum(word in words for word in listed.split(", "))
        if hits > best_hits:
            best, best_hits = label, hits
    return best


def accuracy(prompt, tickets):
    right = sum(toy_model(prompt, t["text"]) == t["label"] for t in tickets)
    return right / len(tickets)

def ablation(definitions, base, tickets):
    full = accuracy(render(definitions), tickets)
    result = []
    for label, words in definitions.items():
        for word in words:
            if word in base.get(label, []):
                continue
            smaller = {k: [w for w in ws if (k, w) != (label, word)]
                       for k, ws in definitions.items()}
            change = round(accuracy(render(smaller), tickets) - full, 2)
            if change:
                result.append([word, change])
    return result


BASE = {"shipping": ["parcel"], "returns": ["return"],
        "refunds": ["refund"], "warranty": ["warranty"],
        "payment": ["pay"]}
NEW = {"shipping": ["parcel", "tracking", "deliver"],
       "returns": ["return", "back", "send"],
       "refunds": ["refund", "money"],
       "warranty": ["warranty", "seam"],
       "payment": ["pay", "card"]}
for word, change in ablation(NEW, BASE, TICKETS[:20]):
    print(word, change)
