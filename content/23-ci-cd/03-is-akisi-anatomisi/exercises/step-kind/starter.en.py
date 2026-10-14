def step_kind(step):
    # First check whether it has both.
    pass


print(step_kind({"uses": "actions/checkout@v4"}))
print(step_kind({"run": "python -m pytest"}))
print(step_kind({"name": "Install", "run": "pip install -U pip\npip install -r requirements.txt"}))
print(step_kind({"uses": "actions/checkout@v4", "run": "ls"}))
print(step_kind({"name": "empty"}))
