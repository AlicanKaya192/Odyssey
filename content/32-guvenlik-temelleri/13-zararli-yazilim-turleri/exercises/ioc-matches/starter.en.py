def ioc_matches(lines, iocs):
    found = []
    for line in lines:
        for ioc in iocs:
            if ioc in line:
                found.append(ioc)
    return found

lines = [
    "10:01 pc1 dns update.example",
    "10:02 pc2 dns cdn.toy-bad.test",
    "10:03 pc3 file 9f86d081884c",
    "10:04 pc2 dns cdn.toy-bad.test",
]
iocs = ["cdn.toy-bad.test", "9f86d081884c", "never-seen.test"]
for found in ioc_matches(lines, iocs):
    print(found)
