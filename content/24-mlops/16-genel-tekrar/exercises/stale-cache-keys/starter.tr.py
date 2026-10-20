def stale_keys(keys, live_version):
    # Anahtari "@" ile ikiye bol.
    pass


keys = ["C1@v2", "C2@v3", "C3@v2", "C4@v3"]
print(stale_keys(keys, "v3"))
print(stale_keys(keys, "v2"))
print(stale_keys([], "v3"))
