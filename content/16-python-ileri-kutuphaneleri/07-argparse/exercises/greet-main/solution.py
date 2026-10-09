import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="greet")
    parser.add_argument("name")
    parser.add_argument("--times", type=int, default=1)
    parser.add_argument("--shout", action="store_true")
    args = parser.parse_args(argv)
    text = f"hello {args.name}"
    if args.shout:
        text = text.upper()
    for _ in range(args.times):
        print(text)
    return 0

code = main(["ada", "--times", "2", "--shout"])
print(code)
