import math


def gradient_through_time(w, xs):
    hs = [0.0]
    for x in xs:
        hs.append(math.tanh(w * hs[-1] + x))
    grads = [1.0]
    for t in range(len(xs), 0, -1):
        grads.append(grads[-1] * w * (1 - hs[t] ** 2))
    return [round(g, 4) for g in grads]

print(gradient_through_time(0.5, [1.0, 0.0, 0.0, 0.0]))
print(gradient_through_time(2.0, [1.0, 0.0, 0.0, 0.0]))
