from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews, make_tickets

REVIEWS = [r["text"] for r in make_reviews(2000)]
TICKETS = [t["text"] for t in make_tickets(300)]


def oov_shares(n_train):
    vectorizer = CountVectorizer().fit(REVIEWS[:n_train])
    analyze = vectorizer.build_analyzer()

    def share(texts):
        tokens = [w for t in texts for w in analyze(t)]
        return round(sum(w not in vectorizer.vocabulary_ for w in tokens) / len(tokens), 3)

    return [share(REVIEWS[1000:]), share(TICKETS)]


for n in [50, 200, 1000]:
    print(n, oov_shares(n))
