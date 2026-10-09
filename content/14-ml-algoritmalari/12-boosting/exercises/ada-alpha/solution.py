import math


def ada_alpha(err):
    return round(math.log((1 - err) / err), 4)

for err in (0.1, 0.3, 0.5):
    print(err, ada_alpha(err))
