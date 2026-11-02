def login_attempts(events, limit):
    results = []
    fails = 0
    locked = False
    for event in events:
        if locked:
            results.append("locked")
        elif event == "right":
            results.append("ok")
            fails = 0
        else:
            results.append("fail")
            fails += 1
            if fails >= limit:
                locked = True
    return results

events = ["wrong", "right", "wrong", "wrong", "wrong", "right", "wrong"]
print(" ".join(login_attempts(events, 3)))
print(" ".join(login_attempts(["wrong", "right"], 1)))
