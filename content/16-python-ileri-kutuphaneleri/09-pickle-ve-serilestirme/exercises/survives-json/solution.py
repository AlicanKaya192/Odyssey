import json


def survives_json(obj):
    try:
        return json.loads(json.dumps(obj)) == obj
    except TypeError:
        return False

print(survives_json({"a": [1, 2]}))
print(survives_json((1, 2)))
print(survives_json({1: "one"}))
print(survives_json({"tags": {"x"}}))
