def pick_version(offered):
    return max(offered)

print(pick_version(["TLSv1.2", "TLSv1.3"]))
print(pick_version(["TLSv1.0", "TLSv1.2"]))
print(pick_version(["SSLv3", "TLSv1.0", "TLSv1.1"]))
