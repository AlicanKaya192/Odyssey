import hashlib


def log_entry(system, reply):
    digest = hashlib.sha256(system.encode("utf-8")).hexdigest()[:8]
    return {"system_version": digest, "reply_words": len(reply.split())}


a = log_entry("Be brief.", "Your parcel left yesterday.")
b = log_entry("Be brief!", "Your parcel left yesterday.")
print(a["system_version"], a["reply_words"])
print(a["system_version"] == b["system_version"])
