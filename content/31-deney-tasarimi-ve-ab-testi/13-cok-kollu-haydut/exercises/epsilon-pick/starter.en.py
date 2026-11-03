def epsilon_pick(estimates, eps, u, random_arm):
    if u > eps:
        return random_arm
    return max(range(len(estimates)), key=lambda i: estimates[i])


print(epsilon_pick([0.05, 0.07, 0.06], 0.1, 0.5, 0))
print(epsilon_pick([0.05, 0.07, 0.06], 0.1, 0.05, 0))
