def shadowed(rules):
    found = []
    # for each rule, look at the rules above it
    return found

print(shadowed([["any", "allow"], [23, "deny"]]))
print(shadowed([[23, "deny"], [80, "allow"], [443, "allow"]]))
print(shadowed([[80, "allow"], [80, "deny"], ["any", "deny"], [22, "allow"]]))
