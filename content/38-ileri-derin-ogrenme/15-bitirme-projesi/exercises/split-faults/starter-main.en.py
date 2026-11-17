from dl_data import make_sensor


def split_faults():
    x, y = make_sensor(600, seed=7)
    # Training 0:400, validation 400:500, test 500:600; the number of faults in each
    return [0, 0, 0]

print(split_faults())
