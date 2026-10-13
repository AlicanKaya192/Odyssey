from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
stop = list(ENGLISH_STOP_WORDS | {"ord", "com", "example", "hi", "hello",
                                  "thanks", "thank", "dear", "support",
                                  "regards", "help"})
tfidf = TfidfVectorizer(stop_words=stop, token_pattern=r"[a-z]{2,}", min_df=5)
X = tfidf.fit_transform(texts)
words = tfidf.get_feature_names_out()
nmf = NMF(n_components=8, random_state=0, max_iter=500)
W = nmf.fit_transform(X)


def main_topic(category):
    return ["", 0.0]

for category in ["billing", "refund"]:
    print(category, main_topic(category))
