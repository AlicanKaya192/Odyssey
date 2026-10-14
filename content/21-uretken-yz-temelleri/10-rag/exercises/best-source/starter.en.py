import re

STOP = {"the", "a", "an", "is", "are", "do", "does", "i", "my", "you", "to", "of", "in", "for"}


def words(text):
    found = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in found if w not in STOP}


def best_source(question, sources, min_overlap):
    return 0


sources = ["Gift cards are valid for 3 years.", "Points expire after 12 months."]
print(best_source("Do gift cards expire?", sources, 2))
print(best_source("Do you sell bikes?", sources, 1))
