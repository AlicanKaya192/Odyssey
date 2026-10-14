import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from doc_data import DOCS


def answer(question):
    return ""


for question in ["Do gift cards expire?", "Do you sell bicycles?"]:
    print(" ".join(answer(question).split()[:5]))
