from stream_data import payments
from collections import defaultdict

LATENESS = 30

# 1. The right counts (the stream in order).


# 2-4. The out-of-order stream, the watermark.
open_windows = defaultdict(int)
results = {}
newest = 0
dropped = 0


# 5. The comparison.
