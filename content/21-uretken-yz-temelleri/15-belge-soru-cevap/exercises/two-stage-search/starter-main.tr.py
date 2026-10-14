from retrieval import Index, by_article, by_sentence


def two_stage(question):
    return []


for sentence in two_stage("Do gift cards expire?"):
    print(" ".join(sentence.split()[:5]))
