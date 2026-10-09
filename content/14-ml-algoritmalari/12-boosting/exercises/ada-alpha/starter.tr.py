import math


def ada_alpha(err):
    # log((1 - err) / err)
    return 0.0

for err in (0.1, 0.3, 0.5):
    print(err, ada_alpha(err))
