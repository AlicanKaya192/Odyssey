from datetime import datetime


def reformat_date(text):
    d = datetime.strptime(text, "%d.%m.%Y")
    return d.strftime("%Y-%m-%d")

print(reformat_date("15.03.2026"))
print(reformat_date("01.12.1999"))
