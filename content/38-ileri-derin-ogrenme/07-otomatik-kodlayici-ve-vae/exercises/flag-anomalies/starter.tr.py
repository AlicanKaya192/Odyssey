import torch


def flag_anomalies(errors, train_errors, q):
    # Kodunu buraya yaz
    return []

train_errors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
print(flag_anomalies([0.5, 0.95, 2.0], train_errors, 0.9))
print(flag_anomalies([0.5, 0.95, 2.0], train_errors, 0.5))
