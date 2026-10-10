import matplotlib.pyplot as plt
import pandas as pd


def top_chart(channels, sales):
    return {"order": [], "labels": [], "highlight": ""}

result = top_chart(["web", "store", "phone", "web", "store", "web"], [5, 3, 2, 4, 6, 1])
print(result["order"])
print(result["labels"])
print(result["highlight"])
