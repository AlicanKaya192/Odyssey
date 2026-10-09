import argparse


def notes(argv):
    parser = argparse.ArgumentParser(prog="notes")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("text")
    show = commands.add_parser("list")
    show.add_argument("--limit", type=int, default=10)
    args = parser.parse_args(argv)
    if args.command == "add":
        return f"added: {args.text}"
    return f"listing {args.limit}"

print(notes(["add", "buy milk"]))
print(notes(["list", "--limit", "3"]))
print(notes(["list"]))
