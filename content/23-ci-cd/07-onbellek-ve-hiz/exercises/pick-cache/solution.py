def pick_cache(key, restore_keys, saved):
    for name, created in saved:
        if name == key:
            return "hit: " + name
    for prefix in restore_keys:
        best = None
        best_time = -1
        for name, created in saved:
            if name.startswith(prefix) and created > best_time:
                best = name
                best_time = created
        if best is not None:
            return "partial: " + best
    return "miss"


saved = [["pip-Linux-aaaa", 10], ["pip-Linux-cccc", 30], ["pip-Windows-bbbb", 20], ["pip-Linux-dddd", 25]]
print(pick_cache("pip-Linux-aaaa", ["pip-Linux-"], saved))
print(pick_cache("pip-Linux-eeee", ["pip-Linux-"], saved))
print(pick_cache("pip-macOS-ffff", ["pip-macOS-", "pip-"], saved))
print(pick_cache("npm-Linux-gggg", ["npm-"], saved))
