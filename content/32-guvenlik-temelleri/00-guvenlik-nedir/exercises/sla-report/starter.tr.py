def sla_report(outages, days, target):
    total = days * 24 * 60
    # kesintileri topla, yuzdeyi hesapla
    return (0, False)

print(sla_report([12, 30], 30, 99.9))
print(sla_report([12, 30, 5], 30, 99.9))
print(sla_report([], 7, 99.99))
