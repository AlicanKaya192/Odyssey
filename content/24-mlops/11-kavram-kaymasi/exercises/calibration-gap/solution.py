def calibration_gap(probabilities, labels):
    expected = sum(probabilities) / len(probabilities)
    actual = sum(labels) / len(labels)
    return round(expected - actual, 3)


print(calibration_gap([0.2, 0.4, 0.6], [0, 1, 0]))
print(calibration_gap([0.5, 0.5], [1, 0]))
print(calibration_gap([0.1, 0.1, 0.1, 0.1], [1, 1, 0, 0]))
