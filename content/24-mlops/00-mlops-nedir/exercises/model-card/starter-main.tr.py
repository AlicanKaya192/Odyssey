from ml_data import make_customers, FEATURES


def model_card(rows, accuracy):
    # Dort anahtarli bir sozluk dondur.
    pass


rows = make_customers(500)
card = model_card(rows, 0.81274)
print("rows =", card["rows"])
print("churn_rate =", card["churn_rate"])
print("accuracy =", card["accuracy"])
print("features:")
for name in card["features"]:
    print("-", name)
