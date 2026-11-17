from dl_data import make_sensor


def split_faults():
    x, y = make_sensor(600, seed=7)
    # Egitim 0:400, dogrulama 400:500, test 500:600; her bolumdeki ariza sayisi
    return [0, 0, 0]

print(split_faults())
