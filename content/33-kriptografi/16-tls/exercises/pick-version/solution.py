def pick_version(offered):
    for version in ["TLSv1.3", "TLSv1.2"]:
        if version in offered:
            return version
    return "protocol_version"

print(pick_version(["TLSv1.2", "TLSv1.3"]))
print(pick_version(["TLSv1.0", "TLSv1.2"]))
print(pick_version(["SSLv3", "TLSv1.0", "TLSv1.1"]))
