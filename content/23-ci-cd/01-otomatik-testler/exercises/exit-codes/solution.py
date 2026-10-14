def step_status(code):
    if code == 0:
        return "green"
    if code == 1:
        return "red: tests failed"
    if code == 5:
        return "red: no tests"
    return "red: error"


def pipeline_status(codes):
    step = 1
    for code in codes:
        if code != 0:
            return "red at step " + str(step) + " (" + step_status(code) + ")"
        step = step + 1
    return "green"


print(step_status(0))
print(step_status(1))
print(step_status(5))
print(step_status(2))
print(pipeline_status([0, 0, 0]))
print(pipeline_status([0, 1, 0]))
print(pipeline_status([0, 0, 5]))
