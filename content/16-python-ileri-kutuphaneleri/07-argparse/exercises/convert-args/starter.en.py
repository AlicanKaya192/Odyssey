import argparse


def convert_args(argv):
    parser = argparse.ArgumentParser(prog="convert")
    parser.add_argument("files")
    args = parser.parse_args(argv)
    return [args.files, "csv"]

print(convert_args(["a.txt", "b.txt", "--format", "json"]))
print(convert_args(["x.txt"]))
