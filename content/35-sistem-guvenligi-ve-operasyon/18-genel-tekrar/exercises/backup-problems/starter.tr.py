def backup_problems(copies, rpo_hours):
    problems = []
    if len(copies) < 3:
        problems.append("fewer than 3 copies")
    # iki farkli ortam?
    if not any(offsite for _, offsite, _ in copies):
        problems.append("no offsite copy")
    if not copies or min(hours for _, _, hours in copies) > rpo_hours:
        problems.append("newest copy too old")
    return problems

GOOD = [["disk", False, 2], ["tape", False, 20], ["cloud", True, 26]]
SAME = [["disk", False, 1], ["disk", True, 5], ["disk", False, 9]]
BAD = [["disk", False, 30], ["disk", False, 40]]
for name, copies in [["GOOD", GOOD], ["SAME", SAME], ["BAD", BAD]]:
    print(name)
    for problem in backup_problems(copies, 24):
        print("-", problem)
