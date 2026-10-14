from shop_data import TICKETS, LABELS, RECORDED


def per_category(version):
    right = {label: 0 for label in LABELS}
    for ticket, reply in zip(TICKETS, RECORDED[version]):
        if reply.strip().lower().rstrip(".!") == ticket["label"]:
            right[ticket["label"]] += 1
    return right


for version in ["v1", "v2"]:
    print(version, list(per_category(version).values()))
