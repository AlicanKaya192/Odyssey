import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# naive: rolling(7).mean(); safe: shift(1) sonra rolling(7).mean().


# 9 Mart 2024: naive ve safe (bir ondalik).


# Elle dogrulama: 3-9 Mart ve 2-8 Mart ortalamalari.


# safe serisindeki bastaki NaN sayisi.


# 7 gun ileri icin: shift(7) sonra rolling(7).mean(); 9 Mart 2024 degeri.
