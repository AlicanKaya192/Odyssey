def valid(created, last_seen, now, idle, absolute):
    return now - last_seen < idle and now - created < absolute

print(valid(0, 0, 600, 900, 28800))
print(valid(0, 0, 1200, 900, 28800))
print(valid(0, 28700, 28900, 900, 28800))
