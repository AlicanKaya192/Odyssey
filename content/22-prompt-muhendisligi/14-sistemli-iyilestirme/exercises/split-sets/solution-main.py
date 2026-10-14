from shop_data import TICKETS


def split_sets(tickets, per_label):
    seen, dev, test = {}, [], []
    for t in tickets:
        seen[t["label"]] = seen.get(t["label"], 0) + 1
        if seen[t["label"]] <= per_label:
            dev.append(t["id"])
        else:
            test.append(t["id"])
    return [dev, test]


dev, test = split_sets(TICKETS, 4)
print(len(dev), len(test))
print(dev[:6])
print(test[:6])
