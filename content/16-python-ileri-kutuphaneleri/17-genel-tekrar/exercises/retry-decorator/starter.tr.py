import functools
import io
import logging

log = logging.getLogger("retry")


def retry(times):
    def decorate(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorate

stream = io.StringIO()
handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
log.addHandler(handler)
log.setLevel(logging.WARNING)
calls = []


@retry(3)
def flaky():
    """Fail twice, then work."""
    calls.append(1)
    if len(calls) < 3:
        raise ValueError(f"try {len(calls)}")
    return "ok"


print(flaky(), len(calls), flaky.__name__)
print(stream.getvalue().strip())
