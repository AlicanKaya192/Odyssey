import re

SLOT = re.compile(r"\{\{(\w+)\}\}")


def render(template, values):
    names = set(SLOT.findall(template))
    missing, unused = names - values.keys(), values.keys() - names
    if missing or unused:
        return f"missing {sorted(missing)}, unused {sorted(unused)}"
    return SLOT.sub(lambda m: str(values[m.group(1)]), template)


T = "{{name}} wrote: {{message}}"
print(render(T, {"name": "Ada", "message": "Is {{name}} ok?"}))
print(render(T, {"name": "Ada"}))
