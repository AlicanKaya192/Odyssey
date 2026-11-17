from dl_data import make_sensor


def split_faults():
    x, y = make_sensor(600, seed=7)
    return [int(y[a:b].sum()) for a, b in [(0, 400), (400, 500), (500, 600)]]

print(split_faults())
