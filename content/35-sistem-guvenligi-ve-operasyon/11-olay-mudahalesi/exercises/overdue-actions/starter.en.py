def overdue_actions(actions, today):
    lines = []
    for action_id, owner, due, done in actions:
        if not done:
            lines.append(f"{action_id} {owner} {due}")
    return lines

ACTIONS = [
    ["A-3", "ada", "2026-11-10", False],
    ["A-1", "bob", "2026-10-20", False],
    ["A-2", "eve", "2026-10-15", True],
    ["A-4", "bob", "2026-10-20", False],
    ["A-5", "ada", "2026-10-01", False],
]
for line in overdue_actions(ACTIONS, "2026-11-01"):
    print(line)
