from llm_client import count_message_tokens

SYSTEM = "You are the support assistant of an outdoor shop."


def messages_for(text):
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": text}]


def cache_run(requests):
    cache, calls, hits, saved = set(), 0, 0, 0
    for text in requests:
        key = " ".join(text.lower().split())
        if key in cache:
            hits += 1
            saved += count_message_tokens(messages_for(text))
        else:
            cache.add(key)
            calls += 1
    return [calls, hits, saved]


REQUESTS = ["How much is shipping?", "how much is  shipping?",
            "Where is ORD-10077?", "How much is shipping?"]
print(cache_run(REQUESTS))
print(cache_run([]))
