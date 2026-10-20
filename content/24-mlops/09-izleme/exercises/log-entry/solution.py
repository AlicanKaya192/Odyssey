def log_entry(row, probability, version, month):
    if not 0 <= probability <= 1:
        return None
    return {"id": row["id"], "month": month, "model_version": version,
            "churn_probability": round(probability, 3)}


row = {"id": "C7", "tenure": 2, "plan": "pro"}
entry = log_entry(row, 0.90112, 3, "2026-05")
for key, value in entry.items():
    print(key, value)
print(log_entry(row, 1.2, 3, "2026-05"))
