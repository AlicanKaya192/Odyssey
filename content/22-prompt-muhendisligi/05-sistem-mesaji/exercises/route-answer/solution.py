def route(problems):
    if "promise" in problems:
        return "human"
    if problems:
        return "retry"
    return "send"


for problems in [[], ["too long"], ["too long", "promise"]]:
    print(problems, route(problems))
