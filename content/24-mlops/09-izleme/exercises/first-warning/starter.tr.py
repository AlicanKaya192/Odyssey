def first_warning(signals):
    # Ay ay ilerle; o ay calan bir sinyal varsa adlariyla dondur.
    pass


signals = {
    "accuracy": [False, False, False, False, True, True],
    "predicted_rate": [False, False, True, True, True, True],
    "usage_mean": [False, False, True, True, True, True],
}
print(first_warning(signals))
print(first_warning({"accuracy": [False, False]}))
