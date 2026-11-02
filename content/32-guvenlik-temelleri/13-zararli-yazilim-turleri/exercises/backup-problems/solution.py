def backup_problems(copies):
    problems = []
    if len(copies) < 3:
        problems.append("need-3-copies")
    if len({c["media"] for c in copies}) < 2:
        problems.append("need-2-media")
    if not any(c["offsite"] for c in copies):
        problems.append("need-offsite")
    if not any(c["offline"] for c in copies):
        problems.append("need-offline")
    return problems

copies = [{"media": "laptop", "offsite": False, "offline": False},
          {"media": "laptop", "offsite": False, "offline": False}]
for problem in backup_problems(copies):
    print(problem)
good = copies[:1] + [{"media": "usb-disk", "offsite": False, "offline": True},
                     {"media": "cloud", "offsite": True, "offline": False}]
print("good:", len(backup_problems(good)), "problems")
