import logging
import sys
from pathlib import Path


def setup():
    log = logging.getLogger("app")
    # setLevel, StreamHandler, FileHandler


setup()

log = logging.getLogger("app")
log.debug("reading config")
log.warning("config missing")
for handler in log.handlers:
    handler.close()
print(Path("app.log").read_text(encoding="utf-8"))
