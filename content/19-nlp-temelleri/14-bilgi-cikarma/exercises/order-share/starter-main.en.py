import re

from text_data import make_tickets

tickets = make_tickets(2000)


def order_share(category):
    return 0.0


for category in ["account", "billing", "refund", "shipping", "technical"]:
    print(category, order_share(category))
