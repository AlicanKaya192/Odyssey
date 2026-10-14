import re


def toy_model(prompt, text):
    words = set(re.findall(r"[a-z]+", text.lower()))
    best, best_hits = "unknown", 0
    for label, listed in re.findall(r"^- (\w+): (.+)$", prompt, re.M):
        hits = sum(word in words for word in listed.split(", "))
        if hits > best_hits:
            best, best_hits = label, hits
    return best


PROMPT = """Classify.
- shipping: parcel, courier
- returns: return, back
- refunds: refund, money"""
for text in ["Where is my parcel?", "I want my money back.",
             "The zip broke."]:
    print(toy_model(PROMPT, text))
