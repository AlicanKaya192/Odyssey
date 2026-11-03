def shadowed(rules):
    found = []
    for i, (port, _action) in enumerate(rules):
        for earlier_port, _earlier in rules[:i]:
            if earlier_port == "any" or earlier_port == port:
                found.append(i + 1)
                break
    return found

print(shadowed([["any", "allow"], [23, "deny"]]))
print(shadowed([[23, "deny"], [80, "allow"], [443, "allow"]]))
print(shadowed([[80, "allow"], [80, "deny"], ["any", "deny"], [22, "allow"]]))
