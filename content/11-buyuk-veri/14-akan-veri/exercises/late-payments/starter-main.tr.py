from stream_data import payments
from collections import defaultdict

LATENESS = 30

# 1. Dogru sayilar (sirali akis).


# 2-4. Sirasiz akis, su isareti.
open_windows = defaultdict(int)
results = {}
newest = 0
dropped = 0


# 5. Karsilastirma.
