import argparse


def parse_report(argv):
    parser = argparse.ArgumentParser(prog="report")
    parser.add_argument("path")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)
    return (args.path, args.top, args.verbose)

print(parse_report(["sales.csv", "--top", "3"]))
print(parse_report(["data.csv", "--verbose"]))
