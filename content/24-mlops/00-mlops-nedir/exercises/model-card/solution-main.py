from ml_data import make_customers, FEATURES


def model_card(rows, accuracy):
    if rows:
        churn_rate = sum(r["churned"] for r in rows) / len(rows)
    else:
        churn_rate = 0.0
    return {
        "rows": len(rows),
        "churn_rate": round(churn_rate, 3),
        "features": FEATURES,
        "accuracy": round(accuracy, 3),
    }


rows = make_customers(500)
card = model_card(rows, 0.81274)
print("rows =", card["rows"])
print("churn_rate =", card["churn_rate"])
print("accuracy =", card["accuracy"])
print("features:")
for name in card["features"]:
    print("-", name)
