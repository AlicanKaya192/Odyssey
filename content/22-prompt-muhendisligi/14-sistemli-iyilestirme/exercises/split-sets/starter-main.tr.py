from shop_data import TICKETS


def split_sets(tickets, per_label):
    return [[], []]


dev, test = split_sets(TICKETS, 4)
print(len(dev), len(test))
print(dev[:6])
print(test[:6])
