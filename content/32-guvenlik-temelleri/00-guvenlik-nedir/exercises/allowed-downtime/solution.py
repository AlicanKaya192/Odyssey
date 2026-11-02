def allowed_downtime(percent, days):
    minutes = round(days * 24 * 60 * (1 - percent / 100))
    return divmod(minutes, 60)

print(allowed_downtime(99.9, 30))
print(allowed_downtime(99, 365))
print(allowed_downtime(99.99, 365))
