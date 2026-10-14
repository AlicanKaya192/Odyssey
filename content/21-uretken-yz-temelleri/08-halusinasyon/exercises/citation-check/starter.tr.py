import re

SOURCES = [
    "Returns are accepted within 30 days of delivery.",
    "Standard delivery takes 3 to 5 working days.",
    "Refunds are paid within 7 days.",
]


def check_citations(answer, sources):
    return []


answer = "Delivery takes 3 to 5 days [2]. Returns are accepted for 60 days [1]. Call us [4]."
print(check_citations(answer, SOURCES))
