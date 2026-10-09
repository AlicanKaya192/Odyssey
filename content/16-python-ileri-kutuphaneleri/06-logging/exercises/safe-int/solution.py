import logging
import sys
import io

buffer = io.StringIO()
log = logging.getLogger("numbers")
handler = logging.StreamHandler(buffer)
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
log.addHandler(handler)


def safe_int(text):
    try:
        return int(text)
    except ValueError:
        log.exception("bad number: %s", text)
        return None

print(safe_int("42"), safe_int("4x"))
lines = buffer.getvalue().splitlines()
print(lines[0])
print(lines[-1].split(":")[0])
