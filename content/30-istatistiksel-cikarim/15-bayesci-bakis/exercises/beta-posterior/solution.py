def beta_posterior(k, n, a=1, b=1):
    new_a, new_b = a + k, b + n - k
    return [new_a, new_b, round(new_a / (new_a + new_b), 4)]


print(beta_posterior(472, 4000))
print(beta_posterior(3, 60, 11.4, 88.6))
