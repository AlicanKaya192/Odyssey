import re
from collections import Counter

from text_data import make_tickets


def hapax_share(n):
    texts = [t["text"] for t in make_tickets(n)]
    counts = Counter(w for t in texts for w in re.findall(r"[a-z0-9']+", t.lower()))
    once = sum(1 for c in counts.values() if c == 1)
    return round(once / len(counts), 3)


for n in [100, 1000, 3000]:
    print(n, hapax_share(n))
