def skewed_columns(names, trained, live, tolerance):
    # Ad, egitim ve canli degerini birlikte gez.
    pass


names = ["tenure", "monthly_fee", "support_calls", "is_pro"]
trained = [36.7, 30.2, 0.74, 0.4]
live = [36.1, 0.75, 30.1, 0.0]
print(skewed_columns(names, trained, live, 0.5))
print(skewed_columns(names, trained, trained, 0.5))
