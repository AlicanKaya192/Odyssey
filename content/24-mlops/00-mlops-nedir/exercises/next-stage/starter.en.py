STAGES = ["data", "train", "evaluate", "serve", "monitor"]


def next_stage(stage):
    # Find the stage's position in the list and return the next one.
    pass


print(next_stage("data"))
print(next_stage("serve"))
print(next_stage("monitor"))
print(next_stage("deploy"))
