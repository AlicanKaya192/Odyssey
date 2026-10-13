import re

from text_data import make_tickets

TOKEN = re.compile(r"""
    [\w.+-]+@\w+\.\w+
  | \$\d+(?:\.\d+)?
  | [A-Z]+-\d+
  | \w+(?:'\w+)?
  | [^\w\s]
""", re.VERBOSE)


def ticket_tokens(text):
    return TOKEN.findall(text)


for ticket in make_tickets(8):
    tokens = ticket_tokens(ticket["text"])
    print(len(tokens), [t for t in tokens if len(t) > 1 and (t[0] == "$" or "@" in t or "-" in t)])
