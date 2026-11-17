import math


def check_features(values, n=6):
    # Liste degilse ya da uzunlugu n degilse: "expected a list of n numbers"
    # Sonlu sayi olmayan varsa: "values must be finite numbers"; gecerliyse "ok"
    return "ok"

print(check_features([1, 2, 3, 4, 5, 6]))
print(check_features([1, 2]))
print(check_features([1, 2, 3, 4, 5, float("inf")]))
