import re

POLICY = ("Orders over 50 euros ship for free. Standard delivery takes "
          "3 to 5 working days. Returns are accepted within 30 days of "
          "delivery. Customer service is open Monday to Friday, 9:00 to 17:00.")
EXAMPLES = [['Shipping is free over 50 euros.', True],
            ['Delivery takes 1 to 2 days.', False],
            ['Returns within 30 days.', True],
            ['Returns within 60 days.', False],
            ['Open every day, even Sunday.', False],
            ['Refunds go to a gift card.', False]]
DETAIL = re.compile(r"\d+(?::\d+)?|[A-Z][a-z]+")


def details(text):
    found = DETAIL.findall(text)
    first = text.split()[0].strip(",.")
    return [d for d in found if d != first]


def unsupported(answer, source):
    known = set(DETAIL.findall(source))
    return [d for d in details(answer) if d not in known]


def score(examples, source):
    return [0, 0, 0, 0, 0.0, 0.0]


print(score(EXAMPLES, POLICY))
