def merge_state(required, runs):
    latest = {}
    for name, status in runs:
        latest[name] = status
    for name in required:
        if latest.get(name) == "failure":
            return f"blocked by {name}"
    for name in required:
        if latest.get(name) not in ("success", "skipped"):
            return f"waiting for {name}"
    return "ready"


required = ["lint", "test (3.12)", "test (3.13)"]
print(merge_state(required, [["lint", "success"]]))
print(merge_state(required, [
    ["lint", "success"],
    ["test (3.12)", "failure"],
    ["test (3.13)", "success"],
    ["test (3.12)", "success"],
]))
print(merge_state(required, [
    ["lint", "skipped"],
    ["test (3.12)", "success"],
    ["test (3.13)", "failure"],
]))
