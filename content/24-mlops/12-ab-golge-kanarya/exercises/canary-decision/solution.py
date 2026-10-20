def canary_decision(n, min_n, canary_score, control_score, tolerance):
    if n < min_n:
        return "wait"
    if canary_score < control_score - tolerance:
        return "rollback"
    return "advance"


print(canary_decision(8, 30, 0.5, 0.685, 0.05))
print(canary_decision(39, 30, 0.538, 0.681, 0.05))
print(canary_decision(39, 30, 0.795, 0.681, 0.05))
