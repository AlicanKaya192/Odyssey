def calibration_gap(probabilities, labels):
    # Beklenen ortalama eksi gerceklesen ortalama.
    pass


print(calibration_gap([0.2, 0.4, 0.6], [0, 1, 0]))
print(calibration_gap([0.5, 0.5], [1, 0]))
print(calibration_gap([0.1, 0.1, 0.1, 0.1], [1, 1, 0, 0]))
