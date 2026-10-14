from llm_client import ChatClient, ContextLengthError, RateLimitError, ServerError

FALLBACK = "We cannot answer right now; an agent will reply."
ERRORS = {"429": RateLimitError, "503": ServerError}
RETRYABLE = (RateLimitError, ServerError)
MESSAGES = [{"role": "user", "content": "Where is my order ORD-48213?"}]


def make_script(spec):
    return [ERRORS[item](item) if item in ERRORS else item for item in spec]


def resilient(spec, deadline):
    client = ChatClient(make_script(spec))
    waits, log = [], []
    for attempt in range(5):
        try:
            return [client.chat(MESSAGES, max_tokens=40).text, waits, log]
        except RETRYABLE as error:
            log.append(str(error))
            wait = 2.0 ** attempt
            if attempt == 4 or sum(waits) + wait > deadline:
                return [FALLBACK, waits, log]
            waits.append(wait)


for spec, deadline in [(["503", "ok"], 10), (["429"] * 5, 10),
                       (["429"] * 5, 100)]:
    text, waits, log = resilient(spec, deadline)
    short = "fallback" if text == FALLBACK else text
    print(short, sum(waits), ",".join(log))
