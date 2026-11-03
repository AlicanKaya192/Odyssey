def outdated(installed, minimum):
    found = []
    for name, version in installed.items():
        if name in minimum and version < minimum[name]:
            found.append(name)
    return sorted(found)

installed = {"pagekit": "2.4.1", "imagelib": "1.10.0",
             "parser": "0.9.3", "tool": "3.0.0"}
minimum = {"pagekit": "2.4.1", "imagelib": "1.9.2", "parser": "1.0.0"}
print(outdated(installed, minimum))
