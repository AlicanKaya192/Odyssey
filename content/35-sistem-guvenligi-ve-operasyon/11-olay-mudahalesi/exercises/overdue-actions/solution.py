from datetime import date


def overdue_actions(actions, today):
    now = date.fromisoformat(today)
    late = []
    for action_id, owner, due, done in actions:
        if not done and date.fromisoformat(due) < now:
            late.append((due, action_id, owner))
    return [f"{action_id} {owner} {due}" for due, action_id, owner in sorted(late)]

ACTIONS = [
    ["A-3", "ada", "2026-11-10", False],
    ["A-1", "bob", "2026-10-20", False],
    ["A-2", "eve", "2026-10-15", True],
    ["A-4", "bob", "2026-10-20", False],
    ["A-5", "ada", "2026-10-01", False],
]
for line in overdue_actions(ACTIONS, "2026-11-01"):
    print(line)
