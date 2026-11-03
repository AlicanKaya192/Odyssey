def canary_intact(frame, size, canary):
    if len(frame) <= size:
        return False
    return frame[size] == canary

print(canary_intact([1, 2, 3, 0, 77, 0], 4, 77))
print(canary_intact([1, 2, 3, 4, 5, 6], 4, 77))
print(canary_intact([1, 2], 4, 77))
