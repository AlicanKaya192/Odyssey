from sklearn.feature_extraction.text import TfidfVectorizer

from shop_data import TICKETS

POOL = [t for t in TICKETS if t["id"] % 4 != 0]


def nearest_labels(text, k):
    return []


print(nearest_labels("My refund has not arrived yet.", 3))
print(nearest_labels("The tent zip is broken.", 2))
