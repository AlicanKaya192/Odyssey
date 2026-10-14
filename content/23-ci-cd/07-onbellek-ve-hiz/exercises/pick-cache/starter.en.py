def pick_cache(key, restore_keys, saved):
    # Full match first, then the prefixes in order.
    pass


saved = [["pip-Linux-aaaa", 10], ["pip-Linux-cccc", 30], ["pip-Windows-bbbb", 20], ["pip-Linux-dddd", 25]]
print(pick_cache("pip-Linux-aaaa", ["pip-Linux-"], saved))
print(pick_cache("pip-Linux-eeee", ["pip-Linux-"], saved))
print(pick_cache("pip-macOS-ffff", ["pip-macOS-", "pip-"], saved))
print(pick_cache("npm-Linux-gggg", ["npm-"], saved))
