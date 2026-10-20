import math


def system_health(requests):
    times = sorted(r["ms"] for r in requests)
    rank = math.ceil(0.95 * len(times))
    errors = sum(1 for r in requests if r["status"] >= 500)
    rejected = sum(1 for r in requests if r["status"] == 422)
    return {"p95_ms": times[rank - 1],
            "error_rate": round(errors / len(requests), 3),
            "rejected_rate": round(rejected / len(requests), 3)}


requests = [
    {"ms": 12, "status": 200}, {"ms": 15, "status": 200}, {"ms": 11, "status": 422},
    {"ms": 90, "status": 200}, {"ms": 13, "status": 500}, {"ms": 14, "status": 200},
    {"ms": 12, "status": 200}, {"ms": 16, "status": 200}, {"ms": 13, "status": 200},
    {"ms": 250, "status": 503},
]
health = system_health(requests)
print("p95:", health["p95_ms"])
print("errors:", health["error_rate"])
print("rejected:", health["rejected_rate"])
