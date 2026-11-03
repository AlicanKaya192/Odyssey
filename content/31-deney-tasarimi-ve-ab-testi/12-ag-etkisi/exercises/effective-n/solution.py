def effective_n(n, cluster_size, icc):
    deff = 1 + (cluster_size - 1) * icc
    return round(n / deff)


print(effective_n(30000, 300, 0.01))
