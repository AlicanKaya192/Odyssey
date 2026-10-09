import textwrap


def wrap_lines(text, width):
    return textwrap.wrap(text, width=width)

text = "The standard library is a large collection of modules that ship with Python."
for line in wrap_lines(text, 25):
    print(line)
