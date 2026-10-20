def calibration_alerts(rows, limit):
    alerts = []
    for month, predicted, actual in rows:
        if abs(predicted - actual) > limit:
            alerts.append(month)
    return alerts


rows = [[0, 0.277, 0.297], [3, 0.425, 0.41], [4, 0.504, 0.413], [6, 0.576, 0.471]]
print(calibration_alerts(rows, 0.05))
print(calibration_alerts(rows, 0.1))
print(calibration_alerts(rows, 0.01))
