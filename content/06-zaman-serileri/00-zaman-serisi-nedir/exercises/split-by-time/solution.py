import pandas as pd
from sklearn.model_selection import train_test_split

table = pd.read_csv("store_sales.csv")

n_train = int(len(table) * 0.8)
train = table.iloc[:n_train]
test = table.iloc[n_train:]

print(train["date"].iloc[-1], test["date"].iloc[0], len(test))
print(train["date"].max() < test["date"].min())

random_train, random_test = train_test_split(table, test_size=0.2, random_state=0)
leaked = (random_test["date"] < random_train["date"].max()).sum()
print(int(leaked), len(random_test))
