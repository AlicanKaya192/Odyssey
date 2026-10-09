A small but complete tool combining what you learned in this section:
`wordcount`, which counts the most frequent words in text files.

```python
import argparse
from collections import Counter
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="wordcount", description="Count words in text files.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--lower", action="store_true")
    args = parser.parse_args(argv)
    counts = Counter()
    for path in args.files:
        text = path.read_text(encoding="utf-8")
        if args.lower:
            text = text.lower()
        counts.update(text.split())
    for word, n in counts.most_common(args.top):
        print(f"{n:>3} {word}")
    return 0


Path("a.txt").write_text("The cat and the dog", encoding="utf-8")
Path("b.txt").write_text("the end", encoding="utf-8")
main(["a.txt", "b.txt", "--top", "2"])
print("---")
main(["a.txt", "b.txt", "--top", "2", "--lower"])
```

```text
  2 the
  1 The
---
  3 the
  1 cat
```

- **`type=Path`**: `type` can be any converter; the file names became `Path`
  objects directly.
- Without `--lower`, `The` and `the` were counted separately; with the switch,
  all three were combined.
- `main` returns a value; in a real file the last line is
  `if __name__ == "__main__": sys.exit(main())`, and it is run in a terminal
  as `python wordcount.py a.txt b.txt --top 2 --lower`.

## A good command line tool

- Write `help=` for every argument; `--help` is the tool's documentation.
- Give sensible defaults; the most common use should work with no options.
- Write the real output to stdout with `print`, and status and error
  messages with `logging` or to stderr: so the output can be piped into
  another program.
- End with exit code 0 on success, non-zero on failure.
- Keep the logic in `main(argv=None)`; call it with a list from tests.
