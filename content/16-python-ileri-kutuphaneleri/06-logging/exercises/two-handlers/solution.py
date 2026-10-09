import logging
import sys
from pathlib import Path


def setup():
    log = logging.getLogger("app")
    log.setLevel(logging.DEBUG)
    screen = logging.StreamHandler(sys.stdout)
    screen.setLevel(logging.WARNING)
    screen.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    file = logging.FileHandler("app.log", encoding="utf-8")
    file.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    log.addHandler(screen)
    log.addHandler(file)


setup()

log = logging.getLogger("app")
log.debug("reading config")
log.warning("config missing")
for handler in log.handlers:
    handler.close()
print(Path("app.log").read_text(encoding="utf-8"))
