import html
import re
import unicodedata

from text_data import messy_reviews

QUOTES = str.maketrans({chr(0x2018): "'", chr(0x2019): "'",
                        chr(0x201C): '"', chr(0x201D): '"'})


def clean(text):
    return text


def vocabulary(texts):
    return {w.strip(".,!?" + chr(34)).lower() for t in texts for w in t.split(" ")}


def vocab_sizes(n):
    raw = [r["text"] for r in messy_reviews(n)]
    return [len(vocabulary(raw)), len(vocabulary(clean(t) for t in raw))]


print(vocab_sizes(2000))
