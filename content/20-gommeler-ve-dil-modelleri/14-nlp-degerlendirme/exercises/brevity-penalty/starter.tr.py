import math


def brevity_penalty(candidate_len, reference_len):
    return 0.0

print(brevity_penalty(10, 10))
print(brevity_penalty(12, 10))
print(brevity_penalty(5, 10))
