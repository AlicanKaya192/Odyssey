def rollout(stages, decisions):
    # Hangi paydasin: bir sira numarasi tut.
    pass


stages = [1, 5, 25, 100]
print(rollout(stages, ["wait", "advance", "advance", "advance", "advance"]))
print(rollout(stages, ["advance", "rollback", "advance"]))
print(rollout(stages, []))
