import numpy as np

angles = np.arange(8) * np.pi / 4
CENTRES = np.stack([2 * np.cos(angles), 2 * np.sin(angles)], axis=1)
EXAMPLE = [[2.0, 0.1], [1.9, -0.1], [0.0, 2.05], [-2.0, 0.0], [-1.41, -1.41],
           [0.0, 0.0], [1.0, 1.0], [2.1, 0.0], [0.1, -1.95], [-2.2, 0.1]]


def mode_summary(points):
    return [0, 0.0]


print(mode_summary(EXAMPLE))
