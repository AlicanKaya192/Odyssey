import json
from pathlib import Path


def load_runs(path):
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def log_run(path, params, metrics):
    run_id = len(load_runs(path)) + 1
    record = {"run": run_id, "params": params, "metrics": metrics}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return run_id


print(log_run("runs.jsonl", {"model": "baseline"}, {"val_accuracy": 0.75}))
print(log_run("runs.jsonl", {"model": "logistic", "C": 1}, {"val_accuracy": 0.83}))
runs = load_runs("runs.jsonl")
print(len(runs), runs[-1]["run"], runs[-1]["params"]["C"])
print(load_runs("missing.jsonl"))
