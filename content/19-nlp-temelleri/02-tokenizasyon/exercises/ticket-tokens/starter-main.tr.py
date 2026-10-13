import re

from text_data import make_tickets


def ticket_tokens(text):
    return text.split()


for ticket in make_tickets(8):
    tokens = ticket_tokens(ticket["text"])
    print(len(tokens), [t for t in tokens if len(t) > 1 and (t[0] == "$" or "@" in t or "-" in t)])
