def loop_steps(actions, max_steps):
    for step, action in enumerate(actions[:max_steps], 1):
        if action == "answer":
            return [step, True]
    return [min(len(actions), max_steps), False]


print(loop_steps(["tool", "tool", "answer"], 5))
print(loop_steps(["tool"] * 9, 5))
