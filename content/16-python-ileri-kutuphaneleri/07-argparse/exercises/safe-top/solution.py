import argparse


def safe_top(argv):
    parser = argparse.ArgumentParser(prog="report", exit_on_error=False)
    parser.add_argument("--top", type=int, default=5)
    try:
        return parser.parse_args(argv).top
    except argparse.ArgumentError:
        return "invalid"

print(safe_top(["--top", "3"]), safe_top(["--top", "ten"]), safe_top([]))
