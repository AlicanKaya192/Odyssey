def route(problems):
    return "send"


for problems in [[], ["too long"], ["too long", "promise"]]:
    print(problems, route(problems))
