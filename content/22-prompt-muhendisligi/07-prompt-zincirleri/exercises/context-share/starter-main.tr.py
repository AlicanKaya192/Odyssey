from doc_data import DOCS
from llm_client import count_tokens


def context_share(doc_id, doc_ids):
    return [0, 0, 0.0]


ALL = ["shipping", "returns", "refunds", "warranty", "payment"]
print(context_share("shipping", ALL))
print(context_share("payment", ALL))
