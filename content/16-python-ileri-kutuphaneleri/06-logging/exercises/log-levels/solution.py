import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(levelname)s: %(message)s")

log = logging.getLogger("app")
log.debug("debug detail")
log.info("job started")
log.warning("low memory")
