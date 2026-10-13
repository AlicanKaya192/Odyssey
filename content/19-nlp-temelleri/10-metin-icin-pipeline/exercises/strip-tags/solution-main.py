import re

from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import messy_reviews

texts = [r["text"] for r in messy_reviews(500)]


def strip_tags(text):
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split()).lower()


def vocab_has(word, preprocessor):
    vectorizer = TfidfVectorizer(preprocessor=preprocessor).fit(texts)
    return word in vectorizer.vocabulary_


print(strip_tags("<b>Good</b> value<br>Works"))
print(vocab_has("br", None))
print(vocab_has("br", strip_tags))
