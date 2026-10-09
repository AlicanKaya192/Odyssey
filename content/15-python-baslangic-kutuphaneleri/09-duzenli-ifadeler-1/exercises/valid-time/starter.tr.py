import re


def valid_time(text):
    # once bicim, sonra saat < 24 ve dakika < 60
    return False

for text in ["09:30", "23:59", "24:00", "7:15", "12:60"]:
    print(text, valid_time(text))
