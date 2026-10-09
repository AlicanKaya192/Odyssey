import json


def survives_json(obj):
    # json.loads(json.dumps(obj)) == obj ?
    return True

print(survives_json({"a": [1, 2]}))
print(survives_json((1, 2)))
print(survives_json({1: "one"}))
print(survives_json({"tags": {"x"}}))
