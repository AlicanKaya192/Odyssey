import re

DETAIL = re.compile(r"\d+(?::\d+)?|[A-Z][a-z]+")


def details(text):
    found = DETAIL.findall(text)
    first = text.split()[0].strip(",.")
    return [d for d in found if d != first]


print(details("Open Monday to Friday, 9:00 to 17:00."))
print(details("Yes, we ship to Canada in 10 days."))
