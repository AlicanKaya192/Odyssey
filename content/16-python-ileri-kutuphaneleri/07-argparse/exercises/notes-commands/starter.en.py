import argparse


def notes(argv):
    parser = argparse.ArgumentParser(prog="notes")
    # commands = parser.add_subparsers(dest="command", required=True)
    return ""

print(notes(["add", "buy milk"]))
print(notes(["list", "--limit", "3"]))
print(notes(["list"]))
