import re

ABBREVIATIONS = {"dr.", "mr.", "mrs.", "e.g.", "i.e."}


def split_sentences(text):
    sentences = []
    for part in re.split(r"(?<=[.!?])\s+", text):
        if sentences and sentences[-1].split()[-1].lower() in ABBREVIATIONS:
            sentences[-1] += " " + part
        else:
            sentences.append(part)
    return sentences


text = "Dr. Lee paid $4.50 today. Great service! Ask Mr. Kim, e.g. by mail. Done?"
for sentence in split_sentences(text):
    print(sentence)
