In a real program, logging is set up **in one function** at the very start
of the program; modules only use `getLogger(__name__)`.

```python
import logging
import sys
from pathlib import Path


def setup_logging(log_file: str, verbose: bool = False) -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    file = logging.FileHandler(log_file, encoding="utf-8")
    file.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    root.handlers[:] = [console, file]


setup_logging("run.log")
log = logging.getLogger("report")
log.debug("rows loaded: %d", 120)
log.info("report ready")
for handler in logging.getLogger().handlers:
    handler.close()
print(Path("run.log").read_text(encoding="utf-8"))
```

```text
INFO: report ready
DEBUG report: rows loaded: 120
INFO report: report ready
```

- The root logger is open to `DEBUG`; filtering happens in the handlers: the
  screen from `INFO` up (or everything with `verbose`), the file takes
  everything. The first line is the screen's, the next two the file's.
- `root.handlers[:] = [...]` replaces earlier handlers: even if the function
  is called twice, records are not written twice.
- `verbose` comes from a command line option (`--verbose`); that is set up
  with `argparse` in the next section.

## Checklist

- `log = logging.getLogger(__name__)` in every module.
- Setup once at the program's entry (`if __name__ == "__main__":`).
- Short on screen, detailed in the file; the file should have the time
  (`%(asctime)s`).
- Information like users' passwords, personal data or full card numbers is
  not written to logs: log files are shared and kept.
- `print` is only for the program's real output; status messages go to the
  log.
