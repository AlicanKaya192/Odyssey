def false_share(n_ideas, share_work, power, alpha):
    false_hits = n_ideas * (1 - share_work) * alpha
    true_hits = n_ideas * share_work * power
    return round(false_hits / (false_hits + true_hits), 3)


print(false_share(2000, 0.10, 0.17, 0.05))
print(false_share(2000, 0.10, 0.80, 0.05))
