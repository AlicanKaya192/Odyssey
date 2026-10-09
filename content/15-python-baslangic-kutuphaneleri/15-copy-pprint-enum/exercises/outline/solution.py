from pprint import pformat


def outline(data):
    return pformat(data, depth=1, sort_dicts=False)

data = {"b": [1, 2, {"deep": True}], "a": {"x": 1}}
print(outline(data))
