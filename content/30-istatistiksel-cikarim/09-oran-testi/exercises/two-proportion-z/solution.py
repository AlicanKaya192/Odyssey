import math
from scipy import stats


def z_test(k_a, n_a, k_b, n_b):
    pa, pb = k_a / n_a, k_b / n_b
    pool = (k_a + k_b) / (n_a + n_b)
    se = math.sqrt(pool * (1 - pool) * (1 / n_a + 1 / n_b))
    z = (pb - pa) / se
    return [round(z, 3), round(float(2 * stats.norm.sf(abs(z))), 4)]


print(z_test(472, 4000, 560, 4000))
print(z_test(50, 500, 70, 500))
