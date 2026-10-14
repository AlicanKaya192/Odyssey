import re

STOP = {"the", "a", "an", "is", "are", "do", "does", "i", "my", "you", "to", "of", "in", "for"}


def words(text):
    found = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in found if w not in STOP}


def best_source(question, sources, min_overlap):
    best, best_overlap = 0, 0
    for n, source in enumerate(sources, 1):
        overlap = len(words(question) & words(source))
        if overlap > best_overlap:
            best, best_overlap = n, overlap
    return best if best_overlap >= min_overlap else 0


sources = ["Gift cards are valid for 3 years.", "Points expire after 12 months."]
print(best_source("Do gift cards expire?", sources, 2))
print(best_source("Do you sell bikes?", sources, 1))
