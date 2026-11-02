def sla_report(outages, days, target):
    total = days * 24 * 60
    down = sum(outages)
    percent = round((total - down) / total * 100, 3)
    return (percent, percent >= target)

print(sla_report([12, 30], 30, 99.9))
print(sla_report([12, 30, 5], 30, 99.9))
print(sla_report([], 7, 99.99))
