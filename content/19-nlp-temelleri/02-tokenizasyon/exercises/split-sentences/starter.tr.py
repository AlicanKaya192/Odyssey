import re

ABBREVIATIONS = {"dr.", "mr.", "mrs.", "e.g.", "i.e."}


def split_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)


text = "Dr. Lee paid $4.50 today. Great service! Ask Mr. Kim, e.g. by mail. Done?"
for sentence in split_sentences(text):
    print(sentence)
