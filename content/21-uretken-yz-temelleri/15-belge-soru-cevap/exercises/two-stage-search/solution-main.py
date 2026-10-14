from retrieval import Index, by_article, by_sentence

ARTICLES = Index(by_article())
SENTENCES = by_sentence()


def two_stage(question):
    (doc, _), _ = ARTICLES.search(question, 1)[0]
    return [text for d, text in SENTENCES if d == doc]


for sentence in two_stage("Do gift cards expire?"):
    print(" ".join(sentence.split()[:5]))
