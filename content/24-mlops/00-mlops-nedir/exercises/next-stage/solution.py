STAGES = ["data", "train", "evaluate", "serve", "monitor"]


def next_stage(stage):
    if stage not in STAGES:
        return None
    i = STAGES.index(stage)
    return STAGES[(i + 1) % len(STAGES)]


print(next_stage("data"))
print(next_stage("serve"))
print(next_stage("monitor"))
print(next_stage("deploy"))
