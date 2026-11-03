def run_frame(size, canary, data):
    frame = [0] * size + [canary, 0]
    for i, value in enumerate(data):
        if i < len(frame):
            frame[i] = value
    if frame[size] != canary:
        return "detected"
    return "ok"

print(run_frame(4, 77, [1, 2, 3]))
print(run_frame(4, 77, [1, 2, 3, 4]))
print(run_frame(4, 77, [1, 2, 3, 4, 5]))
print(run_frame(4, 77, list(range(10))))
