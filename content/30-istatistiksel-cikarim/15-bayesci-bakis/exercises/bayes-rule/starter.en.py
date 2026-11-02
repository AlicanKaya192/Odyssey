def real_given_significant(prior, power, alpha=0.05):
    return round(power, 3)


print(real_given_significant(0.1, 0.8))
print(real_given_significant(0.3, 0.5))
