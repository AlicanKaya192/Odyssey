from contextlib import ExitStack


def first_lines(paths):
    with ExitStack() as stack:
        files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]
        return [f.readline().strip() for f in files]

print(first_lines(["part0.txt", "part1.txt", "part2.txt"]))
