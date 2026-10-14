import textwrap


def feedback(errors):
    if not errors:
        return ""
    return ("Your answer was not valid: " + "; ".join(errors)
            + ". Reply with the JSON object only.")


print(textwrap.fill(feedback(["urgent must be true or false"]), 40))
print(repr(feedback([])))
