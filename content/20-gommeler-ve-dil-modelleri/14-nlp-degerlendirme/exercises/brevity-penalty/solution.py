import math


def brevity_penalty(candidate_len, reference_len):
    if candidate_len >= reference_len:
        return 1.0
    return round(math.exp(1 - reference_len / candidate_len), 3)

print(brevity_penalty(10, 10))
print(brevity_penalty(12, 10))
print(brevity_penalty(5, 10))
