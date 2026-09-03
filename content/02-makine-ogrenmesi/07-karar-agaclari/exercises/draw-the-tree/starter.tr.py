import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("customers.csv")
X = df[["age", "income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

# matplotlib.pyplot ve plot_tree'yi de ice aktar.


# max_depth=2 ile agaci egit (random_state=42).


# Her sutunun onem degerini yazdir: sutun adi ve deger (uc ondalik).


# En onemli sutunun adini yazdir.


# Agaci ciz: feature_names ver, sinif adlari "stays" ve "leaves",
# kutular renkli olsun.


# chart.png olarak kaydet.
