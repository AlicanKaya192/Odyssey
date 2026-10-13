import re

from text_data import make_tickets

RULES = [
    (r"[\w.+-]+@\w+\.\w+", "<email>"),
    (r"\$\d+(?:\.\d+)?", "<money>"),
    (r"[A-Z]+-\d+", "<order>"),
    (r"\d+", "<num>"),
]


def mask(text):
    return text


tickets = [t["text"] for t in make_tickets(1000)]
print(mask("Paid $9.99 on ORD-11111, mail bo7@example.com"))
print(len({w for t in tickets for w in mask(t).lower().split()}))
