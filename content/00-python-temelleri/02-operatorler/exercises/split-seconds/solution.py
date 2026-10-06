total = 200000

days = total // 86400
rest = total % 86400
hours = rest // 3600
rest = rest % 3600
minutes = rest // 60
seconds = rest % 60

print(days, "days", hours, "hours", minutes, "minutes", seconds, "seconds")
