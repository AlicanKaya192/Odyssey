def family_error(m, alpha=0.05):
    return round(alpha * m, 3)


print(family_error(1))
print(family_error(20))
