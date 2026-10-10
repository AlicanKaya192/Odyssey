import functools
import io
import logging

log = logging.getLogger("retry")


def retry(times):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as error:
                    if attempt == times:
                        raise
                    log.warning("retry %d: %s", attempt, error)
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
