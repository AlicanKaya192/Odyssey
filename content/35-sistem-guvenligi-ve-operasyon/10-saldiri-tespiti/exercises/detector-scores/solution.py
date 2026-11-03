def detector_scores(alerts, attacks):
    alerts, attacks = set(alerts), set(attacks)
    tp = len(alerts & attacks)
    fp = len(alerts - attacks)
    fn = len(attacks - alerts)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return [round(precision, 2), round(recall, 2)]

print(detector_scores(["e1", "e2", "e5", "e7"], ["e2", "e5", "e6"]))
print(detector_scores([], ["e1"]))
