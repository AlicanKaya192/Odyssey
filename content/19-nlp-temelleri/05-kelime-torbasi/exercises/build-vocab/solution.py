def build_vocabulary(docs):
    return sorted({w for d in docs for w in d.lower().split()})

print(build_vocabulary(["The battery is great", "the battery died"]))
