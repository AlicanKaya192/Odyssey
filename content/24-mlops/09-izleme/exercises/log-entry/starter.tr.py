def log_entry(row, probability, version, month):
    # Olasiligi denetle, sozlugu kur.
    pass


row = {"id": "C7", "tenure": 2, "plan": "pro"}
entry = log_entry(row, 0.90112, 3, "2026-05")
for key, value in entry.items():
    print(key, value)
print(log_entry(row, 1.2, 3, "2026-05"))
