import math


def percentile(values, p):
    # Bos liste, siralama, sira, en az 1.
    pass


latencies = [12, 15, 11, 14, 13, 90, 12, 16, 13, 14,
             12, 15, 13, 11, 14, 12, 13, 15, 14, 250]
print("p50:", percentile(latencies, 50))
print("p95:", percentile(latencies, 95))
print("p99:", percentile(latencies, 99))
print("empty:", percentile([], 50))
