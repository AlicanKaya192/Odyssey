import re
from collections import Counter

from text_data import make_tickets


def hapax_share(n):
    texts = [t["text"] for t in make_tickets(n)]
    counts = Counter(w for t in texts for w in re.findall(r"[a-z0-9']+", t.lower()))
    return 0.0


for n in [100, 1000, 3000]:
    print(n, hapax_share(n))
