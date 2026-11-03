def run_exchange(p, g, a, b):
    ada_public = pow(g, a, p)
    can_public = pow(g, b, p)
    ada_shared = pow(can_public, a, p)
    can_shared = pow(ada_public, b, p)
    return [ada_public, can_public, ada_shared, can_shared]

result = run_exchange(23, 5, 6, 15)
print(result)
print(result[2] == result[3])
