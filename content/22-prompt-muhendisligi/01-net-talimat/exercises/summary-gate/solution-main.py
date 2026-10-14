import re

from llm_client import ChatClient

RULES = {"max_words": 12, "max_sentences": 1, "must_include": ["tent"]}
SYSTEM = ("Summarize the review between <review> tags. "
          "Words: at most 12. Sentences: at most 1. Mention: tent.")
SCRIPT = ["The tent is warm and quick to pitch.",
          "A warm tent that is quick to pitch even in strong wind at night.",
          "Warm and quick to pitch."]
REVIEWS = ["Warm tent, quick to pitch.", "Pitched it in a storm. Warm!",
           "Quick to pitch, very warm inside."]


def wrap(tag, text):
    clean = text.replace("&", "&amp;")
    clean = clean.replace("<", "&lt;").replace(">", "&gt;")
    return f"<{tag}>\n{clean}\n</{tag}>"


def check(text, rules):
    failed = []
    if len(text.split()) > rules["max_words"]:
        failed.append("max_words")
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if len(sentences) > rules["max_sentences"]:
        failed.append("max_sentences")
    if any(w.lower() not in text.lower() for w in rules["must_include"]):
        failed.append("must_include")
    return failed


def summarize(reviews):
    client = ChatClient(SCRIPT)
    accepted, failures = [], []
    for review in reviews:
        messages = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": wrap("review", review)}]
        reply = client.chat(messages, max_tokens=40)
        failed = check(reply.text, RULES)
        failures.append(failed)
        if not failed:
            accepted.append(reply.text)
    return [accepted, failures]


accepted, failures = summarize(REVIEWS)
print(len(accepted))
for failed in failures:
    print(failed or "ok")
