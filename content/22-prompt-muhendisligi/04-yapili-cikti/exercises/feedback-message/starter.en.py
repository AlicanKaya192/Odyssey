import textwrap


def feedback(errors):
    return ""


print(textwrap.fill(feedback(["urgent must be true or false"]), 40))
print(repr(feedback([])))
