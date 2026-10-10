import numpy as np
from scipy import interpolate


def readings(hours, temps, at):
    linear = np.interp(at, hours, temps)
    curve = interpolate.PchipInterpolator(hours, temps)(at)
    return [round(float(linear), 2), round(float(curve), 2)]

HOURS = [0, 3, 6, 9, 12]
TEMP = [12.0, 10.0, 15.0, 22.0, 25.0]
print(readings(HOURS, TEMP, 7.5))
print(readings(HOURS, TEMP, 1.5))
