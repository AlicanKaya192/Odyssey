from llm_client import ChatClient, ContextLengthError, RateLimitError, ServerError

ERRORS = {"429": RateLimitError, "503": ServerError}
RETRYABLE = (RateLimitError, ServerError)
MESSAGES = [{"role": "user", "content": "Where is my order ORD-48213?"}]


def make_script(spec):
    return [ERRORS[item](item) if item in ERRORS else item for item in spec]


def retry(spec, attempts, window):
    return ["", []]


print(retry(["429", "503", "ok"], 4, 200))
print(retry(["429", "429", "429"], 3, 200))
print(retry(["503", "ok"], 3, 40))
