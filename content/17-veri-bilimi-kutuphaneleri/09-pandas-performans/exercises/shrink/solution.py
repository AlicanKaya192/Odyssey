import pandas as pd


def shrink(qtys, prices):
    df = pd.DataFrame({"qty": qtys, "price": prices})
    small = df.assign(qty=pd.to_numeric(df["qty"], downcast="unsigned"),
                      price=df["price"].astype("float32"))
    before = df.memory_usage(deep=True).sum()
    after = small.memory_usage(deep=True).sum()
    return {"dtypes": small.dtypes.astype(str).tolist(), "smaller": bool(after < before)}

result = shrink([3, 50, 99], [1.5, 2.25, 9.0])
print(result["dtypes"])
print(result["smaller"])
