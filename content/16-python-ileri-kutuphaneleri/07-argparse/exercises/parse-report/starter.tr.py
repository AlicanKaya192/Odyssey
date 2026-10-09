import argparse


def parse_report(argv):
    parser = argparse.ArgumentParser(prog="report")
    parser.add_argument("path")
    # --top, --verbose
    args = parser.parse_args(argv)
    return (args.path,)

print(parse_report(["sales.csv", "--top", "3"]))
print(parse_report(["data.csv", "--verbose"]))
