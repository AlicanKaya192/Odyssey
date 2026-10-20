import json
from pathlib import Path


def load_runs(path):
    # An empty list if the file is missing, otherwise one JSON per line.
    pass


def log_run(path, params, metrics):
    # Find the number, write the line in append mode, return the number.
    pass


print(log_run("runs.jsonl", {"model": "baseline"}, {"val_accuracy": 0.75}))
print(log_run("runs.jsonl", {"model": "logistic", "C": 1}, {"val_accuracy": 0.83}))
runs = load_runs("runs.jsonl")
print(len(runs), runs[-1]["run"], runs[-1]["params"]["C"])
print(load_runs("missing.jsonl"))
