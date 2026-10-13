from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_data import make_articles, make_tickets

articles = make_articles()
article_texts = [a["title"] + " " + a["text"] for a in articles]
tfidf = TfidfVectorizer(stop_words="english").fit(article_texts)


def zero_overlap(n):
    return 0


print(zero_overlap(500))
print(zero_overlap(2000))
