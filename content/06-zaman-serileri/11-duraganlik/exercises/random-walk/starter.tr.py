import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
change = k.diff().dropna()

# Duzeyin ve degisimin bir gun onceyle korelasyonu.


# Naif tahmin ve 20 gunluk ortalama tahmini: ortalama mutlak hata.


# Artis gunlerinin orani; dun artis olan gunlerde ayni oran.
