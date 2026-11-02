def availability_percent(up_minutes, total_minutes):
    return up_minutes / total_minutes

print(availability_percent(43158, 43200))
print(availability_percent(525000, 525600))
print(availability_percent(100, 100))
