from doc_data import DOCS
from llm_client import count_tokens


def context_share(doc_id, doc_ids):
    texts = {doc["id"]: doc["text"] for doc in DOCS}
    one = count_tokens(texts[doc_id])
    everything = sum(count_tokens(texts[i]) for i in doc_ids)
    return [one, everything, round(one / everything, 2)]


ALL = ["shipping", "returns", "refunds", "warranty", "payment"]
print(context_share("shipping", ALL))
print(context_share("payment", ALL))
