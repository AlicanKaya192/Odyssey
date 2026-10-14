import re

SLOT = re.compile(r"\{\{(\w+)\}\}")


def render(template, values):
    return template


T = "{{name}} wrote: {{message}}"
print(render(T, {"name": "Ada", "message": "Is {{name}} ok?"}))
print(render(T, {"name": "Ada"}))
