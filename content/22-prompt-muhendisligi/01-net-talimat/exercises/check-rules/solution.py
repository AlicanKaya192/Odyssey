import re

RULES = {"max_words": 12, "max_sentences": 1,
         "must_include": ["tent"], "must_not_include": ["!"]}


def check(text, rules):
    failed = []
    if "max_words" in rules and len(text.split()) > rules["max_words"]:
        failed.append("max_words")
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if "max_sentences" in rules and len(sentences) > rules["max_sentences"]:
        failed.append("max_sentences")
    lowered = text.lower()
    if any(w.lower() not in lowered for w in rules.get("must_include", [])):
        failed.append("must_include")
    if any(w in text for w in rules.get("must_not_include", [])):
        failed.append("must_not_include")
    return failed


for text in ["The tent is warm and easy to set up.",
             "Great tent! Warm. Easy.",
             "Warm and easy to set up."]:
    print(check(text, RULES) or "ok")
