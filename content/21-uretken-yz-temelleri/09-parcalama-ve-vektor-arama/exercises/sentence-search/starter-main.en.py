import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from doc_data import DOCS


def best_doc(question):
    return ""


for question in ["Do gift cards expire?", "When can I call customer service?"]:
    print(best_doc(question))
