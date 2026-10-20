STAGES = ["data", "train", "evaluate", "serve", "monitor"]


def next_stage(stage):
    # Asamanin listedeki yerini bul, bir sonrakini dondur.
    pass


print(next_stage("data"))
print(next_stage("serve"))
print(next_stage("monitor"))
print(next_stage("deploy"))
