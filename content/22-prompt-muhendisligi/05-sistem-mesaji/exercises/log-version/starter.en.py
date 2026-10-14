import hashlib


def log_entry(system, reply):
    return {}


a = log_entry("Be brief.", "Your parcel left yesterday.")
b = log_entry("Be brief!", "Your parcel left yesterday.")
print(a["system_version"], a["reply_words"])
print(a["system_version"] == b["system_version"])
