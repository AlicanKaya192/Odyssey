import argparse


def safe_top(argv):
    parser = argparse.ArgumentParser(prog="report")
    parser.add_argument("--top", type=int, default=5)
    return parser.parse_args(argv).top

print(safe_top(["--top", "3"]), safe_top(["--top", "ten"]), safe_top([]))
