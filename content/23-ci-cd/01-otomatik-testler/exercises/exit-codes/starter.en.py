def step_status(code):
    # Return the text for the exit code.
    pass


def pipeline_status(codes):
    # Stop at the first non-zero step; use step_status.
    pass


print(step_status(0))
print(step_status(1))
print(step_status(5))
print(step_status(2))
print(pipeline_status([0, 0, 0]))
print(pipeline_status([0, 1, 0]))
print(pipeline_status([0, 0, 5]))
