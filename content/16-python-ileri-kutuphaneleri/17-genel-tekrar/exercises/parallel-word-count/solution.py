from collections import Counter
from concurrent.futures import ThreadPoolExecutor


def count(text):
    return Counter(text.split())


def top_words(texts, n):
    total = Counter()
    with ThreadPoolExecutor() as pool:
        for part in pool.map(count, texts):
            total += part
    return [[word, k] for word, k in total.most_common(n)]

texts = ["a b a", "b a c", "a c c d"]
print(top_words(texts, 2))
