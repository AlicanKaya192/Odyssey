import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Hisse: naif hatasi, h = 1, 5, 10, 20, 40 (iki ondalik, liste).


# 40 gunluk / 1 gunluk hata orani ve 40'in karekoku.


# Satis: mevsimsel naif hatasi, w = 1, 2, 4, 8 hafta (bir ondalik, liste).


# Satis: duz naif hatasi, h = 1, 3, 7 gun (bir ondalik, liste).
