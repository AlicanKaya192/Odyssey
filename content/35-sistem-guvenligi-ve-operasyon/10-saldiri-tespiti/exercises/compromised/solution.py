def compromised(events, threshold):
    lines = []
    fails = {}
    for time, ip, user, result in events:
        key = (ip, user)
        if result == "fail":
            fails[key] = fails.get(key, 0) + 1
        else:
            if fails.get(key, 0) >= threshold:
                lines.append(f"{time} {user} {ip}")
            fails[key] = 0
    return lines

EVENTS = [
    ["10:00", "203.0.113.9", "bob", "fail"],
    ["10:01", "203.0.113.9", "bob", "fail"],
    ["10:02", "203.0.113.9", "bob", "fail"],
    ["10:02", "198.51.100.4", "ada", "fail"],
    ["10:03", "198.51.100.4", "ada", "ok"],
    ["10:04", "203.0.113.9", "bob", "ok"],
    ["10:05", "203.0.113.9", "bob", "ok"],
]
for line in compromised(EVENTS, 3):
    print(line)
