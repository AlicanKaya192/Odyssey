from shop_data import TICKETS, LABELS, RECORDED


def per_category(version):
    return {}


for version in ["v1", "v2"]:
    print(version, list(per_category(version).values()))
