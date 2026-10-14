def step_kind(step):
    if "uses" in step and "run" in step:
        return "invalid"
    if "uses" in step:
        return "action: " + step["uses"]
    if "run" in step:
        return "command: " + step["run"].split("\n")[0]
    return "invalid"


print(step_kind({"uses": "actions/checkout@v4"}))
print(step_kind({"run": "python -m pytest"}))
print(step_kind({"name": "Install", "run": "pip install -U pip\npip install -r requirements.txt"}))
print(step_kind({"uses": "actions/checkout@v4", "run": "ls"}))
print(step_kind({"name": "empty"}))
