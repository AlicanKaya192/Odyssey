def loop_steps(actions, max_steps):
    return [0, False]


print(loop_steps(["tool", "tool", "answer"], 5))
print(loop_steps(["tool"] * 9, 5))
