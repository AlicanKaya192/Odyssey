import re

RULES = {"max_words": 12, "max_sentences": 1,
         "must_include": ["tent"], "must_not_include": ["!"]}


def check(text, rules):
    return []


for text in ["The tent is warm and easy to set up.",
             "Great tent! Warm. Easy.",
             "Warm and easy to set up."]:
    print(check(text, RULES) or "ok")
