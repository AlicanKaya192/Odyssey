def rollout(stages, decisions):
    # Which share you are at: keep an index.
    pass


stages = [1, 5, 25, 100]
print(rollout(stages, ["wait", "advance", "advance", "advance", "advance"]))
print(rollout(stages, ["advance", "rollback", "advance"]))
print(rollout(stages, []))
