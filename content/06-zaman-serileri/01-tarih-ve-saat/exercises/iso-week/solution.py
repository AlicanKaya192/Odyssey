from datetime import date

days = ["2024-03-09", "2024-12-29", "2024-12-30", "2025-01-01", "2021-01-01"]

for text in days:
    day = date.fromisoformat(text)
    iso = day.isocalendar()
    print(text, f"{iso.year}-W{iso.week:02d}")
