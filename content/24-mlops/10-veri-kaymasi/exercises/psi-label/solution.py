def psi_label(value):
    if value < 0.1:
        return "stable"
    if value <= 0.25:
        return "moderate"
    return "large"


for value in [0.012, 0.1, 0.229, 0.25, 0.456]:
    print(value, psi_label(value))
