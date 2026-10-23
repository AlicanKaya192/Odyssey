import re
from datetime import datetime


def dates_in(text, policy):
    return []

TEXT = "Ordered 03/04/2026, delivered 13/04/2026."
print(dates_in(TEXT, "US"))
print(dates_in(TEXT, None))
