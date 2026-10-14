WORKFLOW = {
    "name": "CI",
    "jobs": {
        "lint": {
            "runs-on": "ubuntu-latest",
            "steps": [{"uses": "actions/checkout@v4"}, {"run": "ruff check ."}],
        },
        "test": {
            "runs-on": "windows-latest",
            "steps": [
                {"uses": "actions/checkout@v4"},
                {"uses": "actions/setup-python@v5"},
                {"run": "python -m pytest"},
            ],
        },
    },
}


def job_summary(workflow):
    # For each job, the text "name: machine, N steps".
    pass


for line in job_summary(WORKFLOW):
    print(line)
