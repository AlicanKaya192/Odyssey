import argparse


def convert_args(argv):
    parser = argparse.ArgumentParser(prog="convert")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--format", choices=["csv", "json"], default="csv")
    args = parser.parse_args(argv)
    return [args.files, args.format]

print(convert_args(["a.txt", "b.txt", "--format", "json"]))
print(convert_args(["x.txt"]))
