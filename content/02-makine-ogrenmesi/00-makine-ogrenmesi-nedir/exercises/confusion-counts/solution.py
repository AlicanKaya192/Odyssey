truth = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
guess = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]

tp = sum(1 for t, g in zip(truth, guess) if t == 1 and g == 1)
tn = sum(1 for t, g in zip(truth, guess) if t == 0 and g == 0)
fp = sum(1 for t, g in zip(truth, guess) if t == 0 and g == 1)
fn = sum(1 for t, g in zip(truth, guess) if t == 1 and g == 0)

print(tp, tn, fp, fn)
print(round((tp + tn) / len(truth), 2))
