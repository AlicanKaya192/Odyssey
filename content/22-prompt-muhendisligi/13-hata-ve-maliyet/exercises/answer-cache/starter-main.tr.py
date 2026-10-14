from llm_client import count_message_tokens

SYSTEM = "You are the support assistant of an outdoor shop."


def messages_for(text):
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": text}]


def cache_run(requests):
    return [len(requests), 0, 0]


REQUESTS = ["How much is shipping?", "how much is  shipping?",
            "Where is ORD-10077?", "How much is shipping?"]
print(cache_run(REQUESTS))
print(cache_run([]))
