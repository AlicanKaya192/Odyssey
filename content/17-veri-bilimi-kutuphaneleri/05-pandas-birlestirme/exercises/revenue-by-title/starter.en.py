import pandas as pd


def revenue_by_title(sales, products):
    left = pd.DataFrame(sales, columns=["product_id", "qty"])
    right = pd.DataFrame(products, columns=["id", "title", "price"])
    joined = left.merge(right, left_on="product_id", right_on="id")
    return {}

SALES = [[1, 3], [2, 5], [1, 1]]
PRODUCTS = [["1", "pen", 2.5], ["2", "cup", 4.0], ["3", "box", 9.0]]
print(revenue_by_title(SALES, PRODUCTS))
