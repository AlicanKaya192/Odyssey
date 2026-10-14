import re


def fill(template, values):
    names = re.findall(r"\{(\w+)\}", template)
    missing = [name for name in names if name not in values]
    if missing:
        return [None, missing]
    text = template
    for name in names:
        text = text.replace("{" + name + "}", str(values[name]))
    return [text, []]


TEMPLATE = "Hello {name}, order {order} is {status}."
print(fill(TEMPLATE, {"name": "Ada", "order": "ORD-48213",
                      "status": "shipped"})[0])
print(fill(TEMPLATE, {"name": "Ada"}))
