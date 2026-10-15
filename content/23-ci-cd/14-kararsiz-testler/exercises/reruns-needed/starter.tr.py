def reruns_needed(rate, confidence=0.95):
    # n'i 1'den baslatip olasilik yeterli olana kadar artir.
    pass


for rate in [0.5, 0.1, 0.02]:
    print(rate, reruns_needed(rate))
print(0.1, reruns_needed(0.1, 0.99))
print(0.0, reruns_needed(0.0))
