import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="greet")
    parser.add_argument("name")
    args = parser.parse_args(argv)
    print(f"hello {args.name}")
    return 0

code = main(["ada", "--times", "2", "--shout"])
print(code)
