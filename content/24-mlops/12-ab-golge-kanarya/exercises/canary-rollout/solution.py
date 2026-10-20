def rollout(stages, decisions):
    index = 0
    history = []
    for decision in decisions:
        if decision == "rollback":
            history.append(0)
            break
        if decision == "advance" and index < len(stages) - 1:
            index += 1
        history.append(stages[index])
    return history


stages = [1, 5, 25, 100]
print(rollout(stages, ["wait", "advance", "advance", "advance", "advance"]))
print(rollout(stages, ["advance", "rollback", "advance"]))
print(rollout(stages, []))
