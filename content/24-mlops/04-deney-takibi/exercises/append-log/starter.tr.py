import json
from pathlib import Path


def load_runs(path):
    # Dosya yoksa bos liste, varsa her satir bir JSON.
    pass


def log_run(path, params, metrics):
    # Numarayi bul, satiri ekleme kipinde yaz, numarayi dondur.
    pass


print(log_run("runs.jsonl", {"model": "baseline"}, {"val_accuracy": 0.75}))
print(log_run("runs.jsonl", {"model": "logistic", "C": 1}, {"val_accuracy": 0.83}))
runs = load_runs("runs.jsonl")
print(len(runs), runs[-1]["run"], runs[-1]["params"]["C"])
print(load_runs("missing.jsonl"))
