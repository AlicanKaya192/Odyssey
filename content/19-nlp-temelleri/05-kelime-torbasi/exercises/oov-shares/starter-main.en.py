from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews, make_tickets

REVIEWS = [r["text"] for r in make_reviews(2000)]
TICKETS = [t["text"] for t in make_tickets(300)]


def oov_shares(n_train):
    vectorizer = CountVectorizer().fit(REVIEWS)
    return [0.0, 0.0]


for n in [50, 200, 1000]:
    print(n, oov_shares(n))
