def backup_problems(copies):
    problems = []
    # check the four rules in order
    return problems

copies = [{"media": "laptop", "offsite": False, "offline": False},
          {"media": "laptop", "offsite": False, "offline": False}]
for problem in backup_problems(copies):
    print(problem)
good = copies[:1] + [{"media": "usb-disk", "offsite": False, "offline": True},
                     {"media": "cloud", "offsite": True, "offline": False}]
print("good:", len(backup_problems(good)), "problems")
