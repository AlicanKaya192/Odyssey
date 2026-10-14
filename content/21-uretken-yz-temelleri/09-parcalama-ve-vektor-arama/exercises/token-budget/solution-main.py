from llm_client import count_tokens


def fit_chunks(chunks, budget):
    taken, used = 0, 0
    for chunk in chunks:
        cost = count_tokens(chunk)
        if used + cost > budget:
            break
        taken, used = taken + 1, used + cost
    return [taken, used]


chunks = ["Gift cards are valid for 3 years.", "Points expire after 12 months.", "Repairs take 3 weeks."]
print(fit_chunks(chunks, 12))
print(fit_chunks(chunks, 100))
