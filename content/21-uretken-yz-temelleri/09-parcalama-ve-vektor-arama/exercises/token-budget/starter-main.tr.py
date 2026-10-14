from llm_client import count_tokens


def fit_chunks(chunks, budget):
    return [0, 0]


chunks = ["Gift cards are valid for 3 years.", "Points expire after 12 months.", "Repairs take 3 weeks."]
print(fit_chunks(chunks, 12))
print(fit_chunks(chunks, 100))
