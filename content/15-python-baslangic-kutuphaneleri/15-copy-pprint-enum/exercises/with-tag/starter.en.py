import copy


def with_tag(record, tag):
    result = copy.copy(record)
    result["tags"].append(tag)
    return result

record = {"name": "Ada", "tags": ["math"]}
updated = with_tag(record, "code")
print(updated["tags"])
print(record["tags"])
