import pandas as pd


def shrink(qtys, prices):
    df = pd.DataFrame({"qty": qtys, "price": prices})
    return {"dtypes": df.dtypes.astype(str).tolist(), "smaller": False}

result = shrink([3, 50, 99], [1.5, 2.25, 9.0])
print(result["dtypes"])
print(result["smaller"])
