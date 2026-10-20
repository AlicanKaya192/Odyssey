def utilization(rate, service_ms, workers):
    return round(rate * service_ms / 1000 / workers, 3)


print(utilization(50, 10, 1))
print(utilization(120, 10, 2))
print(utilization(30, 45, 4))
