def reruns_needed(rate, confidence=0.95):
    if rate <= 0:
        return None
    runs = 1
    while 1 - (1 - rate) ** runs < confidence:
        runs += 1
    return runs


for rate in [0.5, 0.1, 0.02]:
    print(rate, reruns_needed(rate))
print(0.1, reruns_needed(0.1, 0.99))
print(0.0, reruns_needed(0.0))
