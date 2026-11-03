def detector_scores(alerts, attacks):
    alerts, attacks = set(alerts), set(attacks)
    tp = len(alerts & attacks)
    # FP ve FN'i bul
    return [0.0, 0.0]

print(detector_scores(["e1", "e2", "e5", "e7"], ["e2", "e5", "e6"]))
print(detector_scores([], ["e1"]))
