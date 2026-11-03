def design_effect(cluster_size, icc):
    return round(1 + (cluster_size - 1) * icc, 3)


print(design_effect(300, 0.01))
