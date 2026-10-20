import math


def system_health(requests):
    # p95, hata orani, reddedilenlerin orani.
    pass


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
